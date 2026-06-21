from qdrant_client import models, QdrantClient
from ..VectorDBInterface import VectorDBInterface
from ..VectorDBEnums import DistanceMethodEnums
import logging
from typing import List
from models.db_schemes import RetrievedDocument

class QdrantDBProvider(VectorDBInterface):

    def __init__(self, db_client: str, default_vector_size: int = 786,
                                     distance_method: str = None, index_threshold: int=100):

        self.client = None
        self.db_client = db_client
        self.distance_method = None
        self.default_vector_size = default_vector_size

        if distance_method == DistanceMethodEnums.COSINE.value:
            self.distance_method = models.Distance.COSINE
        elif distance_method == DistanceMethodEnums.DOT.value:
            self.distance_method = models.Distance.DOT

        self.logger = logging.getLogger('uvicorn')

    async def connect(self):
        self.client = QdrantClient(path=self.db_client)

    async def disconnect(self):
        self.client = None

    async def is_collection_existed(self, collection_name: str) -> bool:
        return self.client.collection_exists(collection_name=collection_name)
    
    async def list_all_collections(self) -> List:
        return self.client.get_collections()
    
    def get_collection_info(self, collection_name: str) -> dict:
        # 🟢 [التصحيح السحري]: تأمين الدالة ضد الـ ValueError لو الكوليكشن مش موجودة
        try:
            return self.client.get_collection(collection_name=collection_name)
        except Exception as e:
            self.logger.warning(f"⚠️ Collection '{collection_name}' not found. Returning None safely.")
            return None
    
    async def delete_collection(self, collection_name: str):
        if await self.is_collection_existed(collection_name):
            self.logger.info(f"Deleting collection: {collection_name}")
            return self.client.delete_collection(collection_name=collection_name)
        
    async def create_collection(self, collection_name: str, 
                                embedding_size: int,
                                do_reset: bool = False):
        if do_reset:
            await self.delete_collection(collection_name=collection_name)
        
        if not await self.is_collection_existed(collection_name):
            self.logger.info(f"Creating new Qdrant collection: {collection_name}")
            
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=embedding_size,
                    distance=self.distance_method
                )
            )

            return True
        
        return False
    
    async def insert_one(self, collection_name: str, text: str, vector: list,
                         metadata: dict = None, 
                         record_id: str = None):
        
        if not await self.is_collection_existed(collection_name):
            self.logger.error(f"Can not insert new record to non-existed collection: {collection_name}")
            return False
        
        try:
            _ = self.client.upload_records(
                collection_name=collection_name,
                records=[
                    models.Record(
                        id=[record_id],
                        vector=vector,
                        payload={
                            "text": text, "metadata": metadata
                        }
                    )
                ]
            )
        except Exception as e:
            self.logger.error(f"Error while inserting batch: {e}")
            return False

        return True
    
    async def insert_many(self, collection_name: str, texts: list, 
                          vectors: list, metadata: list = None, 
                          record_ids: list = None, batch_size: int = 50):
        
        print(f"\n📥 [CHECK QDRANT INSERT] === Start insert_many ===")
        print(f"📥 [CHECK QDRANT INSERT] Target Collection: '{collection_name}'")
        print(f"📥 [CHECK QDRANT INSERT] Total texts to insert: {len(texts)}")

        if not await self.is_collection_existed(collection_name):
            self.logger.error(f"Can not insert many records to non-existed collection: {collection_name}")
            print(f"❌ [CHECK QDRANT INSERT] Collection '{collection_name}' DOES NOT EXIST!")
            return False

        if metadata is None:
            metadata = [None] * len(texts)

        if record_ids is None:
            record_ids = list(range(0, len(texts)))

        print(f"📥 [CHECK QDRANT INSERT] Processing batches (Batch Size: {batch_size})...")
        for i in range(0, len(texts), batch_size):
            batch_end = i + batch_size

            batch_texts = texts[i:batch_end]
            batch_vectors = vectors[i:batch_end]
            batch_metadata = metadata[i:batch_end]
            batch_record_ids = record_ids[i:batch_end]

            # 🟢 [تأمين وحصر]: تحويل الـ IDs للتأكد أنها متوافقة مع Qdrant (رقم صحيح أو UUID)
            batch_records = [
                models.Record(
                    id=int(batch_record_ids[x]) if isinstance(batch_record_ids[x], (int, float, str)) and str(batch_record_ids[x]).isdigit() else x,
                    vector=batch_vectors[x],
                    payload={
                        "text": batch_texts[x], "metadata": batch_metadata[x]
                    }
                )
                for x in range(len(batch_texts))
            ]

            try:
                print(f"⏳ [CHECK QDRANT INSERT] Uploading batch index group {i} to {batch_end}...")
                self.client.upload_records(
                    collection_name=collection_name,
                    records=batch_records,
                )
                print(f"✅ [CHECK QDRANT INSERT] Batch uploaded successfully.")
            except Exception as e:
                self.logger.error(f"Error while inserting batch: {e}")
                print(f"💥 [CHECK QDRANT INSERT] CRASH DURING UPLOAD_RECORDS: {str(e)}")
                return False

        print(f"📥 [CHECK QDRANT INSERT] === End insert_many (Success) ===\n")
        return True
        
    async def search_by_vector(self, collection_name: str, vector: list, limit: int = 5):

        results = self.client.search(
            collection_name=collection_name,
            query_vector=vector,
            limit=limit
        )

        if not results or len(results) == 0:
            return None
        
        return [
            RetrievedDocument(**{
                "score": result.score,
                "text": result.payload["text"],
            })
            for result in results
        ]
from .BaseController import BaseController
from models.db_schemes import Project, DataChunk
from stores.llm.LLMEnums import DocumentTypeEnum
from typing import List
import json

# Web search support
try:
    from duckduckgo_search import DDGS
    SEARCH_AVAILABLE = True
except ImportError:
    SEARCH_AVAILABLE = False

class NLPController(BaseController):

    def __init__(self, vectordb_client, generation_client, 
                 embedding_client, template_parser):
        super().__init__()

        self.vectordb_client = vectordb_client
        self.generation_client = generation_client
        self.embedding_client = embedding_client
        self.template_parser = template_parser

    def create_collection_name(self, project_id: str):
        return f"collection_{self.vectordb_client.default_vector_size}_{project_id}".strip()
    
    async def reset_vector_db_collection(self, project: Project):
        collection_name = self.create_collection_name(project_id=project.project_id)
        return await self.vectordb_client.delete_collection(collection_name=collection_name)
    
    async def get_vector_db_collection_info(self, project: Project):
        collection_name = self.create_collection_name(project_id=project.project_id)
        
        # 🟢 [التصحيح السحري]: شيلنا الـ await لأن الدالة متزامنة (Synchronous)
        collection_info = self.vectordb_client.get_collection_info(collection_name=collection_name)

        return json.loads(
            json.dumps(collection_info, default=lambda x: x.__dict__)
        )
    
    async def index_into_vector_db(self, project: Project, chunks: List[DataChunk],
                                   chunks_ids: List[int], 
                                   do_reset: bool = False):
        
        # step1: get collection name
        collection_name = self.create_collection_name(project_id=project.project_id)

        # step2: manage items
        texts = [ c.chunk_text for c in chunks ]
        metadata = [ c.chunk_metadata for c in  chunks]
        vectors = self.embedding_client.embed_text(text=texts, 
                                                  document_type=DocumentTypeEnum.DOCUMENT.value)

        # step3: create collection if not exists
        _ = await self.vectordb_client.create_collection(
            collection_name=collection_name,
            embedding_size=self.embedding_client.embedding_size,
            do_reset=do_reset,
        )

        # step4: insert into vector db
        _ = await self.vectordb_client.insert_many(
            collection_name=collection_name,
            texts=texts,
            metadata=metadata,
            vectors=vectors,
            record_ids=chunks_ids,
        )

        return True

    async def search_vector_db_collection(self, project: Project, text: str, limit: int = 10):
        print(f"\n🔍 [CHECK VECTOR SEARCH] === Start Search Vector DB ===")
        print(f"🔍 [CHECK VECTOR SEARCH] Target Project ID: {project.project_id}")

        # step1: get collection name
        query_vector = None
        collection_name = self.create_collection_name(project_id=project.project_id)
        print(f"🔍 [CHECK VECTOR SEARCH] Generated Collection Name: '{collection_name}'")

        # step2: get text embedding vector
        print(f"🔍 [CHECK VECTOR SEARCH] Calling embedding_client.embed_text...")
        vectors = self.embedding_client.embed_text(text=text, 
                                                 document_type=DocumentTypeEnum.QUERY.value)

        if not vectors or len(vectors) == 0:
            print(f"❌ [CHECK VECTOR SEARCH] Embedding FAILED! vectors is empty or None.")
            return False
        
        if isinstance(vectors, list) and len(vectors) > 0:
            query_vector = vectors[0]
            print(f"🔍 [CHECK VECTOR SEARCH] Vector extracted. Dimensions length: {len(query_vector) if query_vector else 0}")

        if not query_vector:
            print(f"❌ [CHECK VECTOR SEARCH] query_vector is None!")
            return False    

        # step3: do semantic search
        print(f"🔍 [CHECK VECTOR SEARCH] Querying Qdrant via search_by_vector...")
        results = await self.vectordb_client.search_by_vector(
            collection_name=collection_name,
            vector=query_vector,
            limit=limit
        )

        print(f"🔍 [CHECK VECTOR SEARCH] Qdrant Raw Response: {results}")
        print(f"🔍 [CHECK VECTOR SEARCH] Total matched chunks returned: {len(results) if results else 0}")
        print(f"🔍 [CHECK VECTOR SEARCH] === End Search Vector DB ===\n")

        if not results:
            return False

        return results
    
    async def answer_rag_question(self, project: Project, query: str, limit: int = 10):
        print(f"\n🔮 [CHECK CONTROLLER] Inside answer_rag_question core...")
        answer, full_prompt, chat_history = None, None, None

        # step1: retrieve related documents
        print(f"🔮 [CHECK CONTROLLER] Step 1: Querying Qdrant index for Project {project.project_id}...")
        retrieved_documents = await self.search_vector_db_collection(
            project=project,
            text=query,
            limit=limit,
        )
        
        print(f"🔮 [CHECK CONTROLLER] Qdrant search finished. Found documents count: {len(retrieved_documents) if retrieved_documents else 0}")

        if not retrieved_documents or len(retrieved_documents) == 0:
            print(f"⚠️ [CHECK CONTROLLER] Qdrant returned ZERO documents! Returning None early and triggering 400!")
            return answer, full_prompt, chat_history
        
        # step2: Construct LLM prompt
        print(f"🔮 [CHECK CONTROLLER] Step 2: Constructing templates...")
        system_prompt = self.template_parser.get("rag", "system_prompt")

        documents_prompts = "\n".join([
            self.template_parser.get("rag", "document_prompt", {
                    "doc_num": idx + 1,
                    "chunk_text": self.generation_client.process_text(doc.text),
            })
            for idx, doc in enumerate(retrieved_documents)
        ])

        footer_prompt = self.template_parser.get("rag", "footer_prompt", {
            "query": query
        })

        # step3: Construct Generation Client Prompts
        print(f"🔮 [CHECK CONTROLLER] Step 3: Setting chat history structures...")
        chat_history = [
            self.generation_client.construct_prompt(
                prompt=system_prompt,
                role=self.generation_client.enums.SYSTEM.value,
            )
        ]

        full_prompt = "\n\n".join([ documents_prompts,  footer_prompt])
        print(f"🔮 [CHECK CONTROLLER] Prompt compiled successfully. Length: {len(full_prompt)} chars.")

        # step4: Retrieve the Answer
        print(f"🔮 [CHECK CONTROLLER] Step 4: Invoking LLM text generation model...")
        try:
            answer = self.generation_client.generate_text(
                prompt=full_prompt,
                chat_history=chat_history
            )
            print(f"🔮 [CHECK CONTROLLER] LLM successfully replied! Response length: {len(answer) if answer else 0}")
        except Exception as e:
            print(f"💥 [CHECK CONTROLLER] CRASH DURING LLM TEXT GENERATION: {str(e)}")
            raise e

        print(f"🔮 [CHECK CONTROLLER] Execution finished smoothly.\n")
        return answer, full_prompt, chat_history

    def search_web(self, query: str, max_results: int = 3):
        """Search internet using DuckDuckGo (no API key needed)"""
        if not SEARCH_AVAILABLE:
            return {
                "success": False,
                "error": "Web search not available. Install: pip install duckduckgo-search"
            }
        
        try:
            backends = ['api', 'html', 'lite']
            last_error = None
            
            for backend in backends:
                try:
                    with DDGS() as ddgs:
                        results = list(ddgs.text(
                            query, 
                            max_results=max_results,
                            backend=backend
                        ))
                    
                    if results:
                        return {
                            "success": True,
                            "results": results,
                            "count": len(results)
                        }
                except Exception as e:
                    last_error = str(e)
                    continue
            
            return {
                "success": False,
                "error": f"All search backends failed. Last error: {last_error}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def answer_with_web_search(self, query: str, max_results: int = 3):
        """Generate answer using web search results"""
        import logging
        logger = logging.getLogger('uvicorn.error')
        
        logger.info(f"Starting web search for query: {query}")
        search_results = self.search_web(query, max_results)
        
        if not search_results.get("success"):
            error = search_results.get("error", "Unknown error")
            logger.error(f"Web search failed: {error}")
            return None, None
        
        logger.info(f"Web search successful, found {len(search_results['results'])} results")
        
        results_text = "\n\n".join([
            f"Source {i+1}: {r['title']}\n{r['body']}\nURL: {r['href']}"
            for i, r in enumerate(search_results["results"])
        ])
        
        system_prompt = "You are a helpful assistant. Answer the question using the provided web search results."
        
        full_prompt = f"""Web Search Results:
{results_text}

Question: {query}

Answer the question using the information from the search results above. Include relevant URLs."""
        
        logger.info("Generating LLM answer from search results...")
        
        chat_history = [
            self.generation_client.construct_prompt(
                prompt=system_prompt,
                role=self.generation_client.enums.SYSTEM.value,
            )
        ]
        
        answer = self.generation_client.generate_text(
            prompt=full_prompt,
            chat_history=chat_history
        )
        
        logger.info(f"LLM answer generated, length: {len(answer) if answer else 0}")
        
        return answer, search_results["results"]
"""
Upload & Process Page
Handles agricultural research log upload and vector data processing for Lumora
"""

import streamlit as st
from config import app_config
from utils import api_client, ui_components


def render():
    """Render the upload & process page"""
    
    st.markdown(f"""
    <h1 style='color: {app_config.PRIMARY_COLOR};'>📤 Ingest & Segment System Documents</h1>
    <p style='font-size: 1.1rem; color: #a5d6a7;'>
        Upload technical manuals, sensor specifications, and datasets to feed the Lumora Knowledge Base
    </p>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    project_id = st.session_state.project_id
    
    # Create tabs for different sections
    tab1, tab2 = st.tabs(["📁 Ingest Files", "⚙️ Neural Segmentation"])
    
    # ========================================================================
    # TAB 1: UPLOAD FILES
    # ========================================================================
    with tab1:
        st.markdown("### Upload Research & Hardware Sheets")
        
        ui_components.show_info(
            "Inject PDF blueprints or raw text manuals into the local repository buffer. "
            f"Maximum data stream payload size: {app_config.MAX_FILE_SIZE_MB} MB"
        )
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Choose a document target",
            type=app_config.ALLOWED_FILE_TYPES,
            help=f"Supported engineering formats: {', '.join(app_config.ALLOWED_FILE_TYPES).upper()}"
        )
        
        if uploaded_file is not None:
            # Display file information
            file_size_kb = uploaded_file.size / 1024
            
            st.markdown("#### 📋 Buffer Node Metadata")
            ui_components.render_file_info(
                filename=uploaded_file.name,
                filesize=file_size_kb,
                filetype=uploaded_file.type
            )
            
            # Check file size
            if file_size_kb > app_config.MAX_FILE_SIZE_MB * 1024:
                ui_components.show_error(
                    f"Buffer Overflow! Maximum allowed payload size is {app_config.MAX_FILE_SIZE_MB} MB"
                )
            else:
                # Upload button
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("🚀 Upload to Repository", use_container_width=True):
                        with ui_components.show_loading("Pushing binary stream to repository..."):
                            result = api_client.upload_file(
                                project_id=project_id,
                                file=uploaded_file,
                                filename=uploaded_file.name
                            )
                        
                        if "error" in result:
                            ui_components.show_error(f"Ingestion failed: {result['error']}")
                        else:
                            file_id = result.get('file_id', 'N/A')
                            ui_components.show_success(
                                f"Payload securely buffered! Document Node ID: {file_id}"
                            )
                            st.balloons()
                            
                            # Store in session state
                            if 'uploaded_files' not in st.session_state:
                                st.session_state.uploaded_files = []
                            st.session_state.uploaded_files.append({
                                'filename': uploaded_file.name,
                                'file_id': file_id,
                                'project_id': project_id
                            })
        
        # Show uploaded files for this project
        if st.session_state.get('uploaded_files'):
            st.markdown("---")
            st.markdown("### 📚 Buffered Corpus Nodes (Active Session)")
            
            project_files = [
                f for f in st.session_state.uploaded_files 
                if f['project_id'] == project_id
            ]
            
            if project_files:
                for file_info in project_files:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"📄 **{file_info['filename']}**")
                    with col2:
                        st.code(file_info['file_id'], language=None)
            else:
                ui_components.show_info("No files buffered for this specific system cycle yet.")
    
    # ========================================================================
    # TAB 2: PROCESS DOCUMENTS
    # ========================================================================
    with tab2:
        st.markdown("### Structural Document Tokenization")
        
        ui_components.show_info(
            "Configure structural text splitting configurations. "
            "This splits raw documents into discrete contextual chunks before embedding generation."
        )
        
        # Processing form
        with st.form("process_form", clear_on_submit=False):
            st.markdown("#### ⚙️ Segmentation Matrix")
            
            col1, col2 = st.columns(2)
            
            with col1:
                chunk_size = st.number_input(
                    "Token Block Capacity (chars)",
                    min_value=app_config.CHUNK_SIZE_MIN,
                    max_value=app_config.CHUNK_SIZE_MAX,
                    value=app_config.CHUNK_SIZE_DEFAULT,
                    step=100,
                    help="Character sequence depth per individual text block target."
                )
            
            with col2:
                overlap_size = st.number_input(
                    "Sliding Window Overlap (chars)",
                    min_value=app_config.OVERLAP_SIZE_MIN,
                    max_value=app_config.OVERLAP_SIZE_MAX,
                    value=app_config.OVERLAP_SIZE_DEFAULT,
                    step=50,
                    help="Inter-chunk redundancy sequence to maintain semantic context at chunk junctions."
                )
            
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            
            with col1:
                do_reset = st.checkbox(
                    "🔄 Flush Existing Chunks",
                    value=False,
                    help="Wipe all prior parsed blocks under this project ID before reprocessing"
                )
            
            with col2:
                file_id = st.text_input(
                    "Target File Node ID (Optional)",
                    value="",
                    help="Isolate pipeline execution to a single specific node hash. Leave blank for all."
                )
            
            st.markdown("---")
            
            # Submit button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                submitted = st.form_submit_button(
                    "⚡ Execute Structural Parsing",
                    use_container_width=True
                )
            
        # Handle form submission OUTSIDE the form context
        if submitted:
            # Process documents
            st.markdown("### 🔄 Ingestion Pipeline Graph Status")
            
            with ui_components.show_loading("Executing regex token split patterns... This may take a few seconds."):
                result = api_client.process_documents(
                    project_id=project_id,
                    chunk_size=chunk_size,
                    overlap_size=overlap_size,
                    file_id=file_id if file_id else None,
                    do_reset=1 if do_reset else 0
                )
            
            if "error" in result:
                ui_components.show_error(f"Processing failed: {result['error']}")
            else:
                inserted_chunks = result.get('inserted_chunks', 0)
                processed_files = result.get('processed_files', 0)
                
                ui_components.show_success(
                    f"Segmentation complete! {processed_files} structural nodes parsed, "
                    f"{inserted_chunks} vector payload points prepared."
                )
                
                st.session_state.processing_status = {
                    'chunks': inserted_chunks,
                    'files': processed_files
                }
                
                # Set flag to show index button
                st.session_state.ready_to_index = True
                st.rerun()  # Rerun to exit form context
        
    # Show index button OUTSIDE tab2 context if processing completed
    if st.session_state.get('ready_to_index', False):
        st.markdown("---")
        st.markdown("### 🔄 Secondary Pipeline Vector Synching")
        st.info("💡 Document text points ready. Click below to commit coordinates to Qdrant Vector DB.")
        
        if st.button("🚀 Push to Qdrant Vector Space", use_container_width=True, key="index_button"):
            with ui_components.show_loading("Extracting embeddings & calculating high-density coordinates..."):
                index_result = api_client.push_to_index(
                    project_id=project_id,
                    do_reset=0  # Don't reset when auto-indexing
                )
            
            if "error" in index_result:
                ui_components.show_error(f"Vector committing failed: {index_result['error']}")
            else:
                indexed_count = index_result.get('inserted_items_count', 0)
                ui_components.show_success(
                    f"✅ Ingestion finalized! {indexed_count} vector points mapped to Qdrant clusters successfully."
                )
                st.balloons()
                # Clear the flag after successful indexing
                st.session_state.ready_to_index = False
                st.rerun()
    
    # Show processing stats if available (moved outside tab context)
    if st.session_state.get('processing_status'):
        st.markdown("---")
        st.markdown("### 📊 Pipeline Metric Feedback")
        
        col1, col2 = st.columns(2)
        
        with col1:
            ui_components.render_metric_card(
                title="Committed Corpora Docs",
                value=str(st.session_state.processing_status['files']),
                icon="📄"
            )
        
        with col2:
            ui_components.render_metric_card(
                title="Active Vector Space Chunks",
                value=str(st.session_state.processing_status['chunks']),
                icon="📦"
            )
    
    st.markdown("---")
    
    # Help section
    with st.expander("❓ Neural Pipeline Mechanics"):
        st.markdown("""
        ### Understanding Token Ingestion Boundaries
        
        **Segment Density (Chunk Size):**
        - Controls character limits inside single index records.
        - Recommended parameters: 1000-1500 characters for sensor manuals.
        - Small sizes optimize retrieval speeds but increase prompt fragmentation risk.
        
        **Context Overlap:**
        - Sequence duplication margin flanking adjacent chunk margins.
        - Preserves sentence context across hard block slices.
        - Recommended setting: ~15-20% of maximum block size.
        
        **Wipe Index State:**
        - Erases prior records inside the chosen Project ID workspace to build clean embeddings namespaces.
        """)
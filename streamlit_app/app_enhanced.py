"""
Lumora Smart Aquaponic System - Professional Dashboard (Enhanced Version)
Advanced UI/UX with Lumora Agriculture Branding
Powered by Automation and AI Integration

This is the production-ready version with enhanced UI/UX while maintaining
all working logic from streamlit_app_version2.py
"""

import streamlit as st
import requests
import os
from typing import Optional
import json
from io import BytesIO
from pydantic import BaseModel
import time
from datetime import datetime

# ============================================================================
# CONFIGURATION
# ============================================================================

API_BASE_URL = "http://127.0.0.1:8000"

# ============================================================================
# PYDANTIC MODELS (Same as version2 - Don't change, they work!)
# ============================================================================

class ProcessRequest(BaseModel):
    file_id: Optional[str] = ""
    chunk_size: Optional[int] = 100
    overlap_size: Optional[int] = 20
    do_reset: Optional[int] = 0

class SearchRequest(BaseModel):
    text: str
    limit: int = 5

class PushRequest(BaseModel):
    do_reset: int = 0

# ============================================================================
# API FUNCTIONS (Same as version2 - Don't change, they work!)
# ============================================================================

def upload_file(project_id: int, file: BytesIO, filename: str):
    content_type = 'application/pdf' if filename.lower().endswith('.pdf') else file.type
    files = {'file': (filename, file, content_type)}
    url = f"{API_BASE_URL}/api/v1/data/upload/{project_id}"
    response = requests.post(url, files=files)
    return response.json()

def process_file(project_id: int, process_request: ProcessRequest):
    url = f"{API_BASE_URL}/api/v1/data/process/{project_id}"    
    response = requests.post(url, json=process_request.model_dump())
    return response.json()

def push_to_index(project_id: int, push_request: PushRequest):
    url = f"{API_BASE_URL}/api/v1/nlp/index/push/{project_id}"
    response = requests.post(url, json=push_request.model_dump())
    return response.json()

def get_index_info(project_id: int):
    url = f"{API_BASE_URL}/api/v1/nlp/index/info/{project_id}"
    response = requests.get(url)
    return response.json()

def search_index(project_id: int, search_request: SearchRequest):
    url = f"{API_BASE_URL}/api/v1/nlp/index/search/{project_id}"
    response = requests.post(url, json=search_request.model_dump())
    return response.json()

def ask_question(project_id: int, search_request: SearchRequest):
    url = f"{API_BASE_URL}/api/v1/nlp/index/answer/{project_id}"
    response = requests.post(url, json=search_request.model_dump())
    return response.json()

# ============================================================================
# UI HELPER FUNCTIONS (New - Enhanced UX with Lumora Theme)
# ============================================================================

def render_header():
    """Render the app header with Lumora branding"""
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col1:
        logo_path = "assets/lumora_logo.png"
        if os.path.exists(logo_path):
            st.image(logo_path, width=250)
        else:
            st.markdown("<h1 style='color: #4caf50; margin-top: 15px;'>🌿 LUMORA</h1>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h1 style='color: #ffffff; margin: 0; font-size: 2.5rem; font-weight: 800;'>Lumora Advanced Matrix</h1>
            <p style='color: #a5d6a7; font-size: 1.1rem; margin: 5px 0;'>
                Intelligent Corpus Processing & AI-Powered Aquaponic Inferences
            </p>
            <p style='color: #6c757d; font-size: 0.95rem; margin: 5px 0;'>
                Secured Local RAG Computational Infrastructure
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='text-align: right; padding: 10px;'>
            <p style='color: #6c757d; font-size: 0.9rem; margin: 0;'>
                Version 3.0<br>
                Production UI
            </p>
        </div>
        """, unsafe_allow_html=True)

def render_footer():
    """Render the app footer with credits"""
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(90deg, #11141a 0%, #2e7d32 100%); 
                border-radius: 10px; margin-top: 30px; border: 1px solid #4caf50;'>
        <p style='color: white; font-size: 1rem; margin: 5px 0; font-weight: 600;'>
            🚀 Local Knowledge Augmentation Stack | <strong>Lumora Core Systems</strong>
        </p>
        <p style='color: #a5d6a7; font-size: 0.85rem; margin: 5px 0;'>
            Advanced AI Solutions • Document Intelligence • Local Confined Privacy Architecture
        </p>
    </div>
    """, unsafe_allow_html=True)

def show_status_card(title: str, value: str, icon: str, color: str = "#2e7d32"):
    """Display a status card synced with Lumora colors"""
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #11141a 0%, #1a1f2e 100%); 
                border: 2px solid {color}; padding: 20px; border-radius: 12px; margin: 15px 0;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);'>
        <div style='display: flex; align-items: center; justify-content: center;'>
            <span style='font-size: 2.5rem; margin-right: 20px;'>{icon}</span>
            <div style='text-align: center;'>
                <p style='color: #a5d6a7; font-size: 1rem; margin: 0; font-weight: 500; text-transform: uppercase;'>{title}</p>
                <p style='color: #ffffff; font-size: 2rem; font-weight: 700; margin: 8px 0;'>{value}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_success_message(message: str, show_balloons: bool = False):
    """Display success message with optional animation"""
    st.success(f"✅ {message}")
    if show_balloons:
        st.balloons()

def show_error_message(message: str):
    """Display error message"""
    st.error(f"❌ {message}")

def show_info_box(message: str):
    """Display info box"""
    st.info(f"💡 {message}")

# ============================================================================
# PAGE FUNCTIONS
# ============================================================================

def render_upload_process_page(project_id: int):
    """Upload & Process Documents Page"""
    
    st.markdown("## 📤 Ingest & Segment System Documents")
    st.markdown("Upload technical sheets or datasets and process them into searchable vector blocks")
    st.markdown("---")
    
    # Project ID display
    show_status_card("Active Cycle Project ID", f"#{project_id}", "🎯", "#4caf50")
    
    # Upload Section
    st.markdown("### 📁 Buffer Payload Ingestion")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Choose target manual fileset",
            type=["txt", "pdf"],
            help="Upload PDF specs or TXT logs for vector parsing"
        )
    
    with col2:
        if uploaded_file is not None:
            st.markdown("#### 📊 Buffer Data Node Metrics")
            st.markdown(f"**Name:** {uploaded_file.name}")
            st.markdown(f"**Size:** {uploaded_file.size / 1024:.2f} KB")
            st.markdown(f"**Mime Type:** {uploaded_file.type}")
    
    if uploaded_file is not None:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Upload to Repository", use_container_width=True, type="primary"):
                with st.spinner("⏳ Streaming binary bytes to node buffer..."):
                    try:
                        result = upload_file(project_id, uploaded_file, uploaded_file.name)
                        show_success_message("Payload securely buffered!", show_balloons=True)
                        
                        # Display result in expandable section
                        with st.expander("📋 View Ingestion Handle Metadata", expanded=True):
                            st.json(result)
                            
                            if "file_id" in result:
                                st.session_state.last_file_id = result["file_id"]
                                st.success(f"🆔 Document Node Hash: `{result['file_id']}`")
                    except Exception as e:
                        show_error_message(f"Ingestion failed: {str(e)}")
    
    st.markdown("---")
    
    # Processing Section
    st.markdown("### ⚙️ Regex Structural Tokenization")
    st.markdown("Configure sliding window parameters and slice your buffered documentation blocks")
    
    # Enhanced processing form with custom dark/green theme and sharp visibility
    st.markdown("""
    <style>
        div[data-testid="stForm"] {
            background: linear-gradient(135deg, #11141a 0%, #1a1f2e 100%) !important;
            padding: 30px !important;
            border-radius: 12px !important;
            border: 2px solid #2e7d32 !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.4) !important;
        }
        div[data-testid="stForm"] label {
            color: #ffffff !important;
            font-weight: 600 !important;
            font-size: 1.05rem !important;
        }
        div[data-testid="stForm"] p {
            color: #a5d6a7 !important;
        }
        div[data-testid="stForm"] h4 {
            color: #ffffff !important;
            font-weight: 700 !important;
            margin-bottom: 20px !important;
        }
        div[data-testid="stForm"] input {
            background-color: #1a1f2e !important;
            border: 2px solid #2e7d32 !important;
            color: #ffffff !important;
            font-weight: 500 !important;
        }
        div[data-testid="stForm"] .stNumberInput > div > div > input {
            color: #ffffff !important;
            font-size: 1.1rem !important;
        }
        div[data-testid="stForm"] .stTextInput > div > div > input {
            color: #ffffff !important;
            font-size: 1.1rem !important;
        }
        div[data-testid="stForm"] .stCheckbox > label > div {
            color: #ffffff !important;
        }
        div[data-testid="stForm"] small {
            color: #a5d6a7 !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    with st.form("process_form", clear_on_submit=False):
        st.markdown("""
        <div style='background-color: #1a1f2e; padding: 15px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #2e7d32;'>
            <h4 style='color: #ffffff; font-weight: 600; margin: 0; text-align: center;'>
                🔧 Segmentation Matrix Parameters
            </h4>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            chunk_size = st.number_input(
                "Token Block Size (characters)",
                min_value=100,
                max_value=5000,
                value=1000,
                step=100,
                help="Max capacity size per text slice block"
            )
            
            file_id = st.text_input(
                "Target Node ID restriction (optional)",
                value="",
                placeholder="Leave empty to slice all files",
                help="Isolate tokenization path to a single node hash, or leave blank for all"
            )
        
        with col2:
            overlap_size = st.number_input(
                "Sliding Window Overlap (characters)",
                min_value=0,
                max_value=500,
                value=200,
                step=50,
                help="Semantics redundancy sequence flanked at chunk junctions"
            )
            
            do_reset = st.checkbox(
                "🔄 Flush Prior Namespace Records",
                value=False,
                help="Wipe all older text splits belonging to this project ID before compilation"
            )
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submitted = st.form_submit_button(
                "⚡ Execute Structural Parsing",
                use_container_width=True,
                type="primary"
            )
        
        if submitted:
            st.markdown("---")
            st.markdown("### 🔄 Ingestion Pipeline Execution Graph")
            
            # Process documents
            process_req = {
                "chunk_size": chunk_size,
                "overlap_size": overlap_size,
                "do_reset": 1 if do_reset else 0,
                "file_id": file_id if file_id.strip() else ""
            }
            process_req = ProcessRequest(**process_req)
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Step 1: Process
                status_text.text("📝 Executing segmentation algorithm slices...")
                progress_bar.progress(33)
                
                result = process_file(project_id=project_id, process_request=process_req)
                
                progress_bar.progress(66)
                status_text.text("✅ Segment blocks successfully compiled!")
                
                show_success_message("Text splits successfully saved to data layer!", show_balloons=False)
                
                with st.expander("📋 View Document Node Splitting Logs", expanded=True):
                    st.json(result)
                
                st.markdown("---")
                
                # Step 2: Index
                st.markdown("### 🔄 Multi-Tenant Vector Space Syncing")
                status_text.text("🗂️ Calculating embeddings & committing coordinates to Qdrant cluster...")
                
                do_reset_index = 0
                push_req = PushRequest(do_reset=do_reset_index)
                
                index_result = push_to_index(project_id, push_req)
                
                progress_bar.progress(100)
                status_text.text("✅ Ingestion protocol completed successfully!")
                
                show_success_message("All vector coordinates mapped to Qdrant spatial layers successfully!", show_balloons=False)
                
                with st.expander("📋 View Spatial Index Commit Registry", expanded=True):
                    st.json(index_result)
                
                # Clear progress indicators
                time.sleep(1)
                progress_bar.empty()
                status_text.empty()
                
            except Exception as e:
                progress_bar.empty()
                status_text.empty()
                show_error_message(f"Pipeline execution faulted: {str(e)}")

def render_search_query_page(project_id: int):
    """Search & Query Documents Page"""
    
    st.markdown("## 💬 Real-Time Contextual Inferences Gateway")
    st.markdown("Query spatial index nodes or chat with the automated aquaponic expert system")
    st.markdown("---")
    
    # Project ID display
    show_status_card("Active Cluster Namespace", f"Cycle #{project_id}", "🎯", "#2e7d32")
    
    # Create tabs for different query modes
    tab1, tab2 = st.tabs(["🤖 Query System Expert (RAG)", "🔍 Spatial Vectors Lookup"])
    
    # ========================================================================
    # TAB 1: ASK QUESTIONS
    # ========================================================================
    with tab1:
        st.markdown("### 🤖 Contextual Expert Insights Generation")
        
        show_info_box(
            "Query your uploaded ecosystem models. The context window engine will query Qdrant coordinates "
            "and map relevant knowledge directly into the LLM prompt payload for grounded factual outputs."
        )
        
        # Question input
        question = st.text_area(
            "Your Ecosystem Query",
            height=120,
            placeholder="e.g., What are the optimal water temperature ranges and dissolved oxygen thresholds for Tilapia?",
            help="Type your engineering question here. Be highly explicit for precise semantic lookup weights."
        )
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            pass  # Spacer
        
        with col2:
            limit = st.slider(
                "Inject Window Limit (k)",
                min_value=1,
                max_value=20,
                value=5,
                help="Max similarity chunk nodes to harvest for prompt context enrichment"
            )
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            ask_button = st.button(
                "🚀 Execute Pipeline Inference",
                use_container_width=True,
                type="primary"
            )
        
        if ask_button:
            if not question.strip():
                st.warning("⚠️ Enter a valid string query input!")
            else:
                with st.spinner("🤔 Harvesting nearest context blocks & computing inference logs..."):
                    try:
                        search_req = SearchRequest(text=question, limit=limit)
                        result = ask_question(project_id, search_req)
                        
                        if "answer" in result:
                            st.markdown("---")
                            st.markdown("### 🎯 System Insight Output")
                            
                            # Display as chat messages
                            with st.chat_message("user"):
                                st.markdown(question)
                            
                            with st.chat_message("assistant"):
                                st.markdown(result["answer"])
                            
                            # Success feedback
                            show_success_message("Inference execution finished successfully!", show_balloons=False)
                            
                            # Store in session state for history
                            if 'qa_history' not in st.session_state:
                                st.session_state.qa_history = []
                            
                            st.session_state.qa_history.append({
                                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                'question': question,
                                'answer': result["answer"],
                                'project_id': project_id
                            })
                            
                            # Show details
                            with st.expander("📄 View Augmented Pipeline Full Payload"):
                                st.markdown("**Full Injected Context Prompt Graph:**")
                                st.text_area(
                                    "Prompt Matrix",
                                    value=result.get("full_prompt", ""),
                                    height=200,
                                    disabled=True
                                )
                                
                                if result.get("chat_history"):
                                    st.markdown("**Historical Memory Tokens Array:**")
                                    st.json(result["chat_history"])
                            
                            # Download option
                            st.markdown("---")
                            col1, col2, col3 = st.columns([1, 2, 1])
                            with col2:
                                download_data = {
                                    "question": question,
                                    "answer": result["answer"],
                                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    "project_id": project_id,
                                    "full_prompt": result.get("full_prompt", ""),
                                    "chat_history": result.get("chat_history", [])
                                }
                                
                                st.download_button(
                                    label="💾 Download Inference Artifact (JSON)",
                                    data=json.dumps(download_data, indent=2),
                                    file_name=f"lumora_inference_{int(time.time())}.json",
                                    mime="application/json",
                                    use_container_width=True
                                )
                        else:
                            show_error_message("Generation routine faulted at backend client")
                            st.json(result)
                            
                    except Exception as e:
                        show_error_message(f"Inference pipeline aborted: {str(e)}")
    
    # ========================================================================
    # TAB 2: SEARCH DOCUMENTS
    # ========================================================================
    with tab2:
        st.markdown("### 🔍 Spatial Density Vector Search")
        
        show_info_box(
            "Query the multi-dimensional vector grid via dot product or cosine distance. "
            "Returns localized text segments ranked strictly by semantic similarity indices."
        )
        
        # Search input
        col1, col2 = st.columns([3, 1])
        
        with col1:
            search_query = st.text_input(
                "Semantic Vector Query String",
                placeholder="e.g., Modbus register mapping for pH analog probe transmitter data",
                help="Input the diagnostic string target"
            )
        
        with col2:
            search_limit = st.slider(
                "Hits Max",
                min_value=1,
                max_value=20,
                value=5,
                help="Max nearest points coordinates to capture from Qdrant clusters"
            )
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            search_button = st.button(
                "🔍 Execute Vector Scanning",
                use_container_width=True,
                type="primary"
            )
        
        if search_button:
            if not search_query.strip():
                st.warning("⚠️ Input target query cannot be empty string!")
            else:
                with st.spinner("🔍 Executing hyper-plane distance calculation checks..."):
                    try:
                        search_req = SearchRequest(text=search_query, limit=search_limit)
                        result = search_index(project_id, search_req)
                        
                        if "results" in result:
                            results = result.get("results", [])
                            
                            if not results:
                                st.info("ℹ️ Zero points resolved in the active project vector coordinates.")
                            else:
                                st.markdown("---")
                                st.markdown(f"### 📊 Resolved Coordinates Hits ({len(results)} points found)")
                                
                                show_success_message(f"Resolved {len(results)} exact high-match text points!", show_balloons=False)
                                
                                # Display results
                                for i, res in enumerate(results, 1):
                                    score = res.get('score', 0)
                                    text = res.get('chunk_text', '')
                                    metadata = res.get('chunk_metadata', {})
                                    
                                    # Color code based on relevance weights
                                    if score > 0.8:
                                        border_color = "#28a745"  # Green
                                    elif score > 0.6:
                                        border_color = "#ffc107"  # Yellow
                                    else:
                                        border_color = "#6c757d"  # Gray
                                    
                                    with st.expander(
                                        f"📝 Node Point {i} - Distance Weight Score: {score:.4f}",
                                        expanded=(i == 1)
                                    ):
                                        st.markdown(f"""
                                        <div style='border-left: 4px solid {border_color}; padding-left: 15px;'>
                                        """, unsafe_allow_html=True)
                                        
                                        st.markdown("**Segment Content Data:**")
                                        st.write(text)
                                        
                                        if metadata:
                                            st.markdown("---")
                                            st.markdown("**Node Metadata Payload Hierarchy:**")
                                            st.json(metadata)
                                        
                                        st.markdown("</div>", unsafe_allow_html=True)
                                
                                # Export results
                                st.markdown("---")
                                col1, col2, col3 = st.columns([1, 2, 1])
                                with col2:
                                    export_data = {
                                        "query": search_query,
                                        "total_results": len(results),
                                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                        "project_id": project_id,
                                        "results": results
                                    }
                                    
                                    st.download_button(
                                        label="💾 Export Vector Hits Topology (JSON)",
                                        data=json.dumps(export_data, indent=2),
                                        file_name=f"vector_hits_{int(time.time())}.json",
                                        mime="application/json",
                                        use_container_width=True
                                    )
                        else:
                            show_error_message("Vector index retrieval routine aborted by cluster")
                            st.json(result)
                            
                    except Exception as e:
                        show_error_message(f"Search operation terminated: {str(e)}")

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    # Page configuration
    st.set_page_config(
        page_title="Lumora Advanced RAG Matrix",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for professional dark/green agriculture theme
    st.markdown("""
    <style>
        /* Main theme colors */
        :root {
            --primary-color: #2e7d32;
            --secondary-color: #0f1419;
            --accent-color: #4caf50;
        }
        
        /* Enhanced button styling */
        .stButton>button {
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s ease;
            border: none;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(46, 125, 50, 0.3);
        }
        
        /* Form styling */
        .stForm {
            background: #1a1f2e;
            padding: 20px;
            border-radius: 10px;
            border: 2px solid #2e7d32;
        }
        
        /* Expander styling */
        .streamlit-expanderHeader {
            background-color: #1a1f2e;
            border-radius: 8px;
            font-weight: 600;
            color: white;
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
        }
        
        .stTabs [data-baseweb="tab"] {
            border-radius: 8px 8px 0 0;
            padding: 10px 20px;
            font-weight: 600;
        }
        
        /* Card styling */
        .element-container {
            margin-bottom: 10px;
        }
        
        /* Success/Error message styling */
        .stSuccess, .stError, .stWarning, .stInfo {
            border-radius: 8px;
            padding: 15px;
            font-weight: 500;
        }
        
        /* File uploader styling */
        .uploadedFile {
            border-radius: 8px;
            background: #1a1f2e;
            padding: 10px;
        }
        
        /* Chat message styling */
        .stChatMessage {
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Render header
    render_header()
    
    st.markdown("---")
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("### 🧭 Matrix Routes Map")
        
        page = st.radio(
            "Select Active Viewport Layer",
            ["📤 Upload & Process", "💬 Search & Query"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Project ID input
        st.markdown("### ⚙️ Cluster Configurations")
        project_id = st.number_input(
            "Tenant Project Cycle ID",
            min_value=1,
            value=1,
            help="Select the isolated namespace ID in Qdrant cluster"
        )
        
        st.markdown("---")
        
        # API Status
        st.markdown("### 🔗 Cluster Latency Health")
        if st.button("PING Backend Target Node", use_container_width=True):
            with st.spinner("Executing socket handshake..."):
                try:
                    response = requests.get(f"{API_BASE_URL}/api/v1/", timeout=5)
                    if response.status_code == 200:
                        st.success("✅ Handshake 200 OK!")
                        st.json(response.json())
                    else:
                        st.error(f"❌ Handshake faulted. Code: {response.status_code}")
                except Exception as e:
                    st.error(f"❌ Connection timeout: {str(e)}")
        
        st.markdown("---")
        
        # Quick Stats
        st.markdown("### 📊 Active Cluster Context")
        st.markdown(f"**Tenant Namespace Target:** `Cycle #{project_id}`")
        st.markdown(f"**Resolved Backend Core Address:** `{API_BASE_URL}`")
        
        if 'qa_history' in st.session_state:
            st.markdown(f"**Cached Inferences Pool:** {len(st.session_state.qa_history)} tracks")
        
        if 'last_file_id' in st.session_state:
            st.markdown(f"**Active Ingest Node Hash:** `{st.session_state.last_file_id}`")
        
        st.markdown("---")
        
        # Help section
        with st.expander("❓ Operations Guideline Docs"):
            st.markdown("""
            **Deployment Lifecycle Instructions:**
            
            1️⃣ Buffer data node payload logs (PDF/TXT)
            2️⃣ Execute token splits regex compiler
            3️⃣ Automatic coordinates synthesis into Qdrant index space
            4️⃣ Query contextual expert engine safely
            
            **Best Engineering Practices:**
            - Input clear parameters names when querying calibrations.
            - Keep sliding chunk weights at 1000 characters boundaries.
            - Purge cluster metadata registry layers prior to new deployment cycles.
            """)
    
    # Main content area
    if page == "📤 Upload & Process":
        render_upload_process_page(project_id)
    elif page == "💬 Search & Query":
        render_search_query_page(project_id)
    
    # Render footer
    render_footer()

# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == "__main__":
    main()
"""
Lumora Smart Aquaponic System - ChatGPT Style Interface
Advanced Chat UI with Lumora Agriculture Branding
Powered by Automation and AI Integration
"""

import streamlit as st
import requests
import os
from typing import Optional, List, Dict
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
# PYDANTIC MODELS
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
# API FUNCTIONS
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
# SESSION STATE INITIALIZATION
# ============================================================================

def init_session_state():
    """Initialize session state variables"""
    if 'chat_sessions' not in st.session_state:
        st.session_state.chat_sessions = []
    
    if 'current_chat_id' not in st.session_state:
        st.session_state.current_chat_id = None
    
    if 'current_messages' not in st.session_state:
        st.session_state.current_messages = []
    
    if 'project_id' not in st.session_state:
        st.session_state.project_id = 1
    
    if 'context_limit' not in st.session_state:
        st.session_state.context_limit = 3
    
    if 'show_settings' not in st.session_state:
        st.session_state.show_settings = False

def create_new_chat():
    """Create a new chat session"""
    chat_id = f"chat_{int(time.time())}"
    chat_session = {
        'id': chat_id,
        'name': f"Ecosystem Run {len(st.session_state.chat_sessions) + 1}",
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'messages': []
    }
    st.session_state.chat_sessions.append(chat_session)
    st.session_state.current_chat_id = chat_id
    st.session_state.current_messages = []
    return chat_id

def load_chat(chat_id: str):
    """Load a specific chat session"""
    for session in st.session_state.chat_sessions:
        if session['id'] == chat_id:
            st.session_state.current_chat_id = chat_id
            st.session_state.current_messages = session['messages']
            break

def save_current_chat():
    """Save current messages to the active chat session"""
    if st.session_state.current_chat_id:
        for session in st.session_state.chat_sessions:
            if session['id'] == st.session_state.current_chat_id:
                session['messages'] = st.session_state.current_messages
                break

def add_message(role: str, content: str, metadata: dict = None):
    """Add a message to the current chat"""
    message = {
        'role': role,
        'content': content,
        'timestamp': datetime.now().strftime("%H:%M:%S"),
        'metadata': metadata or {}
    }
    st.session_state.current_messages.append(message)
    save_current_chat()

# ============================================================================
# UI COMPONENTS
# ============================================================================

def render_chat_message(message: dict):
    """Render a single chat message synced with Lumora palette"""
    role = message['role']
    content = message['content']
    timestamp = message.get('timestamp', '')
    
    if role == 'user':
        # User message - right aligned, Lumora Green Gradient
        st.markdown(f"""
        <div style='display: flex; justify-content: flex-end; margin: 15px 0;'>
            <div style='max-width: 70%; background: linear-gradient(135deg, #2e7d32 0%, #1a1f2e 100%); 
                        color: white; padding: 15px 20px; border-radius: 18px 18px 4px 18px;
                        box-shadow: 0 4px 12px rgba(46, 125, 50, 0.25); border-right: 3px solid #4caf50;'>
                <p style='margin: 0; font-size: 1rem; line-height: 1.5; font-weight: 500;'>{content}</p>
                <p style='margin: 8px 0 0 0; font-size: 0.75rem; opacity: 0.9; text-align: right;'>{timestamp} | Operator</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Assistant message - left aligned, Matrix Dark Slate Gradient
        st.markdown(f"""
        <div style='display: flex; justify-content: flex-start; margin: 15px 0;'>
            <div style='max-width: 70%; background: linear-gradient(135deg, #11141a 0%, #1a1f2e 100%); 
                        color: #e8eef5; padding: 15px 20px; border-radius: 18px 18px 18px 4px;
                        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3); border: 2px solid #2e7d32;'>
                <p style='margin: 0; font-size: 1rem; line-height: 1.5; font-weight: 400; color: #ffffff;'>{content}</p>
                <p style='margin: 8px 0 0 0; font-size: 0.75rem; color: #a5d6a7; text-align: left;'>{timestamp} | Lumora Expert</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_sidebar():
    """Render the chat history sidebar"""
    with st.sidebar:
        try:
            st.image("assets/lumora_logo.png", width=150)
        except:
            st.markdown("""
            <div style='text-align: center; padding: 10px 0;'>
                <h2 style='color: #4caf50; margin: 0; font-weight: 900; letter-spacing: 2px;'>LUMORA</h2>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='text-align: center; padding: 5px 0; margin-bottom: 15px;'>
            <h3 style='color: #2e7d32; margin: 0; font-size: 1.2rem;'>Aquaponic RAG Chat</h3>
            <p style='color: #a5d6a7; font-size: 0.85rem; margin: 5px 0; font-weight: 500;'>
                Next-Gen Sustainable Automation<br>Ecosystem Interface
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # New Chat Button
        if st.button("➕ New Ingestion Run", use_container_width=True, type="primary"):
            create_new_chat()
            st.rerun()
        
        st.markdown("---")
        
        # Settings toggle
        if st.button("⚙️ Core Hyperparameters", use_container_width=True):
            st.session_state.show_settings = not st.session_state.show_settings
        
        if st.session_state.show_settings:
            st.markdown("""
            <div style='background: linear-gradient(135deg, #11141a 0%, #1a1f2e 100%); 
                        padding: 10px; border-radius: 8px; margin: 10px 0; border: 1px solid #2e7d32;'>
                <h4 style='color: #4caf50; margin: 0; text-align: center; font-size: 0.9rem;'>Pipeline Configuration</h4>
            </div>
            """, unsafe_allow_html=True)
            
            st.session_state.project_id = st.number_input(
                "Cycle Project ID",
                min_value=1,
                value=st.session_state.project_id,
                help="Isolate vector memory via choosing project code"
            )
            
            st.session_state.context_limit = st.slider(
                "Retrieved Windows (k)",
                min_value=1,
                max_value=10,
                value=st.session_state.context_limit,
                help="Max similarity text points to retrieve from Qdrant"
            )
        
        st.markdown("---")
        
        # Chat History
        st.markdown("### 💬 Ingestion Run History")
        
        if not st.session_state.chat_sessions:
            st.info("No recorded sessions yet.")
        else:
            for session in reversed(st.session_state.chat_sessions):
                is_active = session['id'] == st.session_state.current_chat_id
                button_type = "primary" if is_active else "secondary"
                
                col1, col2 = st.columns([4, 1])
                with col1:
                    if st.button(
                        f"{'📌' if is_active else '💬'} {session['name']}", 
                        key=f"chat_{session['id']}",
                        use_container_width=True,
                        type=button_type
                    ):
                        load_chat(session['id'])
                        st.rerun()
                
                with col2:
                    if st.button("🗑️", key=f"del_{session['id']}", help="Wipe run log"):
                        st.session_state.chat_sessions = [
                            s for s in st.session_state.chat_sessions if s['id'] != session['id']
                        ]
                        if st.session_state.current_chat_id == session['id']:
                            if st.session_state.chat_sessions:
                                load_chat(st.session_state.chat_sessions[-1]['id'])
                            else:
                                st.session_state.current_chat_id = None
                                st.session_state.current_messages = []
                        st.rerun()
                
                st.markdown(f"<p style='font-size: 0.7rem; color: #a5d6a7; margin: 0; padding-left: 5px;'>{session['created_at']}</p>", unsafe_allow_html=True)
                st.markdown("---")
        
        # File Upload Section
        with st.expander("📤 Repository Ingestion Buffer", expanded=False):
            st.markdown("""
            <div style='background: #11141a; padding: 10px; border-radius: 8px; margin-bottom: 10px; border-left: 3px solid #2e7d32;'>
                <p style='color: #ffffff; margin: 0; font-weight: 600; font-size: 0.85rem;'>📁 Ingest Manuals/Data</p>
            </div>
            """, unsafe_allow_html=True)
            
            uploaded_file = st.file_uploader(
                "Choose target fileset",
                type=["txt", "pdf"],
                help="Buffered file limits: PDF/TXT up to 10MB"
            )
            
            if uploaded_file is not None:
                st.markdown(f"**Target Node:** {uploaded_file.name} ({uploaded_file.size / 1024:.2f} KB)")
                if st.button("⬆️ Ingest Payload", use_container_width=True, type="primary"):
                    with st.spinner("Streaming..."):
                        try:
                            result = upload_file(st.session_state.project_id, uploaded_file, uploaded_file.name)
                            add_message("system", f"✅ File '{uploaded_file.name}' buffered securely into project target area!")
                            st.balloons()
                            st.rerun()
                        except Exception as e:
                            st.error(f"Ingestion failed: {str(e)}")
            
            st.markdown("---")
            st.markdown("""
            <div style='background: #11141a; padding: 10px; border-radius: 8px; margin-bottom: 10px; border-left: 3px solid #2e7d32;'>
                <p style='color: #ffffff; margin: 0; font-weight: 600; font-size: 0.85rem;'>⚙️ Regex Segmentation Layer</p>
            </div>
            """, unsafe_allow_html=True)
            
            chunk_size = st.number_input("Token Block Size", min_value=100, value=1000, step=100)
            overlap_size = st.number_input("Sliding Window Overlap", min_value=0, value=200, step=50)
            
            if st.button("⚙️ Tokenize & Push to Space", use_container_width=True, type="primary"):
                with st.spinner("⏳ Compiling tokens and resolving dimensions..."):
                    try:
                        # Process
                        process_req = ProcessRequest(
                            chunk_size=chunk_size,
                            overlap_size=overlap_size,
                            do_reset=0,
                            file_id=""
                        )
                        result = process_file(st.session_state.project_id, process_req)
                        
                        # Index
                        push_req = PushRequest(do_reset=0)
                        index_result = push_to_index(st.session_state.project_id, push_req)
                        
                        add_message("system", f"✅ Knowledge corpus tokenized and synced with Qdrant vector coordinates successfully!")
                        st.success("✅ Done!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Structural parsing failed: {str(e)}")

def render_chat_interface():
    """Render the main chat interface"""
    
    # Custom CSS for chat interface - matching Lumora green/dark theme
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
        
        /* Input box styling */
        .stTextInput > div > div > input {
            border-radius: 20px;
            border: 2px solid #2e7d32;
            padding: 12px 20px;
            font-size: 1rem;
            background-color: #1a1f2e;
            color: #ffffff;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #4caf50;
            box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
        }
        
        /* Number input styling */
        .stNumberInput > div > div > input {
            background-color: #1a1f2e;
            border: 2px solid #2e7d32;
            color: #ffffff;
            font-weight: 500;
            border-radius: 8px;
        }
        
        /* Slider styling */
        .stSlider > div > div > div {
            background-color: #2e7d32;
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
        
        /* Expander styling */
        .streamlit-expanderHeader {
            background-color: #1a1f2e;
            border-radius: 8px;
            font-weight: 600;
            color: white;
        }
        
        /* Scrollable chat area */
        .chat-container {
            max-height: 500px;
            overflow-y: auto;
            padding: 25px;
            background: #0f1419;
            border-radius: 15px;
            margin: 20px 0;
            box-shadow: 0 4px 12px rgba(0,0,0,0.4);
            border: 2px solid #2e7d32;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Header with Lumora branding
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col1:
        st.markdown("<h2 style='color: #4caf50; margin-top: 15px;'>🌿 LUMORA</h2>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 10px;'>
            <h1 style='color: #ffffff; margin: 0; font-size: 2.2rem; font-weight: 800;'>💬 Lumora Intelligence Node</h1>
            <p style='color: #a5d6a7; font-size: 1rem; margin: 8px 0; font-weight: 500;'>
                Real-Time Contextual Inferences Subsystem
            </p>
            <p style='color: #6c757d; font-size: 0.9rem; margin: 5px 0;'>
                Query operational guides, sensory registers boundaries, and ecosystem parameters datasets
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='text-align: right; padding: 10px;'>
            <p style='color: #6c757d; font-size: 0.85rem; margin: 0;'>
                Aquaponic RAG Core<br>
                Build iteration 3.0
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Check if there's an active chat
    if not st.session_state.current_chat_id:
        st.markdown("""
        <div style='text-align: center; padding: 40px 20px; background: linear-gradient(135deg, #11141a 0%, #1a1f2e 100%);
                    border-radius: 12px; border: 2px solid #2e7d32; margin: 20px 0;'>
            <h2 style='color: #ffffff; margin: 0;'>👋 Gateway Active</h2>
            <p style='color: #a5d6a7; font-size: 1.1rem; margin: 15px 0;'>
                Click <strong>'➕ New Ingestion Run'</strong> inside the cluster control panel to initiate query pipelines
            </p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Chat messages container
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    
    if not st.session_state.current_messages:
        st.markdown("""
        <div style='text-align: center; padding: 40px 20px; background: linear-gradient(135deg, #11141a 0%, #1a1f2e 100%);
                    border-radius: 10px; border: 2px dashed #2e7d32;'>
            <h3 style='color: #ffffff; margin: 0;'>💭 Awaiting Operator Inputs</h3>
            <p style='color: #a5d6a7; font-size: 1rem; margin: 10px 0;'>
                Input telemetry or diagnostic queries to extract synchronized insights from vector memory blocks
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Display all messages
        for message in st.session_state.current_messages:
            render_chat_message(message)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Chat input at the bottom
    st.markdown("---")
    
    col1, col2 = st.columns([6, 1])
    
    with col1:
        user_input = st.text_input(
            "Message",
            placeholder="Query water calibrations, modbus mappings, biological thresholds...",
            label_visibility="collapsed",
            key="user_input"
        )
    
    with col2:
        send_button = st.button("📤 Query", use_container_width=True, type="primary")
    
    # Handle message sending
    if send_button and user_input:
        # Add user message
        add_message("user", user_input)
        
        # Get AI response
        with st.spinner("🤔 Scanning Qdrant clusters & formulating response..."):
            try:
                search_req = SearchRequest(
                    text=user_input,
                    limit=st.session_state.context_limit
                )
                result = ask_question(st.session_state.project_id, search_req)
                
                if "answer" in result:
                    answer = result["answer"]
                    add_message("assistant", answer, {'full_result': result})
                else:
                    add_message("assistant", "❌ Failed to generate inference payload. Verify Qdrant index bounds.")
            except Exception as e:
                add_message("assistant", f"❌ Execution error: {str(e)}")
        
        st.rerun()
    
    # Quick actions
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔍 Search Memory Blocks", use_container_width=True):
            st.session_state.show_search = True
    
    with col2:
        if st.button("📊 Space Density Metrics", use_container_width=True):
            try:
                info = get_index_info(st.session_state.project_id)
                add_message("system", f"📊 Qdrant Space Metadata Info:\n```json\n{json.dumps(info, indent=2)}\n```")
                st.rerun()
            except Exception as e:
                st.error(f"Failed to query index stats: {str(e)}")
    
    with col3:
        if st.button("🗑️ Purge Live Run Cache", use_container_width=True):
            st.session_state.current_messages = []
            save_current_chat()
            st.rerun()

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    # Page configuration
    st.set_page_config(
        page_title="Lumora RAG Core Client",
        page_icon="💬",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    init_session_state()
    
    # Render sidebar
    render_sidebar()
    
    # Render main chat interface
    render_chat_interface()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(90deg, #11141a 0%, #2e7d32 100%); 
                border-radius: 10px; margin-top: 30px; box-shadow: 0 4px 12px rgba(0,0,0,0.3); border: 1px solid #4caf50;'>
        <p style='color: white; font-size: 1rem; margin: 5px 0; font-weight: 600;'>
            🚀 Local Knowledge Augmentation Stack | **Lumora Core Systems**
        </p>
        <p style='color: #a5d6a7; font-size: 0.85rem; margin: 5px 0;'>
            Advanced Intelligent Inferences Engine • Qdrant Vectors Routing • Local Confined Privacy Architecture
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == "__main__":
    main()
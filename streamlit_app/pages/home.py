"""
Home Page
Welcome page with system overview and quick stats for Lumora
"""

import streamlit as st
from config import app_config
from utils import api_client, ui_components


def render():
    """Render the home page"""
    
    # Welcome section
    st.markdown(f"""
    <div style='text-align: center; padding: 2rem 0;'>
        <h1 style='color: {app_config.PRIMARY_COLOR}; font-size: 3rem; font-weight: 800;'>
            Welcome to Lumora Intelligence
        </h1>
        <p style='font-size: 1.2rem; color: #a5d6a7; margin-top: 1rem; font-weight: 500;'>
            Next-Gen RAG Knowledge Base for Smart Aquaponic & Sustainable Agriculture
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick info cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        ui_components.render_info_card(
            title="📤 Upload Research Logs",
            content="Upload textbooks, sensor specs, and aquaculture manuals to build your expert knowledge base",
            icon="📄"
        )
    
    with col2:
        ui_components.render_info_card(
            title="🔍 Contextual Retrieval",
            content="Search through ecosystem data, wiring diagrams, and agricultural papers using vector embeddings",
            icon="🎯"
        )
    
    with col3:
        ui_components.render_info_card(
            title="💬 Automated AI Insights",
            content="Get instant, expert diagnostics for water pH, nitrogen cycles, and automation adjustments",
            icon="🤖"
        )
    
    st.markdown("---")
    
    # Current project stats
    st.markdown("## 📊 Active Cycle / Project Overview")
    
    project_id = st.session_state.project_id
    
    # Fetch index info
    with ui_components.show_loading("Fetching project knowledge status..."):
        result = api_client.get_index_info(project_id)
    
    # 🟢 [تصحيح الأمان]: التأكد من نجاح الريكويست وأن الاستجابة عبارة عن قاموس صالح
    if isinstance(result, dict) and "error" not in result and "collection_info" in result:
        collection_info = result.get("collection_info", {})
        
        # 🟢 [تأمين مضاعف]: لو الـ collection_info مبعوتة من الباك إيند بـ None، اِجبرها تبقى قاموس فاضي منعاً للانهيار
        if collection_info is None:
            collection_info = {}
            
        # Display metrics بأمان كامل مع وضع قيم افتراضية
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            ui_components.render_metric_card(
                title="Project ID",
                value=str(project_id),
                icon="🗂️"
            )
        
        with col2:
            points_count = collection_info.get("points_count", 0) if isinstance(collection_info, dict) else 0
            ui_components.render_metric_card(
                title="Indexed Chunks",
                value=str(points_count),
                icon="📚"
            )
        
        with col3:
            vectors_count = collection_info.get("vectors_count", 0) if isinstance(collection_info, dict) else 0
            ui_components.render_metric_card(
                title="Vectors Generated",
                value=str(vectors_count),
                icon="🔢"
            )
        
        with col4:
            status = collection_info.get("status", "red") if isinstance(collection_info, dict) else "red"
            ui_components.render_metric_card(
                title="System Status",
                value=str(status),
                icon="✅"
            )
        
        # Detailed info
        with st.expander("📋 View Detailed Collection Mapping"):
            st.json(collection_info)
    
    else:
        # 🟢 لو الباك إيند مرجعش حاجة خالص، اعرض رسالة التنبيه الاحترافية بشكل مستقر
        ui_components.show_warning(
            "No active vector database index found for this cycle. Please navigate to Upload & Process to inject knowledge base."
        )
    
    st.markdown("---")
    
    # Getting started guide
    st.markdown("## 🚀 Quick Deployment Guide")
    
    with st.expander("📖 System Operations Blueprint", expanded=False):
        st.markdown("""
        ### Steps to configure your Lumora RAG Assistant:
        
        1. **Select Active Project Cycle** - Set your Project ID via the sidebar to isolate documentation (e.g., #1 for Hydroponics, #2 for Automation).
        
        2. **Inject Agricultural Data** 📤
           - Navigate to the **Upload & Process** screen.
           - Upload research materials or hardware troubleshooting steps (PDF/TXT).
           - Set token segmentation settings and initiate vector ingestion.
        
        3. **Neural Search Embedding** 🔄
           - The uploaded corpus will automatically chunk and resolve into vector coordinates inside Qdrant DB.
        
        4. **Initiate Query Protocol** 💬
           - Navigate to **Query Interface** to start chatting with the automated agricultural expert.
        
        ### Best Engineering Practices:
        - Input precise queries regarding aquaculture calibrations.
        - Maintain chunk ranges near 1000 characters for optimal contextual precision during LLM retrieval.
        - Ensure correct metadata structure when compiling manual folders.
        """)
    
    # System information
    st.markdown("---")
    st.markdown("## ⚙️ Ingestion & Inferences Parameters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Ingestion Formats Supported:**
        - 📄 PDF Manuals & Datasheets
        - 📝 Text Data Streams (.txt)
        
        **Payload Constraints:**
        - Up to 10 MB per individual fileset
        """)
    
    with col2:
        st.markdown("""
        **Core Computational Architecture:**
        - Local Asynchronous Document Parsing
        - High-density Vector Embedding Extraction
        - Real-time Qdrant Multi-tenant Vector Subsystem
        - Dynamic Augmentation Context Injections
        """)
    
    # Recent activity (if available)
    if st.session_state.get('chat_history'):
        st.markdown("---")
        st.markdown("## 💬 Recent Expert Queries")
        
        recent_questions = st.session_state.chat_history[-5:]  # Last 5 questions
        for i, qa in enumerate(reversed(recent_questions), 1):
            with st.expander(f"Protocol Q{i}: {qa.get('question', '')[:100]}..."):
                st.markdown(f"**Query:** {qa.get('question', '')}")
                st.markdown(f"**Generated Insights:** {qa.get('answer', '')}")
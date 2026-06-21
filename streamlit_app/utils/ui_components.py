"""
UI Components Module
Reusable UI components for the Streamlit app - Lumora Edition
"""

import streamlit as st
from config import app_config
from typing import Optional, List, Dict, Any
import base64
from pathlib import Path


def apply_custom_css():
    """Apply custom CSS styling to the app oriented for Lumora Agriculture branding"""
    
    css = f"""
    <style>
        /* Main color scheme */
        :root {{
            --primary-color: {app_config.PRIMARY_COLOR};
            --secondary-color: {app_config.SECONDARY_COLOR};
            --accent-color: {app_config.ACCENT_COLOR};
            --background-color: {app_config.BACKGROUND_COLOR};
            --text-color: {app_config.TEXT_COLOR};
        }}
        
        /* Main app container */
        .main {{
            background-color: var(--background-color);
        }}
        
        /* Header styling */
        .app-header {{
            background: linear-gradient(135deg, {app_config.SECONDARY_COLOR} 0%, {app_config.PRIMARY_COLOR} 100%);
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border: 1px solid var(--accent-color);
        }}
        
        .app-header h1 {{
            color: white;
            margin: 0;
            font-size: 2.5rem;
            font-weight: 700;
        }}
        
        .app-header p {{
            color: rgba(255, 255, 255, 0.9);
            margin: 0.5rem 0 0 0;
            font-size: 1.1rem;
        }}
        
        /* Card styling */
        .custom-card {{
            background-color: #1a1f2e;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin-bottom: 1rem;
            border-left: 4px solid var(--primary-color);
        }}
        
        /* Success message */
        .success-message {{
            background-color: rgba(46, 125, 50, 0.2);
            border-left: 4px solid #28a745;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
            color: #fafafa;
        }}
        
        /* Error message */
        .error-message {{
            background-color: rgba(244, 67, 54, 0.2);
            border-left: 4px solid #dc3545;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
            color: #fafafa;
        }}
        
        /* Info message */
        .info-message {{
            background-color: rgba(12, 84, 96, 0.2);
            border-left: 4px solid #00D9C0;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
            color: #fafafa;
        }}
        
        /* Button styling */
        .stButton>button {{
            background: linear-gradient(135deg, {app_config.PRIMARY_COLOR} 0%, #1b5e20 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.5rem 2rem !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(46, 125, 50, 0.3) !important;
        }}
        
        .stButton>button:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4) !important;
        }}
        
        /* File uploader */
        .uploadedFile {{
            border: 2px dashed {app_config.PRIMARY_COLOR} !important;
            border-radius: 10px !important;
            padding: 1rem !important;
        }}
        
        /* Metric styling */
        [data-testid="stMetricValue"] {{
            font-size: 2rem;
            color: {app_config.ACCENT_COLOR};
        }}
        
        /* Sidebar styling */
        section[data-testid="stSidebar"] {{
            background-color: {app_config.SECONDARY_COLOR};
        }}
        
        section[data-testid="stSidebar"] .stMarkdown {{
            color: white;
        }}
        
        /* Footer */
        .app-footer {{
            text-align: center;
            padding: 2rem;
            color: #a5d6a7;
            border-top: 2px solid {app_config.PRIMARY_COLOR};
            margin-top: 3rem;
            background: linear-gradient(180deg, transparent, rgba(46, 125, 50, 0.05));
        }}
        
        /* Progress bar */
        .stProgress > div > div > div > div {{
            background-color: {app_config.PRIMARY_COLOR};
        }}
        
        /* Expander */
        .streamlit-expanderHeader {{
            background-color: #1a1f2e !important;
            border-radius: 5px;
            font-weight: 600;
            color: white !important;
        }}
        
        /* Chat message */
        .chat-message {{
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
            display: flex;
            align-items: flex-start;
        }}
        
        .chat-message.user {{
            background-color: #263238;
            border-left: 4px solid #4caf50;
        }}
        
        .chat-message.assistant {{
            background-color: #1a1f2e;
            border-left: 4px solid {app_config.PRIMARY_COLOR};
        }}
        
        .chat-message .icon {{
            font-size: 1.5rem;
            margin-right: 1rem;
        }}
        
        .chat-message .content {{
            color: #e8eef5;
        }}
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 2rem;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            height: 50px;
            padding: 0 2rem;
            background-color: #1a1f2e;
            border-radius: 10px 10px 0 0;
            font-weight: 600;
            color: #d0d7e0;
        }}
        
        .stTabs [aria-selected="true"] {{
            background-color: {app_config.PRIMARY_COLOR} !important;
            color: white !important;
        }}
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)


def render_header():
    """Render the application header with Lumora identity"""
    header_html = f"""
    <div class="app-header">
        <h1>🌿 {app_config.APP_TITLE}</h1>
        <p>Ecosystem Optimization Node | Secured via local RAG Stack</p>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)


def render_footer():
    """Render the application footer"""
    footer_html = f"""
    <div class="app-footer">
        <p>© 2026 {app_config.COMPANY_NAME} Smart Systems. All rights reserved.</p>
        <p style="font-size: 0.9rem; margin-top: 0.5rem; color: #6c757d;">
            Lumora Intelligent Matrix {app_config.APP_VERSION} | Built for Sustainable Agriculture Optimization
        </p>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)


def render_metric_card(title: str, value: str, icon: str = "📊", delta: Optional[str] = None):
    """Render a metric card synchronized with active system bounds"""
    col1, col2 = st.columns([1, 4])
    with col1:
        st.markdown(f"<div style='font-size: 3rem; text-align: center;'>{icon}</div>", unsafe_allow_html=True)
    with col2:
        st.metric(label=title, value=value, delta=delta)


def render_info_card(title: str, content: str, icon: str = "ℹ️"):
    """Render a styled information card"""
    card_html = f"""
    <div class="custom-card">
        <h3 style="color: white; margin: 0 0 10px 0;">{icon} {title}</h3>
        <p style="color: #d0d7e0; margin: 0;">{content}</p>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)


def render_chat_message(role: str, content: str):
    """Render a chat message in the isolated matrix space"""
    icon = "👤" if role == "user" else "🤖"
    message_class = "user" if role == "user" else "assistant"
    label = "Operator Query" if role == "user" else "Lumora Expert Insight"
    
    message_html = f"""
    <div class="chat-message {message_class}">
        <div class="icon">{icon}</div>
        <div class="content">
            <strong style="color: var(--accent-color);">{label}:</strong>
            <p style="margin: 5px 0 0 0;">{content}</p>
        </div>
    </div>
    """
    st.markdown(message_html, unsafe_allow_html=True)


def render_file_info(filename: str, filesize: float, filetype: str):
    """Render buffered file metrics"""
    info_html = f"""
    <div class="custom-card">
        <h4 style="color: white; margin: 0 0 10px 0;">📄 {filename}</h4>
        <p style="margin: 5px 0; color: #a5d6a7;"><strong>Buffer Size:</strong> {filesize:.2f} KB</p>
        <p style="margin: 5px 0; color: #a5d6a7;"><strong>Data Stream Mime:</strong> {filetype}</p>
    </div>
    """
    st.markdown(info_html, unsafe_allow_html=True)


def render_search_result(result: Dict[str, Any], index: int):
    """Render a vector search hit result"""
    score = result.get('score', 0)
    text = result.get('chunk_text', '')
    metadata = result.get('chunk_metadata', {})
    
    with st.expander(f"📝 Resolved Point {index} - Cosine Similarity Score: {score:.4f}"):
        st.markdown(f"**Segment Text:**")
        st.write(text)
        
        if metadata:
            st.markdown(f"**Payload Metadata:**")
            st.json(metadata)


def show_loading(message: str = "Processing..."):
    """Show loading spinner with message"""
    return st.spinner(message)


def show_success(message: str):
    """Show success message"""
    st.success(f"✅ {message}")


def show_error(message: str):
    """Show error message"""
    st.error(f"❌ {message}")


def show_warning(message: str):
    """Show warning message"""
    st.warning(f"⚠️ {message}")


def show_info(message: str):
    """Show info message"""
    st.info(f"ℹ️ {message}")


def create_download_button(data: str, filename: str, label: str = "Download"):
    """Create a download button"""
    st.download_button(
        label=label,
        data=data,
        file_name=filename,
        mime="text/plain"
    )
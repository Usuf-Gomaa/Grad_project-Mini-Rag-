"""
Lumora Smart Aquaponic System - Intelligent AI Interface
Next-Gen Sustainable Agriculture RAG Assistant
"""

import streamlit as st
from streamlit_option_menu import option_menu
import sys
from pathlib import Path

# Add components to path
sys.path.append(str(Path(__file__).parent))

# Import page modules
from pages import home, upload_process, query_interface, settings_page, about
from utils import api_client, check_api_health, ui_components
from config import app_config

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Lumora | Smart Aquaponic System",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "Lumora - Smart Aquaponic System for Sustainable Agriculture"
    }
)

# ============================================================================
# CUSTOM CSS STYLING - تصميم محسّن مع هوية بصرية قوية
# ============================================================================

custom_css = """
<style>
    /* Main theme colors */
    :root {
        --primary-green: #2e7d32;
        --light-green: #4caf50;
        --dark-green: #1b5e20;
        --accent-white: #f5f7fa;
        --dark-bg: #0f1419;
        --card-bg: #1a1f2e;
    }

    /* Global styling */
    * {
        transition: all 0.3s ease;
    }

    /* Main container */
    .main {
        background: linear-gradient(135deg, #0f1419 0%, #1a1f2e 100%);
        color: #e8eef5;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d0f15 0%, #151b2b 100%);
        border-right: 2px solid #2e7d32;
        box-shadow: 2px 0 15px rgba(46, 125, 50, 0.1);
    }

    /* Sidebar logo container */
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div:first-child {
        animation: slideInDown 0.6s ease-out;
    }

    /* Header animations */
    @keyframes slideInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes glow {
        0%, 100% {
            box-shadow: 0 0 10px rgba(46, 125, 50, 0.3);
        }
        50% {
            box-shadow: 0 0 20px rgba(76, 175, 80, 0.5);
        }
    }

    /* Logo styling */
    .lumora-logo {
        background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 50%, #4caf50 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid #4caf50;
        margin-bottom: 1.5rem;
        text-align: center;
        animation: glow 3s ease-in-out infinite;
        box-shadow: 0 8px 32px rgba(46, 125, 50, 0.2);
    }

    .lumora-logo h1 {
        color: #ffffff;
        font-size: 2.5rem;
        font-weight: 900;
        margin: 0;
        letter-spacing: 3px;
        text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    }

    .lumora-logo p {
        color: #a5d6a7;
        font-size: 0.85rem;
        margin: 8px 0 0 0;
        letter-spacing: 2px;
        font-weight: 600;
    }

    /* Navigation menu styling */
    [role="menuitemradio"] {
        border-radius: 8px;
        margin: 6px 0;
        transition: all 0.3s ease;
    }

    [role="menuitemradio"]:hover {
        background-color: rgba(46, 125, 50, 0.2) !important;
        transform: translateX(5px);
    }

    [aria-selected="true"] {
        background: linear-gradient(90deg, rgba(46, 125, 50, 0.3), rgba(76, 175, 80, 0.2)) !important;
        border-left: 4px solid #4caf50 !important;
        padding-left: 16px !important;
    }

    /* Cards and containers */
    [data-testid="stMetricValue"] {
        color: #4caf50;
        font-weight: bold;
    }

    [data-testid="stMetricLabel"] {
        color: #a5d6a7;
    }

    /* Info/Success/Error boxes */
    .stAlert {
        border-radius: 10px;
        border-left: 4px solid #4caf50;
        animation: fadeInUp 0.5s ease-out;
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #2e7d32 0%, #4caf50 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(46, 125, 50, 0.3);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
        background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 100%);
    }

    /* Input fields */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {
        background-color: #1a1f2e !important;
        border: 2px solid #2e7d32 !important;
        border-radius: 8px !important;
        color: #e8eef5 !important;
        padding: 10px 12px !important;
    }

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #4caf50 !important;
        box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1) !important;
    }

    /* Text styling */
    h1, h2, h3 {
        color: #ffffff;
        font-weight: 700;
    }

    h1 {
        font-size: 2.5rem;
        letter-spacing: 1px;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }

    h2 {
        font-size: 1.8rem;
        border-bottom: 3px solid #2e7d32;
        padding-bottom: 10px;
        display: inline-block;
    }

    p, span {
        color: #d0d7e0;
    }

    /* Divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #2e7d32, transparent);
        margin: 2rem 0;
    }

    /* Markdown links */
    a {
        color: #4caf50 !important;
        text-decoration: none;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    a:hover {
        color: #a5d6a7 !important;
        text-decoration: underline;
    }

    /* Section headers with icon */
    .section-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin: 1.5rem 0 1rem 0;
        padding: 12px 0;
        border-left: 4px solid #4caf50;
        padding-left: 16px;
        animation: slideInDown 0.5s ease-out;
    }

    .section-header h3 {
        margin: 0;
        font-size: 1.3rem;
    }

    /* Status indicator */
    .status-indicator {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
    }

    .status-connected {
        background-color: rgba(76, 175, 80, 0.2);
        color: #a5d6a7;
        border: 1px solid #4caf50;
    }

    .status-disconnected {
        background-color: rgba(244, 67, 54, 0.2);
        color: #ef9a9a;
        border: 1px solid #f44336;
    }

    /* Animation for status pulse */
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.6;
        }
    }

    .status-connected::before {
        content: '';
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #4caf50;
        animation: pulse 2s infinite;
    }

    /* Footer styling */
    .footer-content {
        text-align: center;
        padding: 2rem 1rem;
        border-top: 2px solid #2e7d32;
        margin-top: 3rem;
        background: linear-gradient(180deg, transparent, rgba(46, 125, 50, 0.05));
        color: #a5d6a7;
        font-size: 0.9rem;
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .lumora-logo h1 {
            font-size: 2rem;
        }

        h1 {
            font-size: 2rem;
        }

        h2 {
            font-size: 1.5rem;
        }
    }

    /* Smooth transitions */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(46, 125, 50, 0.1), rgba(76, 175, 80, 0.05)) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(76, 175, 80, 0.2) !important;
        padding: 1.5rem !important;
        animation: fadeInUp 0.6s ease-out;
    }

    /* Expander styling */
    [data-testid="stExpander"] {
        border: 1px solid #2e7d32 !important;
        border-radius: 8px !important;
        background: linear-gradient(135deg, rgba(46, 125, 50, 0.05), transparent) !important;
    }

    [data-testid="stExpander"] button {
        color: #4caf50 !important;
    }

    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #1a1f2e;
    }

    ::-webkit-scrollbar-thumb {
        background: #2e7d32;
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #4caf50;
    }
</style>
"""

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

def initialize_session_state():
    """Initialize session state variables"""
    if 'project_id' not in st.session_state:
        st.session_state.project_id = 1
    
    if 'api_base_url' not in st.session_state:
        st.session_state.api_base_url = app_config.API_BASE_URL
    
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = []
    
    if 'processing_status' not in st.session_state:
        st.session_state.processing_status = None
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'index_info' not in st.session_state:
        st.session_state.index_info = None

initialize_session_state()

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application entry point"""
    
    # 🟢 حقن الـ CSS أول شيء لضمان تحميل الستايل قبل العناصر
    st.markdown(custom_css, unsafe_allow_html=True)
    
    # Header with logo and title
    ui_components.render_header()
    
    # Sidebar navigation
    with st.sidebar:
        try:
            st.image("assets/lumora_logo.png", width=200)
        except:
            # Logo محسن مع هوية بصرية ديناميكية
            st.markdown(f"""
            <div class="lumora-logo">
                <h1>LUMORA</h1>
                <p>🌿 AQUAPONIC INTELLIGENCE</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        selected_page = option_menu(
            menu_title="📱 NAVIGATION",
            options=["Home", "Upload & Process", "Query Interface", "Settings", "About"],
            icons=["🏠", "☁️", "🔍", "⚙️", "ℹ️"],
            menu_icon="🌱",
            default_index=0,
            styles={
                "container": {
                    "padding": "10px 0",
                    "background-color": "transparent"
                },
                "icon": {
                    "color": "#4caf50",
                    "font-size": "18px"
                },
                "nav-link": {
                    "font-size": "15px",
                    "text-align": "left",
                    "margin": "8px 0",
                    "border-radius": "8px",
                    "padding": "10px 16px",
                    "color": "#d0d7e0",
                    "--hover-color": "rgba(46, 125, 50, 0.2)",
                },
                "nav-link-selected": {
                    "background-color": "rgba(46, 125, 50, 0.3)",
                    "color": "#4caf50",
                    "border-left": "4px solid #4caf50",
                    "font-weight": "700"
                },
            }
        )
        
        st.markdown("---")
        
        # Project selector in sidebar
        st.markdown('<div class="section-header"><h3>🗂️ Project</h3></div>', unsafe_allow_html=True)
       # 🟢 [تأمين الكلبشة]: ربط الـ Widget بـ Key ثابت في الـ Session State منعاً لأي تغيير صامت
        project_id = st.number_input(
            "Project ID",
            min_value=1,
            value=st.session_state.project_id,
            step=1,
            key="global_project_id", # 👈 زود السطر ده هنا بالملي
            help="Select or create a project by entering its ID"
        )
        
        if project_id != st.session_state.project_id:
            st.session_state.project_id = project_id
            st.rerun()
        
        # Display current project info
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, rgba(46, 125, 50, 0.2), rgba(76, 175, 80, 0.1)); 
                    border: 2px solid #2e7d32; border-radius: 10px; padding: 12px 16px; 
                    text-align: center; margin: 1rem 0;'>
            <p style='margin: 0; color: #a5d6a7; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px;'>Active Project</p>
            <h2 style='margin: 8px 0 0 0; color: #4caf50; font-size: 1.8rem; border: none; padding: 0;'>#{st.session_state.project_id}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # System status indicator
        st.markdown("---")
        st.markdown('<div class="section-header"><h3>🔌 System Status</h3></div>', unsafe_allow_html=True)
        
        api_status = check_api_health()
        status_class = "status-connected" if api_status else "status-disconnected"
        status_text = "API Connected" if api_status else "API Disconnected"
        
        st.markdown(f"""
        <div style='text-align: center; padding: 12px;'>
            <div class="status-indicator {status_class}">
                {status_text}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Route to selected page
    if selected_page == "Home":
        home.render()
    elif selected_page == "Upload & Process":
        upload_process.render()
    elif selected_page == "Query Interface":
        query_interface.render()
    elif selected_page == "Settings":
        settings_page.render()  # 🟢 تم التصحيح هنا: استدعاء ملف settings_page بالملي لمنع شاشة البياض
    elif selected_page == "About":
        about.render()
    
    # Footer
    st.markdown("""
    <div class="footer-content">
        <p>🌿 <strong>Lumora Smart Aquaponic System</strong> | Sustainable Agriculture Intelligence</p>
        <p style='font-size: 0.8rem; color: #2e7d32; margin-top: 8px;'>
            Powered by Advanced AI & IoT Integration
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == "__main__":
    main()
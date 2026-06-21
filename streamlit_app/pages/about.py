"""
About Page
Information about the application and project - Lumora
"""

import streamlit as st
from config import app_config
from utils import ui_components


def render():
    """Render the about page"""
    
    st.markdown(f"""
    <h1 style='color: {app_config.PRIMARY_COLOR};'>ℹ️ About Lumora System</h1>
    <p style='font-size: 1.1rem; color: #a5d6a7;'>
        Learn more about our Intelligent Aquaponic RAG Assistant
    </p>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Project branding block
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div style='text-align: center; padding: 2.5rem; background: linear-gradient(135deg, 
                    {app_config.SECONDARY_COLOR} 0%, {app_config.PRIMARY_COLOR} 100%); 
                    border-radius: 15px; border: 2px solid {app_config.ACCENT_COLOR};
                    box-shadow: 0 8px 32px rgba(46, 125, 50, 0.2);'>
            <h1 style='color: white; font-size: 4.5rem; font-weight: 900; margin: 0; letter-spacing: 4px;'>LUMORA</h1>
            <p style='color: #a5d6a7; font-size: 1.3rem; margin: 0.5rem 0 0 0; font-weight: 600; letter-spacing: 2px;'>Smart Aquaponic Intelligence</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Main content
    st.markdown(app_config.ABOUT_MESSAGE)
    
    st.markdown("---")
    
    # Features showcase
    st.markdown("## 🌟 Key Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        features_1 = [
            ("📤", "Agricultural Research Upload", "Upload PDF, textbooks, and system manuals seamlessly"),
            ("🔄", "Intelligent Chunking", "Automatic text extraction for complex scientific datasheets"),
            ("🎯", "Semantic Retrieval", "Find aquaponic answers based on contextual agricultural meaning"),
            ("💬", "Expert AI Q&A", "Get precise instructions for water chemistry, feeding, and pH balance")
        ]
        
        for icon, title, description in features_1:
            st.markdown(f"""
            <div class="custom-card" style='background-color: #1a1f2e; padding: 1.2rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid {app_config.ACCENT_COLOR};'>
                <h4 style='margin:0; color: white;'>{icon} {title}</h4>
                <p style='margin: 5px 0 0 0; color: #d0d7e0; font-size: 0.9rem;'>{description}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        features_2 = [
            ("🗂️", "Multi-Cycle Support", "Manage different farming cycles and documentation groups"),
            ("⚡", "Instant Sub-2s Response", "Get real-time troubleshooting answers for automation errors"),
            ("📊", "System Health Monitoring", "Track API connectivity and database status in real-time"),
            ("🔒", "Robust & Offline Ready", "Localized data architecture ensuring project confidentiality")
        ]
        
        for icon, title, description in features_2:
            st.markdown(f"""
            <div class="custom-card" style='background-color: #1a1f2e; padding: 1.2rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid {app_config.ACCENT_COLOR};'>
                <h4 style='margin:0; color: white;'>{icon} {title}</h4>
                <p style='margin: 5px 0 0 0; color: #d0d7e0; font-size: 0.9rem;'>{description}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Technology stack
    st.markdown("## 🛠️ Technology Stack")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### Backend Core
        - **FastAPI** - Modern async API framework
        - **PostgreSQL** - Relational metadata database
        - **Qdrant DB** - Advanced Vector Database
        - **SQLAlchemy** - ORM Layer
        """)
    
    with col2:
        st.markdown("""
        ### AI & RAG Engine
        - **OpenAI GPT Engine** - Generation client
        - **Cohere Multilingual** - Semantic Embeddings
        - **Custom RAG Pipelines** - Context-aware injection
        - **Vector Search** - Metric distance matching
        """)
    
    with col3:
        st.markdown("""
        ### Frontend & Control
        - **Streamlit** - Interactive UI dashboard
        - **Python 3.8+** - Core language
        - **Custom CSS** - Agriculture themed elements
        - **Automation Synced** - Ready for IoT insights
        """)
    
    st.markdown("---")
    
    # Use cases
    st.markdown("## 📚 Core System Use Cases")
    
    use_cases = [
        {
            "title": "🌿 Hydroponic & Aquaculture Troubleshooting",
            "description": "Instantly query manuals to manage water parameters, nitrogen cycles, and bio-filter tuning.",
            "benefits": ["Immediate diagnostic lookups", "Optimized feeding ratio calculation", "Algae control guides"]
        },
        {
            "title": "⚙️ Hardware & PLC Automation Manuals",
            "description": "Index technical sheets for microcontrollers, sensors (pH, EC, Temp), and PLC registers.",
            "benefits": ["Pinout and wiring reference lookup", "MQTT/Modbus protocol explanations", "Calibration steps retrieval"]
        },
        {
            "title": "📈 Crop Yield & Sustainable Research",
            "description": "Query localized academic papers to enhance plant growth and nutrient solutions.",
            "benefits": ["Dynamic deficiency analysis", "Optimal light cycle insights", "Water-saving configurations"]
        },
        {
            "title": "📊 Historical Operations Data",
            "description": "Query internal project logs to compare current cycle trends with older ones.",
            "benefits": ["Cycle performance review", "Anomalies cross-referencing", "Maintenance logs finder"]
        }
    ]
    
    for use_case in use_cases:
        with st.expander(use_case["title"]):
            st.markdown(f"**{use_case['description']}**")
            st.markdown("**Benefits:**")
            for benefit in use_case["benefits"]:
                st.markdown(f"- {benefit}")
    
    st.markdown("---")
    
    # Architecture diagram
    st.markdown("## 🏗️ System Architecture")
    
    architecture_diagram = """
┌─────────────────────────────────────────────────────────────┐
│                 Lumora Interface Dashboard (Streamlit)      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │  Upload  │  │ Process  │  │  Search  │  │   Q&A    │     │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘     │
└────────────────────────────┬────────────────────────────────┘
                             │ REST API
┌────────────────────────────┴────────────────────────────────┐
│                        FastAPI Backend                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │    Routes    │  │ Controllers  │  │    Models    │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└───┬────────────┬────────────┬────────────┬──────────────────┘
    │            │            │            │
┌───┴───┐    ┌───┴───┐    ┌───┴────┐   ┌───┴───────┐
│ Files │    │  LLM  │    │ Vector │   │ PostgreSQL│
│Storage│    │ APIs  │    │   DB   │   │ Database  │
└───────┘    └───────┘    └────────┘   └───────────┘
              (OpenAI,     (Qdrant)    (Project Logs)
               Cohere)
"""

    st.code(architecture_diagram, language=None)

    st.markdown("---")

    # Metrics and stats
    st.markdown("## 📊 System Capabilities")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        ui_components.render_metric_card(
            title="Supported Formats",
            value="PDF, TXT",
            icon="📄"
        )

    with col2:
        ui_components.render_metric_card(
            title="Max Document Size",
            value=f"{app_config.MAX_FILE_SIZE_MB} MB",
            icon="💾"
        )

    with col3:
        ui_components.render_metric_card(
            title="Language Support",
            value="Multilingual",
            icon="🌍"
        )

    with col4:
        ui_components.render_metric_card(
            title="Retrieval Speed",
            value="< 2s",
            icon="⚡"
        )

    st.markdown("---")

    # Contact and support
    st.markdown("## 📞 System Support & Context")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        ### 🏢 Project Vision
        **{app_config.COMPANY_NAME} Smart Systems**  
        Next-Gen Sustainable Automation  
        
        Empowering eco-friendly agricultural transformation through AI-driven expert insight systems.
        """)

    with col2:
        st.markdown("""
        ### 📧 Engineering Core
        - **System Administration:** Contact the Lumora Project Lead
        - **Documentation:** Built-in RAG Assistant Help Module
        - **Deployment:** Powered by Docker Compose Local Stack
        """)

    st.markdown("---")

    # Version history
    with st.expander("📝 System Iteration History"):
        st.markdown("""
        ### Version 3.0 (Current)
        - Complete UI redesign oriented for Lumora branding
        - Upgraded to modern Pydantic Settings & FastAPI lifespan contexts
        - Advanced settings and vector configuration options
        - Enhanced localized search capabilities for farming data
        
        ### Version 2.0
        - Added multi-project isolation filters
        - Structured chunk parser upgrades
        
        ### Version 1.0
        - Initial RAG baseline architecture
        """)

    st.markdown("---")

    # Footer credits
    st.markdown(f"""
    <div style='text-align: center; padding: 2rem; background-color: {app_config.BACKGROUND_COLOR}; 
                border-radius: 10px; margin-top: 2rem;'>
        <h3 style='color: {app_config.PRIMARY_COLOR};'>Lumora Intelligence System {app_config.APP_VERSION}</h3>
        <p style='color: #a5d6a7; margin-top: 1rem;'>
            Developed with ❤️ for Sustainable Agriculture Optimization
        </p>
        <p style='color: #6c757d; font-size: 0.9rem;'>
            © 2026 All Rights Reserved
        </p>
    </div>
    """, unsafe_allow_html=True)
"""
Settings Page
Configure application settings and preferences for Lumora
"""

import streamlit as st
from config import app_config
from utils import ui_components


def render():
    """Render the settings page"""
    
    st.markdown(f"""
    <h1 style='color: {app_config.PRIMARY_COLOR};'>⚙️ Settings</h1>
    <p style='font-size: 1.1rem; color: #a5d6a7;'>
        Configure computational parameters and system pipeline preferences
    </p>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Create tabs for different settings sections
    tab1, tab2, tab3 = st.tabs(["🔌 Core API Nodes", "📊 Vector Segmentation", "🎨 Visualization Identity"])
    
    # ========================================================================
    # TAB 1: API CONFIGURATION
    # ========================================================================
    with tab1:
        st.markdown("### API Gateway Connection Settings")
        
        with st.form("api_settings_form"):
            api_base_url = st.text_input(
                "FastAPI Backend Address",
                value=st.session_state.get('api_base_url', app_config.API_BASE_URL),
                help="Base URL for the FastAPI computational backend serving RAG protocols"
            )
            
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            
            with col1:
                test_connection = st.form_submit_button("🔍 PING Backend Node")
            
            with col2:
                save_settings = st.form_submit_button("💾 Save Network Cluster")
            
            if test_connection:
                with ui_components.show_loading("Testing pipeline latency..."):
                    import requests
                    try:
                        response = requests.get(f"{api_base_url}/api/v1/", timeout=5)
                        if response.status_code == 200:
                            ui_components.show_success("✅ Gateway handshake successful! Cluster is online.")
                        else:
                            ui_components.show_error(f"❌ Handshake failed. HTTP Status: {response.status_code}")
                    except Exception as e:
                        ui_components.show_error(f"❌ Connection timeout: {str(e)}")
            
            if save_settings:
                st.session_state.api_base_url = api_base_url
                ui_components.show_success("Cluster nodes saved successfully!")
                st.rerun()
        
        st.markdown("---")
        st.markdown("### Active Cluster Registry")
        
        config_info = {
            "Resolved API Route": st.session_state.get('api_base_url', app_config.API_BASE_URL),
            "Tenant Project Cycle": st.session_state.get('project_id', 1),
        }
        
        for key, value in config_info.items():
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown(f"**{key}:**")
            with col2:
                st.code(value, language=None)
    
    # ========================================================================
    # TAB 2: PROCESSING DEFAULTS
    # ========================================================================
    with tab2:
        st.markdown("### Neural Text Segmentation Options")
        
        ui_components.show_info(
            "Set optimal default boundaries for textual data chunking. "
            "These hyper-parameters dictate the density of information injected into the LLM context window."
        )
        
        with st.form("processing_defaults_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                default_chunk_size = st.number_input(
                    "Token/Character Chunk Size",
                    min_value=app_config.CHUNK_SIZE_MIN,
                    max_value=app_config.CHUNK_SIZE_MAX,
                    value=st.session_state.get('default_chunk_size', app_config.CHUNK_SIZE_DEFAULT),
                    step=100,
                    help="Character limit per individual embedding node inside Qdrant"
                )
            
            with col2:
                default_overlap_size = st.number_input(
                    "Sliding Window Overlap Size",
                    min_value=app_config.OVERLAP_SIZE_MIN,
                    max_value=app_config.OVERLAP_SIZE_MAX,
                    value=st.session_state.get('default_overlap_size', app_config.OVERLAP_SIZE_DEFAULT),
                    step=50,
                    help="Overlapping content to maintain structural semantics between adjacent chunks"
                )
            
            st.markdown("---")
            
            default_search_limit = st.slider(
                "Default Vector Inferences Limit (k)",
                min_value=app_config.SEARCH_LIMIT_MIN,
                max_value=app_config.SEARCH_LIMIT_MAX,
                value=st.session_state.get('default_search_limit', app_config.SEARCH_LIMIT_DEFAULT),
                help="Default number of similarity search matches to pull"
            )
            
            st.markdown("---")
            
            if st.form_submit_button("💾 Freeze Tokenization Parameters", use_container_width=True):
                st.session_state.default_chunk_size = default_chunk_size
                st.session_state.default_overlap_size = default_overlap_size
                st.session_state.default_search_limit = default_search_limit
                ui_components.show_success("Tokenization boundaries updated successfully!")
        
        st.markdown("---")
        st.markdown("### Agricultural Corpus Recommendations")
        
        recommendations = {
            "Ecosystem & Aquaculture Textbooks": {
                "Chunk Size": "1000-1200",
                "Overlap": "200-250",
                "Use Case": "Nitrogen cycle descriptions, biological criteria, filter mechanics"
            },
            "PLC Regs & Sensor Datasheets": {
                "Chunk Size": "1500-2000",
                "Overlap": "300-450",
                "Use Case": "Modbus registers mapping, calibration equations, analog wiring codes"
            },
            "System Historical Run Logs": {
                "Chunk Size": "500-800",
                "Overlap": "100-150",
                "Use Case": "Daily diagnostic entries, automated error codes, telemetry readings"
            },
            "Academic Research Papers": {
                "Chunk Size": "1200-1600",
                "Overlap": "250-350",
                "Use Case": "Nutrient solution formulas, lighting algorithms, crop yield reports"
            }
        }
        
        for doc_type, settings in recommendations.items():
            with st.expander(f"🌿 {doc_type}"):
                for key, value in settings.items():
                    st.markdown(f"**{key}:** {value}")
    
    # ========================================================================
    # TAB 3: DISPLAY SETTINGS
    # ========================================================================
    with tab3:
        st.markdown("### Visual & Dashboard Dashboard Settings")
        
        with st.form("display_settings_form"):
            show_advanced_options = st.checkbox(
                "Expand Engineering Options by Default",
                value=st.session_state.get('show_advanced_options', False),
                help="Keep advanced computational panels visible at boot"
            )
            
            show_timestamps = st.checkbox(
                "Enable Temporal Ingestion Timestamps",
                value=st.session_state.get('show_timestamps', True),
                help="Show exact execution times in system history expanders"
            )
            
            auto_expand_results = st.checkbox(
                "Auto-expand Primary Vector Hit",
                value=st.session_state.get('auto_expand_results', True),
                help="Instantly expand the most relevant chunk in semantic tabs"
            )
            
            enable_animations = st.checkbox(
                "Enable Ingestion Success Effects",
                value=st.session_state.get('enable_animations', True),
                help="Trigger interface transitions when file parsing concludes"
            )
            
            st.markdown("---")
            
            if st.form_submit_button("💾 Save Dashboard Configurations", use_container_width=True):
                st.session_state.show_advanced_options = show_advanced_options
                st.session_state.show_timestamps = show_timestamps
                st.session_state.auto_expand_results = auto_expand_results
                st.session_state.enable_animations = enable_animations
                ui_components.show_success("Dashboard preferences locked!")
        
        st.markdown("---")
        st.markdown("### Brand Color Space Information")
        
        st.markdown(f"""
        **Active Palette Theme:** {app_config.COMPANY_NAME} Sustainable AI Identity
        
        **Hex Codes Registry:**
        - Primary Node Color: `{app_config.PRIMARY_COLOR}`
        - Background Matrix Color: `{app_config.SECONDARY_COLOR}`
        - Highlight Accent Color: `{app_config.ACCENT_COLOR}`
        """)
        
        # Color preview
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div style='background-color: {app_config.PRIMARY_COLOR}; padding: 2rem; 
                        border-radius: 10px; text-align: center; color: white;'>
                <strong>Primary (Lumora Green)</strong>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style='background-color: {app_config.SECONDARY_COLOR}; padding: 2rem; 
                        border-radius: 10px; text-align: center; color: white;'>
                <strong>Matrix (Dark Slate)</strong>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style='background-color: {app_config.ACCENT_COLOR}; padding: 2rem; 
                        border-radius: 10px; text-align: center; color: white;'>
                <strong>Accent (Bio Leaf)</strong>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # System information
    st.markdown("### 📋 Static Operational Matrix")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        **System Firmware Version:** {app_config.APP_VERSION}  
        **Project Identity:** {app_config.COMPANY_NAME} Systems  
        **Deployment Year:** 2026
        """)
    
    with col2:
        st.markdown(f"""
        **Max Memory Buffer Payload:** {app_config.MAX_FILE_SIZE_MB} MB  
        **Allowed Extractor Ingestions:** {', '.join(app_config.ALLOWED_FILE_TYPES).upper()}  
        **Asynchronous Batch Queue:** {app_config.PROCESSING_BATCH_SIZE} points
        """)
    
    # Reset settings
    st.markdown("---")
    st.markdown("### 🔄 Factory System Reset")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("⚠️ Purge Parameters to Factory State", use_container_width=True):
            # Reset to defaults
            st.session_state.api_base_url = app_config.API_BASE_URL
            st.session_state.default_chunk_size = app_config.CHUNK_SIZE_DEFAULT
            st.session_state.default_overlap_size = app_config.OVERLAP_SIZE_DEFAULT
            st.session_state.default_search_limit = app_config.SEARCH_LIMIT_DEFAULT
            st.session_state.show_advanced_options = False
            st.session_state.show_timestamps = True
            st.session_state.auto_expand_results = True
            st.session_state.enable_animations = True
            
            ui_components.show_success("Cluster parameters initialized to factory settings!")
            st.rerun()
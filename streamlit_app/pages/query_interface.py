"""
Query Interface Page
Handles document search and Q&A functionality oriented for Lumora
"""

import streamlit as st
from config import app_config
from utils import api_client, ui_components
from datetime import datetime


def render():
    """Render the query interface page"""
    
    st.markdown(f"""
    <h1 style='color: {app_config.PRIMARY_COLOR};'>💬 Query Interface</h1>
    <p style='font-size: 1.1rem; color: #a5d6a7;'>
        Ask questions and search through your agricultural research using AI-powered retrieval
    </p>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    project_id = st.session_state.project_id
    
    # Create tabs for different query modes
    tab1, tab2, tab3 = st.tabs(["🤖 Ask Lumora Expert", "🔍 Semantic Vector Search", "💬 Ingestion History"])
    
    # ========================================================================
    # TAB 1: ASK QUESTIONS (RAG)
    # ========================================================================
    with tab1:
        st.markdown("### Ask Your Technical Questions")
        
        ui_components.show_info(
            "Query your uploaded ecosystem blueprints and datasets. The AI will search through your "
            "localized Qdrant knowledge base and provide precise contextual answers."
        )
        
        # Question input
        question = st.text_area(
            "Your Ecosystem Question",
            height=100,
            placeholder="e.g., What is the optimal pH range for Tilapia and Mint in an aquaponic cycle?",
            help="Type your question here. Be as specific as possible regarding sensors, thresholds, or configurations."
        )
        
        # Advanced options
        with st.expander("⚙️ Advanced Hyperparameters"):
            col1, col2 = st.columns(2)
            
            with col1:
                num_results = st.slider(
                    "Context Window Chunks (k)",
                    min_value=app_config.SEARCH_LIMIT_MIN,
                    max_value=app_config.SEARCH_LIMIT_MAX,
                    value=app_config.SEARCH_LIMIT_DEFAULT,
                    help="Number of relevant document blocks to retrieve and inject into the prompt"
                )
            
            with col2:
                show_context = st.checkbox(
                    "Display Retrieved Vector Context",
                    value=False,
                    help="Display the exact raw text chunks used to generate the answer"
                )
        
        # Ask button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            ask_button = st.button("🚀 Get Answer", use_container_width=True)
        
        if ask_button:
            if not question.strip():
                ui_components.show_warning("Please enter a question!")
            else:
                # Show loading
                with ui_components.show_loading("🤔 Retrieving context & generating answer..."):
                    result = api_client.ask_question(
                        project_id=project_id,
                        question=question,
                        limit=num_results
                    )
                
                if "error" in result:
                    ui_components.show_error(f"Failed to get answer: {result['error']}")
                elif "answer" in result:
                    answer = result.get("answer", "")
                    full_prompt = result.get("full_prompt", "")
                    chat_history = result.get("chat_history", [])
                    
                    # Display answer
                    st.markdown("---")
                    st.markdown("### 🎯 System Insight Response")
                    
                    # Render as chat message
                    ui_components.render_chat_message("user", question)
                    ui_components.render_chat_message("assistant", answer)
                    
                    # Store in chat history
                    if 'chat_history' not in st.session_state:
                        st.session_state.chat_history = []
                    
                    st.session_state.chat_history.append({
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'question': question,
                        'answer': answer,
                        'project_id': project_id,
                        'full_prompt': full_prompt,
                        'chat_history': chat_history
                    })
                    
                    # Show context if requested
                    if show_context:
                        with st.expander("📄 View Full Augmented Prompt Payload"):
                            st.markdown("**Full Injected Prompt:**")
                            st.text_area("Prompt", value=full_prompt, height=200, disabled=True)
                            
                            if chat_history:
                                st.markdown("**Injected Chat History:**")
                                st.json(chat_history)
                    
                    # Download option
                    st.markdown("---")
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        download_text = f"""
Lumora Smart Aquaponic System Log
Question: {question}

Answer: {answer}

Timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Project Cycle ID: {project_id}
                        """
                        st.download_button(
                            label="💾 Download Insight Log",
                            data=download_text,
                            file_name=f"lumora_qa_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                else:
                    ui_components.show_error("No answer received from the API")
    
    # ========================================================================
    # TAB 2: SEARCH DOCUMENTS
    # ========================================================================
    with tab2:
        st.markdown("### Semantic Vector Query")
        
        ui_components.show_info(
            "Query the vector space using embeddings distance. "
            "Retrieves raw textual blocks based on semantic similarity weights."
        )
        
        # Search input
        search_query = st.text_input(
            "Vector Query String",
            placeholder="e.g., Water temperature thresholds for nitrification bacteria",
            help="Enter your operational or research query"
        )
        
        # Search options
        col1, col2 = st.columns(2)
        
        with col1:
            search_limit = st.slider(
                "Hits Limit",
                min_value=app_config.SEARCH_LIMIT_MIN,
                max_value=app_config.SEARCH_LIMIT_MAX,
                value=app_config.SEARCH_LIMIT_DEFAULT,
                help="Maximum number of semantic chunks to display"
            )
        
        with col2:
            show_metadata = st.checkbox(
                "Display Payload Metadata",
                value=True,
                help="Show technical file details, chunk hashes, and indices"
            )
        
        # Search button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            search_button = st.button("🔍 Execute Search", use_container_width=True)
        
        if search_button:
            if not search_query.strip():
                ui_components.show_warning("Please enter a query!")
            else:
                with ui_components.show_loading("Querying Qdrant index..."):
                    result = api_client.search_index(
                        project_id=project_id,
                        query=search_query,
                        limit=search_limit
                    )
                
                if "error" in result:
                    ui_components.show_error(f"Search failed: {result['error']}")
                elif "results" in result:
                    results = result.get("results", [])
                    
                    if not results:
                        ui_components.show_warning("No semantic points matched the query.")
                    else:
                        st.markdown("---")
                        st.markdown(f"### 📊 Vector Matches ({len(results)} points resolved)")
                        
                        # Display results
                        for i, res in enumerate(results, 1):
                            score = res.get('score', 0)
                            text = res.get('chunk_text', '')
                            metadata = res.get('chunk_metadata', {})
                            
                            with st.expander(f"📝 Block {i} - Cosine Similarity Score: {score:.4f}", expanded=(i==1)):
                                st.markdown("**Retrieved Segment:**")
                                st.write(text)
                                
                                if show_metadata and metadata:
                                    st.markdown("---")
                                    st.markdown("**Node Metadata Payload:**")
                                    st.json(metadata)
                        
                        # Export results option
                        st.markdown("---")
                        col1, col2, col3 = st.columns([1, 2, 1])
                        with col2:
                            export_text = f"Lumora Semantic Search Query: {search_query}\n\n"
                            export_text += f"Resolved Points: {len(results)}\n\n"
                            export_text += "="*50 + "\n\n"
                            
                            for i, res in enumerate(results, 1):
                                export_text += f"Point Vector {i}:\n"
                                export_text += f"Distance Score: {res.get('score', 0):.4f}\n"
                                export_text += f"Segment Text: {res.get('chunk_text', '')}\n"
                                export_text += "\n" + "="*50 + "\n\n"
                            
                            st.download_button(
                                label="💾 Export Vector Hits",
                                data=export_text,
                                file_name=f"vector_hits_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                                mime="text/plain",
                                use_container_width=True
                            )
                else:
                    ui_components.show_error("No results received from the API")
    
    # ========================================================================
    # TAB 3: CHAT HISTORY
    # ========================================================================
    with tab3:
        st.markdown("### 💬 System Conversation Logs")
        
        if not st.session_state.get('chat_history'):
            ui_components.show_info(
                "No previous local logs recorded for this instance. Query the expert to log data."
            )
        else:
            # Filter options
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                filter_project = st.checkbox(
                    "Isolate current Cycle/Project only",
                    value=True,
                    help="Filter history for active project only"
                )
            
            with col2:
                sort_order = st.selectbox(
                    "Sequence",
                    options=["Newest first", "Oldest first"]
                )
            
            with col3:
                if st.button("🗑️ Purge Local Logs"):
                    st.session_state.chat_history = []
                    st.rerun()
            
            st.markdown("---")
            
            # Filter and sort history
            history = st.session_state.chat_history
            
            if filter_project:
                history = [h for h in history if h.get('project_id') == project_id]
            
            if sort_order == "Oldest first":
                history = list(history)
            else:
                history = list(reversed(history))
            
            # Display history
            if not history:
                ui_components.show_info("No conversation logs match the criteria.")
            else:
                st.markdown(f"**Total Historical Runs: {len(history)}**")
                st.markdown("---")
                
                for i, qa in enumerate(history, 1):
                    timestamp = qa.get('timestamp', 'N/A')
                    question = qa.get('question', '')
                    answer = qa.get('answer', '')
                    qa_project_id = qa.get('project_id', 'N/A')
                    
                    with st.expander(f"💬 Protocol {i} - {timestamp} (Cycle: #{qa_project_id})"):
                        ui_components.render_chat_message("user", question)
                        ui_components.render_chat_message("assistant", answer)
                        
                        # Show full details button
                        if st.button(f"View Vector Blueprint", key=f"details_{i}"):
                            st.markdown("---")
                            st.markdown("**Inference Pipeline Graph Details:**")
                            st.json({
                                'timestamp': timestamp,
                                'project_cycle_id': qa_project_id,
                                'full_prompt': qa.get('full_prompt', ''),
                                'chat_history': qa.get('chat_history', [])
                            })
    
    st.markdown("---")
    
    # Help section
    with st.expander("❓ Optimizing Expert Inference Outputs"):
        st.markdown("""
        ### Strategic Knowledge Retrieval Guide
        
        **Specify Hardware/Biological Node Rules:**
        - Mention exact sensor models (e.g., pH, EC analog probes) or plant types when querying calibrations.
        - Avoid generic phrasing to skip prompt pollution.
        
        **Semantic Optimization:**
        - Write descriptive multi-word query sentences instead of isolated keywords to increase Cosine similarity resolution against Qdrant indices.
        
        **Pipeline Adjustments:**
        - Increase context limits when analyzing multi-page sensor tracking datasheets.
        - Check retrieved raw context chunks if you observe hallucination trends in inference outputs.
        """)
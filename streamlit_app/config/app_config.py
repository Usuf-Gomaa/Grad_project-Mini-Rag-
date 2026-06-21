"""
Application Configuration
Centralized configuration for the Lumora Smart Aquaponic System RAG app
"""

import os
from typing import List

# ============================================================================
# API CONFIGURATION
# ============================================================================

# Default to 127.0.0.1 for local development (more reliable than localhost)
# Use "http://fastapi:8000" when running in Docker
# Set API_BASE_URL environment variable to override
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

# Health check endpoint (backend has /api/v1/ not /api/v1/health)
HEALTH_CHECK_ENDPOINT = "/api/v1/"
HEALTH_CHECK_TIMEOUT = 5  # seconds

# ============================================================================
# FILE UPLOAD CONFIGURATION
# ============================================================================

ALLOWED_FILE_TYPES = ["pdf", "txt"]
MAX_FILE_SIZE_MB = 10
CHUNK_SIZE_DEFAULT = 1000
OVERLAP_SIZE_DEFAULT = 200
CHUNK_SIZE_MIN = 100
CHUNK_SIZE_MAX = 5000
OVERLAP_SIZE_MIN = 0
OVERLAP_SIZE_MAX = 500

# ============================================================================
# RAG CONFIGURATION
# ============================================================================

SEARCH_LIMIT_DEFAULT = 5
SEARCH_LIMIT_MIN = 1
SEARCH_LIMIT_MAX = 20

# ============================================================================
# UI CONFIGURATION
# ============================================================================

APP_TITLE = "Lumora | Smart Aquaponic System"
COMPANY_NAME = "Lumora"
APP_VERSION = "v3.0"

# Color scheme - Lumora Smart Aquaponic & Agriculture branding
PRIMARY_COLOR = "#2e7d32"  # 🟢 الأخضر الزراعي الراقي (بدل الماجينتا)
SECONDARY_COLOR = "#0e1117"  # 🟢 خلفية داكنة فخمة للـ Streamlit (بدل الكحلي)
ACCENT_COLOR = "#4caf50"  # 🟢 الأخضر الفاتح الحيوي للـ Highlights
BACKGROUND_COLOR = "#0f1419"
TEXT_COLOR = "#fafafa"

# ============================================================================
# PROCESSING CONFIGURATION
# ============================================================================

PROCESSING_BATCH_SIZE = 10

# ============================================================================
# TEMPLATES & MESSAGES
# ============================================================================

WELCOME_MESSAGE = """
Welcome to the **Lumora Smart Aquaponic System** powered by **Advanced AI & Automation**! 

This intelligent document retrieval and sustainable agriculture question-answering system helps you:
- 📤 Upload and process documents & research (PDF, TXT)
- 🔍 Search through your agricultural knowledge base
- 💬 Get AI-powered expert answers to your farming & system questions
- 📊 Manage multiple system optimization projects efficiently
"""

ABOUT_MESSAGE = """
### About Lumora Smart Aquaponic System

The Lumora RAG (Retrieval-Augmented Generation) System is a cutting-edge solution 
developed for intelligent system management, sustainable agriculture, and smart farming optimization.

#### Key Features:
- **Agricultural Document Processing**: Upload PDFs and text files with automatic chunking
- **Semantic Vector Indexing**: Advanced semantic search using vector embeddings for farm data
- **Expert AI-Powered Q&A**: Get highly accurate answers from your system research and documentation
- **Multi-Project Support**: Manage multiple document collections and farming cycles
- **Real-time Processing**: Fast document processing and instant knowledge retrieval

#### Technology Stack:
- **Backend**: FastAPI with async support
- **Vector Database**: Qdrant for efficient similarity search
- **LLM Integration**: OpenAI GPT & Cohere models
- **Frontend**: Streamlit for interactive UI
- **Automation & IoT**: Advanced monitoring & control logic integration

#### Version: 3.0
#### Project: Lumora Smart Aquaponic System
#### Year: 2026
"""
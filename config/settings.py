import os
from dotenv import load_dotenv

load_dotenv()

SETTINGS = {
    # API Keys
    "PEXELS_API_KEY": os.getenv("PEXELS_API_KEY"),
    "GROQ_API_KEY": os.getenv("GROQ_API_KEY"),
    "GEMINI_API_KEY": os.getenv("GOOGLE_GEMINI_API_KEY"),

    # Database
    "DATABASE_PATH": "data/blog_suite.db",

    # Agent Configuration
    "MAX_CONCURRENT_AGENTS": 10,
    "AGENT_TIMEOUT_SECONDS": 120,
    "DEFAULT_CONTENT_LENGTH": "1500-2000",

    # Blog Defaults
    "DEFAULT_TONE": "professional",
    "DEFAULT_TARGET_AUDIENCE": "general", 
    "AUTO_PUBLISH": False,
    "ENABLE_SEO_OPTIMIZATION": True,
    "ENABLE_IMAGE_GENERATION": True,
    "ENABLE_PLAGIARISM_CHECK": True,

    # Performance Settings
    "CACHE_DURATION": 3600,  # 1 hour
    "MAX_RETRIES": 3,
    "REQUEST_TIMEOUT": 30,

    # Content Quality
    "MIN_READABILITY_SCORE": 70,
    "MIN_SEO_SCORE": 80,
    "MIN_ORIGINALITY_SCORE": 95,

    # File Paths
    "UPLOAD_FOLDER": "data/uploads",
    "OUTPUT_FOLDER": "data/output",
    "LOG_FOLDER": "data/logs",

    # Social Media
    "GENERATE_SOCIAL_POSTS": True,
    "MAX_SOCIAL_POSTS": 5,
    "SOCIAL_PLATFORMS": ["twitter", "linkedin", "facebook"]
}

# Validation rules
VALIDATION_RULES = {
    "title": {
        "min_length": 10,
        "max_length": 60,
        "required_keywords": True
    },
    "meta_description": {
        "min_length": 120,
        "max_length": 160,
        "required_keywords": True
    },
    "content": {
        "min_words": 800,
        "max_words": 5000,
        "required_sections": ["introduction", "main_content", "conclusion"]
    }
}

# Phase Configuration
PHASE_CONFIG = {
    "Core System & Learning": {"priority": 1, "parallel": False},
    "Ideation & Planning": {"priority": 2, "parallel": True},
    "Research & Structuring": {"priority": 3, "parallel": True},
    "SEO & Keyword Preparation": {"priority": 4, "parallel": True},
    "Drafting & Content Generation": {"priority": 5, "parallel": False},
    "Content Enrichment": {"priority": 6, "parallel": True},
    "SEO Optimization & Linking": {"priority": 7, "parallel": True},
    "Editing & Validation": {"priority": 8, "parallel": False},
    "Plagiarism & Originality": {"priority": 9, "parallel": False},
    "Publishing Preparation": {"priority": 10, "parallel": False}
}

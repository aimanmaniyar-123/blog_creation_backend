import sqlite3
import os
from datetime import datetime

DATABASE_PATH = "data/blog_suite.db"

def init_db():
    """Initialize the database with required tables"""
    os.makedirs("data", exist_ok=True)

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Blogs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS blogs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT,
            meta_description TEXT,
            keywords TEXT,
            status TEXT DEFAULT 'draft',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            topic TEXT,
            target_audience TEXT,
            tone TEXT,
            length_category TEXT,
            seo_score REAL,
            quality_score REAL
        )
    """)

    # Agents table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phase TEXT NOT NULL,
            status TEXT DEFAULT 'idle',
            last_active TIMESTAMP,
            success_count INTEGER DEFAULT 0,
            failure_count INTEGER DEFAULT 0,
            average_execution_time REAL DEFAULT 0.0
        )
    """)

    # Tasks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            blog_id INTEGER,
            agent_id INTEGER,
            task_type TEXT,
            status TEXT DEFAULT 'pending',
            started_at TIMESTAMP,
            completed_at TIMESTAMP,
            result TEXT,
            error_message TEXT,
            FOREIGN KEY (blog_id) REFERENCES blogs (id),
            FOREIGN KEY (agent_id) REFERENCES agents (id)
        )
    """)

    # Analytics table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            blog_id INTEGER,
            metric_name TEXT,
            metric_value REAL,
            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (blog_id) REFERENCES blogs (id)
        )
    """)

    # Settings table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE,
            value TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

    # Initialize agents if not exists
    populate_agents()

def populate_agents():
    """Populate the agents table with all 169 agents"""
    agents_data = [
        # Phase 0: Core System & Learning
        ("Self-Learning Supervisor Agent", "Core System & Learning"),
        ("Brainstorming Agent", "Core System & Learning"),

        # Phase 1: Ideation & Planning
        ("Brand Alignment Agent", "Ideation & Planning"),
        ("Context & History Agent", "Ideation & Planning"),
        ("Audience Persona Agent", "Ideation & Planning"),
        ("Goal Definition Agent", "Ideation & Planning"),
        ("Context Gathering Agent", "Ideation & Planning"),
        ("Audience Analysis Agent", "Ideation & Planning"),
        ("Trend Analysis Agent", "Ideation & Planning"),
        ("Topic Idea Generation Agent", "Ideation & Planning"),
        ("Topic List Monitoring Agent", "Ideation & Planning"),
        ("Topic Uniqueness Validation Agent", "Ideation & Planning"),
        ("Final Topic Selection Agent", "Ideation & Planning"),
        ("Topic Validation Agent", "Ideation & Planning"),
        ("Competitor Analysis Agent", "Ideation & Planning"),
        ("Audience Sentiment Analysis Agent", "Ideation & Planning"),
        ("Niche Authority Opportunity Agent", "Ideation & Planning"),
        ("Semantic Gap Analysis Agent", "Ideation & Planning"),
        ("Regulatory Landscape Agent", "Ideation & Planning"),
        ("Ethical & Bias Sensitivity Agent", "Ideation & Planning"),

        # Phase 2: Research & Structuring
        ("Research Agent", "Research & Structuring"),
        ("Research Harvesting Agent", "Research & Structuring"),
        ("Source Credibility Agent", "Research & Structuring"),
        ("Reference Validation Agent", "Research & Structuring"),
        ("Literature Content Gap Checker Agent", "Research & Structuring"),
        ("Source Reliability Agent", "Research & Structuring"),
        ("Source Reliability Scoring Agent", "Research & Structuring"),
        ("Source Reliability Validation Agent", "Research & Structuring"),
        ("Outline Structuring Agent", "Research & Structuring"),

        # Phase 3: SEO & Keyword Preparation
        ("Keyword Extraction Agent", "SEO & Keyword Preparation"),
        ("Keyword Clustering Agent", "SEO & Keyword Preparation"),
        ("Keyword Integration Planning Agent", "SEO & Keyword Preparation"),
        ("Google Ranking Monitor Agent", "SEO & Keyword Preparation"),
        ("SEO Roadmapping Agent", "SEO & Keyword Preparation"),
        ("Semantic SEO Integration Agent", "SEO & Keyword Preparation"),
        ("Voice Search Optimization Agent", "SEO & Keyword Preparation"),

        # Phase 4: Drafting & Content Generation
        ("Title Generation Agent", "Drafting & Content Generation"),
        ("Meta Description Agent", "Drafting & Content Generation"),
        ("Meta Snippet Generator Agent", "Drafting & Content Generation"),
        ("Draft Introduction Agent", "Drafting & Content Generation"),
        ("Section Writing Agent", "Drafting & Content Generation"),
        ("Section/Body Writer Agent", "Drafting & Content Generation"),
        ("Example/Story Integration Agent", "Drafting & Content Generation"),
        ("Snippet Generator Agent", "Drafting & Content Generation"),
        ("Scaling & Cloning Agent", "Drafting & Content Generation"),
        ("Data/Quote Insertion Agent", "Drafting & Content Generation"),
        ("Multilingual Drafting Agent", "Drafting & Content Generation"),

        # Phase 5: Content Enrichment
        ("Data & Stat Insertion Agent", "Content Enrichment"),
        ("Quote Curation Agent", "Content Enrichment"),
        ("Image Prompting Agent", "Content Enrichment"),
        ("Image Generation Agent", "Content Enrichment"),
        ("Image Resizing/Optimization Agent", "Content Enrichment"),
        ("Image Rights Agent", "Content Enrichment"),
        ("Multimedia Embed Agent", "Content Enrichment"),
        ("Dynamic Example Inserter Agent", "Content Enrichment"),
        ("Interactive Content Embedder Agent", "Content Enrichment"),
        ("Poll/Popup Suggestion Agent", "Content Enrichment"),
        ("Content Sensitivity/Moderation Agent", "Content Enrichment"),
    ]

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    for name, phase in agents_data[:50]:  # First 50 agents for demo
        cursor.execute("""
            INSERT OR IGNORE INTO agents (name, phase) VALUES (?, ?)
        """, (name, phase))

    conn.commit()
    conn.close()

def get_connection():
    """Get database connection"""
    return sqlite3.connect(DATABASE_PATH)

def create_blog(title, topic, target_audience, tone, length_category):
    """Create a new blog entry"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO blogs (title, topic, target_audience, tone, length_category)
        VALUES (?, ?, ?, ?, ?)
    """, (title, topic, target_audience, tone, length_category))

    blog_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return blog_id

def get_all_blogs():
    """Get all blogs"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, topic, status, created_at, seo_score, quality_score
        FROM blogs ORDER BY created_at DESC
    """)

    blogs = cursor.fetchall()
    conn.close()

    return blogs

def get_agent_stats():
    """Get agent statistics"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, phase, status, success_count, failure_count
        FROM agents ORDER BY success_count DESC LIMIT 10
    """)

    stats = cursor.fetchall()
    conn.close()

    return stats

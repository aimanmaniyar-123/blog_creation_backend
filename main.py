"""
FastAPI Backend for End-to-End Blog Creation Suite

- Uses GROQ (Llama-3.1) for blog generation
- Uses Gemini 2.5 Flash Image for AI images
- Optional Pexels integration for stock images
- PDF / DOCX / HTML export
- Dashboard / Agent Monitor / Analytics-style endpoints

API keys are loaded ONLY from environment (.env), not from frontend.
"""

import os
import json
import re
import time
import base64
import traceback
import asyncio
from io import BytesIO
from datetime import datetime
from typing import List, Optional, Dict, Any

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, JSONResponse
from pydantic import BaseModel

import requests
from fpdf import FPDF
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from PIL import Image
from groq import Groq
import google.generativeai as genai

# =========================================================
# ENV + APP BOOTSTRAP
# =========================================================

load_dotenv()

ENV_GROQ_API_KEY = os.getenv("GROQ_API_KEY")
ENV_GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ENV_PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

app = FastAPI(
    title="End-to-End Blog Creation API",
    version="1.0.0",
    description="Backend for blog generation, AI images, and export",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL, "http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# Pydantic Models
# =========================================================

class BlogGenerationRequest(BaseModel):
    topic: str
    category: str
    niche: str = ""
    keywords: str = ""
    targetAudience: str
    contentIntent: str
    expertiseLevel: str
    tone: str
    length: str
    writingStyle: str
    additionalContext: str = ""
    useAiImages: bool = True
    numAiImages: int = 3
    usePexels: bool = False
    numPexelsImages: int = 2


class BlogGenerationResponse(BaseModel):
    success: bool
    title: str = ""
    content: str = ""
    wordCount: int = 0
    readingTime: str = ""
    images: List[str] = []
    imageDescriptions: List[str] = []
    seoScore: str = "N/A"
    error: Optional[str] = None


class ExportRequest(BaseModel):
    title: str
    content: str
    format: str  # "pdf", "docx", "html"
    images: List[str] = []
    imageDescriptions: List[str] = []
    metaInfo: Dict[str, Any] = {}


# For dashboard-style endpoints
class DashboardSummary(BaseModel):
    activeAgents: int
    blogsCreated: int
    successRate: float
    avgQualityScore: float


class AgentInfo(BaseModel):
    agent: str
    phase: str
    status: str
    load: int


# =========================================================
# LLM / Image Helpers (Groq + Gemini + Pexels)
# =========================================================

def get_groq_client():
    """
    Return a Groq client using GROQ_API_KEY from environment.
    """
    api_key = ENV_GROQ_API_KEY
    if not api_key:
        return None, "GROQ_API_KEY not set in environment (.env)"
    try:
        client = Groq(api_key=api_key)
        return client, None
    except Exception as e:
        return None, f"Failed to initialize Groq client: {e}"


def generate_blog_with_llm(
    topic: str,
    category: str,
    niche: str,
    keywords: str,
    target_audience: str,
    content_intent: str,
    expertise_level: str,
    tone: str,
    length: str,
    writing_style: str,
    additional_context: str = "",
) -> str:
    """
    Use Groq (Llama-3.1) to generate a full blog in markdown-style text.
    Mirrors your Streamlit app logic.
    """
    client, err = get_groq_client()
    if err:
        raise RuntimeError(err)

    length_hint = {
        "Short (800-1000 words)": "around 800-1000 words",
        "Medium (2000-2500 words)": "around 2000-2500 words",
        "Long (3500-4000 words)": "around 3500-4000 words",
        "Comprehensive (5000-6000 words)": "around 5000-6000 words",
    }.get(length, "around 3000 words")

    prompt = f"""
You are an expert content writer and SEO strategist.

Write a DETAILED, COMPREHENSIVE blog article in well-structured markdown with:

- H1 title
- H2 / H3 headings
- Bullet lists, numbered lists
- No separator lines like "====" or "----" or "___" or "****"

Topic: {topic}
Category: {category}
Niche: {niche or "Not specified"}
Primary Keywords: {keywords or "Not specified"}
Audience: {target_audience}
Intent: {content_intent}
Expertise Level: {expertise_level}
Tone: {tone}
Writing Style: {writing_style}
Target Length: {length_hint}

Additional Context:
{additional_context or "No extra context."}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a world-class blog writer and SEO expert. "
                    "Use clean markdown headings, bold/italic, lists. "
                    "Avoid using separator-only lines like ====, ----, ****, ___."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=8000,
    )

    return response.choices[0].message.content


def get_gemini_model():
    """
    Return a Gemini image model using GEMINI_API_KEY from environment.
    Uses models/gemini-2.5-flash-image like your app2.py.
    """
    api_key = ENV_GEMINI_API_KEY
    if not api_key:
        return None

    try:
        genai.configure(api_key=api_key)
        # Same as your working script: image model
        model = genai.GenerativeModel("models/gemini-2.5-flash-image")
        return model
    except Exception as e:
        print(f"Failed to initialize Gemini model: {e}")
        return None


def extract_gemini_image_bytes(response):
    """
    Extract image bytes from Gemini response (same logic as your working script).
    """
    try:
        if not hasattr(response, "candidates"):
            return None

        for c in response.candidates:
            content = getattr(c, "content", None)
            if not content:
                continue

            parts = getattr(content, "parts", None) or []
            for p in parts:
                # Inline image data (SDK object)
                if hasattr(p, "inline_data") and getattr(p.inline_data, "data", None):
                    return p.inline_data.data

                # Dict-like fallback
                if isinstance(p, dict):
                    if "inline_data" in p and "data" in p["inline_data"]:
                        return p["inline_data"]["data"]

        return None
    except Exception:
        traceback.print_exc()
        return None


def generate_gemini_image(prompt: str) -> Optional[str]:
    """
    Generate an image with Gemini and return a data URL (data:image/png;base64,...)
    """
    model = get_gemini_model()
    if not model:
        return None

    try:
        response = model.generate_content(prompt)
        image_bytes = extract_gemini_image_bytes(response)

        if not image_bytes:
            print("No image data found in Gemini response.")
            return None

        encoded = base64.b64encode(image_bytes).decode("utf-8")
        data_url = f"data:image/png;base64,{encoded}"
        return data_url

    except Exception as e:
        print(f"Gemini Image Error: {e}")
        traceback.print_exc()
        return None


def fetch_pexels_images(query: str, num_images: int = 3) -> List[str]:
    """
    Fetch image URLs from Pexels API based on query.
    Returns a list of image URLs (landscape images).
    """
    api_key = ENV_PEXELS_API_KEY
    if not api_key:
        return []

    try:
        url = "https://api.pexels.com/v1/search"
        headers = {"Authorization": api_key}
        params = {"query": query, "per_page": num_images, "orientation": "landscape"}
        resp = requests.get(url, headers=headers, params=params, timeout=10)

        if resp.status_code != 200:
            return []

        data = resp.json()
        photos = data.get("photos", [])
        image_urls = [p["src"]["large"] for p in photos if "src" in p and "large" in p["src"]]
        return image_urls
    except Exception:
        return []


def generate_image_prompts(topic: str, num_prompts: int = 3) -> List[str]:
    """
    Generate relevant image prompts based on the blog topic using LLM.
    """
    client, err = get_groq_client()
    if err:
        return []

    prompt = f"""
Generate {num_prompts} highly specific and detailed image generation prompts for a blog about "{topic}".

CRITICAL:
- Directly related to {topic}
- 20-30 words each
- Include visual style keywords

Return ONLY a JSON array of {num_prompts} strings.
Example: ["prompt 1", "prompt 2", "prompt 3"]
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are an expert at creating image generation prompts."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.8,
            max_tokens=500,
        )

        content = response.choices[0].message.content.strip()
        prompts = json.loads(content)
        return prompts if isinstance(prompts, list) else []
    except Exception as e:
        print(f"Could not generate image prompts: {e}")
        return []


def generate_image_captions_from_prompts(topic: str, prompts: List[str]) -> List[str]:
    """
    Convert detailed prompts into short figure captions (max 8 words).
    """
    if not prompts:
        return []

    client, err = get_groq_client()
    if err:
        # Fallback: simple shortening
        captions = []
        for p in prompts:
            short = re.sub(r"[^\w\s]", "", p).strip().split()
            captions.append(" ".join(short[:8]))
        return captions

    system_prompt = "You create short, concise figure captions."
    user_prompt = f"""
Generate a caption for each prompt.

Rules for each caption:
- Maximum 8 words
- Human-friendly
- No technical jargon
- No style words (e.g., cinematic, 8k, ultra HD)
- No verbs like 'illustrating', 'showing', 'depicting'
- Should describe the figure in simple terms

Return ONLY a JSON array of captions.

Prompts:
{json.dumps(prompts, indent=2)}
"""

    try:
        resp = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.3,
            max_tokens=300,
        )

        captions = json.loads(resp.choices[0].message.content.strip())
        clean_caps = []
        for c in captions:
            c = re.sub(r"[^\w\s]", "", c).strip()
            clean_caps.append(" ".join(c.split()[:8]))
        return clean_caps

    except Exception:
        fallback = []
        for p in prompts:
            c = re.sub(r"[^\w\s]", "", p).strip().split()
            fallback.append(" ".join(c[:8]))
        return fallback


# =========================================================
# Text Cleaning Helpers
# =========================================================

def clean_text(text: str) -> str:
    """Remove emojis & unsupported chars for PDF safety."""
    return re.sub(r"[^\x00-\x7F]+", " ", text)


def clean_separator_lines(text: str) -> str:
    """Remove separator lines like ====, ----, ___, ****."""
    lines = text.split("\n")
    cleaned = []
    for line in lines:
        stripped = line.strip()
        if stripped and all(c in "=-_*#" for c in stripped):
            continue
        cleaned.append(line)
    return "\n".join(cleaned)


def clean_markdown_formatting(text: str) -> str:
    """
    Remove markdown formatting like **bold**, *italic*, and leading # from headings.
    """
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"(?<!\*)\*(?!\*)([^*]+?)\*(?!\*)", r"\1", text)
    text = re.sub(r"^\s*#{1,6}\s*", "", text)
    return text


def sanitize_caption(caption: str, max_words: int = 8) -> str:
    caption = re.sub(r"[^\w\s]", " ", caption)
    caption = re.sub(r"\s+", " ", caption).strip()

    words = caption.split()
    if not words:
        return "Image"

    words = words[:max_words]
    words = [w[:20] for w in words]
    return " ".join(words)


# =========================================================
# PDF / DOCX / HTML generation (from your app2.py)
# =========================================================

def add_image_to_pdf(pdf: FPDF, img_url_or_path: str, max_width: int = 160, caption: str = "") -> bool:
    try:
        # Load image
        if img_url_or_path.startswith("data:image"):
            header, b64data = img_url_or_path.split(",", 1)
            img = Image.open(BytesIO(base64.b64decode(b64data)))
        elif img_url_or_path.startswith("http"):
            headers = {"User-Agent": "Mozilla/5.0"}
            resp = requests.get(img_url_or_path, timeout=20, stream=True, headers=headers)
            resp.raise_for_status()
            img = Image.open(BytesIO(resp.content))
        else:
            img = Image.open(img_url_or_path)

        if img.mode in ("RGBA", "LA", "P"):
            bg = Image.new("RGB", img.size, (255, 255, 255))
            img = img.convert("RGBA")
            bg.paste(img, mask=img.split()[3])
            img = bg

        w, h = img.size
        aspect = h / w

        usable_width = pdf.w - pdf.l_margin - pdf.r_margin
        new_w = min(max_width, usable_width)
        new_h = new_w * aspect

        # Convert px → mm (approx 3.78 px/mm)
        resized = img.resize((int(new_w * 3.78), int(new_h * 3.78)), Image.Resampling.LANCZOS)

        temp = f"temp_{int(time.time()*1000)}.jpg"
        resized.save(temp, "JPEG", quality=85)

        x = pdf.l_margin + (usable_width - new_w) / 2
        pdf.image(temp, x=x, w=new_w)

        os.remove(temp)

        pdf.ln(4)

        if caption:
            safe_caption = sanitize_caption(caption)
            page_width = pdf.w - pdf.l_margin - pdf.r_margin
            pdf.set_font("helvetica", "I", 9)
            pdf.set_text_color(110, 110, 110)
            pdf.multi_cell(page_width, 5, safe_caption, 0, "C")
            pdf.set_text_color(40, 40, 40)
            pdf.ln(3)

        return True

    except Exception:
        pdf.set_font("helvetica", "I", 9)
        pdf.set_text_color(150, 150, 150)
        pdf.multi_cell(0, 5, "[Image could not be loaded]", 0, "C")
        pdf.set_text_color(40, 40, 40)
        pdf.ln(4)
        return False


def generate_pdf(
    title: str,
    content: str,
    meta_info: Dict[str, Any],
    images: Optional[List[str]] = None,
    image_descriptions: Optional[List[str]] = None,
) -> bytes:
    images = images or []
    image_descriptions = image_descriptions or []

    content = clean_separator_lines(content)
    content = clean_text(content)
    title = title[:150]

    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_left_margin(15)
    pdf.set_right_margin(15)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title
    pdf.set_font("helvetica", "B", 20)
    pdf.multi_cell(0, 10, clean_markdown_formatting(title), 0, "C")
    pdf.ln(4)

    # Divider
    pdf.set_draw_color(52, 152, 219)
    pdf.set_line_width(0.8)
    y = pdf.get_y()
    pdf.line(pdf.l_margin, y, pdf.w - pdf.r_margin, y)
    pdf.ln(8)

    # Meta info
    pdf.set_font("helvetica", "", 10)
    pdf.set_text_color(90, 90, 90)
    pdf.cell(0, 5, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 0, 1)

    # Expecting keys like word_count, reading_time, seo_score
    for key, val in meta_info.items():
        label = key.replace("_", " ").title()
        pdf.cell(0, 5, f"{label}: {val}", 0, 1)

    pdf.set_text_color(40, 40, 40)
    pdf.ln(8)

    # Images section
    if images:
        pdf.set_font("helvetica", "B", 14)
        pdf.cell(0, 8, "Visual Content", 0, 1)
        pdf.ln(2)

        for i, img in enumerate(images):
            desc = image_descriptions[i] if i < len(image_descriptions) else "Image"
            caption = f"Figure {i+1}: {sanitize_caption(desc)}"
            add_image_to_pdf(pdf, img, max_width=170, caption=caption)

        pdf.ln(4)

    heading_pattern = re.compile(r"^\s*(#{1,6})\s*(.*)")
    page_width = pdf.w - pdf.l_margin - pdf.r_margin

    for raw in content.split("\n"):
        line = raw.strip()

        if not line:
            pdf.ln(3)
            continue

        # Headings
        m = heading_pattern.match(line)
        if m:
            level = len(m.group(1))
            heading = clean_markdown_formatting(m.group(2))

            if level == 1:
                pdf.set_font("helvetica", "B", 16)
            elif level == 2:
                pdf.set_font("helvetica", "B", 13)
            else:
                pdf.set_font("helvetica", "B", 12)

            pdf.multi_cell(0, 7, heading, 0, "L")
            pdf.ln(2)
            continue

        # Numbered list
        num = re.match(r"^(\d+)\.\s+(.*)", line)
        if num:
            number = num.group(1)
            text_line = clean_markdown_formatting(num.group(2))

            pdf.set_font("helvetica", "", 11)

            indent = pdf.l_margin + 5
            pdf.set_x(indent)
            pdf.cell(8, 6, f"{number}.", 0, 0)
            pdf.multi_cell(page_width - 13, 6, text_line, 0, "L")
            continue

        # Bullet list
        if line.startswith("- ") or line.startswith("* "):
            pdf.set_font("helvetica", "", 11)
            bullet = clean_markdown_formatting(line[2:])
            pdf.set_x(pdf.l_margin + 5)
            pdf.multi_cell(page_width - 5, 6, f"- {bullet}", 0, "L")
            continue

        # Blockquote
        if line.startswith("> "):
            pdf.set_font("helvetica", "I", 11)
            pdf.set_text_color(120, 120, 120)
            quote = clean_markdown_formatting(line[2:])
            pdf.multi_cell(page_width, 6, quote, 0, "L")
            pdf.set_text_color(40, 40, 40)
            continue

        # Normal text
        pdf.set_font("helvetica", "", 11)
        safe = re.sub(r"[^\x00-\x7F]+", " ", line)
        pdf.multi_cell(page_width, 6, safe, 0, "L")

    return bytes(pdf.output())


def generate_docx(
    title: str,
    content: str,
    meta_info: Dict[str, Any],
    images: Optional[List[str]] = None,
    image_descriptions: Optional[List[str]] = None,
) -> bytes:
    images = images or []
    image_descriptions = image_descriptions or []

    content = clean_separator_lines(content)

    doc = Document()

    # Title
    title_para = doc.add_heading(clean_markdown_formatting(title), 0)
    title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph()

    # Meta info
    meta_para = doc.add_paragraph()
    run = meta_para.add_run(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(100, 100, 100)
    run.italic = True

    wc = meta_info.get("word_count", "N/A")
    rt = meta_info.get("reading_time", "N/A")

    run = meta_para.add_run(f"Word Count: {wc}\n")
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(100, 100, 100)

    run = meta_para.add_run(f"Reading Time: {rt}\n")
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(100, 100, 100)

    doc.add_paragraph()

    # Images
    if images:
        doc.add_heading("Visual Content", level=2)
        doc.add_paragraph()

        for idx, img_url in enumerate(images, 1):
            try:
                if img_url.startswith("data:image"):
                    header, b64data = img_url.split(",", 1)
                    img = Image.open(BytesIO(base64.b64decode(b64data)))

                    tmp_file = f"temp_docx_img_{int(time.time() * 1000)}_{idx}.jpg"
                    img.save(tmp_file, "JPEG", quality=85)

                    doc.add_picture(tmp_file, width=Inches(6))

                    caption_para = doc.add_paragraph()
                    desc = image_descriptions[idx - 1] if idx - 1 < len(image_descriptions) else "Content Image"
                    caption_run = caption_para.add_run(f"Figure {idx}: {desc}")
                    caption_run.font.size = Pt(9)
                    caption_run.italic = True
                    caption_run.font.color.rgb = RGBColor(100, 100, 100)
                    caption_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

                    try:
                        os.remove(tmp_file)
                    except Exception:
                        pass

                elif img_url.startswith("http"):
                    headers = {
                        "User-Agent": "Mozilla/5.0",
                        "Accept": "image/*",
                    }
                    resp = requests.get(img_url, timeout=25, stream=True, headers=headers)
                    resp.raise_for_status()

                    img = Image.open(BytesIO(resp.content))
                    if img.mode in ("RGBA", "LA", "P"):
                        background = Image.new("RGB", img.size, (255, 255, 255))
                        if img.mode == "P":
                            img = img.convert("RGBA")
                        background.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
                        img = background

                    tmp_file = f"temp_docx_img_{int(time.time() * 1000)}_{idx}.jpg"
                    img.save(tmp_file, "JPEG", quality=85)
                    doc.add_picture(tmp_file, width=Inches(6))

                    caption_para = doc.add_paragraph()
                    desc = image_descriptions[idx - 1] if idx - 1 < len(image_descriptions) else "Content Image"
                    caption_run = caption_para.add_run(f"Figure {idx}: {desc}")
                    caption_run.font.size = Pt(9)
                    caption_run.italic = True
                    caption_run.font.color.rgb = RGBColor(100, 100, 100)
                    caption_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

                    try:
                        os.remove(tmp_file)
                    except Exception:
                        pass

                else:
                    # local path
                    doc.add_picture(img_url, width=Inches(6))
                    caption_para = doc.add_paragraph()
                    desc = image_descriptions[idx - 1] if idx - 1 < len(image_descriptions) else "Content Image"
                    caption_run = caption_para.add_run(f"Figure {idx}: {desc}")
                    caption_run.font.size = Pt(9)
                    caption_run.italic = True
                    caption_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

                doc.add_paragraph()
            except Exception:
                p = doc.add_paragraph()
                desc = image_descriptions[idx - 1] if idx - 1 < len(image_descriptions) else "Content Image"
                run_err = p.add_run(f"[Figure {idx}: {desc} could not be loaded]")
                run_err.italic = True
                run_err.font.color.rgb = RGBColor(150, 150, 150)

    heading_pattern = re.compile(r"^\s*(#{1,6})\s*(.*)")

    # Content
    for line in content.split("\n"):
        line_stripped = line.strip()
        if not line_stripped:
            doc.add_paragraph()
            continue

        m = heading_pattern.match(line_stripped)
        if m:
            level = len(m.group(1))
            heading_text = clean_markdown_formatting(line_stripped)
            level_map = {1: 1, 2: 2, 3: 3}
            doc.add_heading(heading_text, level=level_map.get(level, 4))
            continue

        if line_stripped.startswith("- ") or line_stripped.startswith("* "):
            para = doc.add_paragraph(style="List Bullet")
            para.add_run(clean_markdown_formatting(line_stripped[2:]))
            continue

        label, sep, rest = line_stripped.partition(":")
        if sep and len(label.split()) <= 5 and all(w[:1].isupper() for w in label.split() if w):
            para = doc.add_paragraph()
            run_label = para.add_run(clean_markdown_formatting(label) + ":")
            run_label.bold = True
            if rest.strip():
                para.add_run(" " + clean_markdown_formatting(rest.strip()))
        else:
            para = doc.add_paragraph()
            para.add_run(clean_markdown_formatting(line_stripped))

    docx_file = BytesIO()
    doc.save(docx_file)
    docx_file.seek(0)
    return docx_file.getvalue()


def generate_html(
    title: str,
    content: str,
    meta_info: Dict[str, Any],
    images: Optional[List[str]] = None,
    image_descriptions: Optional[List[str]] = None,
) -> bytes:
    """
    Generate styled HTML report, similar to your Streamlit export.
    """
    images = images or []
    image_descriptions = image_descriptions or []

    title_clean = clean_markdown_formatting(title)
    content = clean_separator_lines(content)

    html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_clean}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.8;
            max-width: 900px;
            margin: 0 auto;
            padding: 30px;
            color: #333;
            background-color: #f8f9fa;
        }}
        .container {{
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 4px solid #3498db;
            padding-bottom: 15px;
            margin-bottom: 30px;
            font-size: 2.5em;
        }}
        h2 {{
            color: #34495e;
            margin-top: 40px;
            margin-bottom: 20px;
            font-size: 1.8em;
            border-left: 4px solid #3498db;
            padding-left: 15px;
        }}
        h3 {{
            color: #555;
            margin-top: 30px;
            margin-bottom: 15px;
            font-size: 1.4em;
        }}
        h4, h5, h6 {{
            color: #555;
            margin-top: 25px;
            margin-bottom: 10px;
        }}
        .meta-info {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            margin: 25px 0;
            font-size: 0.95em;
        }}
        .image-gallery {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        .image-gallery img {{
            width: 100%;
            height: auto;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }}
        .image-gallery img:hover {{
            transform: scale(1.02);
        }}
        p {{
            margin-bottom: 15px;
            line-height: 1.8;
        }}
        blockquote {{
            border-left: 5px solid #3498db;
            margin: 25px 0;
            padding: 15px 25px;
            color: #555;
            font-style: italic;
            background: #ecf0f1;
            border-radius: 5px;
        }}
        ul, ol {{
            margin: 20px 0;
            padding-left: 30px;
        }}
        li {{
            margin-bottom: 12px;
            line-height: 1.6;
        }}
        .caption {{
            text-align: center;
            font-size: 0.85em;
            color: #666;
            margin-top: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title_clean}</h1>
        <div class="meta-info">
            <p><strong>📅 Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
            <p><strong>📝 Word Count:</strong> {meta_info.get('word_count', 'N/A')}</p>
            <p><strong>⏱️ Reading Time:</strong> {meta_info.get('reading_time', 'N/A')}</p>
            <p><strong>🎯 SEO Score:</strong> {meta_info.get('seo_score', 'N/A')}</p>
        </div>
"""

    # Images
    if images:
        html_template += "        <h2>Visual Content</h2>\n"
        html_template += '        <div class="image-gallery">\n'
        for i, img_url in enumerate(images):
            desc = image_descriptions[i] if i < len(image_descriptions) else "Content Image"
            html_template += "            <div>\n"
            html_template += f'                <img src="{img_url}" alt="Content image {i+1}" loading="lazy" />\n'
            html_template += f'                <div class="caption">Figure {i+1}: {desc}</div>\n'
            html_template += "            </div>\n"
        html_template += "        </div>\n"

    html_template += '        <div class="content">\n'

    heading_pattern = re.compile(r"^\s*(#{1,6})\s*(.*)")
    in_list = False

    for line in content.split("\n"):
        raw = line.rstrip()
        stripped = raw.strip()

        if not stripped:
            if in_list:
                html_template += "        </ul>\n"
                in_list = False
            html_template += "        <br>\n"
            continue

        m = heading_pattern.match(stripped)
        if m:
            if in_list:
                html_template += "        </ul>\n"
                in_list = False

            level = len(m.group(1))
            heading_text = clean_markdown_formatting(stripped)
            tag = {1: "h1", 2: "h2", 3: "h3", 4: "h4", 5: "h5"}.get(level, "h6")
            html_template += f"        <{tag}>{heading_text}</{tag}>\n"
            continue

        if stripped.startswith("> "):
            if in_list:
                html_template += "        </ul>\n"
                in_list = False
            html_template += f"        <blockquote>{clean_markdown_formatting(stripped[2:])}</blockquote>\n"
            continue

        if stripped.startswith("- ") or stripped.startswith("* "):
            if not in_list:
                html_template += "        <ul>\n"
                in_list = True
            text_line = clean_markdown_formatting(stripped[2:])
            html_template += f"            <li>{text_line}</li>\n"
            continue

        if in_list:
            html_template += "        </ul>\n"
            in_list = False

        label, sep, rest = stripped.partition(":")
        if sep and len(label.split()) <= 5 and all(w[:1].isupper() for w in label.split() if w):
            label_html = clean_markdown_formatting(label)
            rest_html = clean_markdown_formatting(rest.strip()) if rest.strip() else ""
            html_template += f"        <p><strong>{label_html}:</strong> {rest_html}</p>\n"
        else:
            text_line = clean_markdown_formatting(stripped)
            html_template += f"        <p>{text_line}</p>\n"

    if in_list:
        html_template += "        </ul>\n"

    html_template += """
        </div>
    </div>
</body>
</html>
"""
    return html_template.encode("utf-8")


# =========================================================
# API Endpoints
# =========================================================

@app.get("/api/health")
async def health_check():
    return {
        "status": "ok",
        "message": "Blog Generation API is running",
        "timestamp": datetime.now().isoformat(),
    }


@app.post("/api/blog/generate", response_model=BlogGenerationResponse)
async def generate_blog(request: BlogGenerationRequest):
    """
    Generate blog + optional AI images.
    API keys are taken ONLY from .env, not from headers.
    """
    try:
        if not ENV_GROQ_API_KEY:
            raise HTTPException(
                status_code=500,
                detail="GROQ_API_KEY not configured in environment (.env)",
            )

        # 1) Generate blog content
        blog_content = generate_blog_with_llm(
            topic=request.topic,
            category=request.category,
            niche=request.niche,
            keywords=request.keywords,
            target_audience=request.targetAudience,
            content_intent=request.contentIntent,
            expertise_level=request.expertiseLevel,
            tone=request.tone,
            length=request.length,
            writing_style=request.writingStyle,
            additional_context=request.additionalContext,
        )

        # 2) Basic metrics
        word_count = len(blog_content.split())
        reading_time = max(1, int(word_count / 230))

        all_images: List[str] = []
        image_descriptions: List[str] = []

        # 3) AI Images (Gemini)
        if request.useAiImages and ENV_GEMINI_API_KEY:
            # Prefer your structured infographic/flowchart prompts
            image_prompts = [
                f"{request.topic} infographic, clean layout, labeled sections, icons, flat vector design, pastel colors, corporate look, boxes with labels, arrows showing relationships, modern UI infographic, high resolution",
                f"{request.topic} overview infographic, blocks with titles, arrows, minimal flow structure, flat modern vector style, pastel theme",
                f"{request.topic} visual summary infographic, simplified labeled blocks, icons, modern flat UI, clean corporate infographic style",
                f"{request.topic} flowchart diagram, rectangular blocks with labels, arrows between steps, white background, thin lines, flat vector style, professional process diagram",
                f"{request.topic} decision flowchart, diamond decision nodes, labeled rectangles, directional arrows, minimal pastel colors, clean schematic diagram",
                f"{request.topic} process flowchart, linear step-by-step boxes, arrows connecting each stage, modern vector workflow diagram",
            ][: request.numAiImages]

            if not image_prompts:
                image_prompts = generate_image_prompts(request.topic, request.numAiImages)

            image_titles = generate_image_captions_from_prompts(request.topic, image_prompts)

            for idx, prompt in enumerate(image_prompts):
                img_url = generate_gemini_image(prompt)
                if img_url:
                    all_images.append(img_url)
                    desc = image_titles[idx] if idx < len(image_titles) else request.topic
                    image_descriptions.append(f"{desc} (Source: Gemini)")
                await asyncio.sleep(0.5)

        # 4) Pexels images
        if request.usePexels and ENV_PEXELS_API_KEY:
            pexels_images = fetch_pexels_images(request.topic, request.numPexelsImages)
            all_images.extend(pexels_images)
            for _ in pexels_images:
                image_descriptions.append(f"Stock photo related to {request.topic}")

        return BlogGenerationResponse(
            success=True,
            title=f"{request.topic}: A Comprehensive Guide",
            content=blog_content,
            wordCount=word_count,
            readingTime=f"{reading_time} min",
            images=all_images,
            imageDescriptions=image_descriptions,
            seoScore="N/A",
        )

    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        return BlogGenerationResponse(success=False, error=str(e))


@app.post("/api/blog/export")
async def export_blog(request: ExportRequest):
    """
    Export blog to PDF, DOCX or HTML.
    Expects metaInfo keys: word_count, reading_time, seo_score (optional).
    """
    try:
        fmt = request.format.lower()

        if fmt == "pdf":
            pdf_bytes = generate_pdf(
                request.title,
                request.content,
                request.metaInfo,
                images=request.images,
                image_descriptions=request.imageDescriptions,
            )
            return Response(
                content=pdf_bytes,
                media_type="application/pdf",
                headers={
                    "Content-Disposition": f'attachment; filename="{request.title.replace(" ", "_")}.pdf"'
                },
            )

        if fmt == "docx":
            docx_bytes = generate_docx(
                request.title,
                request.content,
                request.metaInfo,
                images=request.images,
                image_descriptions=request.imageDescriptions,
            )
            return Response(
                content=docx_bytes,
                media_type=(
                    "application/vnd.openxmlformats-"
                    "officedocument.wordprocessingml.document"
                ),
                headers={
                    "Content-Disposition": f'attachment; filename="{request.title.replace(" ", "_")}.docx"'
                },
            )

        if fmt == "html":
            html_bytes = generate_html(
                request.title,
                request.content,
                request.metaInfo,
                images=request.images,
                image_descriptions=request.imageDescriptions,
            )
            return Response(
                content=html_bytes,
                media_type="text/html; charset=utf-8",
                headers={
                    "Content-Disposition": f'attachment; filename="{request.title.replace(" ", "_")}.html"'
                },
            )

        raise HTTPException(status_code=400, detail="Invalid format. Use 'pdf', 'docx', or 'html'.")

    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")


# =========================================================
# Dashboard / Agent Monitor / Analytics-style endpoints
# (Optional: no DB, just static/sample data like Streamlit)
# =========================================================

@app.get("/api/dashboard/summary", response_model=DashboardSummary)
async def get_dashboard_summary():
    """
    Mirrors Dashboard metrics in your Streamlit UI (static sample).
    """
    return DashboardSummary(
        activeAgents=25,
        blogsCreated=147,
        successRate=94.2,
        avgQualityScore=8.7,
    )


@app.get("/api/agents/active", response_model=List[AgentInfo])
async def get_active_agents():
    """
    Mirrors Agent Monitor page: list of agents & their load.
    """
    agents = [
        {"agent": "Content Generation Agent", "phase": "Core System", "status": "Active", "load": 85},
        {"agent": "Image Generation Agent", "phase": "Visual", "status": "Active", "load": 72},
        {"agent": "SEO Optimization Agent", "phase": "SEO", "status": "Processing", "load": 91},
        {"agent": "Format Export Agent", "phase": "Export", "status": "Idle", "load": 15},
        {"agent": "Quality Check Agent", "phase": "Review", "status": "Active", "load": 68},
    ]
    return [AgentInfo(**a) for a in agents]


@app.get("/api/analytics/overview")
async def analytics_overview():
    """
    Rough equivalent of your Analytics page: returns sample data
    (you can later wire this to real storage if needed).
    """
    # Simple static payload similar to your Streamlit charts
    blog_performance = [
        {"date": "2024-01-01", "views": 230},
        {"date": "2024-01-02", "views": 540},
        {"date": "2024-01-03", "views": 900},
    ]
    agent_efficiency = [
        {"agentType": "Content Generation", "successRate": 94.2},
        {"agentType": "Image Generation", "successRate": 92.5},
        {"agentType": "SEO Optimization", "successRate": 89.7},
        {"agentType": "Export", "successRate": 97.1},
    ]
    recent_blogs = [
        {"title": "AI Trends 2025", "views": 2341, "engagement": 8.7, "images": 3},
        {"title": "Tech Innovation Guide", "views": 1876, "engagement": 7.2, "images": 5},
        {"title": "Market Analysis Report", "views": 1543, "engagement": 9.1, "images": 2},
    ]
    return JSONResponse(
        {
            "blogPerformance": blog_performance,
            "agentEfficiency": agent_efficiency,
            "recentBlogs": recent_blogs,
        }
    )


# =========================================================
# Entry point (optional when running with `uvicorn main:app`)
# =========================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST, port=PORT, reload=True)

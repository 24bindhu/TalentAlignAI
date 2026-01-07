import os
import re
import json
import requests
import torch
from sentence_transformers import SentenceTransformer, util
from dotenv import load_dotenv

# =====================================================================
# STEP 1: Setup
# =====================================================================
# Load .env file for Gemini API key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY is None:
    raise ValueError("GEMINI_API_KEY not found in .env file")

GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

# Sentence transformer for semantic similarity
device = "cuda" if torch.cuda.is_available() else "cpu"
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Stopwords for keyword extraction
STOPWORDS = {
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
    'has', 'have', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
    'to', 'was', 'will', 'with', 'looking', 'experience', 'experienced',
    'this', 'these', 'those', 'their', 'our', 'you', 'your', 'they',
    'we', 'us', 'such', 'some', 'also', 'other', 'all', 'any', 'each',
    'can', 'could', 'should', 'would', 'must', 'may', 'might',
    'been', 'being', 'have', 'had', 'do', 'does', 'did', 'about',
    'into', 'through', 'during', 'before', 'after', 'above', 'below',
    'up', 'down', 'out', 'off', 'over', 'under', 'again', 'further',
    'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how',
    'both', 'few', 'more', 'most', 'same', 'than', 'too', 'very',
    'able', 'around', 'based', 'including', 'etc', 'using','what', 'who', 'every', 'everything', 'work', 'making', 'role'
}

# =====================================================================
# Helper Functions
# =====================================================================
def extract_keywords(text):
    """Extract meaningful keywords from text"""
    tokens = re.findall(r'\b\w+\b', text.lower())
    keywords = set()
    for token in tokens:
        if len(token) > 2 and token not in STOPWORDS and not token.isdigit():
            keywords.add(token)
    return keywords

def generate_with_gemini_rest(prompt, max_retries=3):
    """Generate response using Gemini REST API"""
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 2048, "topP": 0.95, "topK": 40},
        "safetySettings": [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
        ]
    }

    headers = {"Content-Type": "application/json"}

    for attempt in range(max_retries):
        try:
            response = requests.post(GEMINI_API_URL, headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and len(result['candidates']) > 0:
                    candidate = result['candidates'][0]
                    if 'content' in candidate and 'parts' in candidate['content']:
                        text = ' '.join([part.get('text', '') for part in candidate['content']['parts']])
                        return text.strip()
                    if 'finishReason' in candidate and candidate['finishReason'] != 'MAX_TOKENS':
                        return "Unable to generate response."
            else:
                print(f"⚠️ API Error {response.status_code}: {response.text}")
        except Exception as e:
            print(f"⚠️ Exception on attempt {attempt + 1}: {e}")
    return "Unable to generate response after retries."

def parse_bullet_points(text):
    """Parse bullet points from LLM response"""
    lines = text.split('\n')
    bullets = []
    for line in lines:
        line = line.strip()
        if re.match(r'^[\d\-\•\*]+[\.\):]?\s+', line):
            clean_line = re.sub(r'^[\d\-\•\*]+[\.\):]?\s+', '', line).strip()
            if clean_line and len(clean_line) > 10:
                bullets.append(clean_line)
    if len(bullets) == 0:
        sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 20]
        bullets = sentences[:5]
    return bullets[:5]

# =====================================================================
# Main Analysis Function
# =====================================================================
def analyze_resume(resume_text, job_text):
    """Analyze resume against job description using Gemini LLM"""
    print("🔍 Starting analysis...\n")

    # 1️⃣ Semantic similarity
    print("📊 Calculating match score...")
    resume_emb = embedding_model.encode(resume_text, convert_to_tensor=True)
    job_emb = embedding_model.encode(job_text, convert_to_tensor=True)
    similarity = util.cos_sim(resume_emb, job_emb).item()
    match_score = round(similarity * 100, 2)

    # 2️⃣ Keywords
    print("🔑 Extracting keywords...")
    resume_keywords = extract_keywords(resume_text)
    job_keywords = extract_keywords(job_text)
    skills_match = sorted(list(resume_keywords.intersection(job_keywords)))
    missing_skills = sorted(list(job_keywords - resume_keywords))

    # 3️⃣ Strengths
    print("💪 Generating strengths with Gemini...")
    prompt_strengths = f"Compare resume to job. List 5 key candidate strengths (10 words each max):\nRESUME: {resume_text[:1000]}\nJOB: {job_text[:1000]}\nStrengths:\n1."
    strengths_text = generate_with_gemini_rest(prompt_strengths)
    strengths = parse_bullet_points(strengths_text)

    # 4️⃣ Improvements
    print("📈 Generating improvements with Gemini...")
    prompt_improvements = f"Compare resume to job. List 5 specific improvements (10 words each max):\nRESUME: {resume_text[:1000]}\nJOB: {job_text[:1000]}\nImprovements:\n1."
    improvements_text = generate_with_gemini_rest(prompt_improvements)
    improvements = parse_bullet_points(improvements_text)

    print("✅ Analysis complete!\n")

    return {
        "match_score": match_score,
        "skills_match": skills_match,
        "missing_skills": missing_skills,
        "strengths": strengths,
        "improvements": improvements,
        "raw_strengths": strengths_text,
        "raw_improvements": improvements_text
    }

# =====================================================================
# Pretty Print Function
# =====================================================================
def print_analysis(result):
    print("=" * 70)
    print(f"📊 OVERALL MATCH SCORE: {result['match_score']}%")
    print("=" * 70)
    print("\n✅ MATCHED SKILLS:")
    for skill in result['skills_match'][:15]:
        print(f"  • {skill}")
    print("\n❌ MISSING SKILLS:")
    for skill in result['missing_skills'][:15]:
        print(f"  • {skill}")
    print("\n💪 KEY STRENGTHS:")
    for i, s in enumerate(result['strengths'], 1):
        print(f"  {i}. {s}")
    print("\n📈 AREAS FOR IMPROVEMENT:")
    for i, imp in enumerate(result['improvements'], 1):
        print(f"  {i}. {imp}")
    print("\n" + "=" * 70)

# =====================================================================
# Minimal test block
# =====================================================================
if __name__ == "__main__":
    print("✅ llm_gemini.py loaded successfully. Use analyze_resume(resume_text, job_text) from main.py")

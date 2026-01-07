# 🤖 AI-Powered Resume Analyzer

An intelligent resume analysis tool that uses Google's Gemini AI to compare your resume against job descriptions and provide actionable insights to improve your application.

## ✨ Features

- 🎯 **Semantic Match Score**: Calculates overall compatibility between resume and job description
- 🔍 **Keyword Analysis**: Identifies matched and missing skills
- 💪 **AI-Powered Strengths**: Gemini AI analyzes your key strengths for the role
- 📈 **Smart Recommendations**: Get specific, actionable improvements to enhance your resume
- 💬 **Interactive CLI**: Easy-to-use command-line interface

## 🚀 Demo
```
Match Score: 58.43%

Skills Matched:
  - python
  - react
  - authentication
  - apis
  - cloud

Strengths:
  - Strong grasp of authentication basics and API security concepts
  - Proven experience designing and deploying scalable software solutions
  - Direct experience with React.js, a key part of their tech stack
  ...

Improvements:
  - Highlight experience with authentication, SSO, and identity platforms
  - Express eagerness to learn Go (Golang) for identity systems
  - Specify AWS and Kubernetes experience for scalable platforms
  ...
```

## 📋 Prerequisites

- Python 3.8 or higher
- 500MB free disk space
- 2GB RAM (4GB recommended)
- Gemini API key (free from [Google AI Studio](https://aistudio.google.com/app/apikey))

## 🛠️ Installation

1. **Clone the repository**
```bash
   git clone https://github.com/yourusername/ai-resume-analyzer.git
   cd ai-resume-analyzer
```

2. **Create a virtual environment** (recommended)
```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
```

3. **Install dependencies**
```bash
   pip install -r requirements.txt
```

4. **Set up your API key**
   
   Create a `.env` file in the project root:
```
   GEMINI_API_KEY=your_gemini_api_key_here
```
   
   Get your free API key from: https://aistudio.google.com/app/apikey

## 💻 Usage

1. **Run the analyzer**
```bash
   python main.py
```

2. **Paste your resume**
   - Copy your entire resume text
   - Paste it into the terminal
   - Type `END` on a new line and press Enter

3. **Paste the job description**
   - Copy the full job posting
   - Paste it into the terminal
   - Type `END` on a new line and press Enter

4. **Review your results**
   - Match score percentage
   - Skills you have vs. skills you're missing
   - AI-generated strengths and improvement suggestions


## 🔧 Troubleshooting

### Storage/Memory Errors

If you encounter storage or memory errors, the semantic similarity feature may be causing issues. You can disable it:

**In `llm_gemini.py`, comment out these lines:**
```python
# Line 7:
# from sentence_transformers import SentenceTransformer, util

# Lines 16-17:
# device = "cuda" if torch.cuda.is_available() else "cpu"
# embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Lines 105-110 (in analyze_resume function):
# print("📊 Calculating match score...")
# resume_emb = embedding_model.encode(resume_text, convert_to_tensor=True)
# job_emb = embedding_model.encode(job_text, convert_to_tensor=True)
# similarity = util.cos_sim(resume_emb, job_emb).item()
# match_score = round(similarity * 100, 2)

# Replace with:
match_score = 0
```

The analyzer will still provide AI-powered strengths and improvements, just without the percentage match score.

### API Key Issues

- **Error: "GEMINI_API_KEY not found"**
  - Make sure your `.env` file exists in the project root
  - Verify the key name is exactly `GEMINI_API_KEY`
  - Check that your API key is valid

- **Error: "404 Model not found"**
  - Verify your API key is active
  - Check your internet connection
  - Ensure you haven't exceeded the free tier limits (60 requests/minute)

### Rate Limits

Gemini API free tier limits:
- 60 requests per minute
- 1,500 requests per day

If you hit rate limits, wait a minute and try again.

## 🎓 How It Works

1. **Keyword Extraction**: Uses natural language processing to extract meaningful keywords from both texts
2. **Semantic Analysis**: Employs sentence transformers to calculate semantic similarity
3. **AI Analysis**: Leverages Gemini 2.5 Flash to generate context-aware insights
4. **Result Synthesis**: Combines all analyses into actionable recommendations


## 🙏 Acknowledgments

- Google Gemini AI for powering the intelligent analysis
- Sentence Transformers for semantic similarity
- The open-source community




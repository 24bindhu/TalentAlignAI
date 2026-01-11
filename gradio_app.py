import gradio as gr
from llm_gemini import analyze_resume

def analyze(resume, job):
    if not resume or not job:
        return "Please fill in both fields!", "", "", "", ""
    
    result = analyze_resume(resume, job)
    
    matched = "\n".join([f"• {s}" for s in result['skills_match'][:15]])
    missing = "\n".join([f"• {s}" for s in result['missing_skills'][:15]])
    strengths = "\n".join([f"{i}. {s}" for i, s in enumerate(result['strengths'], 1)])
    improvements = "\n".join([f"{i}. {s}" for i, s in enumerate(result['improvements'], 1)])
    
    return (
        f"{result['match_score']}%",
        matched,
        missing,
        strengths,
        improvements
    )

# Custom CSS for better styling
css = """
#score {font-size: 48px; font-weight: bold; color: #2563eb; text-align: center;}
.gradio-container {font-family: 'Inter', sans-serif; max-width: 1200px;}
"""

with gr.Blocks(css=css, theme=gr.themes.Soft(), title="TalentAlignAI") as demo:
    gr.Markdown("# 🤖 TalentAlignAI")
    gr.Markdown("### Align your talent with opportunity using AI-powered insights")
    
    with gr.Row():
        with gr.Column():
            resume_input = gr.Textbox(
                label="📄 Your Resume",
                placeholder="Paste your resume here...",
                lines=15
            )
        with gr.Column():
            job_input = gr.Textbox(
                label="💼 Job Description",
                placeholder="Paste job description here...",
                lines=15
            )
    
    analyze_btn = gr.Button("🚀 Analyze Resume", variant="primary", size="lg")
    
    with gr.Row():
        score_output = gr.Textbox(label="📊 Match Score", elem_id="score", interactive=False)
    
    with gr.Row():
        with gr.Column():
            matched_output = gr.Textbox(label="✅ Matched Skills", lines=8, interactive=False)
            strengths_output = gr.Textbox(label="💪 Key Strengths", lines=8, interactive=False)
        with gr.Column():
            missing_output = gr.Textbox(label="❌ Missing Skills", lines=8, interactive=False)
            improvements_output = gr.Textbox(label="📈 Improvements", lines=8, interactive=False)
    
    gr.Markdown("---")
    gr.Markdown("*Powered by Google Gemini AI | Built with Gradio*")
    
    analyze_btn.click(
        fn=analyze,
        inputs=[resume_input, job_input],
        outputs=[score_output, matched_output, missing_output, strengths_output, improvements_output]
    )

if __name__ == "__main__":
    demo.launch()
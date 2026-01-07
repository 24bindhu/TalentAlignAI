# main.py

from llm_gemini import analyze_resume, print_analysis

# ------------------------------
# Interactive input functions
# ------------------------------
def get_input(prompt):
    print(prompt)
    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)
    return "\n".join(lines)

def display_report(result):
    print("\n===== MATCH REPORT =====")
    print(f"Match Score: {result['match_score']}%")
    
    print("\nSkills Matched:")
    for skill in result['skills_match']:
        print(f"  - {skill}")
    
    print("\nMissing Skills:")
    for skill in result['missing_skills']:
        print(f"  - {skill}")
    
    print("\nStrengths:")
    for s in result['strengths']:
        print(f"  - {s}")
    
    print("\nImprovements:")
    for i in result['improvements']:
        print(f"  - {i}")
    
    print("========================\n")

# ------------------------------
# Main interactive function
# ------------------------------
def main():
    resume_text = get_input("Please paste your resume here (Type 'END' on a new line to finish):")
    job_text = get_input("Please paste the job description here (Type 'END' on a new line to finish):")

    print("\nRunning LLM analysis...\n")
    result = analyze_resume(resume_text, job_text)
    display_report(result)

# ------------------------------
# Direct test block with sample data
# ------------------------------
if __name__ == "__main__":
    main()

    
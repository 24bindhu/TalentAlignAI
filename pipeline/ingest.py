import os

def load_inputs(resume_file="data/resume.txt", job_file="data/job_description.txt"):
    """
    Loads resume and job description.
    If files are empty or missing, asks user for multi-line interactive input.
    End input by typing 'END' on a new line.
    """
    
    # Helper function to read multi-line input
    def multiline_input(prompt):
        print(prompt + " (Type 'END' on a new line to finish)")
        lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        return "\n".join(lines)

    # Load resume
    if os.path.exists(resume_file) and os.path.getsize(resume_file) > 0:
        with open(resume_file, "r", encoding="utf-8") as f:
            resume = f.read()
    else:
        resume = multiline_input("Please paste your resume here")

    # Load job description
    if os.path.exists(job_file) and os.path.getsize(job_file) > 0:
        with open(job_file, "r", encoding="utf-8") as f:
            job_description = f.read()
    else:
        job_description = multiline_input("Please paste the job description here")

    return resume, job_description

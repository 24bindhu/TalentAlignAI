import json
import os

def generate_report(llm_result: dict, output_path="data/report.json") -> None:
    """
    Generates a JSON report with scoring and saves it to disk.
    """

    matched_skills = llm_result.get("skills_match", [])
    missing_skills = llm_result.get("missing_skills", [])

    # Simple score: % of skills matched
    total_skills = len(matched_skills) + len(missing_skills)
    if total_skills == 0:
        match_score = 0
    else:
        match_score = round(len(matched_skills) / total_skills * 100, 2)

    report = {
        "skills_match": matched_skills,
        "missing_skills": missing_skills,
        "strengths": llm_result.get("strengths", []),
        "improvements": llm_result.get("improvements", []),
        "match_score_percent": match_score
    }

    # Save JSON to disk
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)

    # Print console summary
    print("\n===== MATCH REPORT =====")
    print(f"Skills Matched: {matched_skills}")
    print(f"Missing Skills: {missing_skills}")
    print(f"Strengths: {llm_result.get('strengths', [])}")
    print(f"Improvements: {llm_result.get('improvements', [])}")
    print(f"Match Score: {match_score}%")
    print("========================\n")

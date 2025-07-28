import os
import json
import time
from pdf_utils import extract_sections_from_pdf
from nlp_utils import rank_sections_by_relevance

def process_documents(input_pdfs, persona, job):
    all_sections = []
    for pdf_file in input_pdfs:
        sections = extract_sections_from_pdf(pdf_file)
        for section in sections:
            section["document_name"] = os.path.basename(pdf_file)
        all_sections.extend(sections)

    # Combine persona and job description as query for ranking
    combined_query = f"{persona}. {job}"
    ranked_sections = rank_sections_by_relevance(all_sections, combined_query)

    output = {
        "metadata": {
            "input_documents": [os.path.basename(f) for f in input_pdfs],
            "persona": persona,
            "job_to_be_done": job,
            "processed_timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")
        },
        "extracted_sections": ranked_sections
    }
    return output

if __name__ == "__main__":
    INPUT_DIR = "/app/input"
    OUTPUT_DIR = "/app/output"
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # -- Customize the persona and job-to-be-done below --
    # For example, Test Case 1 from the challenge brief:
    persona_text = "PhD Researcher in Computational Biology"
    job_text = "Prepare a comprehensive literature review focusing on methodologies, datasets, and performance benchmarks"

    # Get PDF paths
    pdf_filenames = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".pdf")]
    pdf_paths = [os.path.join(INPUT_DIR, f) for f in pdf_filenames]

    # Process documents
    if not pdf_paths:
        print("No PDF files found in input directory.", flush=True)
        exit(0)

    result = process_documents(pdf_paths, persona_text, job_text)

    # Save JSON output
    output_path = os.path.join(OUTPUT_DIR, "result.json")
    with open(output_path, "w", encoding="utf-8") as f_out:
        json.dump(result, f_out, indent=2, ensure_ascii=False)
    print(f"Processing complete. Output saved to {output_path}", flush=True)

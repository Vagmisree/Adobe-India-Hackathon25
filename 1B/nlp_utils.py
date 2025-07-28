from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')  # lightweight, fast, ~100MB

def embed_texts(text_list):
    return model.encode(text_list, convert_to_numpy=True, show_progress_bar=False)

def rank_sections_by_relevance(sections, persona_job_text):
    # Combine persona + job description for embedding
    query_embedding = embed_texts([persona_job_text])[0]
    section_texts = [s['title'] + " " + s['text'][:512] for s in sections]  # limit text size to embed
    section_embeddings = embed_texts(section_texts)
    
    # Compute cosine similarity
    sims = section_embeddings @ query_embedding / (np.linalg.norm(section_embeddings, axis=1) * np.linalg.norm(query_embedding) + 1e-10)
    ranked_sections = sorted(zip(sections, sims), key=lambda x: x[1], reverse=True)
    # Assign importance ranks based on sorted similarity
    output_sections = []
    for idx, (section, score) in enumerate(ranked_sections, start=1):
        output_sections.append({
            "document": section.get("document_name", "unknown"),
            "page_number": section["page"],
            "section_title": section["title"],
            "importance_rank": idx,
            "refined_text": section["text"]
        })
    return output_sections

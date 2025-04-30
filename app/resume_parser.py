import spacy

def extract_skills(resume_text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(resume_text)
    return [chunk.text for chunk in doc.noun_chunks if len(chunk.text) > 2]
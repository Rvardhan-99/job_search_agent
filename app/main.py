import streamlit as st
import io
import docx
from pdfminer.high_level import extract_text as extract_pdf_text
from job_scraper import scrape_career_page_links
from resume_parser import extract_skills

def main():
    st.title("AI Job Finder: Career Page Scraper")

    uploaded_file = st.file_uploader("Upload your resume", type=["pdf", "docx"])
    if uploaded_file:
    file_type = uploaded_file.name.split(".")[-1].lower()
    resume_text = ""

    if file_type == "pdf":
        with open("temp_resume.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        resume_text = extract_pdf_text("temp_resume.pdf")

    elif file_type == "docx":
        doc = docx.Document(io.BytesIO(uploaded_file.getbuffer()))
        resume_text = "\n".join([p.text for p in doc.paragraphs])

    else:
        st.error("Only PDF and DOCX files are supported.")
        return
        
        skills = extract_skills(resume_text)
        st.success("Resume processed.")
        st.write("Extracted Skills:", skills)

    keywords = st.text_input("Enter job keywords (comma-separated)", "software engineer, data")
    location = st.text_input("Enter your location (Zip code, City)")
    radius = st.slider("Commutable Distance (in miles)", 10, 100, 50)

    companies = ["Google", "Microsoft", "Amazon", "Meta", "Apple"]

    if st.button("Search Jobs"):
        keyword_list = [k.strip() for k in keywords.split(",")]
        job_listings = scrape_career_page_links(companies, keyword_list, location, radius)
        st.write(f"Found {len(job_listings)} jobs:")

        for job in job_listings:
            st.markdown(f"**{job['job_title']}** at {job['company']} - [{job['url']}]({job['url']})")

if __name__ == "__main__":
    main()

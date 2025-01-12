

import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(job_description, resume):
    """
    Calculates the cosine similarity between job description and resume.
    """
    texts = [job_description, resume]
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(texts)
    similarity_score = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]
    return similarity_score

def main():
    st.title("ATS System")

    # Upload Job Description
    jd_file = st.file_uploader("Upload Job Description", type=["txt", "pdf"])
    if jd_file is not None:
        if jd_file.type == "text/plain":
            job_description = str(jd_file.read(), 'utf-8')
        elif jd_file.type == "application/pdf":
            # Handle PDF parsing (e.g., using PyPDF2)
            import PyPDF2
            with open(jd_file.name, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                job_description = ""
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    job_description += page.extract_text()

    # Upload Resume
    resume_file = st.file_uploader("Upload Resume", type=["txt", "pdf", "docx"])
    if resume_file is not None:
        if resume_file.type == "text/plain":
            resume_text = str(resume_file.read(), 'utf-8')
        elif resume_file.type == "application/pdf":
            # Handle PDF parsing (e.g., using PyPDF2)
            import PyPDF2
            with open(resume_file.name, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                resume_text = ""
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    resume_text += page.extract_text()
        elif resume_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            # Handle docx parsing (e.g., using python-docx)
            from docx import Document
            doc = Document(resume_file)
            resume_text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])

        # Calculate Similarity Score
        if job_description and resume_text:
            similarity_score = calculate_similarity(job_description, resume_text)

            # Display Results
            st.write("Similarity Score:", similarity_score)

            # Categorize and Provide Feedback
            if similarity_score > 0.7:
                st.success("**Strong Match:** Your resume aligns well with the job description.")
            elif 0.5 < similarity_score <= 0.7:
                st.warning("**Moderate Match:** Your resume shows some relevant skills and experience.")
            else:
                st.error("**Weak Match:** Your resume may not be a strong fit for this position.")

if __name__ == "__main__":
    main()
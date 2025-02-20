import PyPDF2
import re

def extract_text_from_resume(pdf_path):
    """Extract text from PDF resume."""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {str(e)}")
        return ""
    return text

def extract_email(text):
    """Extract email address from text."""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    return emails[0] if emails else "No email found"

def extract_skills(text):
    """Extract common skills from text."""

    common_skills = [
        "python", "java", "javascript", "html", "css", "sql", "react",
        "node", "docker", "kubernetes", "aws", "azure", "machine learning",
        "data analysis", "project management", "agile", "scrum", "artificial intelligence", "deep learning",
        "web development", "full stack", "TensorFlow", "PyTorch", "Scikit-learn", "OpenAI Whisper", "NLP",
        "React.js", "Node.js", "Express.js", "Flask, Streamlit", "RESTful APIs", "Web Scraping", "OpenAI API"
        "yolo", "transferlearing"
    ]
    
    skills_found = []
    text_lower = text.lower()
    
    for skill in common_skills:
        if skill in text_lower:
            skills_found.append(skill)
    
    return skills_found
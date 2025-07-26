import streamlit as st
import pdfplumber
from google import generativeai as genai
from reportlab.pdfgen import canvas
from googletrans import Translator
import tempfile
import os

genai.configure(api_key="AIzaSyBgFM3UZxZYb5CV6W3EWsA_-DAxsC3AgUs")
model = genai.GenerativeModel("gemini-1.5-flash")

translator = Translator()

# PAGE CONFIG
st.set_page_config(page_title="Career Advisor Pro", layout="wide")

# ---------- ADVANCED CSS STYLING ----------
st.markdown("""
    <style>
    .sidebar .sidebar-content {
        background-color: #20222e;
        color: white;
        font-family: 'Segoe UI', sans-serif;
    }
    .css-1d391kg { 
        color: white; 
    }
    .st-emotion-cache-16txtl3 { 
        font-size: 18px !important;
        color: white !important;
    }
    .option-menu .nav-link {
        color: #fff;
    }
    .option-menu .nav-link.active {
        background-color: #4B6CB7;
        color: #fff;
    }
    </style>
""", unsafe_allow_html=True)
# ---------- SIDEBAR ----------
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/29/29302.png", width=100)

st.sidebar.title("🚀 Career Advisor Pro")
nav = st.sidebar.radio("Go to", [
    "Career Match", "Personality Quiz", "Resume Analyzer", "Skills & Courses",
    "Career Roadmap", "Job Trends", "Mock Interview", "Career FAQs",
    "Career Timeline", "Internship Ideas"
])

# ---------- 1. Career Match ----------
if nav == "Career Match":
    st.title("👨‍🎓 carrier Advisor")
    user_input = st.text_area("Describe your interests, skills, or career goals:")
    if st.button("Suggest Careers"):
        with st.spinner("Analyzing..."):
            response = model.generate_content(f"Suggest top careers for: {user_input}")
            st.markdown(f"### 💼 Career Suggestions:\n{response.text}")

# ---------- 2. Personality Quiz ----------
elif nav == "Personality Quiz":
    st.title("🧠 Personality / Aptitude Quiz")
    q1 = st.radio("What excites you most?", ["Problem-solving", "Helping", "Art", "Leadership"])
    q2 = st.radio("You're best at:", ["Logic", "Empathy", "Creativity", "Organizing"])
    q3 = st.radio("Work preference:", ["Solo", "Team", "Both"])
    q4 = st.radio("You value:", ["Stability", "Flexibility", "Fame", "Money"])
    q5 = st.radio("In free time, you like to:", ["Code", "Volunteer", "Draw", "Debate"])
    if st.button("Get Personality-Based Careers"):
        traits = f"I like {q1}, I'm good at {q2}, prefer {q3} work, value {q4}, and enjoy {q5}."
        with st.spinner("Finding matches..."):
            result = model.generate_content(f"Based on this: {traits}, suggest 3 suitable careers.")
            st.markdown(result.text)

# ---------- 3. Resume Analyzer ----------
elif nav == "Resume Analyzer":
    st.title("📄 Resume Analyzer")
    file = st.file_uploader("Upload PDF Resume", type="pdf")
    if file:
        with pdfplumber.open(file) as pdf:
            text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
        if st.button("Analyze Resume"):
            with st.spinner("Reviewing your resume..."):
                feedback = model.generate_content(f"Review and suggest improvements for:\n{text[:3000]}")
                st.markdown("### 📝 Suggestions:")
                st.markdown(feedback.text)

# ---------- 4. Skills & Courses ----------
elif nav == "Skills & Courses":
    st.title("📚 Skill Gap & Course Suggestions")
    job = st.text_input("Target Role (e.g., Cloud Engineer)")
    skills = st.text_area("Your Current Skills:")
    if st.button("Analyze Skill Gap"):
        query = f"I want to become a {job}. I know {skills}. What skills do I need more, and which courses can help?"
        with st.spinner("Checking..."):
            out = model.generate_content(query)
            st.markdown(out.text)

# ---------- 5. Career Roadmap + PDF ----------
elif nav == "Career Roadmap":
    st.title("🗺️ Career Roadmap")
    role = st.text_input("Enter career role:")
    if st.button("Create Roadmap"):
        roadmap = model.generate_content(f"Step-by-step roadmap for becoming a {role}")
        st.markdown(roadmap.text)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            pdf = canvas.Canvas(tmp.name)
            pdf.setFont("Helvetica", 12)
            pdf.drawString(100, 800, f"Career Roadmap: {role}")
            text_obj = pdf.beginText(50, 770)
            for line in roadmap.text.split('\n'):
                text_obj.textLine(line)
            pdf.drawText(text_obj)
            pdf.save()
            st.download_button("📥 Download Roadmap as PDF", tmp.name)

# ---------- 6. Job Trends ----------
elif nav == "Job Trends":
    st.title("📊 Job Trends & Market")
    loc = st.text_input("Location (optional):")
    if st.button("Find Jobs"):
        query = f"Latest career/job trends in {loc or 'India'} with salary info"
        res = model.generate_content(query)
        st.markdown(res.text)

# ---------- 7. Mock Interview ----------
elif nav == "Mock Interview":
    st.title("🎤 Mock Interview")
    target = st.text_input("Job Role:")
    if st.button("Generate Questions"):
        qn = model.generate_content(f"Top 5 interview questions with answers for {target}")
        st.markdown(qn.text)

# ---------- 8. FAQs ----------
elif nav == "Career FAQs":
    st.title("❓ Common Career Questions")
    faqs = [
        "which course is best after 12th science?",
        "Engineering vs medical-what to choose?",
        "Best course in engineering?",
        "Can I become Data Scientist without CS degree?",
        "What to do after B.Com?",
        "which course is trending in market ?",
        "skills required to get a software job?",
        "best govt exams after 12th??"
    ]
    for faq in faqs:
        if st.button(faq):
            st.markdown(model.generate_content(faq).text)


# ---------- 10. Translate Advice ----------
elif nav == "Translate Advice":
    st.title("🌐 Translate Career Advice")
    input_text = st.text_area("Enter career advice text to translate:")
    lang = st.selectbox("Choose language", ["hi", "ta", "te", "ml", "bn", "mr", "kn"])
    if st.button("Translate"):
        translated = translator.translate(input_text, dest=lang)
        st.success("✅ Translated Text:")
        st.write(translated.text)

# ---------- 11. Internship Ideas ----------
elif nav == "Internship Ideas":
    st.title("📍 Internship Finder")
    field = st.text_input("Field of interest:")
    if st.button("Suggest Internships"):
        prompt = f"Suggest internships for a student interested in {field}. Include companies and how to apply."
        st.markdown(model.generate_content(prompt).text)

# ---------- Footer ----------
st.markdown("---")
st.markdown("<center>🧠 Built with ❤️ using Streamlit + Gemini API | Designed for Indian Students 🇮🇳</center>", unsafe_allow_html=True)

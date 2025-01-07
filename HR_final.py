import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
import datetime
import io

# Helper functions
def extract_text_from_pdf(pdf_file):
    """Extract text content from a PDF file."""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def rank_resumes(job_description, resumes):
    """Rank resumes based on similarity to the job description."""
    if not resumes or not job_description:
        return None, "Please upload resumes and provide a job description first."
    
    texts = [job_description] + list(resumes.values())
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(texts)
    similarities = cosine_similarity(vectors[0:1], vectors[1:]).flatten()

    ranked = sorted(
        zip(resumes.keys(), similarities),
        key=lambda x: x[1],
        reverse=True
    )
    return ranked, None

# App state
if "resumes" not in st.session_state:
    st.session_state.resumes = {}
if "payroll_data" not in st.session_state:
    st.session_state.payroll_data = []
if "performance_data" not in st.session_state:
    st.session_state.performance_data = []

# Sidebar navigation
st.sidebar.title("HR Automation System")
options = st.sidebar.radio(
    "Choose an option",
    [
        "Home",
        "Rank Resumes",
        "Chatbot",
        "Interview Scheduling",
        "Payroll Management",
        "Performance Checking"
    ]
)

# Home Page
if options == "Home":
    st.title("Welcome to the HR Automation System!")
    st.write("Navigate through the options in the sidebar to explore different functionalities.")

# Rank Resumes
elif options == "Rank Resumes":
    st.title("Resume Management and Ranking")
    job_description = st.text_area("Job Description", placeholder="Enter the job description here...")
    uploaded_files = st.file_uploader("Upload Resumes (PDF Files)", accept_multiple_files=True, type=["pdf"])

    for file in uploaded_files:
        try:
            content = extract_text_from_pdf(file)
            st.session_state.resumes[file.name] = content
            st.success(f"Resume uploaded: {file.name}")
        except Exception as e:
            st.error(f"Error processing {file.name}: {e}")

    if st.button("Rank Resumes"):
        if not st.session_state.resumes:
            st.warning("Please upload resumes first.")
        elif not job_description:
            st.warning("Please enter a job description.")
        else:
            ranked_resumes, error = rank_resumes(job_description, st.session_state.resumes)
            if error:
                st.warning(error)
            else:
                st.subheader("Ranked Resumes")
                for i, (name, score) in enumerate(ranked_resumes, start=1):
                    st.write(f"{i}. **{name}** - Similarity Score: {score:.2f}")
    
    if st.button("View Uploaded Resumes"):
        st.subheader("Uploaded Resumes")
        for name, content in st.session_state.resumes.items():
            st.write(f"**{name}**: {content[:300]}...")

# Chatbot
elif options == "Chatbot":
    st.title("Chatbot")
    chatbot_responses = {
        "hello": "Hi there! How can I assist you today?",
        # New Q&A responses

        "what is the process for applying for parental leave?":
        "To apply for parental leave:\n\n- Visit the Parental Leave Application section in the HR portal.\n- Complete the form and attach any required documents, such as a medical certificate.\n- Submit the application at least [X weeks] in advance.\n\nNeed help? Contact HR Support.",
        
        "how do i request a letter of employment?": 
        "You can request a letter of employment by:\n\n- Logging into the HR portal.\n- Navigating to Requests > Letter of Employment.\n- Filling in the required details, such as the purpose of the letter.\n- The letter will be ready within [X business days].",
        
        "how do i resign from the company?": 
        "To resign:\n\n- Submit your resignation letter to your manager via email or the HR portal.\n- Ensure your notice period matches your contract requirements ([X weeks/months]).\n- For assistance, contact HR Support.",
        
        "what is the notice period policy?": 
        "The notice period is typically [X weeks/months]. Please refer to your employment agreement for specifics or contact HR for clarity.",
        
        "how do i access my final pay slip?": 
        "Your final pay slip will be available in the Payroll section of the HR portal after completing exit formalities. You will receive a notification once it’s ready.",
        
        "will i receive an experience letter?": 
        "Yes! An experience letter will be issued after you complete all exit formalities. Processing typically takes [X days].",
        
        "how do i request training for professional development?": 
        "Explore training options by:\n\n- Visiting the Learning and Development section in the HR portal.\n- Submitting a request for the desired program.\n\nNeed personalized recommendations? Contact the Learning Team.",
        
        "what is the performance appraisal process?": 
        "The performance appraisal includes:\n\n- **Self-Evaluation**: Submit your goals and progress.\n- **Manager Review**: Receive feedback and discuss growth opportunities.\n- **Goal Setting**: Plan objectives for the next cycle.\n\nCheck the HR portal for the appraisal timeline and guidelines.",
        
        "are there internal opportunities for promotions?": 
        "Yes! View internal openings in the Career Opportunities section of the HR portal. Apply directly to roles that align with your skills and goals.",
        
        "how do i set my career goals within the company?": 
        "Set your career goals by:\n\n- Scheduling a one-on-one meeting with your manager.\n- Using the Career Development Plan template in the HR portal.\n\nFor additional support, contact the Career Coach.",
        
        "who can guide me about career development?": 
        "For career guidance:\n\n- Reach out to the HR Learning and Development team.\n- Participate in mentorship programs (details available on the HR portal).",
        
        "can i request a meeting with my manager?": 
        "Yes! Schedule a meeting by:\n\n- Sending a request via your manager’s calendar.\n- Emailing your manager directly for urgent matters.",
        
        "what is the company’s code of conduct?": 
        "The Code of Conduct outlines ethical and professional standards. Access it in the Policies section of the HR portal. For queries, contact Compliance.",
        
        "what is the dress code policy?": 
        "The dress code is [formal/business casual/casual]. Detailed guidelines are available in the Employee Handbook on the HR portal.",
        
        "what is the policy on remote work?": 
        "The remote work policy allows eligible employees to work from home 2 days per week. Approval from your manager is required. View full details in the HR portal.",
        
        "how do i report workplace harassment?": 
        "Report workplace harassment via:\n\n- The Confidential Reporting Form in the HR portal.\n- Directly contacting the Compliance Officer.\n\nAll reports are handled with strict confidentiality.",
        
        "how do i escalate compliance concerns?": 
        "Escalate concerns by:\n\n- Submitting a report in the Compliance section of the HR portal.\n- For urgent issues, contact the Compliance Team."
    }
    user_query = st.text_input("Ask the Chatbot (e.g., 'Parental Leave', 'Resignation', 'Policies and Compliance')", key="chatbot_query")
    if user_query:
        response = chatbot_responses.get(user_query.lower(), "Sorry, I don't understand that. Please try asking differently or contact HR for support.")
        st.write("Chatbot:", response)

# Interview Scheduling
elif options == "Interview Scheduling":
    st.title("Interview Scheduling")
    with st.form("schedule_form"):
        candidate_name = st.text_input("Candidate Name")
        interview_date = st.date_input("Select Interview Date", min_value=datetime.date.today())
        interview_time = st.time_input("Select Interview Time")
        submit_schedule = st.form_submit_button("Schedule Interview")
        if submit_schedule:
            st.success(f"Interview scheduled for {candidate_name} on {interview_date} at {interview_time}.")

# Payroll Management
elif options == "Payroll Management":
    st.title("Payroll Management")
    with st.form("payroll_form"):
        employee_name = st.text_input("Employee Name")
        base_salary = st.number_input("Base Salary (in USD)", min_value=0)
        performance_bonus = st.number_input("Performance Bonus (in %)", min_value=0.0, max_value=100.0)
        submit_payroll = st.form_submit_button("Add Payroll")
        if submit_payroll:
            total_salary = base_salary + (base_salary * performance_bonus / 100)
            st.session_state.payroll_data.append({
                "Employee Name": employee_name,
                "Base Salary": base_salary,
                "Total Salary": total_salary
            })
            st.success(f"Payroll added for {employee_name}: Total Salary = ${total_salary:.2f}")
    if st.session_state.payroll_data:
        st.subheader("Payroll Records")
        st.dataframe(pd.DataFrame(st.session_state.payroll_data))
        if st.button("Export Payroll to CSV"):
            csv_data = pd.DataFrame(st.session_state.payroll_data).to_csv(index=False)
            st.download_button(
                "Download Payroll CSV",
                data=csv_data,
                file_name="payroll_data.csv",
                mime="text/csv"
            )

# Performance Checking
elif options == "Performance Checking":
    st.title("Performance Checking")
    with st.form("performance_form"):
        employee_name = st.text_input("Performance: Employee Name")
        performance_score = st.slider("Performance Score (1 to 10)", 1, 10)
        submit_performance = st.form_submit_button("Add Performance Score")
        if submit_performance:
            st.session_state.performance_data.append({
                "Employee Name": employee_name,
                "Performance Score": performance_score
            })
            st.success(f"Performance score added for {employee_name}: Score = {performance_score}")
    if st.session_state.performance_data:
        st.subheader("Performance Records")
        st.dataframe(pd.DataFrame(st.session_state.performance_data))
        if st.button("Export Performance Data to CSV"):
            csv_data = pd.DataFrame(st.session_state.performance_data).to_csv(index=False)
            st.download_button(
                "Download Performance CSV",
                data=csv_data,
                file_name="performance_data.csv",
                mime="text/csv"
            )

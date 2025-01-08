# HR-Automation-System

Overview
The HR Automation System is a Streamlit-based web application designed to streamline various HR processes, including resume ranking, chatbot assistance, interview scheduling, payroll management, and performance checking. This tool helps HR professionals manage tasks more efficiently by automating repetitive processes and providing a user-friendly interface.

**Features**

**Resume Management and Ranking:**

Upload multiple resumes in PDF format.

Enter a job description to rank resumes based on their similarity to the job description using TF-IDF and cosine similarity.

View ranked resumes and their similarity scores.

**Chatbot:**

A simple chatbot that provides answers to common HR-related queries.

Predefined responses for questions related to leave policies, employment letters, resignations, and more.

Interview Scheduling:

Schedule interviews by entering candidate details, interview date, and time.

View and manage scheduled interviews in a tabular format.

**Payroll Management:**

Add employee payroll details, including base salary and performance bonus.

View payroll records and visualize total salaries using bar plots.

Export payroll data to a CSV file.

**Performance Checking:**

Add and manage employee performance scores.

Visualize performance trends using line plots.

Export performance data to a CSV file.

Installation
Clone the repository:


git clone https://github.com/NoorUnNisaSoomro//HR-Automation-System.git
cd HR-Automation-System

Set up a virtual environment (optional but recommended):
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

**Install the required dependencies:**

pip install -r requirements.txt
Run the application:

streamlit run Hr_automation_updated.py
Access the application:
Open your web browser and go to http://localhost:8501 to use the HR Automation System.

Usage
Home:

The home page provides an overview of the system and navigation instructions.

Rank Resumes:

Upload resumes and enter a job description to rank the resumes based on their relevance.

Chatbot:

Ask the chatbot common HR-related questions and receive predefined responses.

Interview Scheduling:

Schedule interviews by providing candidate details, interview date, and time.

Payroll Management:

Add and manage employee payroll details. Visualize and export payroll data.

Performance Checking:

Add and manage employee performance scores. Visualize and export performance data.

**Dependencies**

Streamlit: For building and running the web application.

Pandas: For data manipulation and handling.

Scikit-learn: For text processing and similarity calculations.

PyPDF2: For extracting text from PDF files.

Matplotlib and Seaborn: For data visualization.

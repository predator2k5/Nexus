__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from crewai import Agent
from crewai import LLM
import litellm
import openai
import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv
from crewai_tools import FileReadTool, FileWriterTool
import streamlit as st

load_dotenv()

# Title
st.set_page_config(page_title="Job Description Generator", layout="wide")

# Title and description
st.title("Job Description Generator")

# Sidebar
with st.sidebar:
    st.header("Content Settings")
    job_title=st.text_input("Job Title")
    key_responsibility=st.text_area("Key Responsibility")
    required_skills=st.text_area("Required Skills")
    experience=st.text_input("Experience")
    location=st.text_input("Location")
    salary=st.text_input("Salary")
    company_name=st.text_input("Company Name")
    st.markdown("-----")

    generate_button = st.button("Generate Content", type="primary", use_container_width=True)

def generate_content(job_title,key_responsiblity,required_skills,experience,location,salary,company_name):

        # Create a senior blog content researcher
        hr_manager = Agent(
            role='Senior HR Manager',
            goal='Generate job descriptions for new positions',
            description='Generate industry-accepted, official, and well-structured job descriptions based on provided details',
            verbose=True,
            memory=True,
            backstory=(
            "You are an expert in creating job descriptions that are professional, well-structured, and adhere to industry standards. "
            "Generate a job description using the provided details: {job_title}, {key_responsibility}, {required_skills}, {experience}, {location}, and {salary},{company_name}. "
            "Ensure the job description is clear, concise, and appealing to potential candidates."
            "It should be very detailed and lengthy"
            ),
            allow_delegation=True,
        )

        # Create a reporting analyst agent
        hr_writer = Agent(
            role='Senior HR Writer',
            goal='Generate the job description content based on provided details',
            description='Generate well-structured and professional job descriptions for new positions',
            verbose=True,
            memory=True,
            backstory=(
            "You are an expert in writing job descriptions that are clear, concise, and appealing to potential candidates. "
            "Ensure the job description includes all necessary details such as job title, key responsibilities, required skills, experience, location, and salary. "
            "The content should adhere to industry standards and be formatted professionally."
            "It should be very detailed and lengthy"
            ),
            allow_delegation=True,
            tools=[FileWriterTool()]
        )

        research_task = Task(
            description=(
            "Generate a detailed and accurate job description for the new position. "
            "Ensure that all provided details such as {job_title}, {key_responsibility}, {required_skills}, {experience}, {location}, and {salary},{company_name} are included. "
            "The job description should be professional, clear, concise, and appealing to potential candidates. "
            "It should adhere to industry standards and be well-structured."
            ),
            expected_output='A professionally written job description with all the provided details accurately included and well structured.',
            agent=hr_manager,
        )

        reporting_task = Task(
            description=(
            "Write a detailed and professional job description based on the provided details. "
            "Ensure the description is well-structured, error-free, and adheres to industry standards. "
            "Include all necessary information such as {job_title}, {key_responsibility}, {required_skills}, {experience}, {location}, and {salary},{company_name}."
            ),
            expected_output='A professionally written job description with all the provided details accurately included and well structured.',
            agent=hr_writer,
        )

        # Crew
        crew = Crew(
            agents=[hr_manager, hr_writer],
            tasks=[research_task, reporting_task],
            process=Process.sequential,
            verbose=True,
        )

        # Convert joining_date to string
        # joining_date_str = joining_date.strftime('%Y-%m-%d')

        return crew.kickoff(inputs={
            "job_title":job_title,
            "key_responsibility":key_responsibility,
            "required_skills":required_skills,
            "experience":experience,
            "location":location,
            "salary":salary,
            "company_name":company_name
        })

# def generate_pdf(content):
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)
#     for line in content.split('\n'):
#         pdf.cell(200, 10, txt=line, ln=True)
#     return pdf.output(dest='S').encode('latin1')

# Main content area
if generate_button:
    with st.spinner("Generating Content...This may take a moment.."):
        try:
            result = generate_content(job_title, key_responsibility, required_skills, experience, location, salary,company_name)
            if result:
                st.markdown("### Generated Content")
                st.markdown(result)

                # Add download button for text
                st.download_button(
                    label="Download Content",
                    data=result.raw,
                    file_name=f"offer_letter.txt",
                    mime="text/plain"
                )
                # Generate PDF and add download button for PDF
                # pdf_data = generate_pdf(result.raw)
                # st.download_button(
                #     label="Download PDF",
                #     data=pdf_data,
                #     file_name=f"offer_letter.pdf",
                #     mime="application/pdf"
                # )
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Footer
st.markdown("----")
st.markdown("Built by AritraM")

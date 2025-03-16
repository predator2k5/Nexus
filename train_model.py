import pandas as pd
import numpy as np
from resume_analyzer import ResumeAnalyzer
import json
import os

def load_sample_data():
    """
    Load sample resume data for training
    In a real implementation, this would load from a database or files
    """
    # Sample resume texts
    resumes = [
        """
        John Doe
        john.doe@example.com
        (123) 456-7890
        
        Summary
        Experienced software engineer with 5+ years of experience in full-stack development.
        
        Skills
        Python, JavaScript, React, Node.js, SQL, AWS, Docker, Git
        
        Experience
        Senior Software Engineer, Tech Company
        2020 - Present
        • Developed a new feature that increased user engagement by 25%
        • Led a team of 5 developers to rebuild the company's main application
        • Reduced server costs by 30% through optimization
        
        Software Engineer, Another Tech Company
        2018 - 2020
        • Built RESTful APIs using Node.js and Express
        • Implemented CI/CD pipeline reducing deployment time by 50%
        
        Education
        Bachelor of Science in Computer Science
        University of Technology, 2018
        """,
        
        """
        Jane Smith
        jane.smith@example.com
        (987) 654-3210
        
        Summary
        Data Scientist with expertise in machine learning and statistical analysis.
        
        Skills
        Python, R, SQL, Machine Learning, TensorFlow, PyTorch, Data Visualization
        
        Experience
        Senior Data Scientist, Data Company
        2019 - Present
        • Built predictive models that improved forecast accuracy by 40%
        • Led a team of 3 data scientists on a major client project
        • Developed data pipelines processing 500GB of data daily
        
        Data Analyst, Analytics Firm
        2017 - 2019
        • Performed statistical analysis on customer data
        • Created dashboards using Tableau
        
        Education
        Master of Science in Data Science
        University of Data, 2017
        Bachelor of Science in Statistics
        University of Math, 2015
        """,
        
        """
        Bob Johnson
        bob.johnson@example.com
        (555) 123-4567
        
        Summary
        UX/UI Designer with a passion for creating intuitive user experiences.
        
        Skills
        Figma, Sketch, Adobe XD, HTML, CSS, JavaScript, User Research, Prototyping
        
        Experience
        Senior UX Designer, Design Agency
        2018 - Present
        • Redesigned the main product interface increasing user satisfaction by 35%
        • Conducted user research with over 100 participants
        • Created design systems used across multiple products
        
        UI Designer, Tech Startup
        2016 - 2018
        • Designed mobile app interfaces
        • Collaborated with developers to implement designs
        
        Education
        Bachelor of Fine Arts in Graphic Design
        Design University, 2016
        """
    ]
    
    # Sample labels (job categories)
    labels = ["Software Engineer", "Data Scientist", "UX Designer"]
    
    return resumes, labels

def main():
    # Create the ResumeAnalyzer instance
    analyzer = ResumeAnalyzer()
    
    # Load sample data
    resumes, labels = load_sample_data()
    
    print("Training model on sample data...")
    
    # Train the model
    training_results = analyzer.train_model(resumes, labels)
    
    print(f"Model trained with accuracy: {training_results['accuracy']:.2f}")
    print("Classification Report:")
    print(training_results["report"])
    
    # Save the trained model
    model_path = "resume_analyzer_model.pkl"
    analyzer.save_model(model_path)
    print(f"Model saved to {model_path}")
    
    # Test the model on a new resume
    test_resume = """
    Alex Wilson
    alex.wilson@example.com
    (111) 222-3333
    
    Summary
    Full Stack Developer with 3 years of experience building web applications.
    
    Skills
    JavaScript, React, Node.js, Express, MongoDB, HTML, CSS, Git
    
    Experience
    Full Stack Developer, Web Company
    2019 - Present
    • Developed and maintained multiple web applications
    • Implemented new features based on user feedback
    • Optimized database queries improving performance by 20%
    
    Junior Developer, Small Startup
    2018 - 2019
    • Assisted in building the company website
    • Fixed bugs and implemented minor features
    
    Education
    Bachelor of Science in Computer Science
    Tech University, 2018
    """
    
    # Analyze the test resume
    analysis = analyzer.analyze_resume(test_resume)
    
    print("\nTest Resume Analysis:")
    print(json.dumps(analysis, indent=2))

if __name__ == "__main__":
    main()


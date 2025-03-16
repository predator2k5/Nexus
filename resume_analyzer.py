import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pickle
import json

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

class ResumeAnalyzer:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.vectorizer = TfidfVectorizer(max_features=5000)
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.skills_keywords = self._load_skills_keywords()
        self.job_titles = self._load_job_titles()
        
    def _load_skills_keywords(self):
        # In a real implementation, this would load from a comprehensive database
        return {
            "technical": [
                "python", "javascript", "react", "node.js", "typescript", "html", "css", 
                "java", "c++", "c#", "sql", "nosql", "mongodb", "postgresql", "mysql",
                "aws", "azure", "gcp", "docker", "kubernetes", "ci/cd", "git", "github",
                "machine learning", "deep learning", "ai", "data science", "data analysis",
                "tensorflow", "pytorch", "keras", "scikit-learn", "pandas", "numpy"
            ],
            "soft": [
                "communication", "teamwork", "leadership", "problem solving", "critical thinking",
                "time management", "adaptability", "creativity", "collaboration", "presentation",
                "negotiation", "conflict resolution", "decision making", "emotional intelligence"
            ],
            "business": [
                "project management", "agile", "scrum", "kanban", "product management",
                "business analysis", "requirements gathering", "stakeholder management",
                "strategic planning", "market research", "competitive analysis", "budgeting",
                "forecasting", "risk management", "quality assurance", "user experience"
            ]
        }
    
    def _load_job_titles(self):
        # In a real implementation, this would load from a comprehensive database
        return [
            "software engineer", "data scientist", "web developer", "frontend developer",
            "backend developer", "full stack developer", "devops engineer", "cloud engineer",
            "machine learning engineer", "ai researcher", "product manager", "project manager",
            "ux designer", "ui designer", "data analyst", "business analyst", "qa engineer",
            "systems administrator", "network engineer", "security engineer", "database administrator"
        ]
    
    def preprocess_text(self, text):
        # Convert to lowercase
        text = text.lower()
        # Remove special characters and numbers
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        # Tokenize
        tokens = nltk.word_tokenize(text)
        # Remove stopwords
        tokens = [word for word in tokens if word not in self.stop_words]
        # Join tokens back to string
        return ' '.join(tokens)
    
    def extract_skills(self, text):
        text = text.lower()
        found_skills = {
            "technical": [],
            "soft": [],
            "business": []
        }
        
        for category, skills in self.skills_keywords.items():
            for skill in skills:
                if re.search(r'\b' + re.escape(skill) + r'\b', text):
                    found_skills[category].append(skill)
        
        return found_skills
    
    def extract_education(self, text):
        education_keywords = ["bachelor", "master", "phd", "degree", "university", "college", "school"]
        education_pattern = r'(?i)(?:' + '|'.join(education_keywords) + r')[^.]*\.'
        education_matches = re.findall(education_pattern, text)
        return education_matches
    
    def extract_experience(self, text):
        experience_keywords = ["experience", "work", "job", "position", "role"]
        experience_pattern = r'(?i)(?:' + '|'.join(experience_keywords) + r')[^.]*\.'
        experience_matches = re.findall(experience_pattern, text)
        return experience_matches
    
    def calculate_ats_score(self, resume_text, job_description=None):
        # Basic ATS compatibility score
        ats_score = 0
        
        # Check for contact information
        if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', resume_text):
            ats_score += 10  # Email found
        
        if re.search(r'\b(?:\+\d{1,3}[-.\s]?)?$$?\d{3}$$?[-.\s]?\d{3}[-.\s]?\d{4}\b', resume_text):
            ats_score += 10  # Phone number found
        
        # Check for section headings
        section_headings = ["education", "experience", "skills", "projects", "summary", "objective"]
        for heading in section_headings:
            if re.search(r'\b' + heading + r'\b', resume_text.lower()):
                ats_score += 5
        
        # Check for skills
        skills = self.extract_skills(resume_text)
        total_skills = sum(len(skills_list) for skills_list in skills.values())
        if total_skills > 15:
            ats_score += 20
        elif total_skills > 10:
            ats_score += 15
        elif total_skills > 5:
            ats_score += 10
        else:
            ats_score += 5
        
        # Check for job title match if job description is provided
        if job_description:
            for title in self.job_titles:
                if re.search(r'\b' + re.escape(title) + r'\b', resume_text.lower()) and \
                   re.search(r'\b' + re.escape(title) + r'\b', job_description.lower()):
                    ats_score += 15
                    break
        
        # Normalize score to 0-100
        ats_score = min(ats_score, 100)
        
        return ats_score
    
    def calculate_content_quality_score(self, resume_text):
        # Basic content quality score
        quality_score = 0
        
        # Check for action verbs
        action_verbs = ["achieved", "improved", "developed", "created", "implemented", "managed", 
                        "led", "designed", "built", "launched", "increased", "decreased", "reduced"]
        action_verb_count = sum(1 for verb in action_verbs if re.search(r'\b' + re.escape(verb) + r'\b', resume_text.lower()))
        
        if action_verb_count > 10:
            quality_score += 25
        elif action_verb_count > 5:
            quality_score += 15
        else:
            quality_score += 5
        
        # Check for quantifiable achievements
        quantifiable_pattern = r'\b\d+%|\b\d+ percent|\$\d+|\d+ dollars|\d+ users|\d+ customers|\d+ projects|\d+ team'
        quantifiable_count = len(re.findall(quantifiable_pattern, resume_text.lower()))
        
        if quantifiable_count > 5:
            quality_score += 25
        elif quantifiable_count > 2:
            quality_score += 15
        else:
            quality_score += 5
        
        # Check for education details
        education = self.extract_education(resume_text)
        if len(education) > 0:
            quality_score += 15
        
        # Check for experience details
        experience = self.extract_experience(resume_text)
        if len(experience) > 3:
            quality_score += 25
        elif len(experience) > 1:
            quality_score += 15
        else:
            quality_score += 5
        
        # Normalize score to 0-100
        quality_score = min(quality_score, 100)
        
        return quality_score
    
    def calculate_format_score(self, resume_text):
        # Basic format score
        format_score = 0
        
        # Check for section headings
        section_headings = ["education", "experience", "skills", "projects", "summary", "objective"]
        section_count = sum(1 for heading in section_headings if re.search(r'\b' + re.escape(heading) + r'\b', resume_text.lower()))
        
        if section_count >= 4:
            format_score += 30
        elif section_count >= 2:
            format_score += 15
        else:
            format_score += 5
        
        # Check for bullet points
        bullet_pattern = r'•|\*|-|\d+\.'
        bullet_count = len(re.findall(bullet_pattern, resume_text))
        
        if bullet_count > 10:
            format_score += 30
        elif bullet_count > 5:
            format_score += 15
        else:
            format_score += 5
        
        # Check for consistent formatting
        paragraphs = resume_text.split('\n\n')
        if len(paragraphs) > 5:
            format_score += 20
        elif len(paragraphs) > 3:
            format_score += 10
        else:
            format_score += 5
        
        # Check for appropriate length
        word_count = len(resume_text.split())
        if 300 <= word_count <= 700:
            format_score += 20
        elif word_count < 300:
            format_score += 10
        else:
            format_score += 5
        
        # Normalize score to 0-100
        format_score = min(format_score, 100)
        
        return format_score
    
    def calculate_skills_match_score(self, resume_text, job_description=None):
        # Extract skills from resume
        resume_skills = self.extract_skills(resume_text)
        total_resume_skills = sum(len(skills_list) for skills_list in resume_skills.values())
        
        if job_description:
            # Extract skills from job description
            job_skills = self.extract_skills(job_description)
            total_job_skills = sum(len(skills_list) for skills_list in job_skills.values())
            
            # Count matching skills
            matching_skills = 0
            for category in resume_skills:
                for skill in resume_skills[category]:
                    if skill in job_skills[category]:
                        matching_skills += 1
            
            # Calculate match percentage
            if total_job_skills > 0:
                match_percentage = (matching_skills / total_job_skills) * 100
            else:
                match_percentage = 0
            
            # Normalize score to 0-100
            skills_score = min(match_percentage, 100)
        else:
            # Without job description, base score on number of skills
            if total_resume_skills > 15:
                skills_score = 90
            elif total_resume_skills > 10:
                skills_score = 75
            elif total_resume_skills > 5:
                skills_score = 60
            else:
                skills_score = 40
        
        return skills_score
    
    def analyze_resume(self, resume_text, job_description=None):
        # Calculate individual scores
        ats_score = self.calculate_ats_score(resume_text, job_description)
        content_score = self.calculate_content_quality_score(resume_text)
        format_score = self.calculate_format_score(resume_text)
        skills_score = self.calculate_skills_match_score(resume_text, job_description)
        
        # Calculate overall score (weighted average)
        overall_score = int((ats_score * 0.3) + (content_score * 0.3) + (format_score * 0.2) + (skills_score * 0.2))
        
        # Generate feedback
        ats_feedback = self._generate_ats_feedback(ats_score)
        content_feedback = self._generate_content_feedback(content_score)
        format_feedback = self._generate_format_feedback(format_score)
        skills_feedback = self._generate_skills_feedback(skills_score)
        
        # Generate suggestions
        suggestions = self._generate_suggestions(resume_text, ats_score, content_score, format_score, skills_score)
        
        # Extract skills
        skills = self.extract_skills(resume_text)
        
        # Return analysis results
        return {
            "score": overall_score,
            "atsCompatibility": {
                "score": int(ats_score),
                "feedback": ats_feedback
            },
            "contentQuality": {
                "score": int(content_score),
                "feedback": content_feedback
            },
            "formatStructure": {
                "score": int(format_score),
                "feedback": format_feedback
            },
            "skillsMatch": {
                "score": int(skills_score),
                "feedback": skills_feedback
            },
            "suggestions": suggestions,
            "skills": skills
        }
    
    def _generate_ats_feedback(self, score):
        if score >= 80:
            return "Your resume is highly compatible with ATS systems. It contains all the necessary elements for successful parsing."
        elif score >= 60:
            return "Your resume is compatible with most ATS systems, but there's room for improvement in certain areas."
        else:
            return "Your resume may have difficulty passing through ATS systems. Consider restructuring with standard section headings and formats."
    
    def _generate_content_feedback(self, score):
        if score >= 80:
            return "Your content is strong with good use of action verbs and quantifiable achievements."
        elif score >= 60:
            return "Your content is good but could benefit from more action verbs and quantifiable results."
        else:
            return "Your content needs improvement. Focus on using action verbs and quantifying your achievements."
    
    def _generate_format_feedback(self, score):
        if score >= 80:
            return "Your resume has excellent formatting with clear sections and good use of white space."
        elif score >= 60:
            return "Your resume format is good but could be improved with more consistent section headings and bullet points."
        else:
            return "Your resume format needs improvement. Consider using standard section headings and bullet points for better readability."
    
    def _generate_skills_feedback(self, score):
        if score >= 80:
            return "Your skills align well with industry standards and job requirements."
        elif score >= 60:
            return "Your skills are good but could be expanded to better match job requirements."
        else:
            return "Consider adding more relevant skills to your resume to better match job requirements."
    
    def _generate_suggestions(self, resume_text, ats_score, content_score, format_score, skills_score):
        suggestions = []
        
        # ATS suggestions
        if ats_score < 80:
            if not re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', resume_text):
                suggestions.append("Add your email address to improve contact information.")
            
            if not re.search(r'\b(?:\+\d{1,3}[-.\s]?)?$$?\d{3}$$?[-.\s]?\d{3}[-.\s]?\d{4}\b', resume_text):
                suggestions.append("Add your phone number to improve contact information.")
            
            section_headings = ["education", "experience", "skills", "projects"]
            missing_sections = [heading for heading in section_headings if not re.search(r'\b' + re.escape(heading) + r'\b', resume_text.lower())]
            if missing_sections:
                suggestions.append(f"Add standard section headings for: {', '.join(missing_sections)}.")
        
        # Content suggestions
        if content_score < 80:
            action_verbs = ["achieved", "improved", "developed", "created", "implemented", "managed", "led"]
            action_verb_count = sum(1 for verb in action_verbs if re.search(r'\b' + re.escape(verb) + r'\b', resume_text.lower()))
            if action_verb_count < 5:
                suggestions.append("Use more action verbs like 'achieved', 'improved', 'developed', etc.")
            
            quantifiable_pattern = r'\b\d+%|\b\d+ percent|\$\d+|\d+ dollars|\d+ users|\d+ customers|\d+ projects|\d+ team'
            quantifiable_count = len(re.findall(quantifiable_pattern, resume_text.lower()))
            if quantifiable_count < 3:
                suggestions.append("Add metrics to your achievements (e.g., 'Increased sales by 20%' instead of 'Increased sales').")
        
        # Format suggestions
        if format_score < 80:
            bullet_pattern = r'•|\*|-|\d+\.'
            bullet_count = len(re.findall(bullet_pattern, resume_text))
            if bullet_count < 5:
                suggestions.append("Use bullet points to highlight your achievements and responsibilities.")
            
            paragraphs = resume_text.split('\n\n')
            if len(paragraphs) < 4:
                suggestions.append("Improve the structure of your resume with clear section breaks.")
            
            word_count = len(resume_text.split())
            if word_count > 700:
                suggestions.append("Your resume is too long. Consider shortening it to 1-2 pages for better readability.")
            elif word_count < 300:
                suggestions.append("Your resume may be too short. Consider adding more details about your experience and skills.")
        
        # Skills suggestions
        if skills_score < 80:
            skills = self.extract_skills(resume_text)
            total_skills = sum(len(skills_list) for skills_list in skills.values())
            if total_skills < 10:
                suggestions.append("Add more relevant skills to your resume, especially technical and industry-specific ones.")
            
            if len(skills["soft"]) < 3:
                suggestions.append("Include more soft skills like communication, teamwork, and problem-solving.")
        
        # General suggestions
        suggestions.append("Tailor your resume for each job application by matching keywords from the job description.")
        suggestions.append("Keep your resume format consistent with the same font, bullet style, and heading format throughout.")
        
        return suggestions[:7]  # Limit to 7 suggestions
    
    def train_model(self, resumes_data, labels):
        """
        Train the model on resume data
        
        Parameters:
        resumes_data (list): List of resume texts
        labels (list): List of corresponding labels (e.g., job categories)
        """
        # Preprocess the resume texts
        processed_resumes = [self.preprocess_text(resume) for resume in resumes_data]
        
        # Create feature vectors
        X = self.vectorizer.fit_transform(processed_resumes)
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.2, random_state=42)
        
        # Train the model
        self.model.fit(X_train, y_train)
        
        # Evaluate the model
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred)
        
        return {
            "accuracy": accuracy,
            "report": report
        }
    
    def save_model(self, filepath):
        """Save the trained model to a file"""
        model_data = {
            "vectorizer": self.vectorizer,
            "model": self.model
        }
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
    
    def load_model(self, filepath):
        """Load a trained model from a file"""
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)
        
        self.vectorizer = model_data["vectorizer"]
        self.model = model_data["model"]

# Example usage
if __name__ == "__main__":
    analyzer = ResumeAnalyzer()
    
    # Example resume text
    resume_text = """
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
    """
    
    # Example job description
    job_description = """
    We are looking for a Senior Software Engineer with experience in Python and React.
    Responsibilities:
    • Develop and maintain web applications
    • Work with cross-functional teams
    • Optimize application performance
    
    Requirements:
    • 3+ years of experience with Python
    • Experience with React and JavaScript
    • Knowledge of AWS services
    • Experience with CI/CD pipelines
    """
    
    # Analyze the resume
    analysis = analyzer.analyze_resume(resume_text, job_description)
    
    # Print the analysis results
    print(json.dumps(analysis, indent=2))


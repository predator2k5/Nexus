// This is a simplified mock of a resume parser service
// In a real application, you would use a more sophisticated parser or AI service

export interface ParsedResume {
  personalInfo: {
    name: string
    email: string
    phone: string
    location: string
  }
  skills: string[]
  experience: {
    company: string
    title: string
    startDate: string
    endDate: string
    description: string[]
  }[]
  education: {
    institution: string
    degree: string
    field: string
    graduationDate: string
  }[]
}

export async function parseResume(file: File): Promise<ParsedResume> {
  // In a real application, this would send the file to a backend service
  // For this demo, we'll return mock data

  // Simulate API call delay
  await new Promise((resolve) => setTimeout(resolve, 2000))

  return {
    personalInfo: {
      name: "John Doe",
      email: "john.doe@example.com",
      phone: "(123) 456-7890",
      location: "New York, NY",
    },
    skills: [
      "JavaScript",
      "React",
      "Node.js",
      "TypeScript",
      "HTML",
      "CSS",
      "Git",
      "Agile",
      "Project Management",
      "UI/UX Design",
    ],
    experience: [
      {
        company: "Tech Solutions Inc.",
        title: "Senior Frontend Developer",
        startDate: "Jan 2020",
        endDate: "Present",
        description: [
          "Led a team of 5 developers to build a responsive web application",
          "Improved site performance by 40% through code optimization",
          "Implemented CI/CD pipeline reducing deployment time by 60%",
        ],
      },
      {
        company: "Digital Innovations",
        title: "Frontend Developer",
        startDate: "Mar 2017",
        endDate: "Dec 2019",
        description: [
          "Developed and maintained client websites using React and TypeScript",
          "Collaborated with designers to implement UI/UX improvements",
          "Participated in code reviews and mentored junior developers",
        ],
      },
    ],
    education: [
      {
        institution: "University of Technology",
        degree: "Bachelor of Science",
        field: "Computer Science",
        graduationDate: "May 2017",
      },
    ],
  }
}

export function analyzeResumeATS(parsedResume: ParsedResume): {
  score: number
  feedback: { category: string; score: number; feedback: string }[]
} {
  // In a real application, this would use AI to analyze the resume
  // For this demo, we'll return mock analysis

  return {
    score: 78,
    feedback: [
      {
        category: "ATS Compatibility",
        score: 85,
        feedback:
          "Your resume is compatible with most ATS systems. Consider using more industry-standard section headings.",
      },
      {
        category: "Skills Match",
        score: 70,
        feedback:
          "Your technical skills are good, but consider adding more domain-specific skills relevant to your target roles.",
      },
      {
        category: "Format & Structure",
        score: 90,
        feedback:
          "Clean structure with good use of headings and bullet points. Consider adding a summary section at the top.",
      },
      {
        category: "Content Quality",
        score: 65,
        feedback:
          "Use more action verbs and quantify your achievements. Focus on outcomes rather than responsibilities.",
      },
    ],
  }
}

export function generateResumeSuggestions(parsedResume: ParsedResume): string[] {
  // In a real application, this would use AI to generate suggestions
  // For this demo, we'll return mock suggestions

  return [
    "Add metrics to your achievements (e.g., 'Increased sales by 20%' instead of 'Increased sales')",
    "Include keywords from job descriptions like 'data analysis' and 'project management'",
    "Remove outdated skills and focus on current technologies",
    "Shorten your resume to 1-2 pages for better readability",
    "Add a professional summary at the top to highlight your key qualifications",
    "Use bullet points consistently throughout your experience section",
    "Ensure your contact information is prominently displayed and up-to-date",
  ]
}


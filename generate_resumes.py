"""
Generate 1000 sample resume data entries for the chatbot AI system.
"""
import json
import random
from datetime import datetime, timedelta

# Sample data pools
first_names = ["John", "Jane", "Michael", "Sarah", "David", "Emily", "Robert", "Lisa", 
               "James", "Mary", "William", "Patricia", "Richard", "Jennifer", "Thomas",
               "Linda", "Charles", "Elizabeth", "Daniel", "Barbara", "Matthew", "Susan",
               "Anthony", "Jessica", "Mark", "Nancy", "Donald", "Karen", "Steven", "Betty"]

last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
              "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
              "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Thompson", "White",
              "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker"]

job_titles = [
    "Software Engineer", "Data Scientist", "Product Manager", "UX Designer", "DevOps Engineer",
    "Backend Developer", "Frontend Developer", "Full Stack Developer", "Machine Learning Engineer",
    "Business Analyst", "Project Manager", "Marketing Manager", "Sales Representative",
    "Accountant", "Financial Analyst", "HR Manager", "Operations Manager", "Customer Success Manager",
    "Quality Assurance Engineer", "Systems Administrator", "Database Administrator",
    "Network Engineer", "Security Analyst", "Cloud Architect", "Mobile Developer",
    "Technical Writer", "Scrum Master", "Data Engineer", "AI Researcher", "Solutions Architect"
]

companies = [
    "Google", "Microsoft", "Amazon", "Apple", "Meta", "Netflix", "Tesla", "IBM", "Oracle",
    "Salesforce", "Adobe", "Intel", "Cisco", "Dell", "HP", "SAP", "VMware", "Uber", "Airbnb",
    "Twitter", "LinkedIn", "Spotify", "Dropbox", "Slack", "Zoom", "ServiceNow", "Workday",
    "Square", "PayPal", "eBay", "Shopify", "Atlassian", "DocuSign", "Twilio", "Stripe"
]

skills = [
    "Python", "Java", "JavaScript", "C++", "C#", "Ruby", "Go", "Swift", "Kotlin", "TypeScript",
    "React", "Angular", "Vue.js", "Node.js", "Django", "Flask", "Spring Boot", "ASP.NET",
    "SQL", "NoSQL", "MongoDB", "PostgreSQL", "MySQL", "Redis", "Elasticsearch",
    "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Jenkins", "Git", "CI/CD",
    "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Scikit-learn",
    "Data Analysis", "Statistics", "Excel", "Tableau", "Power BI", "Agile", "Scrum",
    "REST API", "GraphQL", "Microservices", "System Design", "Algorithm Design"
]

education_degrees = ["Bachelor of Science", "Master of Science", "Bachelor of Arts", "Master of Arts", "PhD", "MBA"]
education_fields = ["Computer Science", "Software Engineering", "Data Science", "Information Technology",
                   "Business Administration", "Engineering", "Mathematics", "Statistics", "Economics"]
universities = ["MIT", "Stanford", "Harvard", "UC Berkeley", "Carnegie Mellon", "Georgia Tech",
               "University of Washington", "University of Texas", "University of Michigan",
               "Cornell University", "Columbia University", "Princeton", "Yale", "Caltech"]

locations = ["San Francisco, CA", "New York, NY", "Seattle, WA", "Austin, TX", "Boston, MA",
            "Los Angeles, CA", "Chicago, IL", "Denver, CO", "Atlanta, GA", "Portland, OR",
            "San Diego, CA", "Phoenix, AZ", "Dallas, TX", "Miami, FL", "Washington, DC"]

def generate_resume(resume_id):
    """Generate a single resume entry."""
    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    email = f"{name.lower().replace(' ', '.')}{random.randint(1, 999)}@email.com"
    phone = f"+1-{random.randint(200, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
    
    # Generate work experience (1-4 jobs)
    num_jobs = random.randint(1, 4)
    experience = []
    current_year = datetime.now().year
    
    for i in range(num_jobs):
        years_ago = i * random.randint(2, 4)
        start_year = current_year - years_ago - random.randint(2, 4)
        end_year = current_year - years_ago if i > 0 else "Present"
        
        job = {
            "title": random.choice(job_titles),
            "company": random.choice(companies),
            "location": random.choice(locations),
            "start_date": f"{random.choice(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])} {start_year}",
            "end_date": f"{random.choice(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])} {end_year}" if end_year != "Present" else "Present",
            "responsibilities": [
                f"Led development of key features using {random.choice(skills)}",
                f"Collaborated with cross-functional teams to deliver projects",
                f"Improved system performance by {random.randint(10, 80)}%"
            ]
        }
        experience.append(job)
    
    # Generate education (1-2 degrees)
    num_degrees = random.randint(1, 2)
    education = []
    
    for i in range(num_degrees):
        degree = {
            "degree": random.choice(education_degrees),
            "field": random.choice(education_fields),
            "university": random.choice(universities),
            "graduation_year": random.randint(2005, 2023)
        }
        education.append(degree)
    
    # Generate skills (5-15 skills)
    num_skills = random.randint(5, 15)
    candidate_skills = random.sample(skills, num_skills)
    
    # Calculate years of experience
    years_experience = sum([random.randint(2, 5) for _ in range(num_jobs)])
    
    resume = {
        "id": resume_id,
        "name": name,
        "email": email,
        "phone": phone,
        "location": random.choice(locations),
        "summary": f"Experienced {random.choice(job_titles)} with {years_experience}+ years of experience in software development and technology.",
        "years_experience": years_experience,
        "current_title": experience[0]["title"] if experience else random.choice(job_titles),
        "skills": candidate_skills,
        "experience": experience,
        "education": education,
        "certifications": random.sample(["AWS Certified", "PMP", "Scrum Master", "Google Cloud Certified"], random.randint(0, 2)),
        "languages": random.sample(["English", "Spanish", "Mandarin", "French", "German"], random.randint(1, 2))
    }
    
    return resume

def main():
    """Generate 1000 resume entries and save to JSON file."""
    print("Generating 1000 resume entries...")
    resumes = []
    
    for i in range(1, 1001):
        resume = generate_resume(i)
        resumes.append(resume)
        
        if i % 100 == 0:
            print(f"Generated {i} resumes...")
    
    # Save to JSON file
    with open('resumes_data.json', 'w') as f:
        json.dump(resumes, f, indent=2)
    
    print(f"Successfully generated {len(resumes)} resumes!")
    print(f"Data saved to resumes_data.json")
    
    # Print some statistics
    all_skills = []
    all_titles = []
    for resume in resumes:
        all_skills.extend(resume['skills'])
        all_titles.append(resume['current_title'])
    
    print(f"\nStatistics:")
    print(f"Total resumes: {len(resumes)}")
    print(f"Unique job titles: {len(set(all_titles))}")
    print(f"Average skills per resume: {len(all_skills) / len(resumes):.1f}")

if __name__ == "__main__":
    main()

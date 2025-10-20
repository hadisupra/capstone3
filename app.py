"""
Chatbot AI for Resume Search and Analysis
A simple AI chatbot that can search and analyze resume data.
"""
import json
import re
from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Load resume data
with open('resumes_data.json', 'r') as f:
    RESUMES = json.load(f)

class ResumeChatbot:
    """Chatbot for resume search and queries."""
    
    def __init__(self, resumes):
        self.resumes = resumes
        
    def search_by_skill(self, skill):
        """Search resumes by skill."""
        results = []
        skill_lower = skill.lower()
        for resume in self.resumes:
            if any(skill_lower in s.lower() for s in resume['skills']):
                results.append(resume)
        return results
    
    def search_by_title(self, title):
        """Search resumes by job title."""
        results = []
        title_lower = title.lower()
        for resume in self.resumes:
            if title_lower in resume['current_title'].lower():
                results.append(resume)
        return results
    
    def search_by_experience(self, min_years):
        """Search resumes by years of experience."""
        results = []
        for resume in self.resumes:
            if resume['years_experience'] >= min_years:
                results.append(resume)
        return results
    
    def search_by_location(self, location):
        """Search resumes by location."""
        results = []
        location_lower = location.lower()
        for resume in self.resumes:
            if location_lower in resume['location'].lower():
                results.append(resume)
        return results
    
    def search_by_company(self, company):
        """Search resumes by company experience."""
        results = []
        company_lower = company.lower()
        for resume in self.resumes:
            for exp in resume['experience']:
                if company_lower in exp['company'].lower():
                    results.append(resume)
                    break
        return results
    
    def get_statistics(self):
        """Get statistics about the resume database."""
        total = len(self.resumes)
        all_skills = set()
        all_titles = set()
        all_locations = set()
        total_experience = 0
        
        for resume in self.resumes:
            all_skills.update([s.lower() for s in resume['skills']])
            all_titles.add(resume['current_title'])
            all_locations.add(resume['location'])
            total_experience += resume['years_experience']
        
        return {
            'total_resumes': total,
            'unique_skills': len(all_skills),
            'unique_titles': len(all_titles),
            'unique_locations': len(all_locations),
            'avg_experience': round(total_experience / total, 1)
        }
    
    def get_top_skills(self, n=10):
        """Get top N skills by frequency."""
        skill_count = {}
        for resume in self.resumes:
            for skill in resume['skills']:
                skill_lower = skill.lower()
                skill_count[skill_lower] = skill_count.get(skill_lower, 0) + 1
        
        sorted_skills = sorted(skill_count.items(), key=lambda x: x[1], reverse=True)
        return sorted_skills[:n]
    
    def process_query(self, query):
        """Process natural language query and return results."""
        query_lower = query.lower()
        
        # Check for statistics query
        if any(word in query_lower for word in ['statistics', 'stats', 'overview', 'summary']):
            stats = self.get_statistics()
            return {
                'type': 'statistics',
                'data': stats,
                'message': f"Database Statistics:\n- Total Resumes: {stats['total_resumes']}\n- Unique Skills: {stats['unique_skills']}\n- Unique Job Titles: {stats['unique_titles']}\n- Unique Locations: {stats['unique_locations']}\n- Average Experience: {stats['avg_experience']} years"
            }
        
        # Check for top skills query
        if 'top skills' in query_lower or 'most common skills' in query_lower:
            top_skills = self.get_top_skills(10)
            skills_list = '\n'.join([f"{i+1}. {skill.title()}: {count} candidates" 
                                     for i, (skill, count) in enumerate(top_skills)])
            return {
                'type': 'top_skills',
                'data': top_skills,
                'message': f"Top 10 Skills:\n{skills_list}"
            }
        
        # Search for experience requirements
        experience_match = re.search(r'(\d+)\+?\s*years?', query_lower)
        if experience_match:
            years = int(experience_match.group(1))
            results = self.search_by_experience(years)
            return {
                'type': 'experience_search',
                'data': results[:10],
                'count': len(results),
                'message': f"Found {len(results)} candidates with {years}+ years of experience"
            }
        
        # Search for location
        location_keywords = ['in', 'from', 'located in', 'based in']
        for keyword in location_keywords:
            if keyword in query_lower:
                parts = query_lower.split(keyword)
                if len(parts) > 1:
                    location = parts[-1].strip()
                    results = self.search_by_location(location)
                    if results:
                        return {
                            'type': 'location_search',
                            'data': results[:10],
                            'count': len(results),
                            'message': f"Found {len(results)} candidates in {location}"
                        }
        
        # Search for company
        if 'worked at' in query_lower or 'from' in query_lower or 'at' in query_lower:
            # Try to extract company name
            for company in ['google', 'microsoft', 'amazon', 'apple', 'meta', 'netflix', 'tesla']:
                if company in query_lower:
                    results = self.search_by_company(company)
                    return {
                        'type': 'company_search',
                        'data': results[:10],
                        'count': len(results),
                        'message': f"Found {len(results)} candidates who worked at {company.title()}"
                    }
        
        # Search for skills (default)
        # Extract potential skill keywords
        skill_keywords = ['python', 'java', 'javascript', 'react', 'node', 'aws', 'docker', 
                         'kubernetes', 'sql', 'machine learning', 'data science', 'devops']
        
        for skill in skill_keywords:
            if skill in query_lower:
                results = self.search_by_skill(skill)
                return {
                    'type': 'skill_search',
                    'data': results[:10],
                    'count': len(results),
                    'message': f"Found {len(results)} candidates with {skill.title()} skills"
                }
        
        # Search by job title
        title_keywords = ['engineer', 'developer', 'manager', 'analyst', 'designer', 'architect']
        for title in title_keywords:
            if title in query_lower:
                results = self.search_by_title(title)
                return {
                    'type': 'title_search',
                    'data': results[:10],
                    'count': len(results),
                    'message': f"Found {len(results)} candidates with '{title}' in their title"
                }
        
        # Default response
        return {
            'type': 'help',
            'message': "I can help you search resumes! Try asking:\n" +
                      "- 'Show me Python developers'\n" +
                      "- 'Find candidates with 5+ years experience'\n" +
                      "- 'Show candidates in San Francisco'\n" +
                      "- 'Who worked at Google?'\n" +
                      "- 'What are the top skills?'\n" +
                      "- 'Show me statistics'"
        }

# Initialize chatbot
chatbot = ResumeChatbot(RESUMES)

@app.route('/')
def index():
    """Render the main chatbot interface."""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat requests."""
    data = request.json
    query = data.get('query', '')
    
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    result = chatbot.process_query(query)
    return jsonify(result)

@app.route('/api/stats')
def stats():
    """Get database statistics."""
    return jsonify(chatbot.get_statistics())

if __name__ == '__main__':
    print("Starting Resume Chatbot AI...")
    print(f"Loaded {len(RESUMES)} resumes")
    print("Server running at http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

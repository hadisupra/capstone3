# Resume Chatbot AI - 1000 Data

A powerful AI chatbot system for searching and analyzing 1000 professional resumes. This application provides an intelligent interface to query resume data using natural language.

## 🌟 Features

- **1000 Resume Database**: Pre-generated database with 1000 diverse professional resumes
- **AI-Powered Search**: Natural language queries to find candidates
- **Multi-Criteria Search**: Search by skills, experience, location, company, and job title
- **Interactive Web Interface**: Modern, user-friendly chatbot interface
- **Real-time Statistics**: View database statistics and trends
- **Top Skills Analysis**: Identify the most common skills in the database

## 📊 Database Statistics

- Total Resumes: 1000
- Unique Skills: 50+
- Job Titles: 30+
- Years of Experience: 1-20+ years
- Locations: 15+ cities across the US
- Companies: 35+ top tech companies

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/hadisupra/capstone3.git
cd capstone3
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Generate resume data (already done, but you can regenerate):
```bash
python generate_resumes.py
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to:
```
http://localhost:5000
```

## 💬 Usage Examples

### Natural Language Queries

The chatbot understands various types of queries:

**Search by Skills:**
- "Show me Python developers"
- "Find candidates with JavaScript skills"
- "Who knows AWS?"

**Search by Experience:**
- "Find candidates with 5+ years experience"
- "Show me senior developers with 10 years"

**Search by Location:**
- "Find candidates in San Francisco"
- "Show me people from New York"

**Search by Company:**
- "Who worked at Google?"
- "Find candidates from Microsoft"

**Statistics and Analysis:**
- "Show me statistics"
- "What are the top skills?"
- "Give me an overview"

## 📁 Project Structure

```
capstone3/
├── app.py                  # Main Flask application
├── generate_resumes.py     # Script to generate 1000 resume entries
├── resumes_data.json      # JSON file with 1000 resumes
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Web interface template
└── README.md             # This file
```

## 🔧 Technical Details

### Technologies Used

- **Backend**: Python Flask
- **Data Storage**: JSON
- **Frontend**: HTML, CSS, JavaScript
- **Data Processing**: Python (pandas, json)

### Resume Data Schema

Each resume contains:
- Personal information (name, email, phone, location)
- Professional summary
- Years of experience
- Current job title
- Skills (5-15 skills per candidate)
- Work experience (1-4 positions)
- Education (1-2 degrees)
- Certifications
- Languages

### API Endpoints

- `GET /` - Main chatbot interface
- `POST /api/chat` - Process chatbot queries
- `GET /api/stats` - Get database statistics

## 🎯 Search Capabilities

The chatbot can search and filter resumes based on:

1. **Skills**: Match candidates with specific technical skills
2. **Experience Level**: Filter by years of experience
3. **Location**: Find candidates in specific cities
4. **Company History**: Search by past employers
5. **Job Titles**: Filter by current or past positions
6. **Combined Criteria**: Mix multiple search criteria

## 📈 Sample Data

The generated resumes include:
- Realistic names and contact information
- Diverse job titles across tech industry
- Skills from modern tech stack (Python, Java, AWS, React, etc.)
- Work history from top tech companies
- Education from prestigious universities
- Multiple years of experience levels

## 🛠️ Customization

### Adding More Resumes

Edit `generate_resumes.py` and modify:
```python
for i in range(1, 2001):  # Change to generate 2000 resumes
    resume = generate_resume(i)
    resumes.append(resume)
```

### Adding More Skills

Modify the `skills` list in `generate_resumes.py`:
```python
skills = [
    "Python", "Java", "Your-New-Skill", ...
]
```

### Customizing the Chatbot

The chatbot logic is in `app.py` in the `ResumeChatbot` class. You can:
- Add new search methods
- Enhance natural language processing
- Integrate with external AI APIs (like OpenAI)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Created as part of Capstone Project 3

## 🙏 Acknowledgments

- Flask framework for the web application
- Python community for excellent libraries
- All contributors and users of this project
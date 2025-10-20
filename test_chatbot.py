"""
Test script for the Resume Chatbot AI system
"""
import json
from app import chatbot

def test_data_integrity():
    """Test that resume data is loaded correctly."""
    with open('resumes_data.json', 'r') as f:
        resumes = json.load(f)
    
    assert len(resumes) == 1000, "Should have 1000 resumes"
    assert resumes[0]['id'] == 1, "First resume should have ID 1"
    assert resumes[-1]['id'] == 1000, "Last resume should have ID 1000"
    
    # Verify data structure
    required_fields = ['id', 'name', 'email', 'phone', 'location', 'summary', 
                      'years_experience', 'current_title', 'skills', 'experience', 
                      'education', 'certifications', 'languages']
    
    for field in required_fields:
        assert field in resumes[0], f"Resume should have {field} field"
    
    print("✓ Data integrity test passed")

def test_chatbot_statistics():
    """Test chatbot statistics functionality."""
    stats = chatbot.get_statistics()
    
    assert stats['total_resumes'] == 1000, "Should report 1000 resumes"
    assert stats['unique_skills'] > 0, "Should have unique skills"
    assert stats['unique_titles'] > 0, "Should have unique titles"
    assert stats['avg_experience'] > 0, "Should have average experience"
    
    print("✓ Statistics test passed")

def test_skill_search():
    """Test skill-based search."""
    python_devs = chatbot.search_by_skill('python')
    
    assert len(python_devs) > 0, "Should find Python developers"
    
    # Verify each result has Python skill
    for resume in python_devs[:10]:
        skills = [s.lower() for s in resume['skills']]
        assert 'python' in skills, "Result should have Python skill"
    
    print(f"✓ Skill search test passed (found {len(python_devs)} Python developers)")

def test_experience_search():
    """Test experience-based search."""
    experienced = chatbot.search_by_experience(10)
    
    assert len(experienced) > 0, "Should find experienced candidates"
    
    # Verify each result has required experience
    for resume in experienced[:10]:
        assert resume['years_experience'] >= 10, "Should have 10+ years experience"
    
    print(f"✓ Experience search test passed (found {len(experienced)} experienced candidates)")

def test_location_search():
    """Test location-based search."""
    sf_candidates = chatbot.search_by_location('san francisco')
    
    assert len(sf_candidates) > 0, "Should find San Francisco candidates"
    
    # Verify each result is in SF
    for resume in sf_candidates[:10]:
        assert 'san francisco' in resume['location'].lower(), "Should be in San Francisco"
    
    print(f"✓ Location search test passed (found {len(sf_candidates)} SF candidates)")

def test_top_skills():
    """Test top skills analysis."""
    top_skills = chatbot.get_top_skills(10)
    
    assert len(top_skills) == 10, "Should return top 10 skills"
    assert all(isinstance(skill, tuple) for skill in top_skills), "Should return tuples"
    
    # Verify sorted by count
    counts = [count for _, count in top_skills]
    assert counts == sorted(counts, reverse=True), "Should be sorted by count"
    
    print(f"✓ Top skills test passed (top skill: {top_skills[0][0]} with {top_skills[0][1]} candidates)")

def test_natural_language_queries():
    """Test natural language query processing."""
    
    # Test statistics query
    result = chatbot.process_query('show me statistics')
    assert result['type'] == 'statistics', "Should recognize statistics query"
    
    # Test skill query
    result = chatbot.process_query('find python developers')
    assert result['type'] == 'skill_search', "Should recognize skill query"
    assert result['count'] > 0, "Should find results"
    
    # Test experience query
    result = chatbot.process_query('candidates with 5+ years')
    assert result['type'] == 'experience_search', "Should recognize experience query"
    assert result['count'] > 0, "Should find results"
    
    print("✓ Natural language query test passed")

def run_all_tests():
    """Run all tests."""
    print("Running Resume Chatbot AI Tests...\n")
    
    test_data_integrity()
    test_chatbot_statistics()
    test_skill_search()
    test_experience_search()
    test_location_search()
    test_top_skills()
    test_natural_language_queries()
    
    print("\n✅ All tests passed!")

if __name__ == '__main__':
    run_all_tests()

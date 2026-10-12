"""Comprehensive unit tests for backend utilities and services."""

import unittest
from backend.utils.preprocessing import clean_text, extract_keywords_list
from backend.utils.pdf_extractor import extract_text_from_pdf_bytes
from backend.services.parser_service import (
    extract_skills,
    estimate_experience_years,
    extract_education,
    extract_certifications,
    estimate_project_count,
    parse_resume_full,
    extract_required_experience_from_jd,
    extract_required_education_from_jd
)
from backend.services.matcher_service import (
    match_resume_to_job,
    calculate_semantic_similarity,
    synthesize_hiring_decision
)
from backend.services.explainability_service import explain_prediction
from backend.services.model_service import model_service


class TestPreprocessingUtils(unittest.TestCase):

    def test_clean_text_pii_removal(self):
        text = "Candidate email: test.candidate@domain.com, Phone: +1 987-654-3210, Web: https://github.com/profile"
        cleaned = clean_text(text)
        self.assertNotIn("test.candidate@domain.com", cleaned)
        self.assertNotIn("987-654-3210", cleaned)
        self.assertNotIn("https://github.com", cleaned)

    def test_clean_text_preserves_tech_tokens(self):
        text = "Experienced in C++, C#, .NET, Node.js, and REST APIs."
        cleaned = clean_text(text)
        self.assertIn("c++", cleaned)
        self.assertIn("c#", cleaned)
        self.assertIn(".net", cleaned)
        self.assertIn("node.js", cleaned)


class TestParserService(unittest.TestCase):

    def test_extract_skills_boundary_and_aliases(self):
        text = "Frontend dev using JavaScript, Next.js, and CSS3."
        skills = extract_skills(text)
        self.assertIn("javascript", skills)
        self.assertIn("next.js", skills)
        self.assertIn("css", skills)
        self.assertNotIn("java", skills)

    def test_estimate_experience_fresher_vs_experienced(self):
        fresher_text = "Aditya Pratap Singh. B.Tech Computer Science (2020-2024). Fresher looking for software role."
        self.assertEqual(estimate_experience_years(fresher_text), 0)

        exp_text = "Senior Developer with 5+ years of experience in cloud infrastructure."
        self.assertEqual(estimate_experience_years(exp_text), 5)

    def test_extract_education(self):
        self.assertEqual(extract_education("Completed Ph.D in Computer Science"), "PhD")
        self.assertEqual(extract_education("Holds a Master of Science in AI"), "M.Tech")
        self.assertEqual(extract_education("Bachelor of Technology in CS"), "B.Tech")

    def test_extract_certifications(self):
        self.assertEqual(extract_certifications("AWS Certified Solutions Architect"), "AWS Certified")

    def test_parse_resume_full(self):
        resume = """
        Alex Smith
        Summary: Python and Docker Developer with 3 years of experience.
        Education: Bachelor of Technology
        Certifications: Azure Certified
        Projects: Built 2 microservices
        """
        profile = parse_resume_full(resume)
        self.assertIn("python", profile["skills"])
        self.assertIn("docker", profile["skills"])
        self.assertEqual(profile["experience_years"], 3)
        self.assertEqual(profile["education"], "B.Tech")
        self.assertIn("Azure", profile["certification"])


class TestMatcherService(unittest.TestCase):

    def test_match_resume_to_job(self):
        resume = "Python, Docker, PostgreSQL developer with 3 years experience."
        jd = "Seeking developer with Python, Docker, PostgreSQL, and Kubernetes."
        result = match_resume_to_job(resume, jd)
        self.assertIn("python", result["matched_skills"])
        self.assertIn("docker", result["matched_skills"])
        self.assertIn("postgresql", result["matched_skills"])
        self.assertIn("kubernetes", result["missing_skills"])
        self.assertEqual(result["skill_score"], 75.0)

    def test_synthesize_decision_tiers(self):
        # Reject Tier
        res_reject = {
            "composite_score": 20.0,
            "skill_score": 10.0,
            "total_required_skills": 5,
            "missing_skills": ["python", "sql", "aws", "docker"]
        }
        dec_rej = synthesize_hiring_decision(match_result=res_reject, has_job_description=True)
        self.assertEqual(dec_rej["category"], "Reject")

        # Hire Tier
        res_hire = {
            "composite_score": 85.0,
            "skill_score": 100.0,
            "total_required_skills": 4,
            "missing_skills": [],
            "matched_skills": ["python", "docker", "fastapi"]
        }
        dec_hire = synthesize_hiring_decision(match_result=res_hire, has_job_description=True)
        self.assertEqual(dec_hire["category"], "Hire")


class TestModelAndExplainabilityService(unittest.TestCase):

    def test_model_service_prediction(self):
        cat, method, conf = model_service.predict_category("Machine Learning Engineer with Python PyTorch")
        self.assertIsInstance(cat, str)
        self.assertIn("Data Science", cat)

    def test_explain_prediction_generates_questions(self):
        match_res = {
            "composite_score": 75.0,
            "skill_score": 80.0,
            "semantic_score": 60.0,
            "matched_skills": ["python", "fastapi"],
            "missing_skills": ["kubernetes"],
            "candidate_experience": 3,
            "candidate_education": "B.Tech"
        }
        exp = explain_prediction(match_result=match_res)
        self.assertGreaterEqual(len(exp["interview_questions"]), 2)
        self.assertGreaterEqual(len(exp["improvement_tips"]), 1)
        self.assertGreaterEqual(len(exp["summary_reasons"]), 1)


if __name__ == "__main__":
    unittest.main()

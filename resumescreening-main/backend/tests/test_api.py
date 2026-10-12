"""Integration tests for FastAPI endpoints."""

import io
import unittest
from fastapi.testclient import TestClient

from backend.main import app


class TestBackendAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.sample_pdf_bytes = (
            b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
            b"2 0 obj<</Type/Pages/Count 1/Kids[3 0 R]>>endobj\n"
            b"3 0 obj<</Type/Page/MediaBox[0 0 612 792]/Parent 2 0 R/Resources<<>>/Contents 4 0 R>>endobj\n"
            b"4 0 obj<</Length 55>>stream\n"
            b"BT /F1 12 Tf 72 712 Td (Data Scientist Python SQL Docker) Tj ET\n"
            b"endstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000009 00000 n \n"
            b"0000000058 00000 n \n0000000115 00000 n \n0000000216 00000 n \n"
            b"trailer<</Size 5/Root 1 0 R>>\nstartxref\n323\n%%EOF"
        )

    def test_health_check(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["app_name"], "AI Resume Screening & JD Fit API")
        self.assertIn("category_model_loaded", data)

    def test_root_endpoint(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")

    def test_sample_jds_endpoint(self):
        response = self.client.get("/api/sample-jds")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("presets", data)
        self.assertIn("Data Scientist / ML Engineer", data["presets"])
        self.assertIn("Full Stack Web Developer", data["presets"])

    def test_extract_skills_endpoint(self):
        payload = {
            "text": "Experienced Python and React developer with PostgreSQL and Docker expertise."
        }
        response = self.client.post("/api/extract-skills", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("python", data["skills"])
        self.assertIn("react", data["skills"])
        self.assertIn("postgresql", data["skills"])
        self.assertIn("docker", data["skills"])
        self.assertEqual(data["total_skills_found"], len(data["skills"]))

    def test_extract_skills_empty_fails(self):
        response = self.client.post("/api/extract-skills", json={"text": ""})
        self.assertIn(response.status_code, [400, 422])

    def test_extract_text_and_profile(self):
        resume_text = """
        John Doe
        Email: john@example.com | Phone: 9876543210
        Education: Bachelor of Technology in Computer Science (2018 - 2022)
        Experience: 4 years of experience as Python Developer
        Skills: Python, FastAPI, Docker, SQL, Git
        Projects: Built high throughput microservices
        """
        response = self.client.post("/api/extract-text", json={"text": resume_text})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        profile = data["profile"]
        self.assertIn("python", profile["skills"])
        self.assertEqual(profile["experience_years"], 4)
        self.assertEqual(profile["education"], "B.Tech")

    def test_predict_category_endpoint(self):
        resume_text = "Data Scientist specialized in Machine Learning, Deep Learning, PyTorch, and NLP."
        response = self.client.post("/api/predict-category", json={"text": resume_text})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("predicted_category", data)
        self.assertIn("method", data)

    def test_match_job_endpoint(self):
        payload = {
            "resume_text": "Data Scientist with experience in Python, SQL, Machine Learning, and Docker with 4 years experience.",
            "job_description": "Seeking a Data Scientist with 3+ years experience proficient in Python, SQL, Machine Learning, and Tableau."
        }
        response = self.client.post("/api/match-job", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("python", data["matched_skills"])
        self.assertIn("sql", data["matched_skills"])
        self.assertIn("tableau", data["missing_skills"])
        self.assertIn("docker", data["extra_skills"])
        self.assertEqual(data["skill_score"], 80.0)
        self.assertGreater(data["composite_score"], 50.0)

    def test_screen_resume_endpoint_strong_match(self):
        payload = {
            "resume_text": (
                "Senior Python Developer with 4 years of experience building APIs using FastAPI, Docker, "
                "PostgreSQL, and Git. Bachelor of Technology in Computer Science."
            ),
            "job_description": (
                "Looking for a Backend Developer with 3+ years experience in Python, FastAPI, PostgreSQL, and Docker."
            ),
            "filename": "senior_dev.txt"
        }
        response = self.client.post("/api/screen-resume", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["document_name"], "senior_dev.txt")
        self.assertIn("profile", data)
        self.assertIn("match_result", data)
        self.assertIn("hiring_decision", data)
        self.assertIn("explainability", data)
        self.assertEqual(data["hiring_decision"]["category"], "Hire")
        self.assertGreaterEqual(data["hiring_decision"]["confidence"], 70.0)
        self.assertGreaterEqual(len(data["explainability"]["interview_questions"]), 1)

    def test_screen_resume_endpoint_mismatch(self):
        payload = {
            "resume_text": "Graphic designer skilled in Photoshop, Illustrator, and Figma.",
            "job_description": "Looking for a Senior Cloud DevOps Engineer with Kubernetes, Terraform, AWS, and Linux."
        }
        response = self.client.post("/api/screen-resume", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["hiring_decision"]["category"], "Reject")

    def test_upload_resume_pdf_success(self):
        files = {
            "file": ("candidate_sample.pdf", io.BytesIO(self.sample_pdf_bytes), "application/pdf")
        }
        data = {
            "job_description": "Looking for a Data Scientist with Python, SQL, and Machine Learning."
        }
        response = self.client.post("/api/upload-resume", files=files, data=data)
        self.assertEqual(response.status_code, 200)
        res_data = response.json()
        self.assertEqual(res_data["document_name"], "candidate_sample.pdf")
        self.assertIn("python", res_data["match_result"]["matched_skills"])
        self.assertIn("sql", res_data["match_result"]["matched_skills"])

    def test_upload_resume_invalid_file_extension(self):
        files = {
            "file": ("candidate.png", b"fake png bytes", "image/png")
        }
        response = self.client.post("/api/upload-resume", files=files)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Only PDF resume files", response.json()["detail"])

    def test_cors_headers(self):
        response = self.client.options(
            "/api/screen-resume",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type"
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("access-control-allow-origin", response.headers)


if __name__ == "__main__":
    unittest.main()

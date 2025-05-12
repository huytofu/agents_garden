import requests
from smolagents.tools import Tool
from typing import List, Dict

class ResumeScraperTool(Tool):
    name = "resume_scraper"
    description = (
        "Parses a resume (in plain text) to extract key sections such as Summary, "
        "Experience, Education, and Skills. This tool expects the resume text to include "
        "section headers like 'Summary:', 'Experience:', 'Education:', and 'Skills:'."
    )
    inputs = {
        "resume_text": {
            "type": "string",
            "description": "The plain text of the resume"
        }
    }
    output_type = "object"

    def forward(self, resume_text: str) -> dict:
        # Basic extraction using simple markers; in a real-world case, you might want to use NLP.
        sections = {
            "summary": "Summary not found",
            "experience": "Experience not found",
            "education": "Education not found",
            "skills": "Skills not found"
        }
        lower_text = resume_text.lower()

        if "summary:" in lower_text:
            start = lower_text.index("summary:")
            # Assume the section ends at the next double newline or end of text
            end = lower_text.find("\n\n", start)
            sections["summary"] = resume_text[start + len("summary:"): end].strip() if end != -1 else resume_text[start + len("summary:"):].strip()

        if "experience:" in lower_text:
            start = lower_text.index("experience:")
            end = lower_text.find("\n\n", start)
            sections["experience"] = resume_text[start + len("experience:"): end].strip() if end != -1 else resume_text[start + len("experience:"):].strip()

        if "education:" in lower_text:
            start = lower_text.index("education:")
            end = lower_text.find("\n\n", start)
            sections["education"] = resume_text[start + len("education:"): end].strip() if end != -1 else resume_text[start + len("education:"):].strip()

        if "skills:" in lower_text:
            start = lower_text.index("skills:")
            end = lower_text.find("\n\n", start)
            sections["skills"] = resume_text[start + len("skills:"): end].strip() if end != -1 else resume_text[start + len("skills:"):].strip()

        return sections
    
class LinkedInJobSearchTool(Tool):
    name = "linkedin_job_search"
    description = "Searches for job postings on LinkedIn based on job title, location, and work mode (remote, hybrid, in-office)."
    
    inputs = {
        "position": {"type": "string", "description": "Job title (e.g., Data Scientist)"},
        "location": {"type": "string", "description": "City or country (e.g., Germany)"},
        "work_mode": {"type": "string", "description": "remote, hybrid, in-office"}
    }
    
    output_type = "array"

    def forward(self, position: str, location: str, work_mode: str) -> List[Dict]:
        """
        Fetches job listings from LinkedIn using SerpAPI and returns structured JSON.
        """
        SERPAPI_KEY = "YOUR-API-KEY"  # Replace with actual key
        base_url = "https://serpapi.com/search"

        params = {
            "engine": "google_jobs",
            "q": f"{position} {work_mode} jobs",
            "location": location,
            "hl": "en",
            "api_key": SERPAPI_KEY
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()

            data = response.json()
            job_results = data.get("jobs_results", [])

            # ✅ Properly format job URLs
            return [
                {
                    "Title": job["title"],
                    "Company": job.get("company_name", "N/A"),
                    "Location": job.get("location", "N/A"),
                    "Posted": job.get("detected_extensions", {}).get("posted_at", "N/A"),
                    "Link": f"https://www.linkedin.com/jobs/view/{job['job_id']}" if "job_id" in job else "N/A"
                }
                for job in job_results
            ] if job_results else [{"Error": "No jobs found. Try different keywords."}]
        
        except requests.exceptions.RequestException as e:
            return [{"Error": f"Error fetching job listings: {str(e)}"}]
        
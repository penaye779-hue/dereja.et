import anthropic
import json

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env

def screen_cv(job_description: str, cv_text: str) -> dict:
    """Send job + CV to Claude, get back a scoring dict."""

    prompt = f"""You are a professional CV screener. Analyze this CV against the job description.
Respond ONLY with a JSON object, no markdown, no backticks.

Job Description:
{job_description}

CV:
{cv_text}

Return this exact JSON:
{{
  "score": <number 0-100>,
  "skillsMatched": <number>,
  "experienceFit": "<Poor|Fair|Good|Excellent>",
  "verdict": "<Not suitable|Possible|Good match|Strong match>",
  "matchedSkills": ["skill1", "skill2"],
  "missingSkills": ["skill1", "skill2"],
  "summary": "<2-3 sentence honest assessment>",
  "interviewQuestions": ["question1", "question2", "question3"]
}}"""

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )

    text = message.content[0].text.strip()
    return json.loads(text)


def extract_cv_text(cv_file) -> str:
    """Extract plain text from uploaded CV file (PDF or txt)."""
    import PyPDF2, io

    if cv_file.name.endswith('.pdf'):
        reader = PyPDF2.PdfReader(io.BytesIO(cv_file.read()))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    
    return cv_file.read().decode('utf-8', errors='ignore')
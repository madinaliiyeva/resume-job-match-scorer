import anthropic


def score_match(resume_text: str, job_description: str, api_key: str) -> dict:
    """
    Use Claude to score how well a resume matches a job description.

    Returns a dict with keys: score (0-100), summary, strengths, gaps.
    """
    client = anthropic.Anthropic(api_key=api_key)

    prompt = f"""You are an expert technical recruiter. Evaluate how well the following resume matches the job description.

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}

Respond with a JSON object containing:
- "score": integer 0-100 representing match strength
- "summary": one-sentence overall assessment
- "strengths": list of 3-5 resume strengths relevant to this role
- "gaps": list of 0-5 missing skills or experience areas

Return only valid JSON, no additional text."""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    import json
    return json.loads(message.content[0].text)

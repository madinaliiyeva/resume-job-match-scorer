import json

import anthropic


def score_match(resume_text: str, job_description: str, api_key: str) -> dict:
    client = anthropic.Anthropic(api_key=api_key)

    prompt = f"""You are an expert technical recruiter. Evaluate how well the following resume matches the job description.

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}

Respond with a JSON object containing:
- "match_score": integer 0-100 representing overall match strength
- "strengths": list of 3-5 resume strengths relevant to this role
- "gaps": list of 0-5 missing skills or experience areas
- "rewrite_suggestions": list of 3-5 specific bullet-point rewrites from the resume that would better target this role (each as a string showing the improved version)

Return only valid JSON, no additional text."""

    with client.messages.stream(
        model="claude-opus-4-8",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        message = stream.get_final_message()

    raw = message.content[0].text.strip()

    # Claude sometimes wraps JSON in a markdown code fence — strip it
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[-1]
        raw = raw.rsplit("```", 1)[0].strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"\n--- Raw API response ---\n{raw}\n--- End raw response ---\n", flush=True)
        raise ValueError(f"Failed to parse Claude response as JSON: {e}") from e

def format_report(result: dict, resume_path: str) -> str:
    """Format the scorer output into a human-readable report."""
    score = result.get("score", "N/A")
    summary = result.get("summary", "")
    strengths = result.get("strengths", [])
    gaps = result.get("gaps", [])

    bar = _score_bar(score)

    lines = [
        "=" * 60,
        f"  RESUME MATCH REPORT",
        f"  File: {resume_path}",
        "=" * 60,
        f"\n  Match Score: {score}/100  {bar}",
        f"\n  Summary:\n  {summary}",
        "\n  Strengths:",
    ]

    for item in strengths:
        lines.append(f"    + {item}")

    if gaps:
        lines.append("\n  Gaps / Missing Skills:")
        for item in gaps:
            lines.append(f"    - {item}")
    else:
        lines.append("\n  Gaps: None identified")

    lines.append("\n" + "=" * 60)
    return "\n".join(lines)


def _score_bar(score) -> str:
    if not isinstance(score, int):
        return ""
    filled = round(score / 10)
    return "[" + "#" * filled + "." * (10 - filled) + "]"

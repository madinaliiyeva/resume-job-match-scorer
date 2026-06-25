def format_report(result: dict, resume_path: str) -> str:
    score = result.get("match_score", "N/A")
    strengths = result.get("strengths", [])
    gaps = result.get("gaps", [])
    rewrites = result.get("rewrite_suggestions", [])

    bar = _score_bar(score)

    lines = [
        "=" * 60,
        f"  RESUME MATCH REPORT",
        f"  File: {resume_path}",
        "=" * 60,
        f"\n  Match Score: {score}/100  {bar}",
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

    if rewrites:
        lines.append("\n  Rewrite Suggestions:")
        for item in rewrites:
            lines.append(f"    * {item}")

    lines.append("\n" + "=" * 60)
    return "\n".join(lines)


def _score_bar(score) -> str:
    if not isinstance(score, int):
        return ""
    filled = round(score / 10)
    return "[" + "#" * filled + "." * (10 - filled) + "]"

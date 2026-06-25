from src.report import format_report, _score_bar

FULL_RESULT = {
    "match_score": 75,
    "strengths": ["Strong Python skills", "FastAPI experience"],
    "gaps": ["Kubernetes", "Kafka"],
    "rewrite_suggestions": ["Led migration of X, reducing latency by 30%"],
}


def test_match_score_in_output():
    report = format_report(FULL_RESULT, "resume.txt")
    assert "75/100" in report


def test_resume_path_in_header():
    report = format_report(FULL_RESULT, "my_resume.pdf")
    assert "my_resume.pdf" in report


def test_strengths_displayed_with_plus():
    report = format_report(FULL_RESULT, "resume.txt")
    assert "    + Strong Python skills" in report
    assert "    + FastAPI experience" in report


def test_gaps_displayed_with_minus():
    report = format_report(FULL_RESULT, "resume.txt")
    assert "    - Kubernetes" in report
    assert "    - Kafka" in report


def test_no_gaps_shows_none_identified():
    result = {**FULL_RESULT, "gaps": []}
    report = format_report(result, "resume.txt")
    assert "None identified" in report
    assert "Gaps / Missing Skills" not in report


def test_rewrite_suggestions_displayed_with_asterisk():
    report = format_report(FULL_RESULT, "resume.txt")
    assert "    * Led migration of X, reducing latency by 30%" in report


def test_no_rewrite_section_when_empty():
    result = {**FULL_RESULT, "rewrite_suggestions": []}
    report = format_report(result, "resume.txt")
    assert "Rewrite Suggestions" not in report


def test_missing_match_score_shows_na():
    report = format_report({"strengths": [], "gaps": [], "rewrite_suggestions": []}, "r.txt")
    assert "N/A/100" in report


def test_score_bar_full():
    assert _score_bar(100) == "[##########]"


def test_score_bar_empty():
    assert _score_bar(0) == "[..........]"


def test_score_bar_half():
    assert _score_bar(50) == "[#####.....]"


def test_score_bar_non_int_returns_empty():
    assert _score_bar("N/A") == ""
    assert _score_bar(None) == ""

import json
from unittest.mock import MagicMock, patch

import pytest

from src.scorer import score_match

VALID_RESULT = {
    "match_score": 72,
    "strengths": ["Python", "FastAPI"],
    "gaps": ["Kubernetes"],
    "rewrite_suggestions": ["Rewrote X to emphasize Y"],
}


def _make_client_mock(response_text: str) -> MagicMock:
    content_block = MagicMock()
    content_block.text = response_text

    message = MagicMock()
    message.content = [content_block]

    stream = MagicMock()
    stream.get_final_message.return_value = message
    stream.__enter__ = MagicMock(return_value=stream)
    stream.__exit__ = MagicMock(return_value=False)

    client = MagicMock()
    client.messages.stream.return_value = stream
    return client


def test_returns_expected_keys():
    client = _make_client_mock(json.dumps(VALID_RESULT))
    with patch("src.scorer.anthropic.Anthropic", return_value=client):
        result = score_match("resume text", "job text", "fake-key")
    assert set(result.keys()) == {"match_score", "strengths", "gaps", "rewrite_suggestions"}


def test_match_score_value():
    client = _make_client_mock(json.dumps(VALID_RESULT))
    with patch("src.scorer.anthropic.Anthropic", return_value=client):
        result = score_match("resume text", "job text", "fake-key")
    assert result["match_score"] == 72


def test_strips_json_markdown_fence():
    fenced = "```json\n" + json.dumps(VALID_RESULT) + "\n```"
    client = _make_client_mock(fenced)
    with patch("src.scorer.anthropic.Anthropic", return_value=client):
        result = score_match("resume text", "job text", "fake-key")
    assert result["match_score"] == 72


def test_strips_plain_markdown_fence():
    fenced = "```\n" + json.dumps(VALID_RESULT) + "\n```"
    client = _make_client_mock(fenced)
    with patch("src.scorer.anthropic.Anthropic", return_value=client):
        result = score_match("resume text", "job text", "fake-key")
    assert result["match_score"] == 72


def test_raises_value_error_on_invalid_json(capsys):
    client = _make_client_mock("Sorry, I cannot help with that.")
    with patch("src.scorer.anthropic.Anthropic", return_value=client):
        with pytest.raises(ValueError, match="Failed to parse Claude response as JSON"):
            score_match("resume text", "job text", "fake-key")


def test_prints_raw_response_on_json_error(capsys):
    raw = "not valid json at all"
    client = _make_client_mock(raw)
    with patch("src.scorer.anthropic.Anthropic", return_value=client):
        with pytest.raises(ValueError):
            score_match("resume text", "job text", "fake-key")
    captured = capsys.readouterr()
    assert raw in captured.out


def test_uses_correct_model():
    client = _make_client_mock(json.dumps(VALID_RESULT))
    with patch("src.scorer.anthropic.Anthropic", return_value=client):
        score_match("resume text", "job text", "fake-key")
    _, kwargs = client.messages.stream.call_args
    assert kwargs["model"] == "claude-opus-4-8"


def test_resume_and_job_text_in_prompt():
    client = _make_client_mock(json.dumps(VALID_RESULT))
    with patch("src.scorer.anthropic.Anthropic", return_value=client):
        score_match("UNIQUE_RESUME_CONTENT", "UNIQUE_JOB_CONTENT", "fake-key")
    _, kwargs = client.messages.stream.call_args
    prompt = kwargs["messages"][0]["content"]
    assert "UNIQUE_RESUME_CONTENT" in prompt
    assert "UNIQUE_JOB_CONTENT" in prompt

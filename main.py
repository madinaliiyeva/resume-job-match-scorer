#!/usr/bin/env python3
import argparse
import getpass
import sys

from src.parser import extract_text
from src.scorer import score_match
from src.report import format_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="resume-scorer",
        description="Score how well a resume matches a job description using Claude AI.",
    )
    parser.add_argument(
        "resume",
        help="Path to the resume file (.pdf or .docx)",
    )
    parser.add_argument(
        "job_description",
        help="Path to a plain-text file containing the job description",
    )
    parser.add_argument(
        "--api-key",
        help="Anthropic API key (will prompt securely if omitted)",
        default=None,
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    api_key = args.api_key
    if not api_key:
        api_key = getpass.getpass("Anthropic API key: ")

    try:
        print(f"Extracting text from {args.resume}...")
        resume_text = extract_text(args.resume)

        with open(args.job_description, "r", encoding="utf-8") as f:
            job_description = f.read().strip()

        print("Scoring match with Claude...")
        result = score_match(resume_text, job_description, api_key)

        report = format_report(result, args.resume)
        print(report)

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

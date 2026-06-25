# Resume Job Match Scorer

A Python CLI tool that uses Claude AI to score how well a resume matches a job description.

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py path/to/resume.pdf path/to/job_description.txt
```

The tool will securely prompt for your Anthropic API key if not provided via `--api-key`.

### Options

```
positional arguments:
  resume            Path to the resume file (.pdf or .docx)
  job_description   Path to a plain-text file containing the job description

options:
  --api-key         Anthropic API key (will prompt securely if omitted)
```

## Example

```bash
python main.py resume.docx job.txt --api-key sk-ant-...
```

Output:
```
============================================================
  RESUME MATCH REPORT
  File: resume.docx
============================================================

  Match Score: 82/100  [########..]

  Summary:
  Strong backend candidate with most required skills present.

  Strengths:
    + 5 years Python experience
    + Familiar with REST API design
    ...

  Gaps:
    - No Kubernetes experience listed
    ...
============================================================
```

## Project Structure

```
resume-job-match-scorer/
├── main.py           # CLI entrypoint
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── parser.py     # PDF/DOCX text extraction
│   ├── scorer.py     # Claude API integration
│   └── report.py     # Output formatting
└── tests/
    └── __init__.py
```

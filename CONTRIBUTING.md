# 🤝 Contributing to MailApix API

Thanks for helping improve MailApix API.

## Quick Links

- [Contribution Flow](#contribution-flow)
- [Local Setup](#local-setup)
- [Pull Request Checklist](#pull-request-checklist)
- [Code Style Expectations](#code-style-expectations)
- [Issue Reporting](#issue-reporting)
- [Security Issues](#security-issues)

---

## Contribution Flow

1. Fork the repository
2. Create a feature/fix branch from `main`
3. Make focused changes with clear commit messages
4. Run and validate the API locally
5. Open a Pull Request with context and testing notes

## Local Setup

```bash
git clone <your-fork-url>
cd EmaiServiceApp

python -m venv .venv
.venv\Scripts\activate   # Windows

pip install -r requirements.txt
uvicorn MailApixAPI.main:app --reload
```

## Pull Request Checklist

- Keep PR scope small and focused
- Update docs for behavior/config changes
- Add or update tests where applicable
- Avoid unrelated refactors in the same PR
- Include clear title, description, and validation steps

## Code Style Expectations

- Follow existing project structure and naming conventions
- Keep functions/modules single-purpose and maintainable
- Prefer explicit validation and error handling
- Preserve API behavior unless changes are intentional and documented

## Issue Reporting

When opening an issue, include:

- Expected behavior
- Actual behavior
- Steps to reproduce
- Environment details (OS, Python version)
- Relevant logs or traceback snippets

## Security Issues

Please do not disclose vulnerabilities publicly.

- Follow the process in [SECURITY.md](SECURITY.md)

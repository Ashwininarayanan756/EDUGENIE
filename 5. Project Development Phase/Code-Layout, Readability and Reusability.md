# Code-Layout, Readability and Reusability

**Project Title:** EduGenie.ai – Your Smart Budget & Recommendation Assistant
**Team ID:** SWTID-2026-9579
**Team Size:** 3
**Team Leader:** Ashwini N
**Team Members:** Rajasri R, Reshmavathy K

---

| S.No | Criteria | Practice Followed | Applied In |
|---|---|---|---|
| 1 | Code Layout | Separate files for UI, database, logic and AI; consistent indentation (PEP 8) | All modules |
| 2 | Naming Conventions | Meaningful snake_case names for variables and functions | All modules |
| 3 | Comments & Docstrings | Docstring for every function explaining input and output | All modules |
| 4 | Reusability | Common functions (database connection, API call) written once and reused | database.py, ai_assistant.py |
| 5 | Error Handling | try/except for API and database calls with user-friendly messages | ai_assistant.py, database.py |
| 6 | Configuration Management | API key stored in environment variable / secrets file, not in code | ai_assistant.py |
| 7 | Version Control | Regular Git commits with clear messages | GitHub repository |


# Solution Architecture

**Project Title:** EduGenie.ai – Your Smart Budget & Recommendation Assistant
**Team ID:** SWTID-2026-9579
**Team Size:** 3
**Team Leader:** Ashwini N
**Team Members:** Rajasri R, Reshmavathy K

---

## Architecture Flow

```
Student -> Streamlit Web UI -> Application Logic (Python)
                                  |-> SQLite Database (users, expenses, budgets, goals)
                                  |-> Analysis Module (Pandas, scikit-learn)
                                  |-> GenAI Module (Google Gemini API) -> Recommendations / Chat
                                  |-> Dashboard & Report Module (Plotly, CSV)
```

## Components and Technologies

| S.No | Component | Description | Technology |
|---|---|---|---|
| 1 | User Interface | Web interface for entering data, chat and viewing dashboard | Streamlit |
| 2 | Application Logic | Handles budget rules, alerts and workflows | Python |
| 3 | Database | Stores users, expenses, budgets and goals | SQLite |
| 4 | Data Analysis | Category totals, trends and simple spending prediction | Pandas, scikit-learn |
| 5 | GenAI Engine | Generates advice and recommendations from user data | Google Gemini API |
| 6 | Visualisation | Charts for spending and savings | Plotly |
| 7 | Version Control | Code sharing and collaboration | Git, GitHub |

## Team Ownership

| Component | Owner |
|---|---|
| GenAI Engine & Application Logic | Ashwini N |
| User Interface & Dashboard | Rajasri R |
| Database, Testing & Documentation | Reshmavathy K |


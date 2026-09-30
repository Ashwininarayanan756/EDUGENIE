# Data Flow Diagram & User Stories

**Project Title:** EduGenie.ai – Your Smart Budget & Recommendation Assistant
**Team ID:** SWTID-2026-9579
**Team Size:** 3
**Team Leader:** Ashwini N
**Team Members:** Rajasri R, Reshmavathy K

---

## DFD Level 0 – Data Flow Table

| Flow No. | Source | Data Flow | Process | Destination |
|---|---|---|---|---|
| 1 | Student (User) | Profile, income, expenses, budget goals | 1.0 Input Handling | Data Store (SQLite) |
| 2 | Data Store (SQLite) | Stored expense records | 2.0 Expense Analysis (categorisation and totals) | Analysis Module |
| 3 | Analysis Module | Spending summary and patterns | 3.0 Budget & Alert Engine | Student (alerts) |
| 4 | Student (User) | Question / request for advice | 4.0 GenAI Recommendation Engine (Gemini API) | LLM API |
| 5 | LLM API | Personalised recommendations and answers | 4.0 GenAI Recommendation Engine | Student (chat response) |
| 6 | Analysis Module | Charts and report data | 5.0 Dashboard & Report Generator | Student (dashboard / CSV) |

## DFD Level 0 – Diagram (Text)

```
[Student] --> (1.0 Input Handling) --> [SQLite DB] --> (2.0 Expense Analysis) --> (3.0 Budget & Alerts) --> [Student]
[Student] --> (4.0 GenAI Recommendation Engine) <--> [Gemini API] --> [Student]
(2.0 Expense Analysis) --> (5.0 Dashboard & Report) --> [Student]
```

## User Stories

| User Type | Functional Requirement (Epic) | User Story Number | User Story / Task | Acceptance Criteria | Priority | Release |
|---|---|---|---|---|---|---|
| Student | Profile & Expense Entry | USN-1 | As a student, I can enter my profile and monthly income so that the app knows my budget base | Profile is saved and shown on dashboard | High | Sprint-1 |
| Student | Profile & Expense Entry | USN-2 | As a student, I can add daily expenses with category and date | Expense is stored and appears in the list | High | Sprint-1 |
| Student | Budget Planning | USN-3 | As a student, I can set a monthly budget per category | Limits are saved and compared with spending | High | Sprint-2 |
| Student | Budget Planning | USN-4 | As a student, I receive an alert when I cross 80% of a category limit | Alert message displays on threshold | Medium | Sprint-2 |
| Student | AI Assistant | USN-5 | As a student, I can chat with the AI to get budget advice | AI replies in under 10 seconds using my data | High | Sprint-3 |
| Student | Recommendations | USN-6 | As a student, I get suggestions for scholarships, free courses and savings tips | At least 3 relevant suggestions are shown | High | Sprint-3 |
| Student | Dashboard & Reports | USN-7 | As a student, I can view charts of my spending | Pie and bar charts render correctly | Medium | Sprint-4 |
| Student | Dashboard & Reports | USN-8 | As a student, I can download my monthly report as CSV | CSV file downloads with all records | Low | Sprint-4 |
| Parent | Dashboard & Reports | USN-9 | As a parent, I can view a simple spending summary of the student | Summary page shows totals per category | Low | Sprint-4 |


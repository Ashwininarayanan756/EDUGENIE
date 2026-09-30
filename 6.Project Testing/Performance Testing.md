# Performance Testing

**Project Title:** EduGenie.ai – Your Smart Budget & Recommendation Assistant
**Team ID:** SWTID-2026-9579
**Team Size:** 3
**Team Leader:** Ashwini N
**Team Members:** Rajasri R, Reshmavathy K

---

## Functional Test Cases

| Test Case ID | Feature | Test Scenario | Expected Result | Status |
|---|---|---|---|---|
| TC-01 | Profile Setup | Enter valid name and income | Profile saved successfully | To be executed |
| TC-02 | Expense Tracking | Add an expense with category and date | Expense appears in list | To be executed |
| TC-03 | Expense Tracking | Add expense with empty amount | Validation error shown | To be executed |
| TC-04 | Budget Planner | Set budget per category | Limits saved and displayed | To be executed |
| TC-05 | Alerts | Spend above 80% of limit | Alert message displayed | To be executed |
| TC-06 | AI Assistant | Ask "How can I save money this month?" | Relevant advice based on user data | To be executed |
| TC-07 | Recommendations | Request scholarship suggestions | At least 3 relevant suggestions | To be executed |
| TC-08 | Report | Click download report | CSV downloads correctly | To be executed |

## Performance Test Parameters

| S.No | Parameter | Test Scenario | Target / Expected Value | Tested By | Status |
|---|---|---|---|---|---|
| 1 | Page Load Time | Open home page | Less than 3 seconds | Reshmavathy K | To be executed |
| 2 | AI Response Time | Ask one question to AI assistant | Less than 10 seconds | Ashwini N | To be executed |
| 3 | Database Response | Fetch 1,000 expense records | Less than 1 second | Reshmavathy K | To be executed |
| 4 | Dashboard Rendering | Load charts with 1,000 records | Less than 3 seconds | Rajasri R | To be executed |
| 5 | Concurrent Usage | 5 users using the app together | No crash, response within limits | Reshmavathy K | To be executed |
| 6 | Accuracy | Expense category prediction | Above 85% accuracy | Ashwini N | To be executed |


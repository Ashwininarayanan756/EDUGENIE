// EduGenie Interactive Frontend Logic

let currentQuizData = [];

function escapeHtml(text) {
    if (!text) return "";
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

function showLoading(containerId, message = "Generating response...") {
    const el = document.getElementById(containerId);
    if (!el) return;
    el.innerHTML = `
        <div class="result-box loading-container">
            <span class="spinner"></span>
            <span>${message}</span>
        </div>
    `;
}

function showError(containerId, title, errorMsg) {
    const el = document.getElementById(containerId);
    if (!el) return;
    el.innerHTML = `
        <div class="result-box" style="border-left: 4px solid var(--error-color);">
            <strong>⚠️ ${escapeHtml(title)}</strong>
            <p style="margin-top: 8px; color: var(--error-color); font-size: 0.9rem;">
                ${escapeHtml(errorMsg || "An unexpected error occurred. Please try again.")}
            </p>
        </div>
    `;
}

function copyText(elementId) {
    const el = document.getElementById(elementId);
    if (!el) return;
    const text = el.innerText || el.textContent;
    navigator.clipboard.writeText(text).then(() => {
        alert("Copied to clipboard!");
    }).catch(() => {
        const textarea = document.createElement("textarea");
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand("copy");
        document.body.removeChild(textarea);
        alert("Copied to clipboard!");
    });
}

function scrollToSection(sectionId) {
    const target = document.getElementById(sectionId);
    if (target) {
        target.scrollIntoView({ behavior: "smooth", block: "center" });
        document.querySelectorAll(".nav-pill").forEach(pill => {
            if (pill.getAttribute("onclick")?.includes(sectionId)) {
                pill.classList.add("active");
            } else {
                pill.classList.remove("active");
            }
        });
    }
}

// -------------------------------------------------------------
// 1. Q&A Handler
// -------------------------------------------------------------
async function handleQA(event) {
    event.preventDefault();
    const input = document.getElementById("question");
    const btn = document.getElementById("qaBtn");
    const resultBox = document.getElementById("qaResult");
    const question = input.value.trim();

    if (!question) return;

    btn.disabled = true;
    showLoading("qaResult", "EduGenie is thinking...");

    try {
        const response = await fetch(`/qa?question=${encodeURIComponent(question)}`);
        const data = await response.json();

        if (!response.ok || data.error) {
            showError("qaResult", "Error in Q&A", data.error || response.statusText);
            return;
        }

        const answerText = data.answer || data.result || "No answer returned.";
        resultBox.innerHTML = `
            <div class="result-box">
                <div class="result-header">
                    <strong>Answer:</strong>
                    <button type="button" class="copy-btn" onclick="copyText('qaAnswerText')">Copy</button>
                </div>
                <div id="qaAnswerText">${escapeHtml(answerText)}</div>
            </div>
        `;
    } catch (err) {
        showError("qaResult", "Connection Error", err.message);
    } finally {
        btn.disabled = false;
    }
}

// -------------------------------------------------------------
// 2. Explanation Handler
// -------------------------------------------------------------
async function handleExplain(event) {
    event.preventDefault();
    const input = document.getElementById("topic");
    const btn = document.getElementById("explainBtn");
    const resultBox = document.getElementById("explanationResult");
    const topic = input.value.trim();

    if (!topic) return;

    btn.disabled = true;
    showLoading("explanationResult", "EduGenie is simplifying this concept...");

    try {
        const response = await fetch("/explain/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ topic: topic })
        });
        const data = await response.json();

        if (!response.ok || data.error) {
            showError("explanationResult", "Error in Explanation", data.error || response.statusText);
            return;
        }

        const expText = data.explanation || data.result || "No explanation returned.";
        resultBox.innerHTML = `
            <div class="result-box">
                <div class="result-header">
                    <strong>Explanation:</strong>
                    <button type="button" class="copy-btn" onclick="copyText('explainOutText')">Copy</button>
                </div>
                <div id="explainOutText">${escapeHtml(expText)}</div>
            </div>
        `;
    } catch (err) {
        showError("explanationResult", "Connection Error", err.message);
    } finally {
        btn.disabled = false;
    }
}

// -------------------------------------------------------------
// 3. Summary Handler
// -------------------------------------------------------------
async function handleSummary(event) {
    event.preventDefault();
    const input = document.getElementById("summaryText");
    const btn = document.getElementById("summaryBtn");
    const resultBox = document.getElementById("summaryResult");
    const text = input.value.trim();

    if (!text) return;

    btn.disabled = true;
    showLoading("summaryResult", "EduGenie is summarizing...");

    try {
        const response = await fetch("/summarize/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: text })
        });
        const data = await response.json();

        if (!response.ok || data.error) {
            showError("summaryResult", "Error in Summary", data.error || response.statusText);
            return;
        }

        const summaryText = data.summary || data.result || "No summary returned.";
        resultBox.innerHTML = `
            <div class="result-box">
                <div class="result-header">
                    <strong>Summary:</strong>
                    <button type="button" class="copy-btn" onclick="copyText('summaryOutText')">Copy</button>
                </div>
                <div id="summaryOutText">${escapeHtml(summaryText)}</div>
            </div>
        `;
    } catch (err) {
        showError("summaryResult", "Connection Error", err.message);
    } finally {
        btn.disabled = false;
    }
}

// -------------------------------------------------------------
// 4. Quiz Generation Handler
// -------------------------------------------------------------
async function handleQuiz(event) {
    event.preventDefault();
    const input = document.getElementById("quizText");
    const btn = document.getElementById("quizBtn");
    const resultBox = document.getElementById("quizResult");
    const text = input.value.trim();

    if (!text) return;

    btn.disabled = true;
    showLoading("quizResult", "EduGenie is generating 3 questions...");

    try {
        const response = await fetch("/quiz", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: text })
        });
        const data = await response.json();

        if (!response.ok || data.error) {
            showError("quizResult", "Error in Quiz Generation", data.error || response.statusText);
            return;
        }

        const quizList = Array.isArray(data.quiz) ? data.quiz : (data.result || []);
        currentQuizData = quizList;

        if (quizList.length === 0) {
            showError("quizResult", "No Questions", "Could not generate questions for this topic.");
            return;
        }

        let html = `
            <div class="result-box">
                <div class="result-header">
                    <strong>Quiz:</strong>
                </div>
        `;

        quizList.forEach((q, idx) => {
            const options = Array.isArray(q.options) ? q.options : [];
            html += `
                <div class="quiz-question-box" id="quiz-q-${idx}">
                    <p class="quiz-question-title">Q${idx + 1}: ${escapeHtml(q.question)}</p>
                    <div class="quiz-options">
            `;

            options.forEach((opt, optIdx) => {
                html += `
                    <label class="quiz-option-label">
                        <input type="radio" name="quiz_opt_${idx}" value="${escapeHtml(opt)}">
                        <span>${escapeHtml(opt)}</span>
                    </label>
                `;
            });

            html += `
                    </div>
                    <button type="button" class="check-answer-btn" onclick="checkAnswer(${idx})">Check Answer</button>
                    <div id="feedback-${idx}" class="quiz-feedback"></div>
                </div>
            `;
        });

        html += `</div>`;
        resultBox.innerHTML = html;

    } catch (err) {
        showError("quizResult", "Connection Error", err.message);
    } finally {
        btn.disabled = false;
    }
}

function checkAnswer(questionIndex) {
    if (!currentQuizData || !currentQuizData[questionIndex]) return;

    const q = currentQuizData[questionIndex];
    const radios = document.getElementsByName(`quiz_opt_${questionIndex}`);
    const feedbackEl = document.getElementById(`feedback-${questionIndex}`);

    let selectedValue = null;
    for (let r of radios) {
        if (r.checked) {
            selectedValue = r.value;
            break;
        }
    }

    if (!selectedValue) {
        feedbackEl.innerHTML = `<span class="feedback-incorrect">⚠️ Please select an option first.</span>`;
        return;
    }

    const cleanExpected = (q.answer || "").trim().toLowerCase();
    const cleanSelected = selectedValue.trim().toLowerCase();

    const isCorrect = (cleanExpected === cleanSelected) ||
                      cleanSelected.includes(cleanExpected) ||
                      cleanExpected.includes(cleanSelected);

    if (isCorrect) {
        feedbackEl.innerHTML = `<span class="feedback-correct">✔ Correct!</span>`;
    } else {
        feedbackEl.innerHTML = `<span class="feedback-incorrect">❌ Incorrect. Correct answer: ${escapeHtml(q.answer)}</span>`;
    }
}

// -------------------------------------------------------------
// 5. Learning Recommendations Handler
// -------------------------------------------------------------
async function handleRecommendations(event) {
    event.preventDefault();
    const input = document.getElementById("recommendTopic");
    const btn = document.getElementById("recommendBtn");
    const resultBox = document.getElementById("recommendResult");
    const topic = input.value.trim();

    if (!topic) return;

    btn.disabled = true;
    showLoading("recommendResult", "EduGenie is designing your personalized learning path...");

    try {
        const response = await fetch(`/learn/recommendations?topic=${encodeURIComponent(topic)}`);
        const data = await response.json();

        if (!response.ok || data.error) {
            showError("recommendResult", "Error in Recommendations", data.error || response.statusText);
            return;
        }

        const recText = data.recommendation || data.result || "No recommendations generated.";
        resultBox.innerHTML = `
            <div class="result-box">
                <div class="result-header">
                    <strong>Learning Recommendations for "${escapeHtml(topic)}":</strong>
                    <button type="button" class="copy-btn" onclick="copyText('recOutText')">Copy</button>
                </div>
                <div id="recOutText" class="learning-content">${escapeHtml(recText)}</div>
            </div>
        `;
    } catch (err) {
        showError("recommendResult", "Connection Error", err.message);
    } finally {
        btn.disabled = false;
    }
}

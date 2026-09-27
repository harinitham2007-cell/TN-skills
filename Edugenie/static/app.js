const task =
    document.getElementById("task");

const inputText =
    document.getElementById("inputText");

const inputLabel =
    document.getElementById("inputLabel");

const levelGroup =
    document.getElementById("level-group");

const goalGroup =
    document.getElementById("goal-group");

const goal =
    document.getElementById("goal");

const submitBtn =
    document.getElementById("submitBtn");

const result =
    document.getElementById("result");

const loading =
    document.getElementById("loading");


function updateForm() {

    const value = task.value;


    levelGroup.classList.toggle(
        "hidden",

        value !== "qa" &&
        value !== "explain" &&
        value !== "recommendations"
    );


    goalGroup.classList.toggle(
        "hidden",

        value !== "recommendations"
    );


    if (value === "qa") {

        inputLabel.textContent =
            "Your Question";

        inputText.placeholder =
            "Example: Explain photosynthesis in simple terms.";

    }


    else if (value === "explain") {

        inputLabel.textContent =
            "Topic";

        inputText.placeholder =
            "Example: Newton's laws of motion";

    }


    else if (value === "summarize") {

        inputLabel.textContent =
            "Text to Summarize";

        inputText.placeholder =
            "Paste the text you want summarized...";

    }


    else if (value === "quiz") {

        inputLabel.textContent =
            "Educational Content";

        inputText.placeholder =
            "Paste your notes or educational content...";

    }


    else {

        inputLabel.textContent =
            "Topic";

        inputText.placeholder =
            "Example: Python programming";

    }

}


function escapeHtml(value) {

    return String(value)

        .replaceAll(
            "&",
            "&amp;"
        )

        .replaceAll(
            "<",
            "&lt;"
        )

        .replaceAll(
            ">",
            "&gt;"
        )

        .replaceAll(
            '"',
            "&quot;"
        )

        .replaceAll(
            "'",
            "&#039;"
        );
}


function renderQuiz(data) {

    return data.questions

        .map(
            (question, index) => `

            <div class="quiz-question">

                <h3>
                    ${index + 1}.
                    ${escapeHtml(question.question)}
                </h3>

                ${question.options
                    .map(
                        (option, optionIndex) => `

                        <div
                            class="option
                            ${
                                option.is_correct
                                    ? "correct"
                                    : ""
                            }"
                        >

                            ${
                                String.fromCharCode(
                                    65 + optionIndex
                                )
                            }.

                            ${escapeHtml(
                                option.text
                            )}

                            ${
                                option.is_correct
                                    ? " ✓ Correct"
                                    : ""
                            }

                        </div>

                    `
                    )
                    .join("")
                }

            </div>

        `
        )

        .join("");
}


function renderRecommendations(data) {

    return data.recommendations

        .map(
            (item) => `

            <div class="step">

                <h3>

                    Step ${item.step}:

                    ${escapeHtml(
                        item.topic
                    )}

                </h3>

                <p>

                    ${escapeHtml(
                        item.description
                    )}

                </p>

                <strong>
                    Activity:
                </strong>

                ${escapeHtml(
                    item.activity
                )}

            </div>

        `
        )

        .join("");
}


task.addEventListener(
    "change",
    updateForm
);


submitBtn.addEventListener(
    "click",
    async () => {

        const value =
            task.value;

        const text =
            inputText.value.trim();


        if (!text) {

            result.innerHTML =
                "<p>Please enter some content first.</p>";

            return;
        }


        let endpoint;

        let body;


        if (value === "qa") {

            endpoint = "/qa";

            body = {

                question: text,

                learner_level:
                    document
                        .getElementById("level")
                        .value

            };

        }


        else if (value === "explain") {

            endpoint = "/explain";

            body = {

                topic: text,

                learner_level:
                    document
                        .getElementById("level")
                        .value

            };

        }


        else if (value === "summarize") {

            endpoint =
                "/summarize";

            body = {

                text: text

            };

        }


        else if (value === "quiz") {

            endpoint =
                "/quiz";

            body = {

                text: text

            };

        }


        else {

            endpoint =
                "/learn/recommendations";

            body = {

                topic: text,

                learner_level:
                    document
                        .getElementById("level")
                        .value,

                goal:
                    goal.value.trim() ||
                    "understand the fundamentals"

            };

        }


        loading.classList.remove(
            "hidden"
        );

        result.innerHTML = "";

        submitBtn.disabled = true;


        try {

            const response =
                await fetch(
                    endpoint,
                    {

                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(
                                body
                            )

                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Request failed."
                );

            }


            if (value === "qa") {

                result.innerHTML = `

                    <div class="text-result">

                        ${escapeHtml(
                            data.answer
                        )}

                    </div>

                `;

            }


            else if (value === "explain") {

                result.innerHTML = `

                    <div class="text-result">

                        ${escapeHtml(
                            data.explanation
                        )}

                    </div>

                `;

            }


            else if (value === "summarize") {

                result.innerHTML = `

                    <div class="text-result">

                        ${escapeHtml(
                            data.summary
                        )}

                    </div>

                `;

            }


            else if (value === "quiz") {

                result.innerHTML =
                    renderQuiz(data);

            }


            else {

                result.innerHTML =
                    renderRecommendations(
                        data
                    );

            }

        }


        catch (error) {

            result.innerHTML = `

                <div class="error">

                    ${escapeHtml(
                        error.message
                    )}

                </div>

            `;

        }


        finally {

            loading.classList.add(
                "hidden"
            );

            submitBtn.disabled =
                false;

        }

    }
);


updateForm();
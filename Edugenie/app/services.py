from .config import get_settings
from .gemini_service import get_gemini_service
from .local_explainer import explain_with_local_model

from .schemas import (
    QARequest,
    ExplainRequest,
    TextRequest,
    LearningPathRequest,
    QuizResponse,
    LearningPathResponse,
)


def answer_question(
    request: QARequest
) -> str:

    gemini = get_gemini_service()

    prompt = f"""
You are EduGenie, an educational learning assistant.

Answer the following question accurately and clearly.

Learner level:
{request.learner_level}

Question:
{request.question}

Instructions:

- Explain using learner-friendly language.
- Give a simple example when useful.
- Break difficult concepts into smaller parts.
- Do not invent facts.
- Keep the answer educational and practical.
"""

    return gemini.generate_text(prompt)


def explain_topic(
    request: ExplainRequest
) -> str:

    settings = get_settings()

    if settings.use_local_explainer:

        try:

            return explain_with_local_model(
                request.topic,
                request.learner_level
            )

        except Exception:
            # Automatically use Gemini if
            # the optional local model fails.
            pass

    gemini = get_gemini_service()

    prompt = f"""
You are EduGenie, an expert educational tutor.

Explain the following topic to a
{request.learner_level} learner.

Topic:
{request.topic}

Structure the answer as:

1. Simple definition
2. Core idea
3. Step-by-step explanation
4. Practical example
5. Common mistakes
6. Short recap

Use clear educational language.
"""

    return gemini.generate_text(prompt)


def summarize(
    request: TextRequest
) -> str:

    gemini = get_gemini_service()

    prompt = f"""
Summarize the following educational text.

Text:

{request.text}

Return:

1. A concise summary
2. Five key points
3. Important terms, if any

Keep the summary faithful to the original text.
Do not introduce unrelated information.
"""

    return gemini.generate_text(prompt)


def generate_quiz(
    request: TextRequest
) -> QuizResponse:

    gemini = get_gemini_service()

    prompt = f"""
Create an educational quiz from the content below.

Content:

{request.text}

STRICT REQUIREMENTS:

- Exactly 3 questions.
- Exactly 4 options for every question.
- Exactly 1 correct option for every question.
- Each option must be relevant.
- Mark exactly one option with is_correct=true.
- Mark all other options with is_correct=false.
- Do not create more than 3 questions.
"""

    return gemini.generate_structured(
        prompt,
        QuizResponse
    )


def learning_recommendations(
    request: LearningPathRequest
) -> LearningPathResponse:

    gemini = get_gemini_service()

    prompt = f"""
Create a personalized learning path.

Topic:
{request.topic}

Learner level:
{request.learner_level}

Learning goal:
{request.goal}

Create 5 to 7 ordered learning steps.

Every step must contain:

- step
- topic
- description
- activity

Start with prerequisites and gradually progress
towards the learner's goal.
"""

    return gemini.generate_structured(
        prompt,
        LearningPathResponse
    )
from typing import List

from pydantic import BaseModel, Field, model_validator


class QARequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=10000
    )

    learner_level: str = "beginner"


class ExplainRequest(BaseModel):
    topic: str = Field(
        ...,
        min_length=1,
        max_length=5000
    )

    learner_level: str = "beginner"


class TextRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=30000
    )


class LearningPathRequest(BaseModel):
    topic: str = Field(
        ...,
        min_length=1,
        max_length=5000
    )

    learner_level: str = "beginner"

    goal: str = "understand the fundamentals"


class QuizOption(BaseModel):
    text: str
    is_correct: bool


class QuizQuestion(BaseModel):
    question: str
    options: List[QuizOption]

    @model_validator(mode="after")
    def validate_options(self):

        if len(self.options) != 4:
            raise ValueError(
                "Each quiz question must have exactly 4 options."
            )

        correct_answers = sum(
            option.is_correct
            for option in self.options
        )

        if correct_answers != 1:
            raise ValueError(
                "Each quiz question must have exactly one correct option."
            )

        return self


class QuizResponse(BaseModel):
    questions: List[QuizQuestion]

    @model_validator(mode="after")
    def validate_questions(self):

        if len(self.questions) != 3:
            raise ValueError(
                "The quiz must contain exactly 3 questions."
            )

        return self


class LearningStep(BaseModel):
    step: int
    topic: str
    description: str
    activity: str


class LearningPathResponse(BaseModel):
    recommendations: List[LearningStep]
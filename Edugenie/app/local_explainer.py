from functools import lru_cache


@lru_cache(maxsize=1)
def _get_pipeline():

    try:
        from transformers import pipeline

    except ImportError as exc:

        raise RuntimeError(
            "Local explainer is enabled, but transformers "
            "is not installed."
        ) from exc

    return pipeline(
        "text2text-generation",
        model="MBZUAI/LaMini-Flan-T5-783M",
        device=-1,
    )


def explain_with_local_model(
    topic: str,
    learner_level: str
) -> str:

    generator = _get_pipeline()

    prompt = (
        f"Explain {topic} to a {learner_level} learner "
        "using simple language and examples."
    )

    result = generator(
        prompt,
        max_new_tokens=400
    )

    return result[0]["generated_text"].strip()
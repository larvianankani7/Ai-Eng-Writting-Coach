from ai.llm import get_llm
def review_text(user_text: str):
    llm = get_llm()
    prompt = f"""
    You are an expert English writing coach.
    Task:
    1. Correct grammar mistakes
    2. Improve sentence structure
    3. Make it more natural and fluent
    4. Give short feedback
    User text:
    {user_text}
    Return format:
    Corrected Text:
    ...
    Feedback:
    ...
    """
    response = llm.invoke(prompt)
    return response
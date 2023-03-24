from langchain.prompts.prompt import PromptTemplate


def chat_template():
    return PromptTemplate(
        input_variables=[],
        template=load_prompt("chat"),
    )


def diary_template():
    return PromptTemplate(
        input_variables=["text"],
        template=load_prompt("diary"),
    )


def load_prompt(prompt_name):
    with open(f"./src/prompts/{prompt_name}.prompt", "r") as f:
        return f.read()

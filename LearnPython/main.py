from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

prompt_template = PromptTemplate.from_template("Tell me a joke about {topic}")

prompt_response = prompt_template.invoke({"topic":"cats"})
print(prompt_template)

messages = [
    (
        "system",
        "You are a helpful assistant that translates English to French. Translate the user sentence.",
    ),
    ("human", "I love programming."),
]

llm = ChatGroq(
    model="mixtral-8x7b-32768",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key="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"
    # other params...
)

llm_response = llm.invoke(messages)
print(llm_response.content)

print("hello")

x = 4 +2

y = x + 4

print(x)
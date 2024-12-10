from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.agents import tool
from langchain.agents import create_react_agent
from langchain.agents import AgentExecutor
from langchain import hub
import requests
from langchain import hub
from langchain.prompts import PromptTemplate
from pdf_vector_pipeline import getData
# Initialize the ChatOpenAI model
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0
)

embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

@tool
def claim_base_retrieval(text: str) -> str:
    """
    If a particular user needs to retrieve claim details, you'll need the claim ID, which is a 5-digit number. If the user provides a 4-digit number,
    ask them to enter it again. Once you have the 5-digit number, you can use it as the claim ID. This tool will then send a
    request to an external API and return the claim details as a JSON response
    """

    numbers = [word for word in text.split() if word.isdigit()]
    if numbers:
        claimId = numbers[0]
        print("Claim ID:", claimId)  # Output: Claim ID: 1456
        url = f"http://localhost:8082/claims?claim_id={claimId}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status() 
            print("Response:", response.json())
            return response.json()
        except requests.exceptions.RequestException as e:
            print("An error occurred:", e)
            return "use didn't give the claim id should ask him to provide now"
    else:
        return "use didn't give the claim id should ask him to provide now"


@tool
def policy_base_retrieval(text: str) -> str:
    """
      You can use this tool if a user requests to check or retrieve their insurance policy details.
      It will send a request to an external API and return the current policy details as a JSON response.
      If needed, you may also use the knowledge_base_retrieval tool to gather more information about the user’s enrolled insurance policy.
    """

    userdId = "09cb0a5b-d34a-458e-84a9-cf1c7c8bc53e"
    url = f"http://localhost:8082/policy?user_id={userdId}"
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        print("Response:", response.json())
        return response.json()
    except requests.exceptions.RequestException as e:
       return "api request failed can't get user insurance policy for the moment"


@tool
def knowledge_base_retrieval(text: str) -> int:
    """You can use this whenever a user asks about common insurance policies or claims. It could be related to policy lists, FAQs, claim limits more details, or similar information. Use this tool for that purpose.
    """
    data = getData(text)
    return data


tools = [knowledge_base_retrieval, claim_base_retrieval, policy_base_retrieval ]

def init(msg):
    prompt = hub.pull("hwchase17/react")
    print(prompt)

    agent = create_react_agent(tools=tools, llm=llm, prompt= prompt, stop_sequence=True)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

    response = agent_executor.invoke(
        {
            "input":msg,
            "chat_history": [
                SystemMessage(content="You are an AI agent specialized in assisting users with insurance-related questions"),
            ],
        }
    )

    print(response['input'])
    return response

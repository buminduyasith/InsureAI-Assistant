from langchain_openai import ChatOpenAI
import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.agents import tool
from langchain.agents import create_react_agent
from langchain.agents import AgentExecutor
from langchain import hub
import requests

# os.environ['OPENAI_API_KEY'] = open_api_key

# Initialize the ChatOpenAI model
llm = ChatOpenAI(

    model="gpt-3.5-turbo",
    temperature=0
)

embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

# # Load the PDF document
# loader = PyPDFLoader("test2.pdf")
#
# docs = loader.load()


@tool
def word_count(text: str) -> int:
    """Returns the word count."""
    return len(text.split())


@tool
def api_base_retrieval(text: str) -> str:
    """If a particular user needs to get a claim details you can use this tool to continue you need claim id which is 5 digits number
    if you didnt get a 4 digits number ask him to enter it again if user gave the 5 digits number you can use that as the claim id.
    if we get the claim id this tool will send a request external api and give the claim detail as json

    """

    numbers = [word for word in text.split() if word.isdigit()]
    if numbers:
        claimId = numbers[0]
        print("Claim ID:", claimId)  # Output: Claim ID: 1456
        url = f"http://localhost:8082/claims?claim_id={claimId}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raise HTTPError for bad responses
            print("Response:", response.json())
            return response.json()
        except requests.exceptions.RequestException as e:
            print("An error occurred:", e)
    else:
        return "use didn't give the claim id should ask him to provide it to continue"


@tool
def knowledge_base_retrieval(text: str) -> int:
    """You can use this when ever user ask regarding common insurance policy or claims stuff it might be the policy
    list or can FAQ or something use this tool
    """

    data = """
    [Insurance Company Name] - Car Insurance Policy
        Policy Number: XYZ123456
        Policy Holder: [Full Name] Policy Holder Address: [Address] Effective Date: [Start Date] 
        Expiration Date: [End Date]
        Coverage Details:
        • Vehicle Covered: [Make, Model, Year]
        • Coverage Type: Collision, Comprehensive, Liability, and Roadside Assistance
        • Coverage Amount: $50,000 for collision damage, $10,000 for personal injury, $20,000 for 
        property damage, and $5,000 for roadside assistance.
        Premium Details:
        • Premium Amount: $500.00 per year
        • Payment Frequency: Annually
        • Payment Due Date: [Due Date]
        Exclusions:
        • Loss or damage caused by the policyholder’s intentional actions.
        • Loss or damage while the vehicle is being used for commercial purposes.
        • Wear and tear, mechanical breakdowns, and regular maintenance are not covered.
        Claims Procedure:
        • In the event of an accident or damage, the policyholder must report the incident to 
        [Insurance Company Name] immediately and provide details including date, time, location, 
        and description of the accident.
        • The policyholder must not admit fault or responsibility to any other party or insurance 
        company.
        • For a claim to be processed, the policyholder must submit photographs of the damage, an 
        incident report, and a valid police report (if applicable).
        • A claim form must be completed and submitted within 30 days of the incident.
        Claim Limits:
        • Maximum coverage for collision damage: $50,000
        • Maximum coverage for property damage: $20,000
        • Maximum coverage for personal injury: $10,000
        • Maximum coverage for roadside assistance: $5,000
    """

    return data


# List of tools for the agent
tools = [knowledge_base_retrieval, api_base_retrieval]

def init():
    # Pull the prompt template from LangChainHub
    prompt = hub.pull("hwchase17/react")
    print(prompt)
    agent = create_react_agent(tools=tools, llm=llm, prompt=prompt)

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
    # response = agent_executor.invoke(
    #     {"input": "can you explain me the claim procedures and claim limits"})

    response = agent_executor.invoke(
    {"input": "can you give me claim status my claim id is"})
    print(response['output'])
    return response

init()
# history
# agent_executor.invoke(
#     {
#         "input": "what's my name? Don't use tools to look this up unless you NEED to",
#         "chat_history": [
#             HumanMessage(content="hi! my name is bob"),
#             AIMessage(content="Hello Bob! How can I assist you today?"),
#         ],
#     }
# )
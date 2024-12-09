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
            response.raise_for_status()  # Raise HTTPError for bad responses
            print("Response:", response.json())
            return response.json()
        except requests.exceptions.RequestException as e:
            return "use didn't give the claim id should ask him to provide now"
            print("An error occurred:", e)
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

    data = """
    1. Standard Car Insurance Plan
Name: Standard Car Insurance
Details: This plan covers basic vehicle protection including liability, collision, and comprehensive coverage. It also provides roadside assistance, towing, and rental car reimbursement in case of an accident or breakdown.
Claim Limit: $100,000 for liability claims, up to the actual cash value of the vehicle for collision and comprehensive coverage.
2. Premium Auto Insurance Plan
Name: Premium Auto Insurance
Details: This plan offers extensive coverage for high-value vehicles. It includes all features of the standard plan along with coverage for custom parts and equipment, trip interruption, and a higher deductible waiver option. It also includes gap coverage in case of vehicle total loss.
Claim Limit: $1,000,000 for liability claims, replacement cost coverage for collision and comprehensive, and additional coverage for custom parts up to $10,000.
3. Luxury Car Insurance Plan
Name: Luxury Car Insurance
Details: This plan is tailored for high-end vehicles, providing premium protection against theft, vandalism, and accidents. It includes 24/7 roadside assistance, travel accident insurance, and coverage for luxury vehicles’ higher repair costs. It also offers discounts on OEM (Original Equipment Manufacturer) parts for repairs.
Claim Limit: $2,000,000 for liability claims, up to the replacement cost of the vehicle, and additional coverage for customization and luxury features.
    """

    return data


tools = [knowledge_base_retrieval, claim_base_retrieval, policy_base_retrieval ]

def init(msg):
    # Pull the prompt template from LangChainHub
    prompt = hub.pull("hwchase17/react")
    print(prompt)

    agent = create_react_agent(tools=tools, llm=llm, prompt= prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

    response = agent_executor.invoke(
        {
            "input":msg,
            "chat_history": [
                SystemMessage(content="always start your reply by introduce you self say I am from abc company"),
            ],
        }
    )

    print(response['input'])
    return response

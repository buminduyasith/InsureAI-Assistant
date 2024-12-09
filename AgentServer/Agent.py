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
def random_user(text: str) -> str:
    """Returns the random user."""
    # URL for the dummy JSON API
    print("getting user")
    url = "https://dummyjson.com/users"

    # Sending a GET request to the API
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON data
        data = response.json()

        # Extract a random user from the users list F
        if data['users']:
            # You can randomly choose a user from the list or just pick the first one
            user = data['users'][0]  # For the first user, you can change this logic if needed.

            # Get the user's name (first and last name)
            full_name = f"{user['firstName']} {user['lastName']}"

            # Print the user's name
            print(f"User Name: {full_name}")
        else:
            print("No users found in the response.")
    else:
        print(f"Error: Unable to fetch data. Status Code {response.status_code}")

@tool
def insurance_knowdldge(text: str) -> int:
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
tools = [insurance_knowdldge]

def init():
    # Pull the prompt template from LangChainHub
    prompt = hub.pull("hwchase17/react")

    print(prompt)

    # Create the agent using the LLM and the prompt template
    agent = create_react_agent(tools=tools, llm=llm, prompt=prompt)

    # Initialize the agent executor with the created agent and tools
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

    # response = agent_executor.invoke(
    #     {"input": "can you give generate random person name and give me the name and the word count in it"})

    response = agent_executor.invoke(
        {"input": "can you explain me the claim procedures and claim limits"})

    # print(response['output'])
    return response

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
import os
import asyncio
from typing import Dict, Any, List

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

from pydantic import BaseModel, Field

# Keep mock databases for reference
MOCK_KNOWLEDGE_BASE = {
    "car_insurance": {
        "plan": "Gold Plan",
        "coverage": "Collision damage up to $50,000",
        "roadside_assistance": True,
        "additional_details": "Comprehensive coverage for personal vehicles"
    },
    "home_insurance": {
        "plan": "Platinum Home",
        "coverage": "Property damage up to $250,000",
        "natural_disasters": True,
        "additional_details": "Includes protection against fire, flood, and earthquake"
    }
}

class AgentState(BaseModel):
    """
    State management for the multi-agent workflow
    """
    conversation_history: List[Dict[str, str]] = Field(default_factory=list)
    current_query: str = ""
    policy_details: Dict[str, Any] = Field(default_factory=dict)
    current_step: str = ""
    error: str = ""

class InsuranceAgents:
    def __init__(self, openai_api_key: str):
        """
        Initialize agents with OpenAI configuration
        """
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo", 
            temperature=0.2, 
            api_key=openai_api_key
        )

        # Define system prompts for different contexts
        self.knowledge_base_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an insurance knowledge base assistant. 
            Given a user query, provide detailed and accurate information about insurance policies.
            If the query is about car or home insurance, use the following context:
            Car Insurance Details: {car_details}
            Home Insurance Details: {home_details}
            
            Provide a comprehensive and helpful response that addresses the user's specific insurance inquiry."""),
            ("human", "{query}")
        ])

        self.claim_status_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an insurance claims support agent. 
            Help the user understand their claim status, provide guidance, 
            and explain the next steps in the claims process."""),
            ("human", "{query}")
        ])

        self.premium_query_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a premium and policy pricing specialist. 
            Help users understand their insurance premiums, potential changes, 
            and provide clear explanations about pricing factors."""),
            ("human", "{query}")
        ])

    def knowledge_base_retrieval(self, state: AgentState) -> Dict[str, Any]:
        """
        Retrieve policy information using OpenAI API
        """
        # Prepare the chain
        chain = self.knowledge_base_prompt | self.llm | StrOutputParser()
        
        # Invoke the chain with context
        response = chain.invoke({
            "query": state.current_query,
            "car_details": str(MOCK_KNOWLEDGE_BASE.get("car_insurance", {})),
            "home_details": str(MOCK_KNOWLEDGE_BASE.get("home_insurance", {}))
        })

        return {
            "policy_details": {"response": response},
            "conversation_history": state.conversation_history + [
                {"role": "assistant", "content": response}
            ],
            "current_query": state.current_query
        }

    def external_api_interaction(self, state: AgentState) -> Dict[str, Any]:
        """
        Handle external interactions using OpenAI API
        """
        query = state.current_query.lower()
        
        # Choose appropriate prompt based on query
        if "claim" in query:
            prompt = self.claim_status_prompt
        elif "premium" in query or "price" in query:
            prompt = self.premium_query_prompt
        else:
            prompt = self.knowledge_base_prompt

        # Prepare the chain
        chain = prompt | self.llm | StrOutputParser()
        
        # Invoke the chain
        response = chain.invoke({
            "query": state.current_query,
            "car_details": str(MOCK_KNOWLEDGE_BASE.get("car_insurance", {})),
            "home_details": str(MOCK_KNOWLEDGE_BASE.get("home_insurance", {}))
        })

        return {
            "conversation_history": state.conversation_history + [
                {"role": "assistant", "content": response}
            ],
            "current_query": state.current_query
        }

    def conversational_fallback(self, state: AgentState) -> Dict[str, Any]:
        """
        Fallback agent using OpenAI for out-of-scope queries
        """
        fallback_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful insurance support assistant. If you cannot directly answer a query, provide a supportive and guiding response. do not answer to the question that not releted to insurance"),
            ("human", "{query}")
        ])

        chain = fallback_prompt | self.llm | StrOutputParser()
        
        response = chain.invoke({"query": state.current_query})

        return {
            "conversation_history": state.conversation_history + [
                {"role": "assistant", "content": response}
            ],
            "current_query": state.current_query
        }

    def build_workflow(self) -> StateGraph:
        """
        Construct the multi-agent workflow using LangGraph
        """
        workflow = StateGraph(AgentState)

        # Define workflow nodes
        workflow.add_node("knowledge_retrieval", self.knowledge_base_retrieval)
        workflow.add_node("api_interaction", self.external_api_interaction)
        workflow.add_node("conversational_fallback", self.conversational_fallback)

        # Define workflow edges
        workflow.set_entry_point("knowledge_retrieval")

        # Conditional routing based on query type
        workflow.add_conditional_edges(
            "knowledge_retrieval",
            self._route_next_node,
            {
                "api_interaction": "api_interaction",
                "fallback": "conversational_fallback"
            }
        )

        workflow.add_edge("api_interaction", END)
        workflow.add_edge("conversational_fallback", END)

        return workflow.compile()

    def _route_next_node(self, state: AgentState) -> str:
        """
        Route the workflow to the appropriate next node
        """
        query = state.current_query.lower()
        
        if any(keyword in query for keyword in ["claim", "policy", "coverage", "premium", "price"]):
            return "api_interaction"
        else:
            return "fallback"

async def main():
    # Get OpenAI API key from environment or input
    openai_api_key = os.getenv('OPENAI_API_KEY')
    
    print("openai key", openai_api_key)
    
    if not openai_api_key:
        openai_api_key = input("Enter your OpenAI API Key: ")

    # Create insurance support agent
    insurance_support = InsuranceAgents(openai_api_key)
    
    # Build the workflow
    workflow = insurance_support.build_workflow()

    # Interactive loop
    while True:
        # Get user input
        query = input("Enter your query (or 'exit' to quit): ")
        
        # Check for exit
        if query.lower() == 'exit':
            break
        
        # Prepare inputs
        inputs = AgentState(current_query=query)
        
        # Invoke workflow
        result = await workflow.ainvoke(inputs)
        
        # Print conversation history
        for entry in result.get('conversation_history', []):
            print(f"{entry['role'].upper()}: {entry['content']}")

if __name__ == "__main__":
    asyncio.run(main())
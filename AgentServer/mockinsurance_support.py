import os
import asyncio
from typing import Dict, Any, List

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

from pydantic import BaseModel, Field

# Mock Knowledge Base
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

# Mock Claim Status Database
MOCK_CLAIMS_DB = {
    "98765": {
        "claim_id": "98765",
        "status": "In Review",
        "last_updated": "2024-12-01",
        "policy_type": "Car Insurance"
    },
    "54321": {
        "claim_id": "54321", 
        "status": "Approved",
        "last_updated": "2024-11-15",
        "policy_type": "Home Insurance"
    }
}

# Mock Premium Calculation
MOCK_PREMIUM_CALCULATOR = {
    "98765": {
        "current_premium": 500.0,
        "new_premium": 650.0,
        "coverage_increase": 30
    }
}

class AgentState(BaseModel):
    """
    State management for the multi-agent workflow
    """
    conversation_history: List[Dict[str, str]] = Field(default_factory=list)
    current_query: str = ""
    policy_details: Dict[str, Any] = Field(default_factory=dict)
    claim_status: Dict[str, Any] = Field(default_factory=dict)
    current_step: str = ""
    error: str = ""

class MockInsuranceAgents:
    def __init__(self, mock_key: str = "mock_key"):
        """
        Initialize agents with mock configurations
        """
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo", 
            temperature=0.2, 
            api_key=mock_key
        )

    def knowledge_base_retrieval(self, state: AgentState) -> Dict[str, Any]:
        """
        Mock knowledge base retrieval
        """
        query = state.current_query.lower()
        
        # Simple keyword matching for policy retrieval
        if "car" in query:
            policy_info = MOCK_KNOWLEDGE_BASE.get("car_insurance", {})
        elif "home" in query:
            policy_info = MOCK_KNOWLEDGE_BASE.get("home_insurance", {})
        else:
            policy_info = {"error": "No matching policy found"}

        response = f"""Policy Details:
Plan: {policy_info.get('plan', 'N/A')}
Coverage: {policy_info.get('coverage', 'N/A')}
Additional Info: {policy_info.get('additional_details', 'No additional details')}
"""

        return {
            "policy_details": policy_info,
            "conversation_history": state.conversation_history + [
                {"role": "assistant", "content": response}
            ],
            "current_query": state.current_query
        }

    def validate_claim_input(self, state: AgentState) -> Dict[str, Any]:
        """
        Mock input validation
        """
        validation_result = "Input appears valid. Ready to proceed with claim."

        return {
            "current_step": "input_validation",
            "conversation_history": state.conversation_history + [
                {"role": "assistant", "content": validation_result}
            ],
            "current_query": state.current_query
        }

    def external_api_interaction(self, state: AgentState) -> Dict[str, Any]:
        """
        Mock external API interaction
        """
        query = state.current_query.lower()
        
        # Simulate claim status retrieval
        if "claim" in query:
            # Extract claim ID (simulating)
            claim_id = "98765"  # Default mock claim ID
            claim_status = MOCK_CLAIMS_DB.get(claim_id, {"error": "Claim not found"})
            
            response = f"""Claim Status:
Claim ID: {claim_status.get('claim_id', 'N/A')}
Status: {claim_status.get('status', 'N/A')}
Last Updated: {claim_status.get('last_updated', 'N/A')}
"""
            return {
                "claim_status": claim_status,
                "conversation_history": state.conversation_history + [
                    {"role": "assistant", "content": response}
                ],
                "current_query": state.current_query
            }
        
        # Simulate premium calculation
        elif "premium" in query:
            premium_details = MOCK_PREMIUM_CALCULATOR.get("98765", {})
            
            response = f"""Premium Calculation:
Current Premium: ${premium_details.get('current_premium', 'N/A')}
New Premium: ${premium_details.get('new_premium', 'N/A')}
Coverage Increase: {premium_details.get('coverage_increase', 'N/A')}%
"""
            return {
                "claim_status": premium_details,
                "conversation_history": state.conversation_history + [
                    {"role": "assistant", "content": response}
                ],
                "current_query": state.current_query
            }
        
        return {
            "error": "Unable to process the request",
            "current_step": "api_error",
            "current_query": state.current_query
        }

    def conversational_fallback(self, state: AgentState) -> Dict[str, Any]:
        """
        Fallback agent for handling out-of-scope queries
        """
        fallback_response = "I'm afraid I couldn't find specific information for your query. Could you please rephrase or provide more details?"

        return {
            "conversation_history": state.conversation_history + [
                {"role": "assistant", "content": fallback_response}
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
        workflow.add_node("input_validation", self.validate_claim_input)
        workflow.add_node("api_interaction", self.external_api_interaction)
        workflow.add_node("conversational_fallback", self.conversational_fallback)

        # Define workflow edges
        workflow.set_entry_point("knowledge_retrieval")

        # Conditional routing based on query type
        workflow.add_conditional_edges(
            "knowledge_retrieval",
            self._route_next_node,
            {
                "validate_input": "input_validation",
                "api_interaction": "api_interaction",
                "fallback": "conversational_fallback"
            }
        )

        workflow.add_edge("input_validation", "api_interaction")
        workflow.add_edge("api_interaction", END)
        workflow.add_edge("conversational_fallback", END)

        return workflow.compile()

    def _route_next_node(self, state: AgentState) -> str:
        """
        Route the workflow to the appropriate next node
        """
        query = state.current_query.lower()
        
        if "claim" in query:
            return "validate_input"
        elif any(keyword in query for keyword in ["policy", "coverage", "premium"]):
            return "api_interaction"
        else:
            return "fallback"

async def main():
    # Create insurance support agent
    insurance_support = MockInsuranceAgents("key")
    
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
import json
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from config import OPENAI_API_KEY, TABLE_MAP_PATH, METRICS_REGISTRY_PATH
from app.langchain_integration.tools import execute_analytics_query, generate_chart_payload

class PromptProcessor:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=OPENAI_API_KEY, temperature=0)
        self.tools = [execute_analytics_query, generate_chart_payload]
        
        with open(TABLE_MAP_PATH, 'r') as f:
            self.table_map = json.load(f)
        with open(METRICS_REGISTRY_PATH, 'r') as f:
            self.metrics_registry = json.load(f)

        # Create the agent
        prompt = ChatPromptTemplate.from_messages([
            ("system", 
                "You are an expert data analyst. Use the provided tools to answer user requests.\n"
                "AVAILABLE TABLES:\n{tables}\n\n"
                "AVAILABLE METRICS:\n{metrics}\n\n"
                "1. First, use 'execute_analytics_query' to get the data.\n"
                "2. Then, use 'generate_chart_payload' to create a visualization.\n"
                "3. Finally, return a JSON object with 'query_object', 'analytics', and 'chart'."
            ),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        agent = create_openai_functions_agent(self.llm, self.tools, prompt)
        self.agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)

    def process(self, user_input: str) -> Dict[str, Any]:
        # We want the agent to return a structured JSON. 
        # We can guide it in the system prompt.
        
        table_context = json.dumps(self.table_map, indent=2)
        metrics_context = json.dumps(self.metrics_registry, indent=2)

        response = self.agent_executor.invoke({
            "input": user_input,
            "tables": table_context,
            "metrics": metrics_context
        })
        
        # The agent's output should ideally be a JSON string.
        # If it's not, we might need a parser, but GPT-3.5 with functions is usually good.
        try:
            # Try to find JSON in the output
            content = response['output']
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            return json.loads(content)
        except:
            # Fallback if the agent doesn't return clean JSON
            return {"error": "Agent failed to return structured JSON", "raw_output": response['output']}

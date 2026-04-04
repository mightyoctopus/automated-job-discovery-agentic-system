from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv
from openai import OpenAI

from agents.query_agent import QueryAgent

@dataclass
class JobPipeline:
    """
    Orchestrate the main workflow of LLM agents and functions for the job discovery automation
    """

    load_dotenv()

    def run(self):
        print("The main program started running")

        client = OpenAI()
        print(f"OpenAI model was loaded successfully: {client}")

        query_agent = QueryAgent(client)
        serp_queries, exa_queries = query_agent.get_queries()

        print(f"SERP Len: {len(serp_queries)} | Queries: {serp_queries}")
        print(f"EXA len: {len(exa_queries)} | Queries: {exa_queries}")
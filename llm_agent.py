# llm_agent.py

import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

MODEL = "openrouter/cypher-alpha:free"

def load_context(path="mcp.json"):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        return {"error": str(e)}

def ask_llm(question: str):
    context = load_context()
    if "error" in context:
        return f"[ERROR] Could not load context: {context['error']}"

    system_prompt = (
        "You are an intelligent assistant that answers questions about GitHub repositories. "
        "Use the following MCP context to answer user questions.\n\n"
        + json.dumps(context, indent=2)
    )

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[ERROR] LLM failed: {str(e)}"

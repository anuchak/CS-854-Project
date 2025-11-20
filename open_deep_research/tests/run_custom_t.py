import os
import time  # Added for timing
import asyncio
import uuid
from dotenv import load_dotenv
from langsmith import Client

import sys
from pathlib import Path
module_path = Path(__file__).resolve().parent.parent / "src" / "open_deep_research"
print(module_path)
sys.path.append(str(module_path))
from deep_researcher import deep_researcher_builder

from langgraph.checkpoint.memory import MemorySaver

# --- Configuration ---
os.environ["OPENAI_API_KEY"] = "dummy"
os.environ["OPENAI_API_BASE"] = "http://localhost:8000/v1"

load_dotenv("../.env")

# Configurable Parameters
max_structured_output_retries = 3
allow_clarification = False
max_concurrent_research_units = 10
search_api = "tavily"
max_researcher_iterations = 6
max_react_tool_calls = 10
summarization_model = "openai:Alibaba-NLP/Tongyi-DeepResearch-30B-A3B"
summarization_model_max_tokens = 8192

research_model = "openai:Alibaba-NLP/Tongyi-DeepResearch-30B-A3B"
research_model_max_tokens = 30000
compression_model = "openai:Alibaba-NLP/Tongyi-DeepResearch-30B-A3B"
compression_model_max_tokens = 30000
final_report_model = "openai:Alibaba-NLP/Tongyi-DeepResearch-30B-A3B"
final_report_model_max_tokens = 30000

# --- Core Logic ---

async def target(inputs: dict):
    """
    Runs the Deep Research graph for a single input.
    """
    graph = deep_researcher_builder.compile(checkpointer=MemorySaver())
    config = {
        "configurable": {
            "thread_id": str(uuid.uuid4()),
            # Pass all your configs here
            "max_structured_output_retries": max_structured_output_retries,
            "allow_clarification": allow_clarification,
            "max_concurrent_research_units": max_concurrent_research_units,
            "search_api": search_api,
            "max_researcher_iterations": max_researcher_iterations,
            "max_react_tool_calls": max_react_tool_calls,
            "summarization_model": summarization_model,
            "summarization_model_max_tokens": summarization_model_max_tokens,
            "research_model": research_model,
            "research_model_max_tokens": research_model_max_tokens,
            "compression_model": compression_model,
            "compression_model_max_tokens": compression_model_max_tokens,
            "final_report_model": final_report_model,
            "final_report_model_max_tokens": final_report_model_max_tokens,
            # Ensure tools are enabled (critical for vLLM/Tavily)
            "use_tools": True,
            "allow_tools": True,
            "enable_tools": True,
        }
    }

    print("Graph compiled. Invoking agent...")
    
    # 'inputs' is expected to match the structure: {"messages": [{"content": "..."}]}
    final_state = await graph.ainvoke(
        {"messages": [{"role": "user", "content": inputs["messages"][0]["content"]}]},
        config
    )
    return final_state

# --- Main Execution ---

async def main():
    # 1. Define your Single Prompt here
    my_prompt = "You have access to multiple parallel research agents. Do not wait for one topic to finish before starting another. If you need to research 'Competitors', 'Pricing', and 'Features', issue 3 separate 'ConductResearch' tool calls immediately in a single response.Write a paper to discuss the influence of AI interaction on interpersonal relations, considering AI's potential to fundamentally change how and why individuals relate to each other."

    print(f"\nStarting Single Run Request: '{my_prompt}'")
    print("-" * 50)

    # 2. Construct the input dictionary to mimic the dataset format
    single_input = {
        "messages": [
            {"content": my_prompt}
        ]
    }

    # 3. Start Timer
    start_time = time.time()

    # 4. Call target() directly (bypassing LangSmith evaluation)
    try:
        result = await target(single_input)
        success = True
    except Exception as e:
        print(f"An error occurred: {e}")
        success = False
        result = None

    # 5. Stop Timer
    end_time = time.time()
    duration = end_time - start_time

    print("-" * 50)
    if success:
        print(f"✅ Run Complete.")
        print(f"⏱️  Total Duration: {duration:.2f} seconds")
        
        # Optional: Print the final report if available in the state
        # The structure depends on the graph, but usually the last message is the answer
        if "messages" in result:
            print("\n--- Final Response ---")
            print(result["messages"][-1].content)
    else:
        print("❌ Run Failed.")

if __name__ == "__main__":
    asyncio.run(main())
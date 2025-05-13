from transformers import load_tool
from smolagents.tools import Tool

prompt_generator_tool = Tool.from_space(
    "sergiopaniego/Promptist", name="generator_tool", description="Optimizes user input into model-preferred prompts"
)

image_generation_tool = load_tool("m-ric/text-to-image", trust_remote_code=True)
from smolagents import CodeAgent
from code_agents import *


MasterAgent = CodeAgent(
    managed_agents=[
        WebsearchAgent,
        GoogleMapAgent,
        ImageGenerationAgent,
        ProfessionalAgent
    ],
    model = configs.MODELS["master_agent"],
    instructions = configs.INSTRUCTIONS["master_agent"],
    verbosity_level = configs.VERBOSITY_LEVEL["master_agent"],
    verbose = configs.VERBOSE["master_agent"],
    plannning_interval = configs.PLANNING_INTERVAL["master_agent"],
    max_steps = configs.MAX_STEPS["master_agent"],
    prompt_templates = configs.PROMPT_TEMPLATES["master_agent"]
)
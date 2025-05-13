from ...config import all_configs
from ...tools import smolagents_tools
from smolagents import CodeAgent

configs = all_configs["smolagents"]

GoogleSearchTool = smolagents_tools["GoogleSearchTool"]
DuckDuckGoSearchTool = smolagents_tools["DuckDuckGoSearchTool"]
WebSearchTool = smolagents_tools["WebSearchTool"]
ConvertedGooglePlacesTool = smolagents_tools["ConvertedGooglePlacesTool"]
calculate_haversine_distance = smolagents_tools["calculate_haversine_distance"]
prompt_generator_tool = smolagents_tools["prompt_generator_tool"]
image_generation_tool = smolagents_tools["image_generation_tool"]
ResumeScraperTool = smolagents_tools["ResumeScraperTool"]
LinkedInJobSearchTool = smolagents_tools["LinkedInJobSearchTool"]

WebsearchAgent = CodeAgent(
    tools=[
        GoogleSearchTool("serper"),
        DuckDuckGoSearchTool(),
        WebSearchTool()
    ],
    model = configs.MODELS["websearch_agent"],
    instructions = configs.INSTRUCTIONS["websearch_agent"],
    verbosity_level = configs.VERBOSITY_LEVEL["websearch_agent"],
    verbose = configs.VERBOSE["websearch_agent"],
    additional_authorized_imports = configs.ADDITIONAL_AUTHORIZED_IMPORTS["websearch_agent"],
    max_steps = configs.MAX_STEPS["websearch_agent"],
    prompt_templates = configs.PROMPT_TEMPLATES["websearch_agent"]
)

GoogleMapAgent = CodeAgent(
    tools=[
        ConvertedGooglePlacesTool(),
        GoogleSearchTool("serper"),
        calculate_haversine_distance
    ],
    model = configs.MODELS["google_map_agent"],
    instructions = configs.INSTRUCTIONS["google_map_agent"],
    verbosity_level = configs.VERBOSITY_LEVEL["google_map_agent"],
    verbose = configs.VERBOSE["google_map_agent"],
    additional_authorized_imports = configs.ADDITIONAL_AUTHORIZED_IMPORTS["google_map_agent"],
    max_steps = configs.MAX_STEPS["google_map_agent"],
    prompt_templates = configs.PROMPT_TEMPLATES["google_map_agent"]
)

ImageGenerationAgent = CodeAgent(
    tools=[prompt_generator_tool, image_generation_tool], 
    model=configs.MODELS["image_generation_agent"],
    instructions=configs.INSTRUCTIONS["image_generation_agent"],
    verbosity_level=configs.VERBOSITY_LEVEL["image_generation_agent"],
    verbose=configs.VERBOSE["image_generation_agent"],
    additional_authorized_imports=configs.ADDITIONAL_AUTHORIZED_IMPORTS["image_generation_agent"],
    max_steps=configs.MAX_STEPS["image_generation_agent"],
    prompt_templates = configs.PROMPT_TEMPLATES["image_generation_agent"]
)

ProfessionalAgent = CodeAgent(
    tools=[
        ResumeScraperTool(),
        LinkedInJobSearchTool()
    ],
    model = configs.MODELS["professional_agent"],
    instructions = configs.INSTRUCTIONS["professional_agent"],
    verbosity_level = configs.VERBOSITY_LEVEL["professional_agent"],
    verbose = configs.VERBOSE["professional_agent"],
    additional_authorized_imports = configs.ADDITIONAL_AUTHORIZED_IMPORTS["professional_agent"],
    max_steps = configs.MAX_STEPS["professional_agent"],
    prompt_templates = configs.PROMPT_TEMPLATES["professional_agent"]
)

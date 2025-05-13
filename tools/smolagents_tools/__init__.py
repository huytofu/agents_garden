from smolagents import PythonInterpreterTool,FinalAnswerTool,UserInputTool,WebSearchTool,DuckDuckGoSearchTool,GoogleSearchTool,VisitWebpageTool,WikipediaSearchTool,SpeechToTextTool
from .simple_tools import initialize_driver,search_item_ctrl_f,go_back,close_popups,calculate_haversine_distance
from .community_tools import ResumeScraperTool,LinkedInJobSearchTool
from .research_tools import ArxivSearchTool
from .image_tools import prompt_generator_tool,image_generation_tool
from .langchain_tools import ConvertedGooglePlacesTool

smolagents_tools = {
    #default smolagents tools
    "PythonInterpreterTool": PythonInterpreterTool,
    "FinalAnswerTool": FinalAnswerTool,
    "UserInputTool": UserInputTool,
    "WebSearchTool": WebSearchTool,
    "DuckDuckGoSearchTool": DuckDuckGoSearchTool,
    "GoogleSearchTool": GoogleSearchTool, 
    "VisitWebpageTool": VisitWebpageTool, 
    "WikipediaSearchTool": WikipediaSearchTool,
    "SpeechToTextTool": SpeechToTextTool,
    #simple tools
    "initialize_driver": initialize_driver,
    "search_item_ctrl_f": search_item_ctrl_f,
    "go_back": go_back,
    "close_popups": close_popups, 
    "calculate_haversine_distance": calculate_haversine_distance,
    #community tools
    "ResumeScraperTool": ResumeScraperTool,
    "LinkedInJobSearchTool": LinkedInJobSearchTool,
    #langchain community tools
    "ConvertedGooglePlacesTool": ConvertedGooglePlacesTool,
    #research tools
    "ArxivSearchTool": ArxivSearchTool,
    #image tools
    "prompt_generator_tool": prompt_generator_tool,    
    "image_generation_tool": image_generation_tool
}

__all__ = [
    "smolagents_tools"
]















import yaml

prompts = {
    "smolagents": {},
    "llamaindex": {}
}

for prompt_name in [
    "websearch_agent", 
    "google_map_agent", 
    "image_generation_agent", 
    "professional_agent"
]:
    with open(f"prompts/smolagents/{prompt_name}.yaml", 'r') as stream:
        prompt_templates = yaml.safe_load(stream)
        prompts["smolagents"][prompt_name] = prompt_templates


all_configs = {
    "smolagents": {
        "websearch_agent": {
            "model": "gpt-4o-mini",
            "description": "This is a websearch agent equipped with many web-related tools. It is capable of searching the web for information, navigating around websites, and more.",
            "verbosity_level": 2,
            "verbose": True,
            "additional_authorized_imports": ["helium", "selenium", "requests"],
            "prompt_templates": prompts["smolagents"]["websearch_agent"],
            "max_steps": 5
        },
        "google_map_agent": {
            "model": "gpt-4o-mini",
            "description": "This is a google map agent equipped with many google map-related tools. It is capable of using google map for sites' information, distance between two points, directions, and more.",
            "verbosity_level": 2,
            "verbose": True,
            "additional_authorized_imports": ["math"],
            "prompt_templates": prompts["smolagents"]["google_map_agent"],
            "max_steps": 5
        },
        "image_generation_agent": {
            "model": "gpt-4o-mini",
            "description": "This is a image generation agent equipped with many image generation-related tools. It is capable of generating images based on the prompt.",
            "additional_authorized_imports": ["transformers"],
            "prompt_templates": prompts["smolagents"]["image_generation_agent"]
        },
        "professional_agent": {
            "model": "gpt-4o-mini",
            "description": "This is a professional agent equipped with many professional-related tools. It is capable of scraping resumes, roasting resumes, linkedin job searching, and more.",
            "verbosity_level": 1,
            "verbose": True,
            "additional_authorized_imports": ["requests", "typing"],
            "prompt_templates": prompts["smolagents"]["professional_agent"],
            "max_steps": 5
        },
        "master_agent": {
            "model": "gpt-4o-mini",
            "description": """
                This is a master agent that can help the user with their question 
                by delegating tasks to the appropriate agent or agents in its managed 
                list of agents. It can also try to solve the question in multiple 
                steps and have one of its managed agents solve each step if necessary.
            """,
            "verbosity_level": 2,
            "verbose": True,
            "max_steps": 20,
            "plannning_interval": 5,
            "prompt_templates": prompts["smolagents"]["master_agent"]
        }
    }
}
from langchain_community.tools import GooglePlacesTool
from smolagents.tools import Tool

ConvertedGooglePlacesTool = Tool.from_langchain(GooglePlacesTool())
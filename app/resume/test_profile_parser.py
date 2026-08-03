from profile_parser import ProfileParser

profile = """
Python
FastAPI
Machine Learning
Deep Learning
LangChain
TensorFlow
React
LLMs
AI Agents
Docker
"""

parser = ProfileParser()

result = parser.parse(profile)

print(result)
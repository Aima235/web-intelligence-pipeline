from ai.llm_client import LLMClient

llm = LLMClient()

response = llm.generate("Say hello in one sentence.")

print(response)
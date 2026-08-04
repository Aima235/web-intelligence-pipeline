from app.ai.llm_client import LLMClient


def test_llm_client_creation():
    """Test that the LLM client initializes successfully."""

    llm = LLMClient()

    assert llm is not None
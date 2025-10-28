"""
Direct LLM test to diagnose JSON response issues.
"""

from src.modules.docugen.shared.core import create_chat_model
from loguru import logger

def test_llm_response():
    """Test what the LLM actually returns."""

    # Create LLM model
    llm_model = create_chat_model(
        base_url="http://localhost:11434/v1",
        model_name="mistral-nemo:latest",
        api_key_env=None,
        timeout=120
    )

    # Simple test prompt
    prompt = """You are a technical documentation specialist. Generate documentation for this C# class:

**Element Type**: Class
**Element Name**: Calculator
**Element Signature**: class Calculator

**Full File Context**:
```csharp
namespace MathLibrary
{
    public class Calculator
    {
        public int Add(int a, int b)
        {
            return a + b;
        }
    }
}
```

Provide your documentation in valid JSON format:
```json
{
  "description": "2-3 sentence description of the class",
  "purpose": "One sentence high-level purpose"
}
```
"""

    logger.info("Calling LLM...")
    response = llm_model.invoke(prompt)

    logger.info("LLM Response:")
    content = response.content if hasattr(response, 'content') else str(response)
    logger.info(f"Content length: {len(content)}")
    logger.info(f"Content type: {type(content)}")
    logger.info(f"Full content:\n{content}")

    # Try extraction
    logger.info("\nTrying JSON extraction...")
    if "```json" in content:
        logger.info("Found ```json marker")
        extracted = content.split("```json")[1].split("```")[0].strip()
        logger.info(f"Extracted content:\n{extracted}")
    elif "```" in content:
        logger.info("Found ``` marker")
        extracted = content.split("```")[1].split("```")[0].strip()
        logger.info(f"Extracted content:\n{extracted}")
    else:
        logger.info("No code block markers found")
        extracted = content.strip()
        logger.info(f"Raw content:\n{extracted}")

    # Try parsing
    import json
    try:
        data = json.loads(extracted)
        logger.info(f"Successfully parsed JSON: {data}")
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing failed: {e}")
        logger.error(f"Failed content: '{extracted}'")

if __name__ == "__main__":
    test_llm_response()

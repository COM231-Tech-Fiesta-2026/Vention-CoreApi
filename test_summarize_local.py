import asyncio
from src.ventio_api.services.llm_service import summarize

async def test():
    conversation = """
    User: I'm feeling really overwhelmed with work lately
    AI: I hear you, that sounds stressful. Tell me more about what's happening
    User: My boss keeps piling on tasks and I can't keep up. I feel like I'm failing
    AI: That's a tough situation. You're not failing - you're dealing with unrealistic expectations.
    User: Yeah, I think I should talk to my boss. Thanks for listening
    AI: You're welcome. Remember, it's okay to set boundaries
    """
    
    result = await summarize(conversation)
    print("Result:")
    print(result)

if __name__ == "__main__":
    asyncio.run(test())
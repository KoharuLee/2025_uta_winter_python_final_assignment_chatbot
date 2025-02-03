from groq import Groq

client = Groq(api_key="GET_YOUR_API")

def query_llm(prompt: str, model: str = "llama-3.3-70b-versatile") -> str:
    messages = [
        {
            "role": "user",
            "content": prompt,
        }
    ]

    chat_completion = client.chat.completions.create(
        messages=messages,
        model=model,
    )
    
    response = chat_completion.choices[0].message.content
    return response

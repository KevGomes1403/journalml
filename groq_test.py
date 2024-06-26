import os

from groq import Groq

client = Groq(
    api_key="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",
)
def chat_with_groq(client, initial_message, model="mixtral-8x7b-32768", temperature=0.5, max_tokens=1024, top_p=1):
    # Initialize the conversation with a system message
    messages = [{"role": "system", "content": "you are a helpful assistant."}]
    
    # Add the initial user message
    messages.append({"role": "user", "content": initial_message})
    
    while True:
        # Create a chat completion request
        stream = client.chat.completions.create(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stream=True
        )

        # Print the incremental deltas returned by the LLM
        assistant_message = ""
        for chunk in stream:
            if chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="")
                assistant_message += chunk.choices[0].delta.content

            if chunk.choices[0].finish_reason:
                # Usage information is available on the final chunk
                assert chunk.x_groq is not None
                assert chunk.x_groq.usage is not None
                print(f"\n\nUsage stats: {chunk.x_groq.usage}")
                break
        
        # Ask for the next user input
        user_message = input("\n\nYour response: ")

        # Add the assistant and user messages to the conversation history
        messages.append({"role": "assistant", "content": assistant_message})
        messages.append({"role": "user", "content": user_message})


# Start the chat with an initial message
chat_with_groq(client, "Explain the importance of low latency LLMs")

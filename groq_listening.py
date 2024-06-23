from groq import Groq

def chat_with_groq(client, message, model="mixtral-8x7b-32768", temperature=0.5, max_tokens=1024, top_p=1):
    # Initialize the conversation with a system message
    messages = [{"role": "system", "content": "You're a supportive friend who listens attentively and understands deeply. When someone shares their thoughts and feelings with you, focus on acknowledging their emotions with empathy and validating their experiences. Use open-ended questions to delve into their situation, encouraging them to reflect on their thoughts and gain deeper insights into themselves. Show genuine interest in their perspective, asking thoughtful questions that prompt self-reflection and exploration. Avoid giving direct advice but offer gentle prompts that guide them to consider different aspects of their situation. Keep responses concise, maintaining a natural, comforting tone throughout the conversation. ADHERE TO THIS RULE: Only personal insight questions, not more than 10 words, and always generate 3 questions."}]
    
    # Add the initial user message
    messages.append({"role": "user", "content": message})
    
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
        
        print('\n')

        # Create the incremental deltas returned by the LLM
        assistant_message = ""
        for chunk in stream:
            if chunk.choices[0].delta.content:
                assistant_message += chunk.choices[0].delta.content

        # Add the assistant message to the conversation history
        messages.append({"role": "assistant", "content": assistant_message})

        return assistant_message


client = Groq(
    api_key="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", 
) #implement your own api key here
entry = '''
June 23, 2024

Today has been one of those whirlwind days where time seems to slip through my fingers. I woke up earlier than usual, around 5:30 AM, because I had to prepare for a presentation at work. The nerves kept me from having a proper breakfast—just a quick cup of coffee and a piece of toast as I went over my notes one last time. 

The drive to the office was surprisingly smooth, which was a relief. I used the extra time to gather my thoughts and mentally rehearse. The presentation itself went better than I expected. There were a few tricky questions from the board, but I managed to handle them with confidence. My boss seemed pleased, which is always a good sign.

After the presentation, I had back-to-back meetings. The first one was with the marketing team to discuss the upcoming campaign. We brainstormed some exciting ideas, but there was a bit of tension when it came to budget allocations. I hope we can sort that out without too much hassle.

Lunch was a quick affair—a sandwich and a salad eaten at my desk while catching up on emails. There’s a big project deadline looming, and the number of unread messages in my inbox is staggering. I managed to clear a good chunk of them, but there are still so many left.

The afternoon was even more hectic. I had a conference call with a potential new client, which went surprisingly well. They seemed interested in our proposal, but I need to follow up with some additional information. I also had to review some reports and prepare for another meeting tomorrow. 

By the time 5 PM rolled around, I felt like I had run a marathon. I quickly packed up and headed home, hoping for a bit of relaxation. But as soon as I walked through the door, I remembered I had promised to help Alex with his science project. We spent the next couple of hours constructing a model volcano, which was fun but exhausting.

Now, it’s almost 8 PM, and I still need to finish some work. My mind is buzzing with thoughts and to-do lists. It's completely understandable that I'm feeling overwhelmed after such a busy day. I handled many challenges with grace and confidence, but it's taking its toll on me now.

As the day winds down, I find myself reflecting on everything that's happened. I can't help but feel a sense of accomplishment mixed with exhaustion. There's still so much on my mind—emails to send, follow-ups to make, and preparations for tomorrow. I'm worried I might forget something important, but I also know I need to rest.

I guess what I need most right now is a moment of peace to clear my head. Maybe I'll make myself a cup of tea and take a few minutes to breathe and relax. Writing in this journal helps, too. It gives me a chance to sort through my thoughts and let go of some of the stress.

I'm grateful for the little victories today, like the successful presentation and the positive client call. It's these moments that keep me going, even when things get overwhelming. But I also need to remember to take care of myself and not let the pressure get to me too much.

I think I'll wrap this up for now and try to unwind a bit before tackling the rest of my tasks. Tomorrow is another day, and I need to be ready for whatever comes next. 
'''

print("Entry: \n" + entry + "\n")

# Start the chat with an initial message
print(chat_with_groq(client, entry))

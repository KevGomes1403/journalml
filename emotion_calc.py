import asyncio
from hume import HumeStreamClient
from hume.models.config import LanguageConfig

# user_input = '''
# Today has been one of those whirlwind days where time seems to slip through my fingers. I woke up earlier than usual, around 5:30 AM, because I had to prepare for a presentation at work. The nerves kept me from having a proper breakfast—just a quick cup of coffee and a piece of toast as I went over my notes one last time. 

# The drive to the office was surprisingly smooth, which was a relief. I used the extra time to gather my thoughts and mentally rehearse. The presentation itself went better than I expected. There were a few tricky questions from the board, but I managed to handle them with confidence. My boss seemed pleased, which is always a good sign.

# After the presentation, I had back-to-back meetings. The first one was with the marketing team to discuss the upcoming campaign. We brainstormed some exciting ideas, but there was a bit of tension when it came to budget allocations. I hope we can sort that out without too much hassle.

# Lunch was a quick affair—a sandwich and a salad eaten at my desk while catching up on emails. There’s a big project deadline looming, and the number of unread messages in my inbox is staggering. I managed to clear a good chunk of them, but there are still so many left.

# The afternoon was even more hectic. I had a conference call with a potential new client, which went surprisingly well. They seemed interested in our proposal, but I need to follow up with some additional information. I also had to review some reports and prepare for another meeting tomorrow. 

# By the time 5 PM rolled around, I felt like I had run a marathon. I quickly packed up and headed home, hoping for a bit of relaxation. But as soon as I walked through the door, I remembered I had promised to help Alex with his science project. We spent the next couple of hours constructing a model volcano, which was fun but exhausting.

# Now, it’s almost 8 PM, and I still need to finish some work. My mind is buzzing with thoughts and to-do lists. It's completely understandable that I'm feeling overwhelmed after such a busy day. I handled many challenges with grace and confidence, but it's taking its toll on me now.

# As the day winds down, I find myself reflecting on everything that's happened. I can't help but feel a sense of accomplishment mixed with exhaustion. There's still so much on my mind—emails to send, follow-ups to make, and preparations for tomorrow. I'm worried I might forget something important, but I also know I need to rest.

# I guess what I need most right now is a moment of peace to clear my head. Maybe I'll make myself a cup of tea and take a few minutes to breathe and relax. Writing in this journal helps, too. It gives me a chance to sort through my thoughts and let go of some of the stress.

# I'm grateful for the little victories today, like the successful presentation and the positive client call. It's these moments that keep me going, even when things get overwhelming. But I also need to remember to take care of myself and not let the pressure get to me too much.

# I think I'll wrap this up for now and try to unwind a bit before tackling the rest of my tasks. Tomorrow is another day, and I need to be ready for whatever comes next. 
# '''

dictionary = {
    'Admiration': 0, 'Adoration': 0, 'Aesthetic Appreciation': 0, 'Amusement': 0,
    'Anger': 0, 'Annoyance': 0, 'Anxiety': 0, 'Awe': 0, 'Awkwardness': 0, 'Boredom': 0,
    'Calmness': 0, 'Concentration': 0, 'Confusion': 0, 'Contemplation': 0, 'Contempt': 0,
    'Contentment': 0, 'Craving': 0, 'Determination': 0, 'Disappointment': 0, 'Disapproval': 0,
    'Disgust': 0, 'Distress': 0, 'Doubt': 0, 'Ecstasy': 0, 'Embarrassment': 0, 'Empathic Pain': 0,
    'Enthusiasm': 0, 'Entrancement': 0, 'Envy': 0, 'Excitement': 0, 'Fear': 0, 'Gratitude': 0,
    'Guilt': 0, 'Horror': 0, 'Interest': 0, 'Joy': 0, 'Love': 0, 'Nostalgia': 0, 'Pain': 0,
    'Pride': 0, 'Realization': 0, 'Relief': 0, 'Romance': 0, 'Sadness': 0, 'Sarcasm': 0,
    'Satisfaction': 0, 'Desire': 0, 'Shame': 0, 'Surprise (negative)': 0, 'Surprise (positive)': 0,
    'Sympathy': 0, 'Tiredness': 0, 'Triumph': 0
}

async def analyze_emotions(user_input):
    client = HumeStreamClient("j8lpIcgDAtcfCNGCeEG267BoC7tJriRsY50jclNfWnECpnhZ")
    config = LanguageConfig()
    
    # Adjust the chunk size dynamically based on input length
    chunk_size = max(100, len(user_input) // 10) 
    tests = chunk_string(user_input, chunk_size)
    
    async with client.connect([config]) as socket:
        for chunk in tests:
            result = await socket.send_text(chunk)
            emotions = result["language"]["predictions"][0]["emotions"]
            for item in emotions:
                name = item['name']
                score = item['score']
                if name in dictionary:
                    dictionary[name] += score
    
    # Sort the dictionary by values in descending order
    sorted_scores = dict(sorted(dictionary.items(), key=lambda item: item[1], reverse=True))
    return sorted_scores

def chunk_string(string, chunk_size):
    return [string[i:i+chunk_size] for i in range(0, len(string), chunk_size)]

async def hume_scores(user_input):
    scores = await analyze_emotions(user_input)
    return scores

#print(asyncio.run(hume_scores(user_input)))

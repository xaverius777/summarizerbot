# A file used to generate texts, which was used to create the texts I used for experimenting
# when creating the agent. You need an OpenAI API key to run it.
import os
import random
from openai import OpenAI
from time import sleep
api_key = ""
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY", api_key),
)
topics = ["telecommunications", "space_exploration", "satellites", "astrophysics", "astronomy", "spacecraft_building"]
no_texts = 10
target_folder = r"C:\Users\javic\PycharmProjects\texts_for_summarizerbot"
system_prompt = "You are a scientific journalist especialized in writing articles about space. The user will ask you to " \
                "write a text about one of several topics related to space and you will write the article with several paragraphs, " \
                "using a formal style and conventions. You should explain everything so every reader gets access to the knowledge, " \
                "but make sure the text is still enjoyable, it should be enjoyed by people who are new to the field and experts alike. " \
                " Your target public is specifically the readers of a scientific magazine published by a prestigious research " \
                "institution"

# Ensure the target folder exists
os.makedirs(target_folder, exist_ok=True)

# Track how many texts have been generated for each topic
topic_counts = {topic: 0 for topic in topics}

# Generate texts
for _ in range(1, no_texts + 1):
    topic = random.choice(topics)
    topic_counts[topic] += 1
    # print(f"Generating text about {topic}")
    filename = f"{topic}_{topic_counts[topic]}.txt"
    filepath = os.path.join(target_folder, filename)

    user_prompt = f"Write an educative and engaging article about the following topic: {topic}."

    response = client.chat.completions.create(
        model="gpt-4",  # or gpt-3.5-turbo if preferred
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        # max_tokens=800
    )

    #generated_text = response["choices"][0]["message"]["content"]
    #print(response.choices[0].message.content)
    generated_text = response.choices[0].message.content
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(generated_text)
    print(f"Text {filepath} was generated and put in the target folder")
    sleep(5)

print(f"{no_texts} texts have been generated and saved to '{target_folder}'.")

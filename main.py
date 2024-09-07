"""
Main file. Probably the backbone idk.
"""

import os
from dotenv import load_dotenv
from groq import Groq
import sqlite3


load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
system_prompt = {
    "role": "system",
    "content": os.environ.get("prompt"),
}

chat_history = [system_prompt]


def load_chat_history():
    history = []
    conn = sqlite3.connect("HISTORY.db")
    query = "SELECT name from sqlite_master WHERE type='table' AND name='HIST';"
    cursor = conn.execute(query)
    result = cursor.fetchone()
    if result == None:
        cur = conn.cursor()
        query = "CREATE TABLE HIST(ID,USER_MESSAGE,RESPONSE)"
        cur.execute(query)
        conn.close()
    else:
        cursor = conn.execute("SELECT USER_MESSAGE,RESPONSE FROM HIST;")
        for row in cursor:
            temp_history = {}
            temp_history["role"] = "user"
            temp_history["content"] = row[0]
            temp_history["role"] = "assistant"
            temp_history["content"] = row[1]
            history.append(temp_history)
        conn.close()
    return history


chat_history += load_chat_history()
# print(load_chat_history)
print(chat_history)


def ai_response(chat_history):
    # Get user input from the console
    user_input = input("You: ")

    # Append the user input to the chat history
    chat_history.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="llama3-70b-8192", messages=chat_history, max_tokens=100, temperature=1.2
    )
    # Append the response to the chat history
    chat_history.append(
        {"role": "assistant", "content": response.choices[0].message.content}
    )
    # Print the response
    print("Assistant:", response.choices[0].message.content)


def save_chat_history(chat_history):
    conn = sqlite3.connect("HISTORY.db")
    ID = 0
    j = 0
    for i in range(int((len(chat_history) - 1) / 2)):
        conn.execute(
            """INSERT INTO HIST (ID, USER_MESSAGE, RESPONSE)
				VALUES (?,?,?)""",
            (ID, chat_history[j + 1]["content"], chat_history[j + 2]["content"]),
        )
        j += 2
        conn.commit()
    cursor = conn.execute("SELECT id, user_message,response from HIST")
    conn.close()


for i in range(5):
    ai_response(chat_history)
save_chat_history(chat_history)
print(len(chat_history))

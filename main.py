"""
Main file. Probably the backbone idk.
"""

import os
from dotenv import load_dotenv
from groq import Groq
import sqlite3
import sys


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
    query = "SELECT name from sqlite_master WHERE type='table' AND name='HIST';"  # checks if table exists
    cursor = conn.execute(query)
    result = cursor.fetchone()
    if result == None:  # if not creates the table
        cur = conn.cursor()
        query = "CREATE TABLE HIST(ID,USER_MESSAGE,RESPONSE)"
        cur.execute(query)
        conn.close()
    else:  # if table exists selects user and response for response function
        cursor = conn.execute("SELECT * FROM HIST;")
        for row in cursor:
            temp_history = {"role": "user", "content": row[1]}
            history.append(temp_history)
            temp_history = {"role": "assistant", "content": row[2]}
            history.append(temp_history)
        conn.close()
    return history


chat_history += load_chat_history()  # load it
temp_history = chat_history.copy()


def ai_response(chat_history, user_input):
    # Get user input from the console
    # Append the user input to the chat history
    chat_history.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="llama3-70b-8192", messages=chat_history, max_tokens=100, temperature=1.2
    )
    if response.choices[0].message.content.startswith("!"):
        chat_history.append(  # Append the response to the chat history
            {"role": "assistant", "content": response.choices[0].message.content[2:]}
        )

        print(
            "Assistant:", response.choices[0].message.content[2:]
        )  # Print the response
        save_chat_history()
        sys.exit()
    else:
        chat_history.append(  # Append the response to the chat history
            {"role": "assistant", "content": response.choices[0].message.content}
        )

        print("Assistant:", response.choices[0].message.content)


def save_chat_history():
    conn = sqlite3.connect("HISTORY.db")
    ID = 0
    j = 0
    to_commit = [system_prompt]
    for i in chat_history:
        if i not in temp_history:
            to_commit.append(i)

    for i in range(int((len(to_commit) - 1) / 2)):
        if (
            to_commit[j + 1]["role"] == "user"
            and to_commit[j + 2]["role"] == "assistant"
        ):
            conn.execute(  # execute
                """INSERT INTO HIST (ID, USER_MESSAGE, RESPONSE)
		    		VALUES (?,?,?)""",
                (
                    ID,
                    to_commit[j + 1]["content"],
                    to_commit[j + 2]["content"],
                ),  # adds input, response to database for loading and memeory.
            )
            ID += 1
            j += 2
            conn.commit()
    conn.close()


while True:
    user_input = input("You: ")
    ai_response(chat_history, user_input)  # infinite loop whee

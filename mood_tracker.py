from nltk.sentiment import SentimentIntensityAnalyzer
import sqlite3
import datetime


def load_chat_history():
    history = []
    conn = sqlite3.connect("HISTORY.db")
    cursor = conn.execute("SELECT USER_MESSAGE FROM HIST;")
    for row in cursor:
        history.append(row)
    conn.close()
    return history


history = load_chat_history()


def mood_score(text):
    sia = SentimentIntensityAnalyzer()
    sentiment = sia.polarity_scores(text)
    # Compound score is a normalized score ranging from -1 to 1
    sentiment_score = sentiment["compound"]
    # Convert to mood score (e.g., 1 to 10 scale)
    mood_score = (sentiment_score + 1) * 5  # Scale: 0 to 10
    return mood_score


def save_mood_score(history):
    time = datetime.datetime.now()
    id = 0
    conn = sqlite3.connect("mood_tracker.db")
    query = "SELECT name from sqlite_master WHERE type='table' AND name='MOOD';"  # checks if table exists
    cursor = conn.execute(query)
    result = cursor.fetchone()
    if result == None:  # if not creates the table
        cur = conn.cursor()
        query = "CREATE TABLE MOOD(ID,MESSAGE,MOOD_SCORE, DATETIME)"
        cur.execute(query)
        for message in history:
            if int(mood_score(message[0])) != 5:
                conn.execute(
                    """
                        INSERT INTO MOOD (ID,MESSAGE,MOOD_SCORE,DATETIME)
                        VALUES (?,?,?,?)""",
                    (id, message[0], round(mood_score(message[0]), 2), time),
                )
                conn.commit()
                id += 1

    else:
        for message in history:

            if int(mood_score(message[0])) != 5:
                conn.execute(
                    """
                        INSERT INTO MOOD (ID,MESSAGE,MOOD_SCORE,DATETIME)
                        VALUES (?,?,?,?)""",
                    (id, message[0], mood_score(message[0]), time),
                )
                conn.commit()
                id += 1
    conn.close()


save_mood_score(history)

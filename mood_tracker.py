from nltk.sentiment import SentimentIntensityAnalyzer
import sqlite3
import datetime


def load_chat_history():
    history = []
    time = []
    conn = sqlite3.connect("HISTORY.db")
    cursor = conn.execute("SELECT USER_MESSAGE,TIME FROM HIST;")
    for row in cursor:
        history.append(row[0])
        time.append(row[1])
    conn.close()
    return history,time


history,time = load_chat_history()
print(history,time)

def mood_score(text):
    sia = SentimentIntensityAnalyzer()
    sentiment = sia.polarity_scores(text)
    # Compound score is a normalized score ranging from -1 to 1
    sentiment_score = sentiment["compound"]
    # Convert to mood score (e.g., 1 to 10 scale)
    mood_score = (sentiment_score + 1) * 5  # Scale: 0 to 10
    return mood_score


def save_mood_score(history,time):
    id = 0
    i = 0
    conn = sqlite3.connect("mood_tracker.db")
    query = "SELECT name from sqlite_master WHERE type='table' AND name='MOOD';"  # checks if table exists
    cursor = conn.execute(query)
    result = cursor.fetchone()
    if result == None:  # if not creates the table
        cur = conn.cursor()
        query = "CREATE TABLE MOOD(ID,MESSAGE,MOOD_SCORE, TIME)"
        cur.execute(query)
        for i in range(len(history)):
            if int(mood_score(history[i])) != 5:
                print(history[i])
                conn.execute(
                    """
                        INSERT INTO MOOD (ID,MESSAGE,MOOD_SCORE,TIME)
                        VALUES (?,?,?,?)""",
                    (id, history[i],round(mood_score(history[i]), 2), time[i]),
                )
                conn.commit()

                id += 1

    else:
        for i in range(len(history)):
            if int(mood_score(history[i])) != 5:
                conn.execute(
                    """
                        INSERT INTO MOOD (ID,MESSAGE,MOOD_SCORE,DATETIME)
                        VALUES (?,?,?,?)""",
                    (id, history[i], round(mood_score(history[i]), 2), time[i]),
                )
                conn.commit()
                id += 1
    conn.close()


save_mood_score(history,time)

import matplotlib.pyplot as plt
import mplcursors
import sqlite3


def mood_graph():
    x = []
    y = []
    labels = []
    conn = sqlite3.connect("mood_tracker.db")
    cur = conn.execute("""SELECT DATETIME,MOOD_SCORE,MESSAGE FROM MOOD""")
    for row in cur:
        x.append(row[0][:16])
        y.append(row[1])
        labels.append(row[2])
    conn.close()

    fig, ax = plt.subplots()
    (line,) = ax.plot(
        x,
        y,
        color="black",
        linestyle="-",
        linewidth=2,
        marker="o",
        markersize=8,
        markeredgecolor="black",
        markerfacecolor="white",
    )
    # Use mplcursors to add tooltips
    cursor = mplcursors.cursor(line, hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(labels[int(sel.index)]))

    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.title("Interactive Plot with Hover Tooltips")
    plt.show()
    plt.close(fig)


mood_graph()

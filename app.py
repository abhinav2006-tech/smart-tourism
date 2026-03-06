from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

# ---------------- DATABASE ----------------
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS destinations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        description TEXT,
        location TEXT,
        best_time TEXT,
        famous_for TEXT,
        image TEXT
    )
    """)

    # Check if data already exists
    cursor.execute("SELECT COUNT(*) FROM destinations")
    count = cursor.fetchone()[0]

    # Insert data ONLY if table is empty
    if count == 0:
        cursor.executemany("""
        INSERT INTO destinations 
        (name, description, location, best_time, famous_for, image)
        VALUES (?, ?, ?, ?, ?, ?)
        """, [

        ("Taj Mahal",
        "The Taj Mahal is a UNESCO World Heritage Site built by Emperor Shah Jahan in memory of Mumtaz Mahal.",
        "Agra, Uttar Pradesh",
        "October to March",
        "Mughal architecture, white marble beauty",
        "https://upload.wikimedia.org/wikipedia/commons/d/da/Taj-Mahal.jpg"),

        ("Mysore Palace",
        "Mysore Palace is a historic royal residence known for its Indo-Saracenic architecture.",
        "Mysore, Karnataka",
        "October to February",
        "Royal heritage, Dussehra festival",
        "https://upload.wikimedia.org/wikipedia/commons/4/4c/Mysore_Palace_Morning.jpg"),

        ("Golden Temple",
        "The Golden Temple in Amritsar is the holiest shrine of Sikhism.",
        "Amritsar, Punjab",
        "October to March",
        "Spiritual center, golden dome",
        "https://upload.wikimedia.org/wikipedia/commons/3/3e/Golden_Temple%2C_Amritsar.jpg"),

        ("Goa Beaches",
        "Goa is famous for its scenic beaches, nightlife and Portuguese heritage.",
        "Goa",
        "November to February",
        "Beaches, water sports, nightlife",
        "https://upload.wikimedia.org/wikipedia/commons/2/2c/Goa_beach.jpg")

        ])

    conn.commit()
    conn.close()


# ---------------- HOME PAGE ----------------
@app.route("/")
def home():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM destinations")
    destinations = cursor.fetchall()
    conn.close()

    return render_template("home.html", destinations=destinations)


# ---------------- DESTINATION DETAILS ----------------
@app.route("/destination/<int:id>")
def destination(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM destinations WHERE id=?", (id,))
    place = cursor.fetchone()
    conn.close()

    return render_template("destination.html", place=place)


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
import streamlit as st
import pandas as pd
st.title("Sunway Club Activities Portal")

# Sample activities
activities = [
    "Basketball Training",
    "Robotics Workshop",
    "Coding Bootcamp",
    "Photography Club",
    "Debate Competition"
]

# Session state to store registrations
if "registered" not in st.session_state:
    st.session_state.registered = []

st.header("Available Activities")

# Show activities with buttons
for activity in activities:
    col1, col2 = st.columns([3, 1])

    with col1:
        st.write(activity)

    with col2:
        if st.button(f"Join {activity}"):
            if activity not in st.session_state.registered:
                st.session_state.registered.append(activity)
                st.success(f"You joined {activity}")
            else:
                st.warning("Already registered!")

st.divider()

st.header("Your Registered Activities")

if st.session_state.registered:
    for item in st.session_state.registered:
        st.write("✅", item)
else:
    st.info("No activities registered yet.")

# ---------------------------
# Session State Setup
# ---------------------------
if "posts" not in st.session_state:
    st.session_state.posts = []

if "registrations" not in st.session_state:
    st.session_state.registrations = {}

# ---------------------------
# CREATE NEW POST
# ---------------------------
st.header("📌 Create a New Post")

with st.form("post_form"):
    title = st.text_input("Event Title")
    category = st.selectbox("Category", ["Activity", "Tournament", "Workshop", "Other"])
    description = st.text_area("Description")
    date = st.date_input("Event Date")

    submitted = st.form_submit_button("Post Event")

    if submitted:
        if title:
            post = {
                "title": title,
                "category": category,
                "description": description,
                "date": str(date),
                "created_at": str(datetime.now())
            }
            st.session_state.posts.append(post)
            st.success("Event posted successfully!")
        else:
            st.error("Title is required!")

# ---------------------------
# VIEW POSTS
# ---------------------------
st.divider()
st.header("📋 All Club Events")

if not st.session_state.posts:
    st.info("No events posted yet.")
else:
    for i, post in enumerate(st.session_state.posts):
        st.subheader(f"{post['title']} ({post['category']})")
        st.write("📅 Date:", post["date"])
        st.write(post["description"])

        # Register button
        if st.button(f"Register for {post['title']}", key=f"reg_{i}"):
            if post["title"] not in st.session_state.registrations:
                st.session_state.registrations[post["title"]] = True
                st.success(f"Registered for {post['title']}")
            else:
                st.warning("Already registered!")

        st.divider()

# ---------------------------
# USER REGISTRATIONS
# ---------------------------
st.header("📝 My Registrations")

if not st.session_state.registrations:
    st.info("You haven't registered for any events yet.")
else:
    for event in st.session_state.registrations:
        st.write("✅", event)
import streamlit as st
from datetime import datetime

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="Sunway Club Hub", page_icon="🎓", layout="wide")

st.title("🎓 Sunway Club Hub")
st.caption("Activities • Tournaments • Workshops • Community Board")

# ---------------------------
# SESSION STATE
# ---------------------------
if "posts" not in st.session_state:
    st.session_state.posts = []

if "registrations" not in st.session_state:
    st.session_state.registrations = set()

# ---------------------------
# CREATE POST (SIDEBAR)
# ---------------------------
st.sidebar.header("📌 Create Event")

with st.sidebar.form("create_event_form"):  # ✅ FIXED KEY
    title = st.text_input("Event Title")
    category = st.selectbox(
        "Category",
        ["🎯 Activity", "🏆 Tournament", "📚 Workshop", "✨ Other"]
    )
    description = st.text_area("Description")
    date = st.date_input("Event Date")

    submitted = st.form_submit_button("Post Event")

    if submitted:
        if title:
            st.session_state.posts.append({
                "title": title,
                "category": category,
                "description": description,
                "date": str(date),
                "created_at": str(datetime.now())
            })
            st.success("Event posted!")
        else:
            st.error("Title is required!")

# ---------------------------
# EVENTS DISPLAY
# ---------------------------
st.subheader("📋 Upcoming Events")

if not st.session_state.posts:
    st.info("No events yet. Create one from the sidebar 👈")
else:
    for i, post in enumerate(reversed(st.session_state.posts)):
        with st.container():
            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(f"### {post['category']} {post['title']}")
                st.write(f"📅 **Date:** {post['date']}")
                st.write(post["description"])

            with col2:
                if post["title"] in st.session_state.registrations:
                    st.success("✅ Registered")
                else:
                    if st.button("Register", key=f"reg_{i}"):
                        st.session_state.registrations.add(post["title"])
                        st.rerun()

        st.markdown("---")

# ---------------------------
# REGISTRATIONS
# ---------------------------
st.subheader("📝 My Registrations")

if not st.session_state.registrations:
    st.info("No registrations yet.")
else:
    for event in st.session_state.registrations:
        st.markdown(f"- 🎟️ {event}")

import streamlit as st
import sqlite3
from datetime import datetime

# ---------------------------
# DB SETUP
# ---------------------------
conn = sqlite3.connect("club.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    role TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    category TEXT,
    description TEXT,
    date TEXT,
    created_at TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS registrations (
    username TEXT,
    event_id INTEGER
)
""")

conn.commit()

# ---------------------------
# SESSION STATE
# ---------------------------
if "user" not in st.session_state:
    st.session_state.user = None

if "role" not in st.session_state:
    st.session_state.role = None

# ---------------------------
# LOGIN SYSTEM
# ---------------------------
def login():
    st.title("🎓 Sunway Club Login")

    username = st.text_input("Username")
    role = st.selectbox("Role", ["student", "admin"])

    if st.button("Login"):
        st.session_state.user = username
        st.session_state.role = role

        c.execute("INSERT OR IGNORE INTO users VALUES (?, ?)", (username, role))
        conn.commit()

        st.rerun()

# ---------------------------
# LOGOUT
# ---------------------------
def logout():
    st.sidebar.write(f"Logged in as: {st.session_state.user} ({st.session_state.role})")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.session_state.role = None
        st.rerun()

# ---------------------------
# ADMIN PANEL (CREATE EVENTS)
# ---------------------------
def admin_panel():
    st.sidebar.header("📌 Create Event")

    with st.sidebar.form("create_event"):
        title = st.text_input("Event Title")
        category = st.selectbox("Category", ["Activity", "Tournament", "Workshop", "Other"])
        description = st.text_area("Description")
        date = st.date_input("Event Date")

        submit = st.form_submit_button("Post Event")

        if submit and title:
            c.execute(
                "INSERT INTO events VALUES (NULL, ?, ?, ?, ?, ?)",
                (title, category, description, str(date), str(datetime.now()))
            )
            conn.commit()
            st.success("Event posted!")

# ---------------------------
# STUDENT VIEW + REGISTRATION
# ---------------------------
def student_panel():
    st.subheader("📋 Events")

    events = c.execute("SELECT * FROM events").fetchall()

    if not events:
        st.info("No events yet.")
        return

    for event in events:
        event_id, title, category, desc, date, created = event

        st.markdown(f"### {category} - {title}")
        st.write("📅", date)
        st.write(desc)

        # Check registration
        reg = c.execute(
            "SELECT * FROM registrations WHERE username=? AND event_id=?",
            (st.session_state.user, event_id)
        ).fetchone()

        if reg:
            st.success("✅ Registered")
        else:
            if st.button("Register", key=f"reg_{event_id}"):
                c.execute(
                    "INSERT INTO registrations VALUES (?, ?)",
                    (st.session_state.user, event_id)
                )
                conn.commit()
                st.rerun()

        st.divider()

# ---------------------------
# ADMIN VIEW (DELETE EVENTS + STATS)
# ---------------------------
def admin_dashboard():
    st.subheader("📊 Admin Dashboard")

    events = c.execute("SELECT * FROM events").fetchall()
    users = c.execute("SELECT * FROM users").fetchall()

    st.write("👥 Users:", len(users))
    st.write("📌 Events:", len(events))

    st.subheader("🗑️ Manage Events")

    for event in events:
        event_id, title, category, desc, date, created = event

        col1, col2 = st.columns([3, 1])

        with col1:
            st.write(f"{title} ({category}) - {date}")

        with col2:
            if st.button("Delete", key=f"del_{event_id}"):
                c.execute("DELETE FROM events WHERE id=?", (event_id,))
                c.execute("DELETE FROM registrations WHERE event_id=?", (event_id,))
                conn.commit()
                st.rerun()

# ---------------------------
# MAIN APP
# ---------------------------
if not st.session_state.user:
    login()
else:
    st.title("🎓 Sunway Club Hub")

    logout()

    if st.session_state.role == "admin":
        admin_panel()
        admin_dashboard()
    else:
        student_panel()
import streamlit as st
from datetime import datetime
import sqlite3
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# 初始化数据库
def init_db():
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 timestamp TEXT,
                 user TEXT,
                 message TEXT)''')
    conn.commit()
    conn.close()

# 获取所有消息
def get_messages():
    conn = sqlite3.connect('chat.db')
    df = pd.read_sql('SELECT timestamp, user, message FROM messages ORDER BY timestamp', conn)
    conn.close()
    return df

# 添加新消息
def add_message(user, message):
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    timestamp = datetime.now().strftime("%H:%M:%S")
    c.execute("INSERT INTO messages (timestamp, user, message) VALUES (?, ?, ?)",
              (timestamp, user, message))
    conn.commit()
    conn.close()

# 初始化
init_db()
st.set_page_config(page_title="实时聊天室", page_icon="💬")

# 自动刷新：每2000毫秒刷新一次
st_autorefresh(interval=2000, key="chat_refresh")

# 用户设置
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""

with st.sidebar:
    st.title("聊天室设置")
    new_name = st.text_input("你的名字", value=st.ses

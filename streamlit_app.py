import streamlit as st
from datetime import datetime
import pandas as pd
import time

# 设置页面标题和图标
st.set_page_config(page_title="实时聊天室", page_icon="💬")

# 使用缓存存储全局聊天记录
@st.cache_data(ttl=300)  # 缓存5分钟
def get_chat_data():
    return pd.DataFrame(columns=['timestamp', 'user', 'message'])

# 使用session_state存储用户信息
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""

# 侧边栏 - 用户设置
with st.sidebar:
    st.title("聊天室设置")
    
    # 用户名输入
    new_name = st.text_input("你的名字", value=st.session_state.user_name)
    if new_name != st.session_state.user_name:
        st.session_state.user_name = new_name
        st.success(f"已设置用户名: {new_name}")
    
    # 清空聊天记录按钮
    if st.button("清空聊天记录"):
        get_chat_data.clear()  # 清空缓存
        st.success("已清空聊天记录")

# 主页面标题
st.title("💬 实时聊天室")
st.caption("多人可以同时在不同设备上聊天")

# 获取当前聊天数据
chat_data = get_chat_data()

# 显示聊天记录
for _, row in chat_data.iterrows():
    with st.chat_message(name=row['user']):
        st.write(f"**{row['user']}** ({row['timestamp']}): {row['message']}")

# 输入新消息
if prompt := st.chat_input("输入消息..."):
    if not st.session_state.user_name:
        st.warning("请先在侧边栏设置你的名字")
        st.stop()
    
    # 添加新消息到聊天记录
    new_message = {
        'timestamp': datetime.now().strftime("%H:%M:%S"),
        'user': st.session_state.user_name,
        'message': prompt
    }
    
    # 更新全局聊天数据
    updated_data = chat_data.append(new_message, ignore_index=True)
    st.cache_data.update(updated_data)  # 更新缓存
    
    # 显示新消息
    with st.chat_message(name=st.session_state.user_name):
        st.write(f"**{st.session_state.user_name}** ({new_message['timestamp']}): {prompt}")

# 自动刷新页面以获取新消息
time.sleep(3)  # 每3秒刷新一次
st.rerun()

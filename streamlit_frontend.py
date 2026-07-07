import streamlit as st
import uuid  
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = str(uuid.uuid4())

CONFIG = {"configurable": {"thread_id": st.session_state["thread_id"]}}

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.text(message["content"])

user_input = st.chat_input("user")

if user_input:
    st.session_state["message_history"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.text(user_input)

    try:
        response = chatbot.invoke({"messages": [HumanMessage(content=user_input)]}, config=CONFIG)
        ai_message = response["messages"][-1].content
    except Exception as exc:
        ai_message = str(exc)

    st.session_state["message_history"].append({"role": "assistant", "content": ai_message})
    with st.chat_message("assistant"):
        st.text(ai_message)
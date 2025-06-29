import streamlit as st
import json
import os

USER_DB_FILE = "users.json"

def load_users():
    if not os.path.exists(USER_DB_FILE):
        with open(USER_DB_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)
    with open(USER_DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

if "page" not in st.session_state:
    st.session_state.page = "login"

def login_page():
    st.title("🔐 เข้าสู่ระบบ")
    email = st.text_input("อีเมล (@gmail.com)")
    password = st.text_input("รหัสผ่าน", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("เข้าสู่ระบบ"):
            if not email.endswith("@gmail.com"):
                st.error("อีเมลต้องลงท้ายด้วย @gmail.com")
            else:
                users = load_users()
                if email not in users:
                    st.error("ไม่พบอีเมลดังกล่าวในระบบ")
                elif users[email]["password"] != password:
                    st.error("รหัสผ่านไม่ถูกต้อง")
                else:
                    st.success(f"ยินดีต้อนรับ {email}")

    with col2:
        if st.button("ลงทะเบียน"):
            st.session_state.page = "register"

def register_page():
    from PII import show_registration_form
    show_registration_form()

# Routing
if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "register":
    register_page()

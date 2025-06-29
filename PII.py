import streamlit as st
import json

USER_DB_FILE = "users.json"

def show_registration_form():
    st.title("📝 ลงทะเบียนผู้ใช้ใหม่")

    email = st.text_input("อีเมล (@gmail.com)", key="reg_email")
    password = st.text_input("รหัสผ่าน", type="password", key="reg_pass")

    if st.button("ยืนยันการลงทะเบียน"):
        if not email.endswith("@gmail.com"):
            st.error("ต้องลงท้ายด้วย @gmail.com")
            return

        try:
            with open(USER_DB_FILE, "r", encoding="utf-8") as f:
                users = json.load(f)
        except FileNotFoundError:
            users = {}

        if email in users:
            st.warning("อีเมลนี้มีอยู่แล้ว")
        else:
            users[email] = {"password": password}
            with open(USER_DB_FILE, "w", encoding="utf-8") as f:
                json.dump(users, f, indent=2, ensure_ascii=False)
            st.success("✅ ลงทะเบียนสำเร็จ! กลับไปล็อกอิน")

            if st.button("กลับไปหน้าเข้าสู่ระบบ"):
                st.session_state.page = "login"

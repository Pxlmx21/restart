import streamlit as st
import json
import os
import subprocess

USER_DB_FILE = "users.json"

# โหลดข้อมูลผู้ใช้
def load_users():
    if not os.path.exists(USER_DB_FILE):
        with open(USER_DB_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)
    with open(USER_DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# ฟังก์ชันหลัก
def main():
    st.title("Civloop")

    email = st.text_input("อีเมล")
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
            # เรียกใช้ไฟล์ PII.py
            try:
                subprocess.Popen(["python", "PII.py"])
                st.info("กรุณารอสักครู่")
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {e}")

if __name__ == "__main__":
    main()

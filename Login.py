import streamlit as st
import json
import os

# ไฟล์จำลองฐานข้อมูลผู้ใช้
USER_DB_FILE = "users.json"

# โหลดข้อมูลผู้ใช้จากไฟล์ JSON
@st.cache_data
def load_users():
    if not os.path.exists(USER_DB_FILE):
        with open(USER_DB_FILE, "w") as f:
            json.dump({}, f)
    with open(USER_DB_FILE, "r") as f:
        return json.load(f)

# บันทึกข้อมูลผู้ใช้ลงไฟล์
def save_users(users):
    with open(USER_DB_FILE, "w") as f:
        json.dump(users, f, indent=2)

# ฟังก์ชันลงทะเบียน
def register():
    st.title("\U0001F4DD ลงทะเบียน")
    email_input = st.text_input("อีเมล (เฉพาะ @gmail.com)")
    password = st.text_input("รหัสผ่าน", type="password")

    if st.button("ลงทะเบียน"):
        if not email_input.endswith("@gmail.com"):
            st.error("อีเมลต้องลงท้ายด้วย @gmail.com")
            return

        users = load_users()
        if email_input in users:
            st.warning("มีอีเมลนี้ในระบบแล้ว")
        else:
            users[email_input] = {"password": password}
            save_users(users)
            st.success("ลงทะเบียนสำเร็จ")

# ฟังก์ชันเข้าสู่ระบบ

def login():
    st.title("\U0001F511 เข้าสู่ระบบ")
    email_input = st.text_input("อีเมล")
    password = st.text_input("รหัสผ่าน", type="password")

    if st.button("เข้าสู่ระบบ"):
        users = load_users()
        if email_input in users:
            if users[email_input]["password"] == password:
                st.success(f"ยินดีต้อนรับ {email_input}")
            else:
                st.error("รหัสผ่านไม่ถูกต้อง")
        else:
            st.error("ไม่พบอีเมลดังกล่าวในระบบ")

# เมนูเลือก
st.sidebar.title("เมนู")
page = st.sidebar.radio("เลือกหน้า", ["เข้าสู่ระบบ", "ลงทะเบียน"])

if page == "เข้าสู่ระบบ":
    login()
else:
    register()

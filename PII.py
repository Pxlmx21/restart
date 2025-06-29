import streamlit as st
import json
import pandas as pd
from datetime import datetime
import os

USER_DB_FILE = "users.json"
EXCEL_FILE = "user_data.xlsx"
LOCATION_FILE = "thai_location_data.json"

# โหลดข้อมูล location
@st.cache_data

def load_location_data():
    if not os.path.exists(LOCATION_FILE):
        return {}
    with open(LOCATION_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

location_data = load_location_data()

# คำนวณอายุ

def calculate_age(birthdate):
    today = datetime.today()
    return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

def show_registration_form():
    st.title("📝 ลงทะเบียนผู้ใช้ใหม่")

    full_name = st.text_input("ชื่อ - นามสกุล")
    birth_date = st.date_input("วันเกิด")
    age = calculate_age(birth_date)
    st.write(f"อายุ: {age} ปี")

    email = st.text_input("อีเมล (@gmail.com)", key="reg_email")
    password = st.text_input("รหัสผ่าน (อย่างน้อย 8 ตัวอักษร)", type="password", key="reg_pass")

    if len(password) < 8:
        st.warning("รหัสผ่านต้องมีอย่างน้อย 8 ตัวอักษร")

    address_no = st.text_input("เลขที่บริษัท")

    province = st.selectbox("จังหวัด", options=sorted(location_data.keys()))
    district = st.selectbox("เขต/อำเภอ", options=sorted(location_data[province].keys()) if province else [])
    subdistrict = st.selectbox("แขวง/ตำบล", options=sorted(location_data[province][district].keys()) if district else [])
    postcode = location_data[province][district][subdistrict] if subdistrict else ""
    st.write(f"รหัสไปรษณีย์: {postcode}")

    phone = st.text_input("เบอร์โทรศัพท์ที่ติดต่อได้")
    status = st.selectbox("สถานะ", ["ผู้ซื้อ", "ผู้ขาย"])

    if st.button("ยืนยันข้อมูลการลงทะเบียน"):
        if not email.endswith("@gmail.com"):
            st.error("อีเมลต้องลงท้ายด้วย @gmail.com")
            return
        if len(password) < 8:
            st.error("รหัสผ่านต้องมีอย่างน้อย 8 ตัวอักษร")
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

            # บันทึกข้อมูลทั้งหมดใน Excel
            user_data = {
                "ชื่อ-นามสกุล": full_name,
                "วันเกิด": birth_date.strftime("%Y-%m-%d"),
                "อายุ": age,
                "อีเมล": email,
                "เลขที่บริษัท": address_no,
                "จังหวัด": province,
                "เขต/อำเภอ": district,
                "แขวง/ตำบล": subdistrict,
                "รหัสไปรษณีย์": postcode,
                "เบอร์โทร": phone,
                "สถานะ": status
            }

            try:
                df_exist = pd.read_excel(EXCEL_FILE)
            except FileNotFoundError:
                df_exist = pd.DataFrame()

            df_new = pd.DataFrame([user_data])
            df_combined = pd.concat([df_exist, df_new], ignore_index=True)
            df_combined.to_excel(EXCEL_FILE, index=False)

            st.success("✅ ลงทะเบียนสำเร็จแล้ว")

    if st.button("⬅️ กลับไปหน้าเข้าสู่ระบบ"):
        st.session_state.page = "login"

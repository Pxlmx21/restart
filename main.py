import streamlit as st
import json
from datetime import datetime
import pandas as pd

# โหลดข้อมูลจังหวัด-เขต-แขวง-รหัสไปรษณีย์
@st.cache_data
def load_location_data():
    with open('thai_location_data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

location_data = load_location_data()

# ฟังก์ชันคำนวณอายุจากวันเกิด
def calculate_age(birthdate):
    today = datetime.today()
    return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

# Session State สำหรับเก็บสถานะผู้ใช้
if "page" not in st.session_state:
    st.session_state.page = "login"

if "user" not in st.session_state:
    st.session_state.user = None

def login_page():
    st.title("เข้าสู่ระบบ")

    email = st.text_input("อีเมล")
    password = st.text_input("รหัสผ่าน", type="password")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("ล็อกอิน (กรอกข้อมูล)"):
            # สมมติล็อกอินสำเร็จ (ในโปรเจกต์จริงควรตรวจสอบข้อมูล)
            st.session_state.page = "form"
            st.session_state.user = email

    with col2:
        if st.button("เข้าสู่ระบบ (หน้า Homepage)"):
            # สมมติล็อกอินสำเร็จและไปหน้า Homepage
            st.session_state.page = "homepage"
            st.session_state.user = email

def form_page():
    st.title("กรอกข้อมูลส่วนตัว")

    with st.form("personal_info_form"):
        full_name = st.text_input("ชื่อ - นามสกุล")
        birth_date = st.date_input("วันเกิด")
        age = calculate_age(birth_date)
        st.write(f"อายุ: {age} ปี")

        company_address_no = st.text_input("เลขที่บริษัท")

        # Dropdown จังหวัด
        province = st.selectbox("จังหวัด", options=sorted(location_data.keys()))

        # Dropdown เขต/อำเภอ ขึ้นกับจังหวัด
        district = None
        if province:
            district = st.selectbox("เขต/อำเภอ", options=sorted(location_data[province].keys()))
        else:
            st.warning("กรุณาเลือกจังหวัด")

        # Dropdown แขวง/ตำบล ขึ้นกับเขต/อำเภอ
        subdistrict = None
        postcode = None
        if province and district:
            subdistrict = st.selectbox("แขวง/ตำบล", options=sorted(location_data[province][district].keys()))
        if province and district and subdistrict:
            postcode = location_data[province][district][subdistrict]
            st.write(f"รหัสไปรษณีย์: {postcode}")

        phone = st.text_input("เบอร์โทรศัพท์ที่ติดต่อได้")

        status = st.selectbox("สถานะ", options=["ผู้ซื้อ", "ผู้ขาย"])

        submitted = st.form_submit_button("ยืนยันข้อมูล")

        if submitted:
            data = {
                "อีเมล": st.session_state.user,
                "ชื่อ-นามสกุล": full_name,
                "วันเกิด": birth_date.strftime("%Y-%m-%d"),
                "อายุ": age,
                "เลขที่บริษัท": company_address_no,
                "จังหวัด": province,
                "เขต/อำเภอ": district,
                "แขวง/ตำบล": subdistrict,
                "รหัสไปรษณีย์": postcode,
                "เบอร์โทรศัพท์": phone,
                "สถานะ": status,
            }

            # บันทึกลง Excel
            try:
                df_existing = pd.read_excel("personal_info.xlsx")
            except FileNotFoundError:
                df_existing = pd.DataFrame()

            df_new = pd.DataFrame([data])
            df_all = pd.concat([df_existing, df_new], ignore_index=True)
            df_all.to_excel("personal_info.xlsx", index=False)

            st.success("บันทึกข้อมูลเรียบร้อยแล้ว")
            st.session_state.page = "login"  # กลับไปหน้า login หรือจะเปลี่ยนหน้าอื่นก็ได้

def homepage():
    st.title("หน้า Homepage")
    st.write(f"ยินดีต้อนรับคุณ {st.session_state.user}")
    if st.button("ออกจากระบบ"):
        st.session_state.page = "login"
        st.session_state.user = None

# Routing หน้าเว็บ
if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "form":
    form_page()
elif st.session_state.page == "homepage":
    homepage()

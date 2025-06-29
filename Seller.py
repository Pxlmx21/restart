import streamlit as st
import pandas as pd
from datetime import date, datetime
import json

# โหลดข้อมูลจังหวัด-เขต-แขวง-รหัสไปรษณีย์จากไฟล์ JSON
with open("thai_location_data.json", "r", encoding="utf-8") as f:
    location_data = json.load(f)

all_provinces = list(location_data.keys())

# ฟังก์ชันคำนวณอายุ
def calculate_age(birth_date):
    today = date.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

# ฟังก์ชันบันทึกข้อมูลลง Excel
def save_to_excel(data):
    df_new = pd.DataFrame([data])
    try:
        df_old = pd.read_excel("user_data.xlsx")
        df = pd.concat([df_old, df_new], ignore_index=True)
    except FileNotFoundError:
        df = df_new
    df.to_excel("user_data.xlsx", index=False)

# หน้าแบบฟอร์มกรอกข้อมูล

def personal_info_page():
    st.title("📋 แบบฟอร์มข้อมูลส่วนตัว")

    full_name = st.text_input("ชื่อ-นามสกุล")
    birth_date = st.date_input("วันเกิด", value=date(2000, 1, 1))
    age = calculate_age(birth_date)
    st.number_input("อายุ", value=age, disabled=True)

    st.subheader("🏢 ที่อยู่ของบริษัท")
    house_no = st.text_input("เลขที่")

    province = st.selectbox("จังหวัด", all_provinces)
    districts = list(location_data[province].keys())
    district = st.selectbox("เขต / อำเภอ", districts)

    subdistricts = list(location_data[province][district].keys())
    subdistrict = st.selectbox("แขวง / ตำบล", subdistricts)

    zipcode = location_data[province][district][subdistrict]
    st.selectbox("รหัสไปรษณีย์", [zipcode], disabled=True)

    phone = st.text_input("เบอร์โทรศัพท์ที่ติดต่อได้")
    status = st.selectbox("สถานะ", ["ผู้ซื้อ", "ผู้ขาย"])

    if st.button("✅ ยืนยันข้อมูล"):
        data = {
            "ชื่อ-นามสกุล": full_name,
            "วันเกิด": birth_date.strftime("%Y-%m-%d"),
            "อายุ": age,
            "เลขที่": house_no,
            "จังหวัด": province,
            "เขต": district,
            "แขวง": subdistrict,
            "รหัสไปรษณีย์": zipcode,
            "เบอร์โทร": phone,
            "สถานะ": status,
            "เวลาที่บันทึก": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        save_to_excel(data)
        st.success("✅ บันทึกข้อมูลเรียบร้อยแล้ว")

# หน้า Homepage
def homepage():
    st.title("🏠 Homepage")
    st.markdown("ยินดีต้อนรับเข้าสู่เว็บไซต์ของเรา!")

# หน้า Login
def login_page():
    st.title("🔐 ระบบล็อกอิน")
    email = st.text_input("อีเมล")
    password = st.text_input("รหัสผ่าน", type="password")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔑 ล็อกอิน"):
            if email and password:
                st.session_state.page = "form"
            else:
                st.warning("กรุณากรอกอีเมลและรหัสผ่าน")
    with col2:
        if st.button("➡️ เข้าสู่ระบบ"):
            st.session_state.page = "home"

# ฟังก์ชันหลัก

def main():
    st.set_page_config(page_title="ระบบเว็บ", layout="centered")
    if "page" not in st.session_state:
        st.session_state.page = "login"

    if st.session_state.page == "login":
        login_page()
    elif st.session_state.page == "form":
        personal_info_page()
    elif st.session_state.page == "home":
        homepage()

if __name__ == "__main__":
    main()

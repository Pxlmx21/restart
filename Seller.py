import streamlit as st
import pandas as pd
from datetime import date

# สำหรับใช้ dropdown
provinces = ["กรุงเทพมหานคร", "เชียงใหม่", "ชลบุรี", "ภูเก็ต", "ขอนแก่น", "นครราชสีมา", "สงขลา", "อุดรธานี", "สุราษฎร์ธานี", "อื่น ๆ"]
districts = ["เขตพระนคร", "เขตดุสิต", "เขตบางรัก", "เขตปทุมวัน", "อื่น ๆ"]
subdistricts = ["แขวงวัดสามพระยา", "แขวงสวนจิตรลดา", "แขวงมหาพฤฒาราม", "อื่น ๆ"]
postcodes = ["10200", "10300", "10500", "10110", "อื่น ๆ"]

def save_to_excel(data):
    df = pd.DataFrame([data])
    try:
        old_df = pd.read_excel("user_data.xlsx")
        df = pd.concat([old_df, df], ignore_index=True)
    except FileNotFoundError:
        pass
    df.to_excel("user_data.xlsx", index=False)

# หน้า homepage
def homepage():
    st.title("🌐 Homepage")
    st.write("ยินดีต้อนรับเข้าสู่ระบบ!")

# หน้ากรอกข้อมูล
def form_page():
    st.title("📋 กรอกข้อมูลส่วนตัว")

    full_name = st.text_input("ชื่อ-นามสกุล")
    birth_date = st.date_input("วันเกิด", value=date(2000, 1, 1))
    age = st.number_input("อายุ", min_value=1, max_value=120)
    
    st.subheader("ที่อยู่บริษัท")
    house_number = st.text_input("เลขที่")
    province = st.selectbox("จังหวัด", provinces)
    district = st.selectbox("เขต", districts)
    subdistrict = st.selectbox("แขวง", subdistricts)
    postcode = st.selectbox("รหัสไปรษณีย์", postcodes)

    phone = st.text_input("เบอร์โทรศัพท์ที่ติดต่อได้")
    status = st.selectbox("สถานะ", ["ผู้ซื้อ", "ผู้ขาย"])

    if st.button("✅ ยืนยันข้อมูล"):
        data = {
            "ชื่อ-นามสกุล": full_name,
            "วันเกิด": birth_date,
            "อายุ": age,
            "เลขที่": house_number,
            "จังหวัด": province,
            "เขต": district,
            "แขวง": subdistrict,
            "รหัสไปรษณีย์": postcode,
            "เบอร์โทรศัพท์": phone,
            "สถานะ": status,
        }
        save_to_excel(data)
        st.success("บันทึกข้อมูลเรียบร้อยแล้ว 🎉")

# --------------------------- Main App --------------------------- #
def main():
    st.set_page_config(page_title="ระบบลงทะเบียน", layout="centered")
    st.title("🔐 ระบบลงชื่อเข้าใช้")

    email = st.text_input("อีเมล")
    password = st.text_input("รหัสผ่าน", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔑 ล็อกอิน"):
            if email and password:
                st.session_state.page = "form"
            else:
                st.warning("กรุณากรอกอีเมลและรหัสผ่านให้ครบ")

    with col2:
        if st.button("➡️ เข้าสู่ระบบ"):
            st.session_state.page = "home"

    # จัดการหน้า
    if "page" not in st.session_state:
        st.session_state.page = "login"

    if st.session_state.page == "form":
        form_page()
    elif st.session_state.page == "home":
        homepage()

# เรียกโปรแกรมหลัก
if __name__ == "__main__":
    main()

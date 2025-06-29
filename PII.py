# main_app.py

import streamlit as st
import pandas as pd
from datetime import datetime, date
import os

st.set_page_config(page_title="แบบฟอร์มข้อมูลส่วนตัว", layout="centered")

st.title("📄 แบบฟอร์มกรอกข้อมูลส่วนตัว")

# ----------- ตัวเลือกจังหวัด เขต แขวง รหัสไปรษณีย์ (อย่างง่าย) --------
# สำหรับตัวอย่างนี้จะใช้แบบย่อ โดยคุณสามารถใส่ข้อมูลจริงในภายหลังได้
provinces = {
    "กรุงเทพมหานคร": {
        "เขต": ["เขตพระนคร", "เขตดุสิต"],
        "แขวง": ["แขวงวัดสามพระยา", "แขวงถนนนครไชยศรี"],
        "รหัสไปรษณีย์": ["10200", "10300"]
    },
    "เชียงใหม่": {
        "เขต": ["เมืองเชียงใหม่", "สันทราย"],
        "แขวง": ["ช้างม่อย", "สุเทพ"],
        "รหัสไปรษณีย์": ["50000", "50210"]
    },
    # เพิ่มจังหวัดอื่นตามต้องการ
}

# --------- แบบฟอร์มกรอกข้อมูล ----------
with st.form("personal_form"):
    st.subheader("1. ข้อมูลส่วนบุคคล")
    full_name = st.text_input("ชื่อ - นามสกุล")
    birth_date = st.date_input("วันเกิด", min_value=date(1900, 1, 1), max_value=date.today())
    age = date.today().year - birth_date.year - ((date.today().month, date.today().day) < (birth_date.month, birth_date.day))
    st.text_input("อายุ (ปี)", value=str(age), disabled=True)

    st.subheader("2. ที่อยู่ของบริษัท")
    house_no = st.text_input("เลขที่")

    province = st.selectbox("จังหวัด", list(provinces.keys()))
    district = st.selectbox("เขต", provinces[province]["เขต"])
    sub_district = st.selectbox("แขวง", provinces[province]["แขวง"])
    zipcode = st.selectbox("รหัสไปรษณีย์", provinces[province]["รหัสไปรษณีย์"])

    st.subheader("3. ข้อมูลติดต่อ")
    phone = st.text_input("เบอร์โทรศัพท์ที่ติดต่อได้")

    st.subheader("4. สถานะ")
    status = st.selectbox("สถานะ", ["ผู้ซื้อ", "ผู้ขาย"])

    submitted = st.form_submit_button("✅ ยืนยันข้อมูล")

if submitted:
    # เตรียมข้อมูลบันทึก
    data = {
        "ชื่อ-นามสกุล": [full_name],
        "วันเกิด": [birth_date.strftime("%Y-%m-%d")],
        "อายุ": [age],
        "เลขที่": [house_no],
        "จังหวัด": [province],
        "เขต": [district],
        "แขวง": [sub_district],
        "รหัสไปรษณีย์": [zipcode],
        "เบอร์โทรศัพท์": [phone],
        "สถานะ": [status],
        "เวลาที่ส่งข้อมูล": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    }

    df = pd.DataFrame(data)

    file_name = "data.xlsx"
    if os.path.exists(file_name):
        existing = pd.read_excel(file_name)
        df = pd.concat([existing, df], ignore_index=True)

    df.to_excel(file_name, index=False)
    st.success("✅ บันทึกข้อมูลเรียบร้อยแล้ว!")

    # แสดงปุ่มดาวน์โหลดเฉพาะผู้ดูแลระบบ (สมมุติว่าเจ้าของเว็บรู้ password)
    with st.expander("🔒 ผู้ดูแลระบบ: ดาวน์โหลดข้อมูลทั้งหมด"):
        password = st.text_input("กรุณาใส่รหัสผ่าน", type="password")
        if password == "admin123":  # ปรับรหัสได้ตามต้องการ
            st.download_button(
                label="📥 ดาวน์โหลดไฟล์ Excel",
                data=open(file_name, "rb"),
                file_name="ข้อมูลผู้ใช้งาน.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        elif password:
            st.error("รหัสผ่านไม่ถูกต้อง")


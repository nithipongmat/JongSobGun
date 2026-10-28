import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Jongsob Admin Dashboard", page_icon="📊", layout="wide")

st.title("📊 Jongsob - ระบบจัดการหลังบ้านและการรายงานผลการจอง")
st.markdown("แดชบอร์ดสำหรับตรวจสอบตารางเวลา สรุปสถิติการใช้งาน และดาวน์โหลดรายงานผ่านระบบ Jongsob")

if 'bookings_data' not in st.session_state:
    st.session_state.bookings_data = [
        {"date": datetime.now().strftime("%Y-%m-%d"), "resource": "เตียงฝึกปฏิบัติ #1", "timeSlot": "09:00 - 10:00", "name": "กิตติ"},
        {"date": datetime.now().strftime("%Y-%m-%d"), "resource": "Ultrasonic", "timeSlot": "10:00 - 11:00", "name": "เพื่อนร่วมรุ่น"},
    ]

df = pd.DataFrame(st.session_state.bookings_data)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("การจองทั้งหมดในระบบ", len(df))
with col2:
    st.metric("อุปกรณ์ยอดนิยม", "เตียงฝึกปฏิบัติ #1")
with col3:
    st.metric("สถานะระบบ Jongsob", "🟢 ออนไลน์ (Online)")

st.divider()

st.subheader("📋 รายการข้อมูลการจองทั้งหมดใน Jongsob")
if not df.empty:
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
    
    def convert_df_to_excel(df):
        from io import BytesIO
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Jongsob_Bookings')
        return output.getvalue()

    excel_data = convert_df_to_excel(df)
    st.download_button(
        label="📥 ดาวน์โหลดรายงานสรุป Jongsob เป็นไฟล์ Excel (.xlsx)",
        data=excel_data,
        file_name=f"Jongsob_Booking_Report_{datetime.now().strftime('%Y-%m-%d')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.info("ยังไม่มีข้อมูลการจองในระบบ Jongsob")

import streamlit as st
import pandas as pd
import datetime
from datetime import datetime, timedelta

# 1. 網頁基本配置（必須維持在最頂端）
st.set_page_config(page_title="欣川豐杰請假系統", page_icon="📊", layout="wide")

# --- 常數設定 ---
DEFAULT_PASSWORD = '04698438'
START_YEAR = 2026

# --- 2026 年台灣主要國定假日對照表 (用於自動扣除) ---
HOLIDAYS_2026 = {
    "2026-01-01", # 元旦
    "2026-02-16", "2026-02-17", "2026-02-18", "2026-02-19", "2026-02-20", "2026-02-21", # 春節連假
    "2026-02-27", # 228連假調整
    "2026-02-28", # 和平紀念日
    "2026-04-02", "2026-04-03", # 兒童節與清明節連假
    "2026-05-01", # 勞動節 (勞工放假)
    "2026-06-19", # 端午節連假調整
    "2026-06-20", # 端午節
    "2026-09-25", # 中秋節
    "2026-10-09", # 國慶日連假調整
    "2026-10-10", # 國慶日
}

# --- 計算實際請假天數（扣除六日與國定假日） ---
def calculate_work_days(start_date, end_date, shift):
    if shift in ['上午', '下午']:
        return 0.5
        
    current_date = start_date
    total_days = 0.0
    
    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")
        is_weekend = current_date.weekday() >= 5
        is_holiday = date_str in HOLIDAYS_2026
        
        if not is_weekend and not is_holiday:
            total_days += 1.0
            
        current_date += timedelta(days=1)
        
    return total_days

# --- 判定是否在請假一星期（7天）內，允許修改或刪除 ---
def is_action_allowed(date_str, is_legacy):
    if is_legacy: 
        return False # 歷史匯入數據不允許修改刪除
    try:
        base_date_str = date_str.split(" ")[0]
        leave_date = datetime.strptime(base_date_str, "%Y-%m-%d")
        days_diff = (datetime.now() - leave_date).days
        return days_diff <= 7
    except:
        return False

# --- 初始化 Session State（狀態管理） ---
if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'view' not in st.session_state:
    st.session_state.view = 'dashboard'
if 'selected_year' not in st.session_state:
    st.session_state.selected_year = START_YEAR
if 'edit_req_id' not in st.session_state:
    st.session_state.edit_req_id = None

# 16位員工資料
if 'employees' not in st.session_state:
    st.session_state.employees = [
        { 'id': 'E001', 'name': '陳秋漢', 'role': 'employee', 'department': '儀控部', 'totalAnnual': 30, 'carryOver': 20, 'password': DEFAULT_PASSWORD },
        { 'id': 'E002', 'name': '楊偉昇', 'role': 'employee', 'department': '儀控部', 'totalAnnual': 30, 'carryOver': 0, 'password': DEFAULT_PASSWORD },
        { 'id': 'E003', 'name': '施文吉', 'role': 'employee', 'department': '儀控部', 'totalAnnual': 30, 'carryOver': 0, 'password': DEFAULT_PASSWORD },
        { 'id': 'E004', 'name': '黃兩家', 'role': 'employee', 'department': '儀控部', 'totalAnnual': 30, 'carryOver': 0, 'password': DEFAULT_PASSWORD },
        { 'id': 'E016', 'name': '蔡秀惠', 'role': 'admin', 'department': '行政部', 'totalAnnual': 30, 'carryOver': 0, 'password': DEFAULT_PASSWORD },
        { 'id': 'E005', 'name': '鄭惠蓉', 'role': 'employee', 'department': '儀控部', 'totalAnnual': 3

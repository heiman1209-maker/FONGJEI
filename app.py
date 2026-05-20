import streamlit as st
import pandas as pd
import datetime
from datetime import datetime, timedelta

# 1. 網頁基本配置（必須維持在最頂端）
st.set_page_config(page_title="欣川豐假請假系統", page_icon="📊", layout="wide")

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
   # 16位員工資料
if 'employees' not in st.session_state:
    st.session_state.employees = [
        { 'id': 'E001', 'name': '陳秋漢', 'role': 'employee', 'department': '儀控部', 'totalAnnual': 30, 'carryOver': 20, 'password': DEFAULT_PASSWORD },
        { 'id': 'E002', 'name': '楊偉昇', 'role': 'employee', 'department': '儀控部', 'totalAnnual': 30, 'carryOver': 0, 'password': DEFAULT_PASSWORD },
        { 'id': 'E003', 'name': '施文吉', 'role': 'employee', 'department': '儀控部', 'totalAnnual': 30, 'carryOver': 0, 'password': DEFAULT_PASSWORD },
        { 'id': 'E004', 'name': '黃兩家', 'role': 'employee', 'department': '儀控部', 'totalAnnual': 30, 'carryOver': 0, 'password': DEFAULT_PASSWORD },
        { 'id': 'E016', 'name': '蔡秀惠', 'role': 'admin', 'department': '行政部', 'totalAnnual': 30, 'carryOver': 0, 'password': DEFAULT_PASSWORD },
        { 'id': 'E005', 'name': '鄭惠蓉', 'role': 'employee', 'department': '儀控部', 'totalAnnual': 30, 'carryOver': 0, 'password': DEFAULT_PASSWORD },
        { 'id': 'E006', 'name': '蔡雅菁', 'role': 'employee', 'department': '儀控部', 'totalAnnual': 30, 'carryOver': 0, 'password': DEFAULT_PASSWORD },
        { 'id': 'E007', 'name': '呂麗杏', 'role': 'employee', 'department': '儀控部', 'totalAnnual': 30, 'carryOver': 0, 'password': DEFAULT_PASSWORD },
        { 'id': 'E008', 'name': '黃嘉銘', 'role': 'employee', 'department': '儀控部', 'totalAnnual': 25, 'carryOver': 0, 'password': DEFAULT_PASSWORD },
        { 'id': 'E009', 'name': '蘇忠泰', 'role': 'employee', 'department': '流量計', 'totalAnnual': 30, 'carryOver': 0, 'password': DEFAULT_PASSWORD },
        { 'id': 'E010', 'name': '葉錦達', 'role': 'employee', 'department': '流量計', 'totalAnnual': 30, 'carryOver': 0, 'password': DEFAULT_PASSWORD },
        { 'id': 'E011', 'name': '陳秋霞', 'role': 'employee', 'department': '流量計', 'totalAnnual': 30, 'carryOver': 0, 'password': DEFAULT_PASSWORD },
        { 'id': 'E012', 'name': '林信佑', 'role': 'employee', 'department': '流量計', 'totalAnnual': 30, 'carryOver': 0, 'password': DEFAULT_PASSWORD },
        { 'id': 'E013', 'name': '宋志銘', 'role': 'employee', 'department': '流量計', 'totalAnnual': 14, 'carryOver': 0, 'password': DEFAULT_PASSWORD },
        { 'id': 'E014', 'name': '王英杰', 'role': 'employee', 'department': '譯碼器', 'totalAnnual': 26, 'carryOver': 0, 'password': DEFAULT_PASSWORD },
        { 'id': 'E015', 'name': '蘇雅瑄', 'role': 'employee', 'department': '譯碼器', 'totalAnnual': 23, 'carryOver': 0, 'password': DEFAULT_PASSWORD }
    ]

# 歷史請假紀錄明細
if 'requests' not in st.session_state:
    legacy_dates = {
        'E002': ['2026-01-29', '2026-02-26', '2026-03-18', '2026-03-30', '2026-04-16'],
        'E005': ['2026-03-12', '2026-03-18', '2026-03-27', '2026-04-23'],
        'E006': ['2026-01-13', '2026-01-16', '2026-01-23', '2026-02-09', '2026-03-05', '2026-03-13'],
        'E007': ['2026-01-21', '2026-02-12', '2026-03-02', '2026-03-03', '2026-03-27', '2026-04-20'],
        'E008': ['2026-04-02', '2026-04-14', '2026-04-15'],
        'E011': ['2026-03-16', '2026-03-23', '2026-03-30', '2026-04-20'],
        'E015': ['2026-01-02', '2026-02-24', '2026-04-01', '2026-04-02'],
        'E001': ['2026-01-19', '2026-01-29', '2026-03-17'],
        'E016': ['2026-03-10', '2026-03-11', '2026-03-12', '2026-03-13']
    }
    
    initial_reqs = []
    for emp_id, dates in legacy_dates.items():
        for d in dates:
            initial_reqs.append({'id': f"L_{emp_id}_{d}", 'employeeId': emp_id, 'type': '特休', 'date': d, 'shift': '全天', 'days': 1.0, 'status': 'approved', 'isLegacy': True, 'agent': '不需要代理人'})
    for emp_id, dates in legacy_half_dates.items():
        for d in dates:
            initial_reqs.append({'id': f"L_{emp_id}_H_{d}", 'employeeId': emp_id, 'type': '特休', 'date': d, 'shift': '上午', 'days': 0.5, 'status': 'approved', 'isLegacy': True, 'agent': '不需要代理人'})
    st.session_state.requests = initial_reqs

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# 1. 網頁基本配置
st.set_page_config(page_title="欣川豐杰請假系統", page_icon="📊", layout="wide")

DEFAULT_PASSWORD = '04698438'
START_YEAR = 2026

# --- 2026 年台灣主要國定假日 ---
HOLIDAYS_2026 = {
    "2026-01-01", "2026-02-16", "2026-02-17", "2026-02-18", "2026-02-19", "2026-02-20", 
    "2026-02-21", "2026-02-27", "2026-02-28", "2026-04-02", "2026-04-03", "2026-05-01", 
    "2026-06-19", "2026-06-20", "2026-09-25", "2026-10-09", "2026-10-10"
}

# --- 計算請假天數 ---
def calculate_work_days(start_date, end_date, shift):
    if shift in ['上午', '下午']: return 0.5
    current_date, total_days = start_date, 0.0
    while current_date <= end_date:
        if current_date.weekday() < 5 and current_date.strftime("%Y-%m-%d") not in HOLIDAYS_2026:
            total_days += 1.0
        current_date += timedelta(days=1)
    return total_days

# --- 7天時效防護 ---
def is_action_allowed(date_str, is_legacy):
    if is_legacy: return False
    try:
        leave_date = datetime.strptime(date_str.split(" ")[0], "%Y-%m-%d")
        return (datetime.now() - leave_date).days <= 7
    except: return False

# --- 初始化 Session State ---
if 'is_logged_in' not in st.session_state: st.session_state.is_logged_in = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'view' not in st.session_state: st.session_state.view = 'dashboard'
if 'selected_year' not in st.session_state: st.session_state.selected_year = START_YEAR
if 'edit_req_id' not in st.session_state: st.session_state.edit_req_id = None

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

# 歷史紀錄精簡整合
if 'requests' not in st.session_state:
    reqs = []
    legacy = {
        'E002': (['2026-01-29', '2026-02-26', '2026-03-18', '2026-03-30', '2026-04-16'], []),
        'E005': (['2026-03-12', '2026-03-18', '2026-03-27', '2026-04-23'], []),
        'E006': (['2026-01-13', '2026-01-16', '2026-01-23', '2026-02-09', '2026-03-05', '2026-03-13'], ['2026-01-09', '2026-01-30', '2026-02-06', '2026-03-03', '2026-03-27']),
        'E007': (['2026-01-21', '2026-02-12', '2026-03-02', '2026-03-03', '2026-03-27', '2026-04-20'], ['2026-01-16', '2026-01-19', '2026-01-20', '2026-03-20', '2026-03-23', '2026-04-28']),
        'E008': (['2026-04-02', '2026-04-14', '2026-04-15'], ['2026-03-17', '2026-03-20', '2026-03-27', '2026-04-21', '2026-04-28', '2026-04-30']),
        'E011': (['2026-03-16', '2026-03-23', '2026-03-30', '2026-04-20'], ['2026-01-16', '2026-02-05', '2026-03-25']),
        'E015': (['2026-01-02', '2026-02-24', '2026-04-01', '2026-04-02'], []),
        'E001': (['2026-01-19', '2026-01-29', '2026-03-17'], ['2026-01-28', '2026-04-28']),
        'E016': (['2026-03-10', '2026-03-11', '2026-03-12', '2026-03-13'], ['2026-03-26', '2026-04-21', '2026-04-24', '2026-04-28']),
        'E003': ([], ['2026-01-26', '2026-02-10', '2026-02-13', '2026-02-23', '2026-03-06', '2026-03-09', '2026-03-10', '2026-03-11', '2026-03-12', '2026-03-13', '2026-03-23', '2026-03-31', '2026-04-02', '2026-04-07'])
    }
    for emp_id, (full, half) in legacy.items():
        for d in full: reqs.append({'id': f"L_{emp_id}_{d}", 'employeeId': emp_id, 'type': '特休', 'date': d, 'shift': '全天', 'days': 1.0, 'status': 'approved', 'isLegacy': True, 'agent': '不需要代理人'})
        for d in half: reqs.append({'id': f"L_{emp_id}_H_{d}", 'employeeId': emp_id, 'type': '特休', 'date': d, 'shift': '上午', 'days': 0.5, 'status': 'approved', 'isLegacy': True, 'agent': '不需要代理人'})
    st.session_state.requests = reqs

# ==================== 1. 登入介面 ====================
if not st.session_state.is_logged_in:
    st.markdown("<h2 style='text-align: center; color: #10B981;'>欣川豐杰請假系統</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.write("### 🔑 員工登入")
        emp_options = {f"{emp['id']} - {emp['name']}": emp for emp in sorted(st.session_state.employees, key=lambda x: x['id'])}
        selected_emp_label = st.selectbox("選擇您的姓名", ["請選擇員工..."] + list(emp_options.keys()), key="login_emp_select")
        password_input = st.text_input("輸入登入密碼", type="password", key="login_pwd_input")
        if st.button("立即進入系統", use_container_width=True, key="login_submit_btn"):
            if selected_emp_label != "請選擇員工...":
                user_data = emp_options[selected_emp_label]
                if password_input == user_data['password']:
                    st.session_state.is_logged_in = True
                    st.session_state.current_user = user_data
                    st.session_state.view = 'dashboard'
                    st.rerun()
                else: st.error("密碼驗證失敗。")
        st.caption("💡 預設密碼為 04698438")
    st.stop()

# ==================== 2. 主導航與配置 ====================
current_user = st.session_state.current_user
with st.sidebar:
    st.markdown(f"### 🏢 欣川豐杰\n**使用者:** {current_user['name']} ({current_user['department']})")
    st.write("---")
    if st.button("📊 個人功能儀表板", use_container_width=True, key="sb_dash"):
        st.session_state.view = 'dashboard'; st.session_state.edit_req_id = None; st.rerun()
    if st.button("📝 填寫請假申請單", use_container_width=True, key="sb_apply"):
        st.session_state.view = 'apply'; st.session_state.edit_req_id = None; st.rerun()
    if current_user['role'] == 'admin':
        st.write("---")
        st.markdown("<span style='color:#10B981; font-weight:bold;'>🛠️ 管理員控制台</span>", unsafe_allow_html=True)
        if st.button("👥 全公司特休統計", use_container_width=True, key="sb_stats"): st.session_state.view = 'employees'; st.rerun()
        p_count = len([r for r in st.session_state.requests if r['status'] == 'pending'])
        if st.button(f"📩 待辦審核單據 ({p_count})", use_container_width=True, key="sb_mgr"): st.session_state.view = 'manage'; st.rerun()
    st.write("---")

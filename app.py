import streamlit as st
import pandas as pd
from datetime import datetime

# 1. 網頁基本配置（必須是除了註解以外的第一行 Python 程式碼）
st.set_page_config(page_title="欣川豐杰請假系統", page_icon="📊", layout="wide")

# --- 常數設定 ---
DEFAULT_PASSWORD = '04698438'
START_YEAR = 2026

# --- 初始化 Session State（狀態管理） ---
if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'view' not in st.session_state:
    st.session_state.view = 'dashboard'
if 'selected_year' not in st.session_state:
    st.session_state.selected_year = START_YEAR

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
        { 'id': 'E015', 'name': '蘇雅瑄', 'role': 'employee', 'department': '譯碼器', 'totalAnnual': 23, 'carryOver': 0, 'password': DEFAULT_PASSWORD },
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
    legacy_half_dates = {
        'E003': ['2026-01-26', '2026-02-10', '2026-02-13', '2026-02-23', '2026-03-06', '2026-03-09', '2026-03-10', '2026-03-11', '2026-03-12', '2026-03-13', '2026-03-23', '2026-03-31', '2026-04-02', '2026-04-07'],
        'E006': ['2026-01-09', '2026-01-30', '2026-02-06', '2026-03-03', '2026-03-27'],
        'E007': ['2026-01-16', '2026-01-19', '2026-01-20', '2026-03-20', '2026-03-23', '2026-04-28'],
        'E008': ['2026-03-17', '2026-03-20', '2026-03-27', '2026-04-21', '2026-04-28', '2026-04-30'],
        'E011': ['2026-01-16', '2026-02-05', '2026-03-25'],
        'E001': ['2026-01-28', '2026-04-28'],
        'E016': ['2026-03-26', '2026-04-21', '2026-04-24', '2026-04-28']
    }
    
    initial_reqs = []
    for emp_id, dates in legacy_dates.items():
        for d in dates:
            initial_reqs.append({'id': f"L_{emp_id}_{d}", 'employeeId': emp_id, 'type': '特休', 'date': d, 'shift': '全天', 'days': 1.0, 'status': 'approved', 'isLegacy': True, 'reason': '前期數據'})
    for emp_id, dates in legacy_half_dates.items():
        for d in dates:
            initial_reqs.append({'id': f"L_{emp_id}_H_{d}", 'employeeId': emp_id, 'type': '特休', 'date': d, 'shift': '上午', 'days': 0.5, 'status': 'approved', 'isLegacy': True, 'reason': '前期數據'})
    st.session_state.requests = initial_reqs

# ==================== 1. 登入介面 ====================
if not st.session_state.is_logged_in:
    st.markdown("<h2 style='text-align: center; color: #10B981;'>欣川豐杰請假系統</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.write("### 🔑 員工登入")
        emp_options = {f"{emp['id']} - {emp['name']}": emp for emp in sorted(st.session_state.employees, key=lambda x: x['id'])}
        selected_emp_label = st.selectbox("選擇您的姓名", ["請選擇員工..."] + list(emp_options.keys()))
        password_input = st.text_input("輸入登入密碼", type="password", placeholder="••••••••")
        
        if st.button("立即進入系統", use_container_width=True):
            if selected_emp_label != "請選擇員工...":
                user_data = emp_options[selected_emp_label]
                if password_input == user_data['password']:
                    st.session_state.is_logged_in = True
                    st.session_state.current_user = user_data
                    st.rerun()
                else:
                    st.error("密碼驗證失敗，請重試。")
            else:
                st.warning("請先選取您的員工姓名。")
        st.caption("💡 初次登入預設密碼為 04698438")
    st.stop()

# ==================== 2. 主導航與配置 ====================
current_user = st.session_state.current_user

with st.sidebar:
    st.markdown(f"### 🏢 欣川豐杰\n**使用者:** {current_user['name']} ({current_user['department']})")
    st.write("---")
    if st.button("📊 個人功能儀表板", use_container_width=True):
        st.session_state.view = 'dashboard'
    if st.button("📝 填寫請假申請單", use_container_width=True):
        st.session_state.view = 'apply'
    
    if current_user['role'] == 'admin':
        st.write("---")
        st.markdown("<span style='color:#10B981; font-weight:bold;'>🛠️ 管理員控制台</span>", unsafe_allow_html=True)
        if st.button("👥 全公司特休統計", use_container_width=True):
            st.session_state.view = 'employees'
        pending_count = len([r for r in st.session_state.requests if r['status'] == 'pending'])
        if st.button(f"📩 待辦審核單據 ({pending_count})", use_container_width=True):
            st.session_state.view = 'manage'
            
    st.write("---")
    if st.button("🔒 安全登出系統", use_container_width=True):
        st.session_state.is_logged_in = False
        st.session_state.current_user = None
        st.rerun()

# 頂部抬頭
col_title, col_year = st.columns([3, 1])
with col_title:
    st.subheader(f"{current_user['name']}，您好")
with col_year:
    st.session_state.selected_year = st.selectbox("追蹤年度", [2026, 2027], index=0)

# 計算個人額度
used_days = sum([r['days'] for r in st.session_state.requests if r['employeeId'] == current_user['id'] and r['status'] == 'approved' and r['type'] == '特休' and r['date'].startswith(str(st.session_state.selected_year))])
total_entitlement = current_user['totalAnnual']
carry_over = current_user['carryOver'] if st.session_state.selected_year == START_YEAR else 0
total_possible = total_entitlement + carry_over
remaining_days = total_possible - used_days

# ==================== 3. 功能分頁 ====================
if st.session_state.view == 'dashboard':
    st.markdown("#### 📅 當前年度特休權益摘要")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("當年度新特休", f"{total_entitlement} 天")
    m2.metric("前一年度結轉", f"{carry_over} 天")
    m3.metric("累計已休天數", f"{used_days} 天")
    m4.metric("剩餘可用淨額度", f"{remaining_days} 天")
    
    st.write("---")
    st.markdown("#### 📋 個人請假明細紀錄")
    my_all_reqs = [r for r in st.session_state.requests if r['employeeId'] == current_user['id']]
    if not my_all_reqs:
        st.info("目前尚無個人的請假申請紀錄。")
    else:
        df_my = pd.DataFrame(my_all_reqs).sort_values(by='date', ascending=False)
        st.dataframe(df_my[['type', 'date', 'shift', 'days', 'status', 'reason']], use_container_width=True)

elif st.session_state.view == 'apply':
    st.markdown("#### 📝 填寫請假申請單")
    with st.form("leave_form"):
        l_type = st.selectbox("選擇請假假別", ['特休', '病假', '事假', '公假'])
        l_date = st.date_input("請假日期")
        l_shift = st.radio("請假時段", ['全天', '上午', '下午'], horizontal=True)
        l_reason = st.text_area("請假具體事由")
        
        if st.form_submit_button("送出申請"):
            days_calc = 1.0 if l_shift == '全天' else 0.5
            new_req = {
                'id': f"R{int(datetime.now().timestamp())}",
                'employeeId': current_user['id'],
                'type': l_type,
                'date': l_date.strftime("%Y-%m-%d"),
                'shift': l_shift,
                'days': days_calc,
                'status': 'pending',
                'isLegacy': False,
                'reason': l_reason
            }
            st.session_state.requests.append(new_req)
            st.success("🎉 申請已成功送出，請靜候後台審核。")
            st.session_state.view = 'dashboard'
            st.rerun()

elif st.session_state.view == 'employees' and current_user['role'] == 'admin':
    st.markdown("#### 👥 全公司特休總額度統計")
    summary_data = []
    for emp in st.session_state.employees:
        emp_used = sum([r['days'] for r in st.session_state.requests if r['employeeId'] == emp['id'] and r['status'] == 'approved' and r['type'] == '特休' and r['date'].startswith(str(st.session_state.selected_year))])
        emp_carry = emp['carryOver'] if st.session_state.selected_year == START_YEAR else 0
        summary_data.append({
            '工號': emp['id'], '姓名': emp['name'], '部門': emp['department'],
            '年度新假': emp['totalAnnual'], '上年結轉': emp_carry,
            '總額度': emp['totalAnnual'] + emp_carry, '已休累計': emp_used,
            '剩餘可休': (emp['totalAnnual'] + emp_carry) - emp_used
        })
    st.dataframe(pd.DataFrame(summary_data), use_container_width=True)

elif st.session_state.view == 'manage' and current_user['role'] == 'admin':
    st.markdown("#### 📩 待審核單據管理")
    pending_list = [r for r in st.session_state.requests if r['status'] == 'pending']
    if not pending_list:
        st.info("🎉 暫無任何需要審核的假單。")
    else:
        for req in pending_list:
            emp_info = next((e for e in st.session_state.employees if e['id'] == req['employeeId']), None)
            st.write(f"**申請人:** {emp_info['name']} ｜ **假別:** {req['type']} ｜ **日期:** {req['date']} ({req['shift']}共 {req['days']} 天)")
            st.write(f"**事由:** {req['reason']}")
            c1, c2 = st.columns(2)
            if c1.button("✅ 核准", key=f"ok_{req['id']}"):
                req['status'] = 'approved'
                st.rerun()
            if c2.button("❌ 駁回", key=f"no_{req['id']}"):
                req['status'] = 'rejected'
                st.rerun()
            st.write("---")

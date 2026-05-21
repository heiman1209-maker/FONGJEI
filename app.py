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

# --- 初始化 Session State（修正 view 的預設機制） ---
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
    for emp_id, (full, half) in legacy.items(): Full_d = full; half_d = half
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
    if st.button("🔒 安全登出系統", use_container_width=True, key="sb_logout"):
        st.session_state.is_logged_in = False; st.session_state.current_user = None; st.rerun()

col_title, col_year = st.columns([3, 1])
col_title.subheader(f"{current_user['name']}，您好")
st.session_state.selected_year = col_year.selectbox("追蹤年度", [2026, 2027], index=0, key="global_year_select")

used_days = sum([r['days'] for r in st.session_state.requests if r['employeeId'] == current_user['id'] and r['status'] == 'approved' and r['type'] == '特休' and str(st.session_state.selected_year) in r['date']])
carry_over = current_user['carryOver'] if st.session_state.selected_year == START_YEAR else 0
remaining_days = (current_user['totalAnnual'] + carry_over) - used_days

# ==================== 3. 功能分頁 ====================
if st.session_state.view == 'dashboard':
    st.markdown("#### 📅 當前年度特休權益摘要")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("當年度新特休", f"{current_user['totalAnnual']} 天")
    m2.metric("前一年度結轉", f"{carry_over} 天")
    m3.metric("審核通過已休", f"{used_days} 天")
    m4.metric("剩餘可用淨額度", f"{remaining_days} 天")
    st.write("---")
    st.markdown("#### 📋 個人請假明細紀錄 (一星期內可修改或刪除)")
    my_reqs = [r for r in st.session_state.requests if r['employeeId'] == current_user['id']]
    if not my_reqs: st.info("目前尚無請假紀錄。")
    else:
        h1, h2, h3, h4, h5, h6, h7 = st.columns([1.5, 2.5, 1, 1, 1.2, 2, 2.5])
        h1.markdown("**假別**"); h2.markdown("**請假期間**"); h3.markdown("**時段**"); h4.markdown("**天數**"); h5.markdown("**狀態**"); h6.markdown("**代理人**"); h7.markdown("**功能操作**")
        st.markdown("<hr style='margin: 5px 0;'/>", unsafe_allow_html=True)
        for req in sorted(my_reqs, key=lambda x: x['date'], reverse=True):
            c1, c2, c3, c4, c5, c6, c7 = st.columns([1.5, 2.5, 1, 1, 1.2, 2, 2.5])
            c1.write(req['type']); c2.write(req['date']); c3.write(req['shift']); c4.write(f"{req['days']} 天")
            c5.write({'approved': '🟢 已核准', 'pending': '🟡 待審核', 'rejected': '🔴 已駁回'}.get(req['status'], req['status']))
            c6.write(req['agent'])
            if is_action_allowed(req['date'], req.get('isLegacy', False)):
                b1, b2 = c7.columns(2)
                if b1.button("📝 修改", key=f"ed_{req['id']}", use_container_width=True):
                    st.session_state.edit_req_id = req['id']; st.session_state.view = 'apply'; st.rerun()
                if b2.button("🗑️ 刪除", key=f"dl_{req['id']}", use_container_width=True):
                    st.session_state.requests.remove(req); st.toast("🗑️ 已成功刪除！"); st.rerun()
            else: c7.caption("🔒 已超過1星期鎖定")

elif st.session_state.view == 'apply':
    is_editing = st.session_state.edit_req_id is not None
    target_req = next((r for r in st.session_state.requests if r['id'] == st.session_state.edit_req_id), None) if is_editing else None
    st.markdown(f"#### 📝 {'修改' if is_editing else '填寫'}請假申請單")
    agents = ["不需要代理人"] + [e['name'] for e in sorted(st.session_state.employees, key=lambda x: x['id']) if e['id'] != current_user['id']]
    
    l_type = st.selectbox("選擇請假假別", ['特休', '病假', '事假', '公假'], index=['特休', '病假', '事假', '公假'].index(target_req['type'] if is_editing else '特休'))
    c_d1, c_d2 = st.columns(2)
    l_start = c_d1.date_input("請假開始日期", datetime.now())
    l_end = c_d2.date_input("請假結束日期", value=l_start)
    l_shift = st.radio("請假時段", ['全天', '上午', '下午'], index=['全天', '上午', '下午'].index(target_req['shift'] if is_editing else '全天'), horizontal=True)
    l_agent = st.selectbox("職務代理人協助", agents, index=agents.index(target_req['agent'] if is_editing and target_req['agent'] in agents else "不需要代理人"))
    
    if st.button("🚀 確認送出假單", use_container_width=True, key="form_submit"):
        if l_end < l_start: st.error("❌ 結束日期不能早於開始日期！")
        else:
            days = calculate_work_days(l_start, l_end, l_shift)
            if days == 0: st.warning("⚠️ 期間內均為例假日，不需請假。")
            else:
                lbl = f"{l_start.strftime('%Y-%m-%d')} 至 {l_end.strftime('%Y-%m-%d')}" if l_start != l_end else l_start.strftime('%Y-%m-%d')
                if is_editing and target_req:
                    target_req.update({'type': l_type, 'date': lbl, 'shift': l_shift, 'days': days, 'agent': l_agent, 'status': 'pending'})
                    st.toast("🎉 假單修改成功！")
                else:
                    st.session_state.requests.append({'id': f"R{int(datetime.now().timestamp())}", 'employeeId': current_user['id'], 'type': l_type, 'date': lbl, 'shift': l_shift, 'days': days, 'status': 'pending', 'isLegacy': False, 'agent': l_agent})
                    st.toast("🎉 請假申請成功！")
                st.session_state.edit_req_id = None; st.session_state.view = 'dashboard'; st.rerun()

elif st.session_state.view == 'employees' and current_user['role'] == 'admin':
    st.markdown("#### 👥 全公司特休總額度統計")
    s_data = []
    for emp in st.session_state.employees:
        emp_used = sum([r['days'] for r in st.session_state.requests if r['employeeId'] == emp['id'] and r['status'] == 'approved' and r['type'] == '特休' and str(st.session_state.selected_year) in r['date']])
        carry = emp['carryOver'] if st.session_state.selected_year == START_YEAR else 0
        s_data.append({'工號': emp['id'], '姓名': emp['name'], '部門': emp['department'], '年度新假': emp['totalAnnual'], '上年結轉': carry, '總額度': emp['totalAnnual'] + carry, '已休累計': emp_used, '剩餘可休': (emp['totalAnnual'] + carry) - emp_used})
    st.dataframe(pd.DataFrame(s_data), use_container_width=True)

elif st.session_state.view == 'manage' and current_user['role'] == 'admin':
    st.markdown("#### 📩 待審核單據管理")
    p_list = [r for r in st.session_state.requests if r['status'] == 'pending']
    if not p_list: st.info("🎉 暫無任何需要審核的假單。")
    else:
        for req in p_list:
            emp = next((e for e in st.session_state.employees if e['id'] == req['employeeId']), None)
            st.write(f"**申請人:** {emp['name']} ｜ **假別:** {req['type']} ｜ **期間:** {req['date']} ({req['shift']} ｜ 共 {req['days']} 天) ｜ **代理人:** {req['agent']}")
            ca, cr = st.columns(2)
            if ca.button("✅ 核准", key=f"ok_{req['id']}", use_container_width=True): req['status'] = 'approved'; st.rerun()
            if cr.button("❌ 駁回", key=f"no_{req['id']}", use_container_width=True): req['status'] = 'rejected'; st.rerun()
            st.write("---")

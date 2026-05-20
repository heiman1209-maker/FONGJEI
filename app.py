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
            initial_reqs.append({'id': f"L_{emp_id}_{d}", 'employeeId': emp_id, 'type': '特休', 'date': d, 'shift': '全天', 'days': 1.0, 'status': 'approved', 'isLegacy': True, 'agent': '不需要代理人'})
    for emp_id, dates in legacy_half_dates.items():
        for d in dates:
            initial_reqs.append({'id': f"L_{emp_id}_H_{d}", 'employeeId': emp_id, 'type': '特休', 'date': d, 'shift': '上午', 'days': 0.5, 'status': 'approved', 'isLegacy': True, 'agent': '不需要代理人'})
    st.session_state.requests = initial_reqs

# ==================== 1. 登入介面 ====================
if not st.session_state.is_logged_in:
    st.markdown("<h2 style='text-align: center; color: #10B981;'>欣川豐杰請假系統</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.write("### 🔑 員工登入")
        emp_options = {f"{emp['id']} - {emp['name']}": emp for emp in sorted(st.session_state.employees, key=lambda x: x['id'])}
        selected_emp_label = st.selectbox("選擇您的姓名", ["請選擇員工..."] + list(emp_options.keys()), key="login_emp_select")
        password_input = st.text_input("輸入登入密碼", type="password", placeholder="••••••••", key="login_pwd_input")
        
        if st.button("立即進入系統", use_container_width=True, key="login_submit_btn"):
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

# 只有在登入成功後，側邊欄才繪製按鈕，徹底防止撞名
with st.sidebar:
    st.markdown(f"### 🏢 欣川豐杰\n**使用者:** {current_user['name']} ({current_user['department']})")
    st.write("---")
    if st.button("📊 個人功能儀表板", use_container_width=True, key="main_sidebar_dashboard_key"):
        st.session_state.view = 'dashboard'
        st.session_state.edit_req_id = None
    if st.button("📝 填寫請假申請單", use_container_width=True, key="main_sidebar_apply_key"):
        st.session_state.view = 'apply'
        st.session_state.edit_req_id = None
    
    if current_user['role'] == 'admin':
        st.write("---")
        st.markdown("<span style='color:#10B981; font-weight:bold;'>🛠️ 管理員控制台</span>", unsafe_allow_html=True)
        if st.button("👥 全公司特休統計", use_container_width=True, key="main_sidebar_stats_key"):
            st.session_state.view = 'employees'
        pending_count = len([r for r in st.session_state.requests if r['status'] == 'pending'])
        if st.button(f"📩 待辦審核單據 ({pending_count})", use_container_width=True, key="main_sidebar_manage_key"):
            st.session_state.view = 'manage'
            
    st.write("---")
    if st.button("🔒 安全登出系統", use_container_width=True, key="main_sidebar_logout_key"):
        st.session_state.is_logged_in = False
        st.session_state.current_user = None
        st.rerun()

# 頂部抬頭
col_title, col_year = st.columns([3, 1])
with col_title:
    st.subheader(f"{current_user['name']}，您好")
with col_year:
    st.session_state.selected_year = st.selectbox("追蹤年度", [2026, 2027], index=0, key="global_year_select")

# 計算個人額度
used_days = sum([r['days'] for r in st.session_state.requests if r['employeeId'] == current_user['id'] and r['status'] == 'approved' and r['type'] == '特休' and str(st.session_state.selected_year) in r['date']])
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
    m3.metric("審核通過累計已休", f"{used_days} 天")
    m4.metric("剩餘可用淨額度", f"{remaining_days} 天")
    
    st.write("---")
    st.markdown("#### 📋 個人請假明細紀錄 (請假首日起一星期內可修改或刪除)")
    
    my_all_reqs = [r for r in st.session_state.requests if r['employeeId'] == current_user['id']]
    if not my_all_reqs:
        st.info("目前尚無個人的請假申請紀錄。")
    else:
        sorted_reqs = sorted(my_all_reqs, key=lambda x: x['date'], reverse=True)
        
        h1, h2, h3, h4, h5, h6, h7 = st.columns([1.5, 2.5, 1, 1, 1.2, 2, 2.5])
        h1.markdown("**假別**")
        h2.markdown("**請假期間**")
        h3.markdown("**時段**")
        h4.markdown("**計算天數**")
        h5.markdown("**審核狀態**")
        h6.markdown("**職務代理人**")
        h7.markdown("**功能操作**")
        st.markdown("<hr style='margin: 5px 0; border-color: #E5E7EB;'/>", unsafe_allow_html=True)
        
        for req in sorted_reqs:
            c1, c2, c3, c4, c5, c6, c7 = st.columns([1.5, 2.5, 1, 1, 1.2, 2, 2.5])
            c1.write(req['type'])
            c2.write(req['date'])
            c3.write(req['shift'])
            c4.write(f"{req['days']} 天")
            
            status_map = {'approved': '🟢 已核准', 'pending': '🟡 待審核', 'rejected': '🔴 已駁回'}
            c5.write(status_map.get(req['status'], req['status']))
            c6.write(req['agent'])
            
            allowed = is_action_allowed(req['date'], req.get('isLegacy', False))
            
            if allowed:
                btn_col1, btn_col2 = c7.columns(2)
                if btn_col1.button("📝 修改", key=f"edit_btn_{req['id']}", use_container_width=True):
                    st.session_state.edit_req_id = req['id']
                    st.session_state.view = 'apply'
                    st.rerun()
                if btn_col2.button("🗑️ 刪除", key=f"del_btn_{req['id']}", use_container_width=True):
                    st.session_state.requests.remove(req)
                    st.toast("🗑️ 請假單已成功刪除並撤回！")
                    st.rerun()
            else:
                c7.caption("🔒 已超過1星期，鎖定不可動")
                
elif st.session_state.view == 'apply':
    is_editing = st.session_state.edit_req_id is not None
    target_req = None
    if is_editing:
        target_req = next((r for r in st.session_state.requests if r['id'] == st.session_state.edit_req_id), None)
        st.markdown("#### 📝 修改請假申請單")
    else:
        st.markdown("#### 📝 填寫請假申請單")
        
    agent_options = ["不需要代理人"] + [emp['name'] for emp in sorted(st.session_state.employees, key=lambda x: x['id']) if emp['id'] != current_user['id']]
    
    with st.form("leave_form"):
        default_type = target_req['type'] if is_editing else '特休'
        default_shift = target_req['shift'] if is_editing else '全天'
        default_agent = target_req['agent'] if is_editing and target_req['agent'] in agent_options else "不需要代理人"
        
        l_type = st.selectbox("選擇請假假別", ['特休', '病假', '事假', '公假'], index=['特休', '病假', '事假', '公假'].index(default_type), key="form_type_select")
        
        c_date1, c_date2 = st.columns(2)
        l_start_date = c_date1.date_input("請假開始日期", datetime.now(), key="form_start_date")
        l_end_date = c_date2.date_input("請假結束日期", datetime.now(), key="form_end_date")
        
        l_shift = st.radio("請假時段（註：選擇上午/下午將固定算 0.5 天）", ['全天', '上午', '下午'], index=['全天', '上午', '下午'].index(default_shift), horizontal=True, key="form_shift_radio")
        l_agent = st.selectbox("職務代理人協助", agent_options, index=agent_options.index(default_agent), key="form_agent_select")
        
        submit_btn_label = "確認修改並重新送出" if is_editing else "計算天數並送出申請"
        
        if st.form_submit_button(submit_btn_label):
            if l_end_date < l_start_date:
                st.error("❌ 錯誤：結束日期不能早於開始日期，請重新檢查！")
            else:
                days_calc = calculate_work_days(l_start_date, l_end_date, l_shift)
                
                if days_calc == 0:
                    st.warning("⚠️ 您選取的日期區間內全為國定假日或例假日，不需請假！")
                else:
                    date_label = f"{l_start_date.strftime('%Y-%m-%d')} 至 {l_end_date.strftime('%Y-%m-%d')}" if l_start_date != l_end_date else l_start_date.strftime('%Y-%m-%d')
                    
                    if is_editing and target_req:
                        target_req['type'] = l_type
                        target_req['date'] = date_label
                        target_req['shift'] = l_shift
                        target_req['days'] = days_calc
                        target_req['agent'] = l_agent
                        target_req['status'] = 'pending'
                        st.toast(f"🎉 假單已成功更新，本次重新計算共 **{days_calc}** 天。")
                    else:
                        new_req = {
                            'id': f"R{int(datetime.now().timestamp())}",
                            'employeeId': current_user['id'],
                            'type': l_type,
                            'date': date_label,
                            'shift': l_shift,
                            'days': days_calc,
                            'status': 'pending',
                            'isLegacy': False,
                            'agent': l_agent
                        }
                        st.session_state.requests.append(new_req)
                        st.toast(f"🎉 申請成功！本次共計 **{days_calc}** 天，已送交審核。")
                        
                    st.session_state.edit_req_id = None
                    st.session_state.view = 'dashboard'
                    st.rerun()
                    
    if is_editing:
        if st.button("❌ 取消修改並返回", use_container_width=True, key="form_cancel_edit_btn"):
            st.session_state.edit_req_id = None
            st.session_state.view = 'dashboard'
            st.rerun()

elif st.session_state.view == 'employees' and current_user['role'] == 'admin':
    st.markdown("#### 👥 全公司特休總額度統計")
    summary_data = []
    for emp in st.session_state.employees:
        emp_used = 0.0
        for r in st.session_state.requests:
            if r['employeeId'] == emp['id'] and r['status'] == 'approved' and r['type'] == '特休' and str(st.session_state.selected_year) in r['date']:
                emp_used += r['days']
                
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
    pending_list

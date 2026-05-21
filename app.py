import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="欣川豐杰請假系統", page_icon="📊", layout="wide")
DEFAULT_PASSWORD, START_YEAR = '04698438', 2026
HOLIDAYS_2026 = {"2026-01-01", "2026-02-16", "2026-02-17", "2026-02-18", "2026-02-19", "2026-02-20", "2026-02-21", "2026-02-27", "2026-02-28", "2026-04-02", "2026-04-03", "2026-05-01", "2026-06-19", "2026-06-20", "2026-09-25", "2026-10-09", "2026-10-10"}

def calculate_work_days(s, e, shift):
    if shift in ['上午', '下午']: return 0.5
    curr, days = s, 0.0
    while curr <= e:
        if curr.weekday() < 5 and curr.strftime("%Y-%m-%d") not in HOLIDAYS_2026: days += 1.0
        curr += timedelta(days=1)
    return days

def is_action_allowed(d_str, is_legacy):
    if is_legacy: return False
    try: return (datetime.now() - datetime.strptime(d_str.split(" ")[0], "%Y-%m-%d")).days <= 7
    except: return False

for k, v in [('is_logged_in', False), ('current_user', None), ('view', 'dashboard'), ('selected_year', START_YEAR), ('edit_req_id', None)]:
    if k not in st.session_state: st.session_state[k] = v

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

if 'requests' not in st.session_state:
    reqs, lg = [], {'E002': (['2026-01-29', '2026-02-26', '2026-03-18', '2026-03-30', '2026-04-16'], []), 'E005': (['2026-03-12', '2026-03-18', '2026-03-27', '2026-04-23'], []), 'E006': (['2026-01-13', '2026-01-16', '2026-01-23', '2026-02-09', '2026-03-05', '2026-03-13'], ['2026-01-09', '2026-01-30', '2026-02-06', '2026-03-03', '2026-03-27']), 'E007': (['2026-01-21', '2026-02-12', '2026-03-02', '2026-03-03', '2026-03-27', '2026-04-20'], ['2026-01-16', '2026-01-19', '2026-01-20', '2026-03-20', '2026-03-23', '2026-04-28']), 'E008': (['2026-04-02', '2026-04-14', '2026-04-15'], ['2026-03-17', '2026-03-20', '2026-03-27', '2026-04-21', '2026-04-28', '2026-04-30']), 'E011': (['2026-03-16', '2026-03-23', '2026-03-30', '2026-04-20'], ['2026-01-16', '2026-02-05', '2026-03-25']), 'E015': (['2026-01-02', '2026-02-24', '2026-04-01', '2026-04-02'], []), 'E001': (['2026-01-19', '2026-01-29', '2026-03-17'], ['2026-01-28', '2026-04-28']), 'E016': (['2026-03-10', '2026-03-11', '2026-03-12', '2026-03-13'], ['2026-03-26', '2026-04-21', '2026-04-24', '2026-04-28']), 'E003': ([], ['2026-01-26', '2026-02-10', '2026-02-13', '2026-02-23', '2026-03-06', '2026-03-09', '2026-03-10', '2026-03-11', '2026-03-12', '2026-03-13', '2026-03-23', '2026-03-31', '2026-04-02', '2026-04-07'])}
    for em_id, (f, h) in lg.items():
        for d in f: reqs.append({'id': f"L_{em_id}_{d}", 'employeeId': em_id, 'type': '特休', 'date': d, 'shift': '全天', 'days': 1.0, 'status': 'approved', 'isLegacy': True, 'agent': '不需要代理人'})
        for d in h: reqs.append({'id': f"L_{em_id}_H_{d}", 'employeeId': em_id, 'type': '特休', 'date': d, 'shift': '上午', 'days': 0.5, 'status': 'approved', 'isLegacy': True, 'agent': '不需要代理人'})
    st.session_state.requests = reqs

if not st.session_state.is_logged_in:
    st.markdown("<h2 style='text-align: center; color: #10B981;'>欣川豐杰請假系統</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.write("### 🔑 員工登入")
        em_opts = {f"{e['id']} - {e['name']}": e for e in sorted(st.session_state.employees, key=lambda x: x['id'])}
        sel_emp = st.selectbox("選擇您的姓名", ["請選擇員工..."] + list(em_opts.keys()), key="l_emp")
        pwd = st.text_input("輸入登入密碼", type="password", key="l_pwd")
        if st.button("立即進入系統", use_container_width=True, key="l_sub") and sel_emp != "請選擇員工...":
            if pwd == em_opts[sel_emp]['password']: st.session_state.is_logged_in, st.session_state.current_user, st.session_state.view = True, em_opts[sel_emp], 'dashboard'; st.rerun()
            else: st.error("密碼驗證失敗。")
    st.stop()

u = st.session_state.current_user
with st.sidebar:
    st.markdown(f"### 🏢 欣川豐杰\n**使用者:** {u['name']} ({u['department']})")
    st.write("---")
    if st.button("📊 個人功能儀表板", use_container_width=True, key="b_dash"): st.session_state.view, st.session_state.edit_req_id = 'dashboard', None; st.rerun()
    if st.button("📝 填寫請假申請單", use_container_width=True, key="b_apply"): st.session_state.view, st.session_state.edit_req_id = 'apply', None; st.rerun()
    if u['role'] == 'admin':
        st.write("---")
        st.markdown("<span style='color:#10B981; font-weight:bold;'>🛠️ 管理員控制台</span>", unsafe_allow_html=True)
        if st.button("👥 全公司特休統計", use_container_width=True, key="b_stat"): st.session_state.view = 'employees'; st.rerun()
        if st.button(f"📩 待辦審核單據 ({len([r for r in st.session_state.requests if r['status'] == 'pending'])})", use_container_width=True, key="b_mgr"): st.session_state.view = 'manage'; st.rerun()
    st.write("---")
    if st.button("🔒 安全登出系統", use_container_width=True, key="b_out"): st.session_state.is_logged_in, st.session_state.current_user = False, None; st.rerun()

t1, t2 = st.columns([3, 1])
t1.subheader(f"{u['name']}，您好")
st.session_state.selected_year = t2.selectbox("追蹤年度", [2026, 2027], index=0, key="g_year")
ud = sum([r['days'] for r in st.session_state.requests if r['employeeId'] == u['id'] and r['status'] == 'approved' and r['type'] == '特休' and str(st.session_state.selected_year) in r['date']])
co = u['carryOver'] if st.session_state.selected_year == START_YEAR else 0

if st.session_state.view == 'dashboard':
    st.markdown("#### 📅 當前年度特休權益摘要")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("當年度新特休", f"{u['totalAnnual']} 天"); m2.metric("前一年度結轉", f"{co} 天"); m3.metric("審核通過已休", f"{ud} 天"); m4.metric("剩餘可用淨額度", f"{(u['totalAnnual'] + co) - ud} 天")
    st.write("---")
    st.markdown("#### 📋 個人請假明細紀錄 (一星期內可修改或刪除)")
    my = [r for r in st.session_state.requests if r['employeeId'] == u['id']]
    if not my: st.info("目前尚無請假紀錄。")
    else:
        h1, h2, h3, h4, h5, h6, h7 = st.columns([1.5, 2.5, 1, 1, 1.2, 2, 2.5])
        h1.markdown("**假別**"); h2.markdown("**請假期間**"); h3.markdown("**時段**"); h4.markdown("**天數**"); h5.markdown("**狀態**"); h6.markdown("**代理人**"); h7.markdown("**功能操作**")
        st.markdown("<hr style='margin: 5px 0;'/>", unsafe_allow_html=True)
        for r in sorted(my, key=lambda x: x['date'], reverse=True):
            c1, c2, c3, c4, c5, c6, c7 = st.columns([1.5, 2.5, 1, 1, 1.2, 2, 2.5])
            c1.write(r['type']); c2.write(r['date']); c3.write(r['shift']); c4.write(f"{r['days']} 天")
            c5.write({'approved': '🟢 已核准', 'pending': '🟡 待審核', 'rejected': '🔴 已駁回'}.get(r['status'], r['status'])); c6.write(r['agent'])
            if is_action_allowed(r['date'], r.get('isLegacy', False)):
                b1, b2 = c7.columns(2)
                if b1.button("📝 修改", key=f"ed_{r['id']}", use_container_width=True): st.session_state.edit_req_id, st.session_state.view = r['id'], 'apply'; st.rerun()
                if b2.button("🗑️ 刪除", key=f"dl_{r['id']}", use_container_width=True): st.session_state.requests.remove(r); st.toast("🗑️ 已成功刪除！"); st.rerun()
            else: c7.caption("🔒 已超過1星期鎖定")
    st.write("---")
    st.markdown("#### 🔒 修改個人登入密碼")
    c_p1, c_p2 = st.columns([2, 1])
    new_pwd = c_p1.text_input("輸入您想設定的新密碼", type="password", key="new_pwd_input", placeholder="請輸入新密碼...")
    if c_p2.button("💾 確認修改密碼", use_container_width=True, key="change_pwd_btn") and new_pwd:
        next(e for e in st.session_state.employees if e['id'] == u['id'])['password'] = new_pwd
        st.toast("🎉 密碼修改成功！")

elif st.session_state.view == 'apply':
    is_ed = st.session_state.edit_req_id is not None
    treq = next((r for r in st.session_state.requests if r['id'] == st.session_state.edit_req_id), None) if is_ed else None
    st.markdown(f"#### 📝 {'修改' if is_ed else '填寫'}請假申請單")
    ag_opts = ["不需要代理人"] + [e['name'] for e in sorted(st.session_state.employees, key=lambda x: x['id']) if e['id'] != u['id']]
    l_type = st.selectbox("選擇請假假別", ['特休', '病假', '事假', '公假'], index=['特休', '病假', '事假', '公假'].index(treq['type'] if is_ed else '特休'))
    c_d1, c_d2 = st.columns(2)
    l_start = c_d1.date_input("請假開始日期", datetime.now())
    l_end = c_d2.date_input("請假結束日期", value=l_start)
    l_shift = st.radio("請假時段", ['全天', '上午', '下午'], index=['全天', '上午', '下午'].index(treq['shift'] if is_ed else '全天'), horizontal=True)
    l_agent = st.selectbox("職務代理人協助", ag_opts, index=ag_opts.index(treq['agent'] if is_ed and treq['agent'] in ag_opts else "不需要代理人"))
    if st.button("🚀 確認送出假單", use_container_width=True, key="f_sub"):
        if l_end < l_start: st.error("❌ 結束日期不能早於開始日期！")
        else:
            ds = calculate_work_days(l_start, l_end, l_shift)
            if ds == 0: st.warning("⚠️ 期間內均為例假日，不需請假。")
            else:
                lbl = f"{l_start.strftime('%Y-%m-%d')} 至 {l_end.strftime('%Y-%m-%d')}" if l_start != l_end else l_start.strftime('%Y-%m-%d')
                if is_ed and treq: treq.update({'type': l_type, 'date': lbl, 'shift': l_shift, 'days': ds, 'agent': l_agent, 'status': 'pending'})
                else: st.session_state.requests.append({'id': f"R{int(datetime.now().timestamp())}", 'employeeId': u['id'], 'type': l_type, 'date': lbl, 'shift': l_shift, 'days': ds, 'status': 'pending', 'isLegacy': False, 'agent': l_agent})
                st.session_state.edit_req_id, st.session_state.view = None, 'dashboard'; st.rerun()

elif st.session_state.view == 'employees' and u['role'] == 'admin':
    st.markdown("#### 👥 全公司特休總額度統計")
    s_data = []
    for emp in st.session_state.employees:
        emp_used = sum([r['days'] for r in st.session_state.requests if r['employeeId'] == emp['id'] and r['status'] == 'approved' and r['type'] == '特休' and str(st.session_state.selected_year) in r['date']])
        carry = emp['carryOver'] if st.session_state.selected_year == START_YEAR else 0
        s_data.append({'工號': emp['id'], '姓名': emp['name'], '部門': emp['department'], '年度新假': emp['totalAnnual'], '上年結轉': carry, '總額度': emp['totalAnnual'] + carry, '已休': emp_used, '剩餘': (emp['totalAnnual'] + carry) - emp_used})
    st.dataframe(pd.DataFrame(s_data), use_container_width=True)
    st.write("---")
    st.markdown("#### 🔍 員工個別請假詳細內容查詢")
    emp_map = {f"{e['id']} - {e['name']}": e for e in sorted(st.session_state.employees, key=lambda x: x['id'])}
    sel_q = st.selectbox("選擇要查詢的員工姓名", ["請選擇員工..."] + list(emp_map.keys()), key="q_emp")
    if sel_q != "請選擇員工...":
        t_emp = emp_map[sel_q]
        e_list = [r for r in st.session_state.requests if r['employeeId'] == t_emp['id']]
        if not e_list: st.info(f"💡 員工 【{t_emp['name']}】 目前尚無請假紀錄。")
        else:
            q_df = [{'假別': r['type'], '請假期間': r['date'], '時段': r['shift'], '扣除天數': f"{r['days']} 天", '狀態': {'approved': '🟢 已核准', 'pending': '🟡 待審核', 'rejected': '🔴 已駁回'}.get(r['status'], r['status']), '職務代理人': r['agent']} for r in sorted(e_list, key=lambda x: x['date'], reverse=True)]
            st.dataframe(pd.DataFrame(q_df), use_container_width=True)

elif st.session_state.view == 'manage' and u['role'] == 'admin':
    st.markdown("#### 📩 待審核單據管理")
    p_list = [r for r in st.session_state.requests if r['status'] == 'pending']
    if not p_list: st.info("🎉 暫無任何需要審核的假單。")
    else:
        for r in p_list:
            emp = next((e for e in st.session_state.employees if e['id'] == r['employeeId']), None)
            st.write(f"**申請人:** {emp['name']} ｜ **假別:** {r['type']} ｜ **期間:** {r['date']} ({r['shift']} ｜ 共 {r['days']} 天) ｜ **代理人:** {r['agent']}")
            ca, cr = st.columns(2)
            if ca.button("✅ 核准", key=f"ok_{r['id']}", use_container_width=True): r['status'] = 'approved'; st.rerun()
            if cr.button("❌ 駁回", key=f"no_{r['id']}", use_container_width=True): r['status'] = 'rejected'; st.rerun()
            st.write("---")
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="欣川豐杰請假系統", page_icon="📊", layout="wide")
DEFAULT_PASSWORD, START_YEAR = '04698438', 2026
HOLIDAYS_2026 = {"2026-01-01", "2026-02-16", "2026-02-17", "2026-02-18", "2026-02-19", "2026-02-20", "2026-02-21", "2026-02-27", "2026-02-28", "2026-04-02", "2026-04-03", "2026-05-01", "2026-06-19", "2026-06-20", "2026-09-25", "2026-10-09", "2026-10-10"}

def calculate_work_days(s, e, shift):
    if shift in ['上午', '下午']: return 0.5
    curr, days = s, 0.0
    while curr <= e:
        if curr.weekday() < 5 and curr.strftime("%Y-%m-%d") not in HOLIDAYS_2026: days += 1.0
        curr += timedelta(days=1)
    return days

def is_action_allowed(d_str, is_legacy):
    if is_legacy: return False
    try: return (datetime.now() - datetime.strptime(d_str.split(" ")[0], "%Y-%m-%d")).days <= 7
    except: return False

for k, v in [('is_logged_in', False), ('current_user', None), ('view', 'dashboard'), ('selected_year', START_YEAR), ('edit_req_id', None)]:
    if k not in st.session_state: st.session_state[k] = v

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

if 'requests' not in st.session_state:
    reqs, lg = [], {'E002': (['2026-01-29', '2026-02-26', '2026-03-18', '2026-03-30', '2026-04-16'], []), 'E005': (['2026-03-12', '2026-03-18', '2026-03-27', '2026-04-23'], []), 'E006': (['2026-01-13', '2026-01-16', '2026-01-23', '2026-02-09', '2026-03-05', '2026-03-13'], ['2026-01-09', '2026-01-30', '2026-02-06', '2026-03-03', '2026-03-27']), 'E007': (['2026-01-21', '2026-02-12', '2026-03-02', '2026-03-03', '2026-03-27', '2026-04-20'], ['2026-01-16', '2026-01-19', '2026-01-20', '2026-03-20', '2026-03-23', '2026-04-28']), 'E008': (['2026-04-02', '2026-04-14', '2026-04-15'], ['2026-03-17', '2026-03-20', '2026-03-27', '2026-04-21', '2026-04-28', '2026-04-30']), 'E011': (['2026-03-16', '2026-03-23', '2026-03-30', '2026-04-20'], ['2026-01-16', '2026-02-05', '2026-03-25']), 'E015': (['2026-01-02', '2026-02-24', '2026-04-01', '2026-04-02'], []), 'E001': (['2026-01-19', '2026-01-29', '2026-03-17'], ['2026-01-28', '2026-04-28']), 'E016': (['2026-03-10', '2026-03-11', '2026-03-12', '2026-03-13'], ['2026-03-26', '2026-04-21', '2026-04-24', '2026-04-28']), 'E003': ([], ['2026-01-26', '2026-02-10', '2026-02-13', '2026-02-23', '2026-03-06', '2026-03-09', '2026-03-10', '2026-03-11', '2026-03-12', '2026-03-13', '2026-03-23', '2026-03-31', '2026-04-02', '2026-04-07'])}
    for em_id, (f, h) in lg.items():
        for d in f: reqs.append({'id': f"L_{em_id}_{d}", 'employeeId': em_id, 'type': '特休', 'date': d, 'shift': '全天', 'days': 1.0, 'status': 'approved', 'isLegacy': True, 'agent': '不需要代理人'})
        for d in h: reqs.append({'id': f"L_{em_id}_H_{d}", 'employeeId': em_id, 'type': '特休', 'date': d, 'shift': '上午', 'days': 0.5, 'status': 'approved', 'isLegacy': True, 'agent': '不需要代理人'})
    st.session_state.requests = reqs

if not st.session_state.is_logged_in:
    st.markdown("<h2 style='text-align: center; color: #10B981;'>欣川豐杰請假系統</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.write("### 🔑 員工登入")
        em_opts = {f"{e['id']} - {e['name']}": e for e in sorted(st.session_state.employees, key=lambda x: x['id'])}
        sel_emp = st.selectbox("選擇您的姓名", ["請選擇員工..."] + list(em_opts.keys()), key="l_emp")
        pwd = st.text_input("輸入登入密碼", type="password", key="l_pwd")
        if st.button("立即進入系統", use_container_width=True, key="l_sub") and sel_emp != "請選擇員工...":
            if pwd == em_opts[sel_emp]['password']: st.session_state.is_logged_in, st.session_state.current_user, st.session_state.view = True, em_opts[sel_emp], 'dashboard'; st.rerun()
            else: st.error("密碼驗證失敗。")
    st.stop()

u = st.session_state.current_user
with st.sidebar:
    st.markdown(f"### 🏢 欣川豐杰\n**使用者:** {u['name']} ({u['department']})")
    st.write("---")
    if st.button("📊 個人功能儀表板", use_container_width=True, key="b_dash"): st.session_state.view, st.session_state.edit_req_id = 'dashboard', None; st.rerun()
    if st.button("📝 填寫請假申請單", use_container_width=True, key="b_apply"): st.session_state.view, st.session_state.edit_req_id = 'apply', None; st.rerun()
    if u['role'] == 'admin':
        st.write("---")
        st.markdown("<span style='color:#10B981; font-weight:bold;'>🛠️ 管理員控制台</span>", unsafe_allow_html=True)
        if st.button("👥 全公司特休統計", use_container_width=True, key="b_stat"): st.session_state.view = 'employees'; st.rerun()
        if st.button(f"📩 待辦審核單據 ({len([r for r in st.session_state.requests if r['status'] == 'pending'])})", use_container_width=True, key="b_mgr"): st.session_state.view = 'manage'; st.rerun()
    st.write("---")
    if st.button("🔒 安全登出系統", use_container_width=True, key="b_out"): st.session_state.is_logged_in, st.session_state.current_user = False, None; st.rerun()

t1, t2 = st.columns([3, 1])
t1.subheader(f"{u['name']}，您好")
st.session_state.selected_year = t2.selectbox("追蹤年度", [2026, 2027], index=0, key="g_year")
ud = sum([r['days'] for r in st.session_state.requests if r['employeeId'] == u['id'] and r['status'] == 'approved' and r['type'] == '特休' and str(st.session_state.selected_year) in r['date']])
co = u['carryOver'] if st.session_state.selected_year == START_YEAR else 0

if st.session_state.view == 'dashboard':
    st.markdown("#### 📅 當前年度特休權益摘要")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("當年度新特休", f"{u['totalAnnual']} 天"); m2.metric("前一年度結轉", f"{co} 天"); m3.metric("審核通過已休", f"{ud} 天"); m4.metric("剩餘可用淨額度", f"{(u['totalAnnual'] + co) - ud} 天")
    st.write("---")
    st.markdown("#### 📋 個人請假明細紀錄 (一星期內可修改或刪除)")
    my = [r for r in st.session_state.requests if r['employeeId'] == u['id']]
    if not my: st.info("目前尚無請假紀錄。")
    else:
        h1, h2, h3, h4, h5, h6, h7 = st.columns([1.5, 2.5, 1, 1, 1.2, 2, 2.5])
        h1.markdown("**假別**"); h2.markdown("**請假期間**"); h3.markdown("**時段**"); h4.markdown("**天數**"); h5.markdown("**狀態**"); h6.markdown("**代理人**"); h7.markdown("**功能操作**")
        st.markdown("<hr style='margin: 5px 0;'/>", unsafe_allow_html=True)
        for r in sorted(my, key=lambda x: x['date'], reverse=True):
            c1, c2, c3, c4, c5, c6, c7 = st.columns([1.5, 2.5, 1, 1, 1.2, 2, 2.5])
            c1.write(r['type']); c2.write(r['date']); c3.write(r['shift']); c4.write(f"{r['days']} 天")
            c5.write({'approved': '🟢 已核准', 'pending': '🟡 待審核', 'rejected': '🔴 已駁回'}.get(r['status'], r['status'])); c6.write(r['agent'])
            if is_action_allowed(r['date'], r.get('isLegacy', False)):
                b1, b2 = c7.columns(2)
                if b1.button("📝 修改", key=f"ed_{r['id']}", use_container_width=True): st.session_state.edit_req_id, st.session_state.view = r['id'], 'apply'; st.rerun()
                if b2.button("🗑️ 刪除", key=f"dl_{r['id']}", use_container_width=True): st.session_state.requests.remove(r); st.toast("🗑️ 已成功刪除！"); st.rerun()
            else: c7.caption("🔒 已超過1星期鎖定")
    st.write("---")
    st.markdown("#### 🔒 修改個人登入密碼")
    c_p1, c_p2 = st.columns([2, 1])
    new_pwd = c_p1.text_input("輸入您想設定的新密碼", type="password", key="new_pwd_input", placeholder="請輸入新密碼...")
    if c_p2.button("💾 確認修改密碼", use_container_width=True, key="change_pwd_btn") and new_pwd:
        next(e for e in st.session_state.employees if e['id'] == u['id'])['password'] = new_pwd
        st.toast("🎉 密碼修改成功！")

elif st.session_state.view == 'apply':
    is_ed = st.session_state.edit_req_id is not None
    treq = next((r for r in st.session_state.requests if r['id'] == st.session_state.edit_req_id), None) if is_ed else None
    st.markdown(f"#### 📝 {'修改' if is_ed else '填寫'}請假申請單")
    ag_opts = ["不需要代理人"] + [e['name'] for e in sorted(st.session_state.employees, key=lambda x: x['id']) if e['id'] != u['id']]
    l_type = st.selectbox("選擇請假假別", ['特休', '病假', '事假', '公假'], index=['特休', '病假', '事假', '公假'].index(treq['type'] if is_ed else '特休'))
    c_d1, c_d2 = st.columns(2)
    l_start = c_d1.date_input("請假開始日期", datetime.now())
    l_end = c_d2.date_input("請假結束日期", value=l_start)
    l_shift = st.radio("請假時段", ['全天', '上午', '下午'], index=['全天', '上午', '下午'].index(treq['shift'] if is_ed else '全天'), horizontal=True)
    l_agent = st.selectbox("職務代理人協助", ag_opts, index=ag_opts.index(treq['agent'] if is_ed and treq['agent'] in ag_opts else "不需要代理人"))
    if st.button("🚀 確認送出假單", use_container_width=True, key="f_sub"):
        if l_end < l_start: st.error("❌ 結束日期不能早於開始日期！")
        else:
            ds = calculate_work_days(l_start, l_end, l_shift)
            if ds == 0: st.warning("⚠️ 期間內均為例假日，不需請假。")
            else:
                lbl = f"{l_start.strftime('%Y-%m-%d')} 至 {l_end.strftime('%Y-%m-%d')}" if l_start != l_end else l_start.strftime('%Y-%m-%d')
                if is_ed and treq: treq.update({'type': l_type, 'date': lbl, 'shift': l_shift, 'days': ds, 'agent': l_agent, 'status': 'pending'})
                else: st.session_state.requests.append({'id': f"R{int(datetime.now().timestamp())}", 'employeeId': u['id'], 'type': l_type, 'date': lbl, 'shift': l_shift, 'days': ds, 'status': 'pending', 'isLegacy': False, 'agent': l_agent})
                st.session_state.edit_req_id, st.session_state.view = None, 'dashboard'; st.rerun()

elif st.session_state.view == 'employees' and u['role'] == 'admin':
    st.markdown("#### 👥 全公司特休總額度統計")
    s_data = []
    for emp in st.session_state.employees:
        emp_used = sum([r['days'] for r in st.session_state.requests if r['employeeId'] == emp['id'] and r['status'] == 'approved' and r['type'] == '特休' and str(st.session_state.selected_year) in r['date']])
        carry = emp['carryOver'] if st.session_state.selected_year == START_YEAR else 0
        s_data.append({'工號': emp['id'], '姓名': emp['name'], '部門': emp['department'], '年度新假': emp['totalAnnual'], '上年結轉': carry, '總額度': emp['totalAnnual'] + carry, '已休': emp_used, '剩餘': (emp['totalAnnual'] + carry) - emp_used})
    st.dataframe(pd.DataFrame(s_data), use_container_width=True)
    st.write("---")
    st.markdown("#### 🔍 員工個別請假詳細內容查詢")
    emp_map = {f"{e['id']} - {e['name']}": e for e in sorted(st.session_state.employees, key=lambda x: x['id'])}
    sel_q = st.selectbox("選擇要查詢的員工姓名", ["請選擇員工..."] + list(emp_map.keys()), key="q_emp")
    if sel_q != "請選擇員工...":
        t_emp = emp_map[sel_q]
        e_list = [r for r in st.session_state.requests if r['employeeId'] == t_emp['id']]
        if not e_list: st.info(f"💡 員工 【{t_emp['name']}】 目前尚無請假紀錄。")
        else:
            q_df = [{'假別': r['type'], '請假期間': r['date'], '時段': r['shift'], '扣除天數': f"{r['days']} 天", '狀態': {'approved': '🟢 已核准', 'pending': '🟡 待審核', 'rejected': '🔴 已駁回'}.get(r['status'], r['status']), '職務代理人': r['agent']} for r in sorted(e_list, key=lambda x: x['date'], reverse=True)]
            st.dataframe(pd.DataFrame(q_df), use_container_width=True)

elif st.session_state.view == 'manage' and u['role'] == 'admin':
    st.markdown("#### 📩 待審核單據管理")
    p_list = [r for r in st.session_state.requests if r['status'] == 'pending']
    if not p_list: st.info("🎉 暫無任何需要審核的假單。")
    else:
        for r in p_list:
            emp = next((e for e in st.session_state.employees if e['id'] == r['employeeId']), None)
            st.write(f"**申請人:** {emp['name']} ｜ **假別:** {r['type']} ｜ **期間:** {r['date']} ({r['shift']} ｜ 共 {r['days']} 天) ｜ **代理人:** {r['agent']}")
            ca, cr = st.columns(2)
            if ca.button("✅ 核准", key=f"ok_{r['id']}", use_container_width=True): r['status'] = 'approved'; st.rerun()
            if cr.button("❌ 駁回", key=f"no_{r['id']}", use_container_width=True): r['status'] = 'rejected'; st.rerun()
            st.write("---")

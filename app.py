import React, { useState, useMemo, useEffect } from 'react';
import { 
  Calendar, User, ShieldCheck, Clock, CheckCircle2, XCircle, Plus, Users, 
  FileText, LogOut, ChevronRight, Lock, Settings, KeyRound, ListOrdered, 
  ArrowUpDown, UserCheck, Bell, Search, Filter, Mail, Send, Edit, 
  Trash2, AlertCircle, PieChart, ClipboardList, UserPlus, Hash, ChevronDown, 
  History, Loader2
} from 'lucide-react';

// Firebase Imports
import { initializeApp } from 'firebase/app';
import { getAuth, signInAnonymously, signInWithCustomToken, onAuthStateChanged } from 'firebase/auth';
import { getFirestore, collection, doc, setDoc, getDoc, getDocs, updateDoc, deleteDoc, onSnapshot, query } from 'firebase/firestore';

// --- 配置與常數 ---
const DEFAULT_PASSWORD = '04698438';
const MANAGER_EMAIL = 'heiman1209@gmail.com';
const START_YEAR = 2026; 

// 初始員工資料 (種子資料)
const SEED_EMPLOYEES = [
  { id: 'E001', name: '陳秋漢', role: 'employee', department: '儀控部', totalAnnual: 30, carryOver: 20, password: DEFAULT_PASSWORD },
  { id: 'E002', name: '楊偉昇', role: 'employee', department: '儀控部', totalAnnual: 30, carryOver: 0, password: DEFAULT_PASSWORD },
  { id: 'E003', name: '施文吉', role: 'employee', department: '儀控部', totalAnnual: 30, carryOver: 0, password: DEFAULT_PASSWORD },
  { id: 'E004', name: '黃兩家', role: 'employee', department: '儀控部', totalAnnual: 30, carryOver: 0, password: DEFAULT_PASSWORD },
  { id: 'E016', name: '蔡秀惠', role: 'admin', department: '行政部', totalAnnual: 30, carryOver: 0, password: DEFAULT_PASSWORD },
  { id: 'E005', name: '鄭惠蓉', role: 'employee', department: '儀控部', totalAnnual: 30, carryOver: 0, password: DEFAULT_PASSWORD },
  { id: 'E006', name: '蔡雅菁', role: 'employee', department: '儀控部', totalAnnual: 30, carryOver: 0, password: DEFAULT_PASSWORD },
  { id: 'E007', name: '呂麗杏', role: 'employee', department: '儀控部', totalAnnual: 30, carryOver: 0, password: DEFAULT_PASSWORD },
  { id: 'E008', name: '黃嘉銘', role: 'employee', department: '儀控部', totalAnnual: 25, carryOver: 0, password: DEFAULT_PASSWORD },
  { id: 'E009', name: '蘇忠泰', role: 'employee', department: '流量計', totalAnnual: 30, carryOver: 0, password: DEFAULT_PASSWORD },
  { id: 'E010', name: '葉錦達', role: 'employee', department: '流量計', totalAnnual: 30, carryOver: 0, password: DEFAULT_PASSWORD },
  { id: 'E011', name: '陳秋霞', role: 'employee', department: '流量計', totalAnnual: 30, carryOver: 0, password: DEFAULT_PASSWORD },
  { id: 'E012', name: '林信佑', role: 'employee', department: '流量計', totalAnnual: 30, carryOver: 0, password: DEFAULT_PASSWORD },
  { id: 'E013', name: '宋志銘', role: 'employee', department: '流量計', totalAnnual: 14, carryOver: 0, password: DEFAULT_PASSWORD },
  { id: 'E014', name: '王英杰', role: 'employee', department: '譯碼器', totalAnnual: 26, carryOver: 0, password: DEFAULT_PASSWORD },
  { id: 'E015', name: '蘇雅瑄', role: 'employee', department: '譯碼器', totalAnnual: 23, carryOver: 0, password: DEFAULT_PASSWORD },
];

// 1-4 月歷史紀錄 (種子資料)
const SEED_REQUESTS = [
  ...['2026-01-29', '2026-02-26', '2026-03-18', '2026-03-30', '2026-04-16'].map(d => ({ id: `L_E002_${d}`, employeeId: 'E002', type: '特休', date: d, duration: '1.0', shift: '全天', days: 1.0, status: 'approved', isLegacy: true })),
  ...['2026-01-26', '2026-02-10', '2026-02-13', '2026-02-23', '2026-03-06', '2026-03-09', '2026-03-10', '2026-03-11', '2026-03-12', '2026-03-13', '2026-03-23', '2026-03-31', '2026-04-02', '2026-04-07'].map(d => ({ id: `L_E003_${d}`, employeeId: 'E003', type: '特休', date: d, duration: '0.5', shift: '上午', days: 0.5, status: 'approved', isLegacy: true })),
  ...['2026-03-12', '2026-03-18', '2026-03-27', '2026-04-23'].map(d => ({ id: `L_E005_${d}`, employeeId: 'E005', type: '特休', date: d, duration: '1.0', shift: '全天', days: 1.0, status: 'approved', isLegacy: true })),
  ...['2026-01-13', '2026-01-16', '2026-01-23', '2026-02-09', '2026-03-05', '2026-03-13'].map(d => ({ id: `L_E006_${d}`, employeeId: 'E006', type: '特休', date: d, duration: '1.0', shift: '全天', days: 1.0, status: 'approved', isLegacy: true })),
  ...['2026-01-09', '2026-01-30', '2026-02-06', '2026-03-03', '2026-03-27'].map(d => ({ id: `L_E006_H_${d}`, employeeId: 'E006', type: '特休', date: d, duration: '0.5', shift: '上午', days: 0.5, status: 'approved', isLegacy: true })),
  ...['2026-01-21', '2026-02-12', '2026-03-02', '2026-03-03', '2026-03-27', '2026-04-20'].map(d => ({ id: `L_E007_${d}`, employeeId: 'E007', type: '特休', date: d, duration: '1.0', shift: '全天', days: 1.0, status: 'approved', isLegacy: true })),
  ...['2026-01-16', '2026-01-19', '2026-01-20', '2026-03-20', '2026-03-23', '2026-04-28'].map(d => ({ id: `L_E007_H_${d}`, employeeId: 'E007', type: '特休', date: d, duration: '0.5', shift: '上午', days: 0.5, status: 'approved', isLegacy: true })),
  ...['2026-04-02', '2026-04-14', '2026-04-15'].map(d => ({ id: `L_E008_${d}`, employeeId: 'E008', type: '特休', date: d, duration: '1.0', shift: '全天', days: 1.0, status: 'approved', isLegacy: true })),
  ...['2026-03-17', '2026-03-20', '2026-03-27', '2026-04-21', '2026-04-28', '2026-04-30'].map(d => ({ id: `L_E008_H_${d}`, employeeId: 'E008', type: '特休', date: d, duration: '0.5', shift: '上午', days: 0.5, status: 'approved', isLegacy: true })),
  ...['2026-03-16', '2026-03-23', '2026-03-30', '2026-04-20'].map(d => ({ id: `L_E011_${d}`, employeeId: 'E011', type: '特休', date: d, duration: '1.0', shift: '全天', days: 1.0, status: 'approved', isLegacy: true })),
  ...['2026-01-16', '2026-02-05', '2026-03-25'].map(d => ({ id: `L_E011_H_${d}`, employeeId: 'E011', type: '特休', date: d, duration: '0.5', shift: '上午', days: 0.5, status: 'approved', isLegacy: true })),
  ...['2026-01-02', '2026-02-24', '2026-04-01', '2026-04-02'].map(d => ({ id: `L_E015_${d}`, employeeId: 'E015', type: '特休', date: d, duration: '1.0', shift: '全天', days: 1.0, status: 'approved', isLegacy: true })),
  ...['2026-01-19', '2026-01-29', '2026-03-17'].map(d => ({ id: `L_E001_${d}`, employeeId: 'E001', type: '特休', date: d, duration: '1.0', shift: '全天', days: 1.0, status: 'approved', isLegacy: true })),
  ...['2026-01-28', '2026-04-28'].map(d => ({ id: `L_E001_H_${d}`, employeeId: 'E001', type: '特休', date: d, duration: '0.5', shift: '上午', days: 0.5, status: 'approved', isLegacy: true })),
  ...['2026-03-10', '2026-03-11', '2026-03-12', '2026-03-13'].map(d => ({ id: `L_E016_${d}`, employeeId: 'E016', type: '特休', date: d, duration: '1.0', shift: '全天', days: 1.0, status: 'approved', isLegacy: true })),
  ...['2026-03-26', '2026-04-21', '2026-04-24', '2026-04-28'].map(d => ({ id: `L_E016_H_${d}`, employeeId: 'E016', type: '特休', date: d, duration: '0.5', shift: '上午', days: 0.5, status: 'approved', isLegacy: true })),
];

// --- Firebase 初始化 ---
const firebaseConfig = JSON.parse(__firebase_config);
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);
const appId = typeof __app_id !== 'undefined' ? __app_id : 'leave-flow-system';

export default function App() {
  // --- 狀態定義 ---
  const [user, setUser] = useState(null);
  const [employees, setEmployees] = useState([]);
  const [requests, setRequests] = useState([]);
  const [currentUserData, setCurrentUserData] = useState(null); 
  const [loading, setLoading] = useState(true);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  
  const [view, setView] = useState('dashboard');
  const [selectedYear, setSelectedYear] = useState(START_YEAR);
  const [passwordInput, setPasswordInput] = useState('');
  const [loginError, setLoginError] = useState('');
  const [emailNotification, setEmailNotification] = useState(null);
  
  // UI 狀態
  const [adminFilterId, setAdminFilterId] = useState(''); 
  const [adminSortBy, setAdminSortBy] = useState('id'); 
  const [editingRequestId, setEditingRequestId] = useState(null);
  const [formData, setFormData] = useState({ 
    type: '特休', date: '', duration: '1.0', shift: '全天', deputyId: '', reason: '' 
  });

  // --- Firebase 核心邏輯 ---

  // 1. 初始化 Auth
  useEffect(() => {
    const initAuth = async () => {
      try {
        if (typeof __initial_auth_token !== 'undefined' && __initial_auth_token) {
          await signInWithCustomToken(auth, __initial_auth_token);
        } else {
          await signInAnonymously(auth);
        }
      } catch (err) {
        console.error("Auth error", err);
      }
    };
    initAuth();
    const unsubscribe = onAuthStateChanged(auth, setUser);
    return () => unsubscribe();
  }, []);

  // 2. 初始化與實時監聽數據 (RULE 1 & 3)
  useEffect(() => {
    if (!user) return;

    const employeesRef = collection(db, 'artifacts', appId, 'public', 'data', 'employees');
    const requestsRef = collection(db, 'artifacts', appId, 'public', 'data', 'requests');

    // 監聽員工資料
    const unsubEmployees = onSnapshot(employeesRef, (snapshot) => {
      if (snapshot.empty) {
        # 第一次啟動：種子初始化
        SEED_EMPLOYEES.forEach(emp => {
          setDoc(doc(employeesRef, emp.id), emp);
        });
      } else {
        const emps = snapshot.docs.map(doc => doc.data());
        setEmployees(emps);
      }
    }, (err) => console.error("Employee snapshot error", err));

    // 監聽請假紀錄
    const unsubRequests = onSnapshot(requestsRef, (snapshot) => {
      if (snapshot.empty) {
        // 第一次啟動：匯入前期紀錄
        SEED_REQUESTS.forEach(req => {
          setDoc(doc(requestsRef, req.id), req);
        });
      } else {
        const reqs = snapshot.docs.map(doc => doc.data());
        setRequests(reqs);
      }
      setLoading(false);
    }, (err) => console.error("Request snapshot error", err));

    return () => { unsubEmployees(); unsubRequests(); };
  }, [user]);

  // --- 計算屬性 ---

  // 計算當前登入者數據
  const myYearlyStats = useMemo(() => {
    if (!currentUserData) return { totalPossible: 0, used: 0, remaining: 0, carryOver: 0, currentEntitlement: 0 };
    const yearRequests = requests.filter(r => 
      r.employeeId === currentUserData.id && 
      new Date(r.date).getFullYear() === selectedYear &&
      r.status === 'approved' && 
      r.type === '特休'
    );
    const used = yearRequests.reduce((sum, r) => sum + r.days, 0);
    const totalPossible = (currentUserData.totalAnnual || 0) + (currentUserData.carryOver || 0);
    return { 
      currentEntitlement: currentUserData.totalAnnual,
      carryOver: currentUserData.carryOver || 0,
      totalPossible,
      used, 
      remaining: totalPossible - used 
    };
  }, [requests, currentUserData, selectedYear]);

  const availableDeputies = useMemo(() => 
    employees.filter(emp => emp.id !== currentUserData?.id),
    [employees, currentUserData]
  );

  const filteredApprovedRequests = useMemo(() => {
    let result = requests.filter(r => r.status === 'approved' && new Date(r.date).getFullYear() === selectedYear);
    if (adminFilterId) result = result.filter(r => r.employeeId === adminFilterId);
    return [...result].sort((a, b) => {
      if (adminSortBy === 'id') {
        const idSort = a.employeeId.localeCompare(b.employeeId);
        return idSort !== 0 ? idSort : b.date.localeCompare(a.date);
      }
      return b.date.localeCompare(a.date);
    });
  }, [requests, adminFilterId, adminSortBy, selectedYear]);

  // --- 操作邏輯 ---

  const handleLogin = (e) => {
    e.preventDefault();
    const found = employees.find(emp => emp.name === currentUserData?.name);
    if (found && passwordInput === found.password) {
      setIsLoggedIn(true);
      setLoginError('');
      setPasswordInput('');
    } else {
      setLoginError('密碼驗證失敗，請重試。');
    }
  };

  const isActionExpired = (dateString, isLegacy) => {
    if (isLegacy) return true;
    if (!dateString) return true;
    const leaveDate = new Date(dateString);
    const today = new Date();
    const expiryDate = new Date(leaveDate);
    expiryDate.setDate(leaveDate.getDate() + 7);
    return today > expiryDate;
  };

  const triggerMultiNotification = (request, isUpdate = false) => {
    const deputy = employees.find(e => e.id === request.deputyId);
    setEmailNotification({
      message: `【欣川豐杰】請假${isUpdate ? '修改' : '申請'}通知`,
      manager: MANAGER_EMAIL,
      deputyName: deputy ? deputy.name : null
    });
    setTimeout(() => setEmailNotification(null), 6000);
  };

  const handleSubmitLeave = async (e) => {
    e.preventDefault();
    if (!formData.date || !user) return;
    const days = parseFloat(formData.duration);
    const requestsRef = collection(db, 'artifacts', appId, 'public', 'data', 'requests');

    if (editingRequestId) {
      await updateDoc(doc(requestsRef, editingRequestId), { ...formData, days, status: 'pending' });
      setEditingRequestId(null);
    } else {
      const newId = `R${Date.now()}`;
      const newRequest = {
        id: newId, employeeId: currentUserData.id, ...formData, days, status: 'pending',
        createdAt: new Date().toISOString()
      };
      await setDoc(doc(requestsRef, newId), newRequest);
      triggerMultiNotification(newRequest);
    }
    setView('dashboard');
    setFormData({ type: '特休', date: '', duration: '1.0', shift: '全天', deputyId: '', reason: '' });
  };

  const handleDeleteRequest = async (id) => {
    const req = requests.find(r => r.id === id);
    if (req && !isActionExpired(req.date, req.isLegacy)) {
      const requestsRef = collection(db, 'artifacts', appId, 'public', 'data', 'requests');
      await deleteDoc(doc(requestsRef, id));
    }
  };

  const handleReview = async (requestId, status) => {
    const requestsRef = collection(db, 'artifacts', appId, 'public', 'data', 'requests');
    await updateDoc(doc(requestsRef, requestId), { status });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-900 flex flex-col items-center justify-center text-white gap-4">
        <Loader2 className="w-10 h-10 animate-spin text-emerald-500" />
        <p className="font-black uppercase tracking-widest text-xs animate-pulse">Connecting to LeaveFlow Cloud...</p>
      </div>
    );
  }

  if (!isLoggedIn) {
    return (
      <div className="min-h-screen bg-slate-900 flex items-center justify-center p-4">
        <div className="max-w-md w-full bg-white rounded-[2.5rem] shadow-2xl overflow-hidden p-10 text-center border-t-8 border-emerald-500">
          <div className="flex flex-col items-center mb-8">
            <div className="w-20 h-20 bg-emerald-50 text-emerald-600 rounded-full flex items-center justify-center mb-4"><Lock className="w-10 h-10" /></div>
            <h2 className="text-2xl font-black text-slate-800">欣川豐杰請假系統</h2>
            <p className="text-slate-400 text-sm font-medium mt-1 uppercase tracking-widest">雲端同步版已架設</p>
          </div>
          <form onSubmit={handleLogin} className="space-y-4">
            <div className="space-y-1">
              <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest text-left ml-2">選擇您的姓名</p>
              <select className="w-full p-4 bg-slate-50 border-2 border-slate-100 rounded-2xl outline-none font-bold text-slate-700" value={currentUserData?.id || ''} onChange={(e) => setCurrentUserData(employees.find(emp => emp.id === e.target.value))}>
                <option value="">請點擊選擇員工...</option>
                {employees.sort((a,b) => a.id.localeCompare(b.id)).map(emp => <option key={emp.id} value={emp.id}>{emp.id} - {emp.name}</option>)}
              </select>
            </div>
            <div className="space-y-1">
              <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest text-left ml-2">登入密碼</p>
              <input type="password" placeholder="••••••••" className="w-full p-4 bg-slate-50 border-2 border-slate-100 rounded-2xl outline-none text-center text-xl tracking-widest focus:border-emerald-500" value={passwordInput} onChange={(e) => setPasswordInput(e.target.value)}/>
            </div>
            {loginError && <p className="text-red-500 text-xs font-bold">{loginError}</p>}
            <button type="submit" className="w-full bg-slate-900 text-white font-black py-5 rounded-2xl hover:bg-black transition-all shadow-xl mt-4">立即進入系統</button>
          </form>
          <p className="mt-6 text-[10px] text-slate-300 font-bold">初次登入預設密碼為 04698438</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col md:flex-row font-sans text-slate-900">
      {/* Toast */}
      {emailNotification && (
        <div className="fixed top-6 right-6 z-50 animate-in slide-in-from-right">
          <div className="bg-slate-900 text-white p-5 rounded-3xl shadow-2xl border border-slate-700 flex flex-col gap-2 min-w-[280px]">
            <div className="flex items-center gap-3">
              <div className="bg-emerald-500 p-2 rounded-xl"><Mail className="w-4 h-4" /></div>
              <p className="text-sm font-bold">{emailNotification.message}</p>
            </div>
            <div className="text-[10px] bg-slate-800 p-2 rounded-xl text-slate-400">
              通知已送至管理員與 {emailNotification.deputyName || '相關人員'}
            </div>
          </div>
        </div>
      )}

      {/* 側邊導航 */}
      <aside className="w-full md:w-64 bg-slate-900 text-white p-6 flex flex-col border-r border-white/5">
        <div className="flex items-center gap-3 mb-10">
          <div className="bg-emerald-600 p-2 rounded-xl shadow-lg"><Calendar className="w-6 h-6" /></div>
          <h1 className="text-xl font-black tracking-tight uppercase">欣川豐杰</h1>
        </div>
        <nav className="flex-1 space-y-2">
          <button onClick={() => setView('dashboard')} className={`w-full flex items-center gap-3 px-4 py-3 rounded-2xl transition-all ${view === 'dashboard' ? 'bg-emerald-600 text-white shadow-lg shadow-emerald-900/50' : 'text-slate-400 hover:bg-white/5'}`}><Clock className="w-5 h-5" /><span>特休年度概況</span></button>
          <button onClick={() => {setView('apply'); setEditingRequestId(null);}} className={`w-full flex items-center gap-3 px-4 py-3 rounded-2xl transition-all ${view === 'apply' ? 'bg-emerald-600 text-white shadow-lg shadow-emerald-900/50' : 'text-slate-400 hover:bg-white/5'}`}><Plus className="w-5 h-5" /><span>請假申請</span></button>
          {currentUserData?.role === 'admin' && (
            <div className="pt-6 mt-6 border-t border-white/10 space-y-2">
              <button onClick={() => setView('employees')} className={`w-full flex items-center gap-3 px-4 py-3 rounded-2xl transition-all ${view === 'employees' ? 'bg-emerald-600 text-white shadow-lg' : 'text-slate-400 hover:bg-white/5'}`}><Users className="w-5 h-5" /><span>全公司統計</span></button>
              <button onClick={() => setView('manage')} className={`w-full flex items-center gap-3 px-4 py-3 rounded-2xl transition-all ${view === 'manage' ? 'bg-emerald-600 text-white shadow-lg' : 'text-slate-400 hover:bg-white/5'}`}><ShieldCheck className="w-5 h-5" /><span>待辦審核 ({requests.filter(r=>r.status==='pending').length})</span></button>
            </div>
          )}
        </nav>
        <div className="mt-auto pt-6 border-t border-white/10">
          <button onClick={() => setIsLoggedIn(false)} className="w-full flex items-center gap-3 px-4 py-3 text-red-400 hover:bg-red-500/10 rounded-2xl transition-all text-sm font-bold"><LogOut className="w-4 h-4" />安全登出</button>
        </div>
      </aside>

      <main className="flex-1 p-4 md:p-10 overflow-y-auto max-h-screen">
        <header className="mb-10 flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 text-[10px] font-black text-emerald-600 uppercase tracking-widest mb-2">
              <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div>
              雲端服務運行中 · {selectedYear === 2026 ? '民國 115 年' : '民國 116 年'}
            </div>
            <h2 className="text-3xl font-black text-slate-800 tracking-tight">{currentUserData?.name}，您好</h2>
          </div>
          <select className="bg-white border border-slate-200 text-sm font-black p-3 rounded-2xl outline-none shadow-sm" value={selectedYear} onChange={(e) => setSelectedYear(Number(e.target.value))}>
            <option value={2026}>民國 115 年度</option>
            <option value={2027}>民國 116 年度</option>
          </select>
        </header>

        {view === 'dashboard' && (
          <div className="space-y-8">
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="bg-white p-8 rounded-[2rem] shadow-sm border border-slate-100">
                <p className="text-slate-400 text-[10px] font-black uppercase tracking-widest mb-2">當年度新假</p>
                <p className="text-4xl font-black text-slate-800">{myYearlyStats.currentEntitlement} <span className="text-xs opacity-30">天</span></p>
              </div>
              <div className="bg-blue-50/50 p-8 rounded-[2rem] border-2 border-blue-100">
                <p className="text-blue-400 text-[10px] font-black uppercase tracking-widest mb-2 flex items-center gap-1"><History className="w-3 h-3" /> 前一年度結轉</p>
                <p className="text-4xl font-black text-blue-600">{myYearlyStats.carryOver} <span className="text-xs opacity-40">天</span></p>
              </div>
              <div className="bg-white p-8 rounded-[2rem] shadow-sm border border-slate-100">
                <p className="text-slate-400 text-[10px] font-black uppercase tracking-widest mb-2">已使用累計</p>
                <p className="text-4xl font-black text-orange-500">{myYearlyStats.used} <span className="text-xs opacity-30">天</span></p>
              </div>
              <div className="bg-emerald-600 p-8 rounded-[2rem] shadow-2xl shadow-emerald-200 text-white">
                <p className="text-emerald-100 text-[10px] font-black uppercase tracking-widest mb-2">剩餘可用額度</p>
                <p className="text-5xl font-black text-white">{myYearlyStats.remaining} <span className="text-xs opacity-50">天</span></p>
              </div>
            </div>

            <div className="bg-white rounded-[2rem] shadow-sm border border-slate-100 overflow-hidden">
              <div className="p-8 border-b border-slate-50 font-black flex justify-between items-center">
                <span className="text-xl">個人請假紀錄明細</span>
                <span className="text-[10px] font-black text-orange-500 bg-orange-50 px-4 py-2 rounded-2xl border border-orange-100">七天內可異動</span>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                  <thead className="bg-slate-50/50 text-slate-400 font-black text-[10px] uppercase tracking-[0.2em]">
                    <tr><th className="px-8 py-6">假別</th><th className="px-8 py-6">日期</th><th className="px-8 py-6">天數</th><th className="px-8 py-6">狀態</th><th className="px-8 py-6 text-center">操作</th></tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {requests.filter(r => r.employeeId === currentUserData?.id).sort((a,b)=>b.date.localeCompare(a.date)).map(req => {
                      const expired = isActionExpired(req.date, req.isLegacy);
                      return (
                        <tr key={req.id} className="hover:bg-slate-50/50 transition-colors">
                          <td className="px-8 py-6 font-black"><span className={`px-2 py-1 rounded-lg text-[10px] ${req.isLegacy ? 'bg-amber-100 text-amber-700' : 'bg-emerald-100 text-emerald-700'}`}>{req.type}{req.isLegacy ? ' (匯入)' : ''}</span></td>
                          <td className="px-8 py-6 font-black text-slate-700">{req.date}</td>
                          <td className="px-8 py-6 font-bold">{req.days}天 ({req.shift})</td>
                          <td className="px-8 py-6">
                            <span className={`px-3 py-1 rounded-full text-[10px] font-black ${req.status === 'approved' ? 'text-emerald-600' : 'text-orange-500'}`}>
                              {req.status === 'approved' ? '● 已核准' : '○ 審核中'}
                            </span>
                          </td>
                          <td className="px-8 py-6 text-center">
                            {!expired ? (
                              <div className="flex justify-center gap-2">
                                <button onClick={() => { setEditingRequestId(req.id); setFormData({ ...req }); setView('apply'); }} className="p-2 text-blue-500 hover:bg-blue-50 rounded-lg"><Edit className="w-4 h-4" /></button>
                                <button onClick={() => handleDeleteRequest(req.id)} className="p-2 text-red-400 hover:bg-red-50 rounded-lg"><Trash2 className="w-4 h-4" /></button>
                              </div>
                            ) : (<span className="text-[10px] text-slate-300 font-bold uppercase italic">Locked</span>)}
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {view === 'apply' && (
          <div className="max-w-2xl mx-auto bg-white p-12 rounded-[3rem] shadow-sm border border-slate-100">
            <form onSubmit={handleSubmitLeave} className="space-y-10">
              <div className="space-y-4">
                <label className="text-xs font-black text-slate-400 uppercase tracking-[0.2em] block">選擇假別</label>
                <div className="flex gap-2">
                  {['特休', '病假', '事假', '公假'].map(t => (
                    <button key={t} type="button" onClick={() => setFormData({...formData, type: t})} className={`flex-1 py-5 rounded-[1.5rem] border-2 font-black text-sm transition-all ${formData.type === t ? 'bg-slate-900 border-slate-900 text-white shadow-2xl scale-[1.02]' : 'bg-white border-slate-100 text-slate-300'}`}>{t}</button>
                  ))}
                </div>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-8">
                <div className="space-y-4">
                  <label className="text-xs font-black text-slate-400 uppercase tracking-[0.2em]">請假日期</label>
                  <input type="date" className="w-full p-6 bg-slate-50 border-2 border-slate-50 rounded-[1.5rem] outline-none font-bold text-slate-800 focus:bg-white focus:border-emerald-500 shadow-inner" value={formData.date} onChange={(e)=>setFormData({...formData, date: e.target.value})} required/>
                </div>
                <div className="space-y-4">
                  <label className="text-xs font-black text-slate-400 uppercase tracking-[0.2em]">職務代理人</label>
                  <select className="w-full p-6 bg-slate-50 border-2 border-slate-50 rounded-[1.5rem] outline-none font-bold text-slate-800 focus:bg-white" value={formData.deputyId} onChange={(e) => setFormData({...formData, deputyId: e.target.value})}>
                    <option value="">(不指定代理人)</option>
                    {availableDeputies.map(emp => (<option key={emp.id} value={emp.id}>{emp.name}</option>))}
                  </select>
                </div>
              </div>
              <div className="space-y-4">
                <label className="text-xs font-black text-slate-400 uppercase tracking-[0.2em]">選擇時段</label>
                <div className="grid grid-cols-3 gap-4">
                  {['全天','上午','下午'].map(s => (
                    <button key={s} type="button" onClick={() => setFormData({...formData, shift: s, duration: s==='全天'?'1.0':'0.5'})} className={`py-5 rounded-[1.5rem] border-2 font-black text-xs transition-all ${formData.shift===s ? 'bg-emerald-600 border-emerald-600 text-white shadow-xl shadow-emerald-100' : 'bg-white border-slate-50 text-slate-400'}`}>{s}</button>
                  ))}
                </div>
              </div>
              <button type="submit" className="w-full bg-emerald-600 text-white font-black py-6 rounded-[1.5rem] shadow-2xl shadow-emerald-200 hover:bg-emerald-700 active:scale-95 transition-all text-xl">{editingRequestId ? '儲存並重送審核' : '提交申請並雲端同步'}</button>
            </form>
          </div>
        )}

        {view === 'employees' && (
          <div className="space-y-12 pb-20">
            <div className="bg-white rounded-[2.5rem] shadow-sm border border-slate-100 overflow-hidden">
              <div className="p-10 border-b border-slate-50 flex items-center gap-4 font-black text-2xl text-slate-800">
                <div className="p-3 bg-emerald-50 rounded-2xl text-emerald-600"><Users className="w-6 h-6" /></div>
                欣川豐杰特休額度統計
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                  <thead className="bg-slate-50/50 text-[10px] text-slate-400 font-black uppercase tracking-[0.2em]">
                    <tr><th className="px-10 py-8">工號 / 姓名</th><th className="px-8 py-8 text-center">年度新假</th><th className="px-8 py-8 text-center text-blue-500">結轉天數</th><th className="px-8 py-8 text-center text-orange-400">累計已休</th><th className="px-8 py-8 text-center text-emerald-600">剩餘可休</th></tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {employees.sort((a,b)=>a.id.localeCompare(b.id)).map(emp => {
                      const userUsed = requests.filter(r => r.employeeId === emp.id && r.status === 'approved' && r.type === '特休' && new Date(r.date).getFullYear() === selectedYear).reduce((s, r) => s + r.days, 0);
                      const totalPossible = (emp.totalAnnual || 0) + (emp.carryOver || 0);
                      return (
                        <tr key={emp.id} className="hover:bg-slate-50/30 transition-all">
                          <td className="px-10 py-8"><div className="text-[11px] font-black text-blue-600">{emp.id}</div><div className="font-black text-slate-700">{emp.name}</div></td>
                          <td className="px-8 py-8 text-center font-bold text-slate-400">{emp.totalAnnual}</td>
                          <td className="px-8 py-8 text-center font-black text-blue-500 bg-blue-50/20">{emp.carryOver}</td>
                          <td className="px-8 py-8 text-center font-bold text-orange-400">{userUsed}</td>
                          <td className="px-8 py-8 text-center font-black text-emerald-600 bg-emerald-50/20">{totalPossible - userUsed}</td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>
            
            <div className="bg-white rounded-[2.5rem] shadow-sm border border-slate-100 overflow-hidden">
               <div className="p-8 border-b border-slate-50 flex items-center justify-between">
                 <div className="flex items-center gap-3 font-black text-xl text-blue-800"><ClipboardList className="w-6 h-6" /> 核准紀錄查詢</div>
                 <select className="bg-slate-50 p-2 rounded-xl text-sm font-black outline-none border border-slate-100" value={adminFilterId} onChange={(e)=>setAdminFilterId(e.target.value)}>
                    <option value="">(顯示全部人員明細)</option>
                    {employees.map(e => <option key={e.id} value={e.id}>{e.name}</option>)}
                 </select>
               </div>
               <div className="overflow-x-auto">
                 <table className="w-full text-left text-sm">
                   <thead className="bg-slate-50/50 text-[10px] text-slate-400 font-black uppercase">
                     <tr><th className="px-8 py-6">工號 / 姓名</th><th className="px-8 py-6">日期</th><th className="px-8 py-6 text-center">天數</th><th className="px-8 py-6">備註</th></tr>
                   </thead>
                   <tbody className="divide-y divide-slate-100">
                     {filteredApprovedRequests.map(req => {
                       const emp = employees.find(e=>e.id===req.employeeId);
                       return (
                         <tr key={req.id}>
                           <td className="px-8 py-6 font-black text-slate-700">[{emp?.id}] {emp?.name}</td>
                           <td className="px-8 py-6 font-bold">{req.date}</td>
                           <td className="px-8 py-6 text-center text-blue-600 font-black">{req.days}</td>
                           <td className="px-8 py-6 text-xs text-slate-400 italic">{req.isLegacy ? '前期數據' : req.reason}</td>
                         </tr>
                       );
                     })}
                   </tbody>
                 </table>
               </div>
            </div>
          </div>
        )}

        {view === 'manage' && (
          <div className="space-y-6">
            {requests.filter(r=>r.status==='pending').length === 0 ? <div className="p-20 bg-white text-center rounded-[3rem] text-slate-300 font-bold border-4 border-dashed border-slate-50">暫無待處理單據</div> : 
            requests.filter(r=>r.status==='pending').map(req => {
              const emp = employees.find(e => e.id === req.employeeId);
              return (
                <div key={req.id} className="bg-white p-10 rounded-[2.5rem] border border-slate-100 flex flex-col lg:flex-row lg:items-center justify-between shadow-sm border-l-[10px] border-l-emerald-500">
                  <div className="space-y-4">
                    <div className="flex items-center gap-4"><p className="font-black text-2xl text-slate-800">{emp?.name}</p><span className="text-[10px] font-black text-white bg-slate-800 px-3 py-1.5 rounded-xl uppercase">{emp?.department}</span></div>
                    <p className="text-lg text-slate-500 font-bold">申請 {req.type} {req.days} 天：<span className="text-slate-800 font-black">{req.date} ({req.shift})</span></p>
                  </div>
                  <div className="flex gap-4 mt-8 lg:mt-0">
                    <button onClick={() => handleReview(req.id, 'approved')} className="px-10 py-5 bg-emerald-600 text-white rounded-[1.5rem] text-sm font-black shadow-xl hover:bg-emerald-700 transition-all uppercase">核准</button>
                    <button onClick={() => handleReview(req.id, 'rejected')} className="px-10 py-5 border-2 border-red-50 text-red-400 rounded-[1.5rem] text-sm font-black hover:bg-red-50 transition-all uppercase">駁回</button>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </main>
    </div>
  );
}

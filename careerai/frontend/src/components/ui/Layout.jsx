import { Outlet, NavLink, useNavigate } from 'react-router-dom'
import { useAuthStore } from '../../services/store'
import { LayoutDashboard, Upload, Briefcase, Map, BarChart3, GraduationCap, Bot, User, Settings, LogOut, Sparkles } from 'lucide-react'

const NAV_ITEMS = [
  { to: '/', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/resume', icon: Upload, label: 'Upload Resume' },
  { to: '/careers', icon: Briefcase, label: 'Careers' },
  { to: '/roadmap', icon: Map, label: 'Roadmap' },
  { to: '/analytics', icon: BarChart3, label: 'Analytics' },
  { to: '/courses', icon: GraduationCap, label: 'Courses' },
  { to: '/chatbot', icon: Bot, label: 'AI Chatbot' },
  { to: '/profile', icon: User, label: 'Profile' },
]

export default function Layout() {
  const { user, logout } = useAuthStore()
  const navigate = useNavigate()

  const handleLogout = () => { logout(); navigate('/login') }
  const initials = user?.name?.split(' ').map(n => n[0]).join('').slice(0,2).toUpperCase() || 'RS'

  return (
    <div style={{ display:'flex', minHeight:'100vh' }}>
      {/* Sidebar */}
      <aside style={{ width:220, background:'#111118', borderRight:'1px solid rgba(255,255,255,0.08)', display:'flex', flexDirection:'column', padding:'24px 16px', position:'fixed', top:0, left:0, bottom:0, zIndex:100 }}>
        {/* Logo */}
        <div style={{ display:'flex', alignItems:'center', gap:10, marginBottom:32 }}>
          <div style={{ width:36, height:36, background:'linear-gradient(135deg,#6c63ff,#ff6b9d)', borderRadius:10, display:'flex', alignItems:'center', justifyContent:'center', fontSize:18, fontWeight:800, fontFamily:'Syne,sans-serif', color:'white' }}>C</div>
          <span style={{ fontFamily:'Syne,sans-serif', fontWeight:700, fontSize:18 }}>Career<span style={{color:'#6c63ff'}}>AI</span></span>
        </div>

        <nav style={{ flex:1 }}>
          {NAV_ITEMS.map(({ to, icon: Icon, label }) => (
            <NavLink key={to} to={to} end={to==='/'} style={({ isActive }) => ({
              display:'flex', alignItems:'center', gap:10, padding:'10px 12px', borderRadius:10,
              marginBottom:2, fontSize:14, textDecoration:'none',
              background: isActive ? 'rgba(108,99,255,0.15)' : 'transparent',
              color: isActive ? '#6c63ff' : '#9090b0',
              transition:'all 0.2s',
            })}>
              <Icon size={16} />
              {label}
            </NavLink>
          ))}
        </nav>

        {/* User */}
        <div style={{ padding:12, background:'rgba(255,255,255,0.04)', border:'1px solid rgba(255,255,255,0.08)', borderRadius:12 }}>
          <div style={{ display:'flex', alignItems:'center', gap:8, marginBottom:10 }}>
            <div style={{ width:32, height:32, borderRadius:8, background:'linear-gradient(135deg,#6c63ff,#ff6b9d)', display:'flex', alignItems:'center', justifyContent:'center', fontFamily:'Syne,sans-serif', fontWeight:700, fontSize:12 }}>{initials}</div>
            <div>
              <div style={{ fontSize:13, fontWeight:500 }}>{user?.name || 'Ram Swagath'}</div>
              <div style={{ fontSize:11, color:'#6c63ff' }}>✦ {user?.plan || 'Pro'} Plan</div>
            </div>
          </div>
          <button onClick={handleLogout} style={{ width:'100%', display:'flex', alignItems:'center', gap:6, padding:'7px 8px', background:'transparent', border:'1px solid rgba(255,255,255,0.08)', borderRadius:8, color:'#9090b0', fontSize:12, cursor:'pointer' }}>
            <LogOut size={12} /> Sign Out
          </button>
        </div>
      </aside>

      {/* Main */}
      <main style={{ marginLeft:220, flex:1, padding:'28px 32px', minHeight:'100vh' }}>
        <Outlet />
      </main>
    </div>
  )
}

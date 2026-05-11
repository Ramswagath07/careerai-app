import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { authAPI } from '../services/api'
import { useAuthStore } from '../services/store'

export default function RegisterPage() {
  const [form, setForm] = useState({ name:'', email:'', password:'' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { setAuth } = useAuthStore()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (form.password.length < 6) { setError('Password must be at least 6 characters'); return }
    setLoading(true); setError('')
    try {
      const { data } = await authAPI.register(form)
      setAuth(data.user, data.access_token)
      navigate('/')
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ minHeight:'100vh', display:'flex', alignItems:'center', justifyContent:'center', background:'#0a0a0f' }}>
      <div style={{ width:'100%', maxWidth:400, padding:'40px', background:'rgba(255,255,255,0.04)', border:'1px solid rgba(255,255,255,0.08)', borderRadius:20 }}>
        <div style={{ textAlign:'center', marginBottom:32 }}>
          <div style={{ width:56, height:56, background:'linear-gradient(135deg,#6c63ff,#ff6b9d)', borderRadius:14, display:'flex', alignItems:'center', justifyContent:'center', fontFamily:'Syne,sans-serif', fontWeight:800, fontSize:24, margin:'0 auto 16px' }}>C</div>
          <h1 style={{ fontFamily:'Syne,sans-serif', fontSize:24, fontWeight:700 }}>Create Account</h1>
          <p style={{ color:'#9090b0', fontSize:14, marginTop:6 }}>Start your AI-powered career journey</p>
        </div>

        {error && <div style={{ background:'rgba(255,107,107,0.1)', border:'1px solid rgba(255,107,107,0.3)', borderRadius:10, padding:'10px 14px', color:'#ff6b6b', fontSize:13, marginBottom:20 }}>{error}</div>}

        <form onSubmit={handleSubmit} style={{ display:'flex', flexDirection:'column', gap:16 }}>
          {[['name','Full Name','Ram Swagath','text'],['email','Email','ram@example.com','email'],['password','Password','Min. 6 characters','password']].map(([field, label, placeholder, type]) => (
            <div key={field}>
              <label style={{ fontSize:13, color:'#9090b0', marginBottom:6, display:'block' }}>{label}</label>
              <input type={type} value={form[field]} onChange={e=>setForm({...form,[field]:e.target.value})} required placeholder={placeholder}
                style={{ width:'100%', padding:'11px 14px', background:'rgba(255,255,255,0.04)', border:'1px solid rgba(255,255,255,0.12)', borderRadius:10, color:'#f0f0f8', fontSize:14, outline:'none' }} />
            </div>
          ))}
          <button type="submit" disabled={loading}
            style={{ padding:'12px', background:'linear-gradient(135deg,#6c63ff,#9f8fff)', border:'none', borderRadius:10, color:'white', fontSize:15, fontWeight:500, cursor:'pointer', opacity:loading?0.7:1, fontFamily:'DM Sans,sans-serif' }}>
            {loading ? 'Creating account...' : 'Create Account'}
          </button>
        </form>
        <p style={{ textAlign:'center', marginTop:20, fontSize:13, color:'#9090b0' }}>
          Already have an account? <Link to="/login" style={{ color:'#6c63ff', textDecoration:'none' }}>Sign in</Link>
        </p>
      </div>
    </div>
  )
}

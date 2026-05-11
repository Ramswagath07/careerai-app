import { useAuthStore } from '../services/store'
import { useResumeStore } from '../services/store'

export default function ProfilePage() {
  const { user } = useAuthStore()
  const { latestAnalysis: a } = useResumeStore()
  const initials = user?.name?.split(' ').map(n=>n[0]).join('').slice(0,2).toUpperCase() || 'RS'
  return (
    <div>
      <div style={{ marginBottom:28 }}>
        <h1 style={{ fontFamily:'Syne,sans-serif', fontSize:22, fontWeight:700 }}>Profile</h1>
        <p style={{ fontSize:13, color:'#9090b0', marginTop:4 }}>Your CareerAI account overview</p>
      </div>
      <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:20 }}>
        <div style={{ background:'rgba(255,255,255,0.04)', border:'1px solid rgba(255,255,255,0.08)', borderRadius:16, padding:24 }}>
          <div style={{ display:'flex', alignItems:'center', gap:16, marginBottom:24 }}>
            <div style={{ width:64, height:64, borderRadius:16, background:'linear-gradient(135deg,#6c63ff,#ff6b9d)', display:'flex', alignItems:'center', justifyContent:'center', fontFamily:'Syne,sans-serif', fontWeight:800, fontSize:24 }}>{initials}</div>
            <div>
              <div style={{ fontFamily:'Syne,sans-serif', fontSize:20, fontWeight:700 }}>{user?.name || 'Ram Swagath'}</div>
              <div style={{ fontSize:13, color:'#6c63ff' }}>✦ {user?.plan || 'Pro'} Member</div>
              <div style={{ fontSize:12, color:'#9090b0', marginTop:2 }}>{user?.email || 'ram.swagath@email.com'}</div>
            </div>
          </div>
          {[
            ['Experience Level', user?.experience_level || 'Mid-Level'],
            ['Location', user?.location || 'Chennai, India'],
            ['Target Role', user?.target_role || 'Software Engineer'],
            ['Resumes Analyzed', user?.resume_count || (a ? 1 : 0)],
            ['Member Since', new Date(user?.created_at || Date.now()).toLocaleDateString('en-US', {month:'short', year:'numeric'})],
          ].map(([label, val]) => (
            <div key={label} style={{ display:'flex', justifyContent:'space-between', alignItems:'center', padding:'10px 12px', background:'rgba(255,255,255,0.02)', border:'1px solid rgba(255,255,255,0.06)', borderRadius:8, marginBottom:8 }}>
              <span style={{ fontSize:13, color:'#9090b0' }}>{label}</span>
              <span style={{ fontSize:13, fontWeight:500, color: label==='Target Role'?'#6c63ff':'#f0f0f8' }}>{val}</span>
            </div>
          ))}
        </div>
        <div style={{ background:'rgba(255,255,255,0.04)', border:'1px solid rgba(255,255,255,0.08)', borderRadius:16, padding:24 }}>
          <h3 style={{ fontFamily:'Syne,sans-serif', fontSize:16, fontWeight:600, marginBottom:16 }}>Achievement Badges</h3>
          <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:10 }}>
            {[
              {emoji:'🚀', label:'Early Adopter', color:'rgba(108,99,255', unlocked:true},
              {emoji:'🎯', label:'Goal Setter', color:'rgba(0,212,170', unlocked:true},
              {emoji:'📊', label:'Data Driven', color:'rgba(255,107,157', unlocked:!!a},
              {emoji:'🏆', label:'Top Scorer', color:'rgba(255,179,71', unlocked:a?.ats_score>=80},
            ].map(b => (
              <div key={b.label} style={{ padding:14, background:`${b.color},0.08)`, border:`1px solid ${b.color},0.2)`, borderRadius:10, textAlign:'center', opacity:b.unlocked?1:0.35 }}>
                <div style={{ fontSize:28, marginBottom:6 }}>{b.emoji}</div>
                <div style={{ fontSize:12, fontWeight:500 }}>{b.label}</div>
                {!b.unlocked && <div style={{ fontSize:10, color:'#5a5a7a', marginTop:4 }}>Locked</div>}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

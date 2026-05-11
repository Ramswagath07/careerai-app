import { useAuthStore } from '../services/store'
import { useResumeStore } from '../services/store'
import { Link } from 'react-router-dom'

export default function DashboardPage() {
  const { user } = useAuthStore()
  const { latestAnalysis: a } = useResumeStore()
  const name = user?.name?.split(' ')[0] || 'Ram'

  const stats = [
    { label:'ATS Score', val: a ? `${a.ats_score}%` : '—', color:'#00d4aa', sub:'Upload to analyze' },
    { label:'Skills Detected', val: a ? a.detected_skills?.length : '—', color:'#6c63ff', sub:'From your resume' },
    { label:'Career Matches', val: a ? a.career_matches?.length || 6 : 6, color:'#ff6b9d', sub:'Best fits found' },
    { label:'Skill Gaps', val: a ? a.missing_skills?.length : '—', color:'#ffb347', sub:'To fill' },
  ]

  return (
    <div>
      <div style={{ marginBottom:28, display:'flex', alignItems:'flex-start', justifyContent:'space-between' }}>
        <div>
          <h1 style={{ fontFamily:'Syne,sans-serif', fontSize:22, fontWeight:700 }}>Good morning, {name} 👋</h1>
          <p style={{ fontSize:13, color:'#9090b0', marginTop:4 }}>Your career intelligence dashboard</p>
        </div>
        <Link to="/resume" style={{ padding:'11px 22px', background:'linear-gradient(135deg,#6c63ff,#9f8fff)', border:'none', borderRadius:10, color:'white', fontSize:14, fontWeight:500, textDecoration:'none', display:'flex', alignItems:'center', gap:6 }}>
          ⬆ Upload Resume
        </Link>
      </div>

      <div style={{ display:'grid', gridTemplateColumns:'repeat(4,1fr)', gap:16, marginBottom:24 }}>
        {stats.map(s => (
          <div key={s.label} style={{ background:'rgba(255,255,255,0.04)', border:'1px solid rgba(255,255,255,0.08)', borderRadius:14, padding:'18px 20px' }}>
            <div style={{ fontSize:12, color:'#9090b0', marginBottom:8 }}>{s.label}</div>
            <div style={{ fontFamily:'Syne,sans-serif', fontSize:26, fontWeight:700, color:s.color }}>{s.val}</div>
            <div style={{ fontSize:12, color:'#5a5a7a', marginTop:4 }}>{s.sub}</div>
          </div>
        ))}
      </div>

      {!a && (
        <div style={{ background:'rgba(108,99,255,0.06)', border:'2px dashed rgba(108,99,255,0.35)', borderRadius:16, padding:48, textAlign:'center' }}>
          <div style={{ fontSize:48, marginBottom:16 }}>📄</div>
          <h2 style={{ fontFamily:'Syne,sans-serif', fontSize:20, fontWeight:700, marginBottom:8 }}>Upload your first resume</h2>
          <p style={{ color:'#9090b0', fontSize:14, marginBottom:20 }}>Get your ATS score, skill analysis, and AI career recommendations in seconds</p>
          <Link to="/resume" style={{ padding:'12px 28px', background:'linear-gradient(135deg,#6c63ff,#9f8fff)', borderRadius:10, color:'white', textDecoration:'none', fontWeight:500, fontSize:14 }}>
            Get Started →
          </Link>
        </div>
      )}

      {a && (
        <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:20 }}>
          <div style={{ background:'rgba(255,255,255,0.04)', border:'1px solid rgba(255,255,255,0.08)', borderRadius:16, padding:20 }}>
            <h3 style={{ fontFamily:'Syne,sans-serif', fontSize:16, fontWeight:600, marginBottom:12 }}>Latest Analysis</h3>
            {[['Keyword Density','keyword_score','#6c63ff'],['Experience','experience_score','#ff6b9d'],['Education','education_score','#ffb347'],['Format','format_score','#00d4aa']].map(([l,k,c]) => (
              <div key={k} style={{ marginBottom:10 }}>
                <div style={{ display:'flex', justifyContent:'space-between', fontSize:13, marginBottom:4 }}>
                  <span style={{ color:'#9090b0' }}>{l}</span>
                  <span style={{ color:c, fontWeight:500 }}>{a[k]}/100</span>
                </div>
                <div style={{ height:5, background:'rgba(255,255,255,0.06)', borderRadius:3, overflow:'hidden' }}>
                  <div style={{ height:'100%', width:`${a[k]}%`, background:c, borderRadius:3 }}/>
                </div>
              </div>
            ))}
          </div>
          <div style={{ background:'rgba(255,255,255,0.04)', border:'1px solid rgba(255,255,255,0.08)', borderRadius:16, padding:20 }}>
            <h3 style={{ fontFamily:'Syne,sans-serif', fontSize:16, fontWeight:600, marginBottom:12 }}>AI Recommendations</h3>
            {a.recommendations?.slice(0,4).map((r,i) => (
              <div key={i} style={{ padding:'8px 12px', marginBottom:8, background:'rgba(108,99,255,0.06)', border:'1px solid rgba(108,99,255,0.15)', borderRadius:8, fontSize:13, color:'#d0d0e8' }}>
                {i+1}. {r}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

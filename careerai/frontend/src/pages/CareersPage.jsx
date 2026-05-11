import { useResumeStore } from '../services/store'

const CAREERS = [
  { title:'Software Engineer', icon:'💻', base:88, color:'#6c63ff', skills:['Python','JavaScript','React'], salary:'$85K–$140K', demand:'Very High', growth:'+25%' },
  { title:'AI/ML Engineer', icon:'🤖', base:76, color:'#00d4aa', skills:['TensorFlow','PyTorch','Python'], salary:'$110K–$165K', demand:'Very High', growth:'+35%' },
  { title:'Data Analyst', icon:'📊', base:82, color:'#ff6b9d', skills:['Python','SQL','Tableau'], salary:'$65K–$100K', demand:'High', growth:'+20%' },
  { title:'Cloud Engineer', icon:'☁️', base:71, color:'#ffb347', skills:['AWS','Docker','Kubernetes'], salary:'$95K–$145K', demand:'High', growth:'+28%' },
  { title:'Full Stack Developer', icon:'🛠️', base:80, color:'#54a0ff', skills:['React','Node.js','MongoDB'], salary:'$80K–$130K', demand:'Very High', growth:'+24%' },
  { title:'Cybersecurity Analyst', icon:'🛡️', base:59, color:'#ee5a24', skills:['Linux','Python','Networking'], salary:'$80K–$130K', demand:'High', growth:'+32%' },
]

export default function CareersPage() {
  const { latestAnalysis: a } = useResumeStore()
  const detected = a?.detected_skills?.map(s=>s.toLowerCase()) || []

  const careers = CAREERS.map(c => {
    const overlap = c.skills.filter(s => detected.some(d => d.includes(s.toLowerCase()) || s.toLowerCase().includes(d)))
    const score = Math.min(98, c.base + overlap.length * 4)
    return { ...c, score }
  }).sort((a,b) => b.score - a.score)

  return (
    <div>
      <div style={{ marginBottom:28 }}>
        <h1 style={{ fontFamily:'Syne,sans-serif', fontSize:22, fontWeight:700 }}>Career Recommendations</h1>
        <p style={{ fontSize:13, color:'#9090b0', marginTop:4 }}>AI-matched roles based on your skills and resume</p>
      </div>
      <div style={{ display:'grid', gridTemplateColumns:'repeat(3,1fr)', gap:16 }}>
        {careers.map((c,i) => (
          <div key={c.title} style={{ background:'rgba(255,255,255,0.04)', border:`1px solid rgba(255,255,255,0.08)`, borderRadius:16, padding:20, position:'relative', overflow:'hidden', transition:'transform 0.2s', cursor:'pointer' }}
            onMouseEnter={e=>e.currentTarget.style.transform='translateY(-2px)'}
            onMouseLeave={e=>e.currentTarget.style.transform='translateY(0)'}>
            <div style={{ position:'absolute', top:0, left:0, right:0, height:3, background:c.color, borderRadius:'16px 16px 0 0' }}/>
            {i === 0 && <div style={{ position:'absolute', top:14, right:14, fontSize:10, padding:'3px 8px', background:'rgba(0,212,170,0.15)', border:'1px solid rgba(0,212,170,0.3)', borderRadius:20, color:'#00d4aa' }}>Top Match</div>}
            <div style={{ fontSize:32, marginBottom:10 }}>{c.icon}</div>
            <h3 style={{ fontFamily:'Syne,sans-serif', fontSize:15, fontWeight:600, marginBottom:4 }}>{c.title}</h3>
            <div style={{ fontSize:12, color:'#9090b0', marginBottom:10 }}>{c.score}% match · {c.demand} demand</div>
            <div style={{ height:4, background:'rgba(255,255,255,0.06)', borderRadius:2, marginBottom:10, overflow:'hidden' }}>
              <div style={{ height:'100%', width:`${c.score}%`, background:c.color, borderRadius:2 }}/>
            </div>
            <div style={{ fontSize:12, color:'#9090b0', marginBottom:10 }}>{c.salary} · {c.growth} YoY</div>
            <div style={{ display:'flex', flexWrap:'wrap', gap:5 }}>
              {c.skills.map(s => <span key={s} style={{ fontSize:10, padding:'2px 8px', borderRadius:20, background:'rgba(255,255,255,0.05)', border:'1px solid rgba(255,255,255,0.1)', color:'#9090b0' }}>{s}</span>)}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

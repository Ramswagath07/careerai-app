const STEPS = [
  { title:'Core Programming', desc:'Master Python/JS, data structures, OOP, algorithms (LeetCode Easy)', months:2, status:'done' },
  { title:'Web Frameworks', desc:'Build real projects using React (frontend) + FastAPI/Django (backend)', months:2, status:'active' },
  { title:'Databases & APIs', desc:'SQL, MongoDB, REST APIs, authentication patterns', months:1, status:'todo' },
  { title:'Cloud & DevOps', desc:'AWS deployment, Docker, CI/CD pipelines, GitHub Actions', months:2, status:'todo' },
  { title:'System Design', desc:'Scalable systems, microservices, caching, load balancers', months:2, status:'todo' },
]

export default function RoadmapPage() {
  return (
    <div>
      <div style={{ marginBottom:28 }}>
        <h1 style={{ fontFamily:'Syne,sans-serif', fontSize:22, fontWeight:700 }}>Learning Roadmap</h1>
        <p style={{ fontSize:13, color:'#9090b0', marginTop:4 }}>Your personalized path to Software Engineer — estimated 9 months</p>
      </div>
      <div style={{ background:'rgba(255,255,255,0.04)', border:'1px solid rgba(255,255,255,0.08)', borderRadius:16, padding:28 }}>
        {STEPS.map((s, i) => (
          <div key={i} style={{ display:'flex', gap:16, paddingBottom:i<STEPS.length-1?24:0, position:'relative' }}>
            {i < STEPS.length-1 && <div style={{ position:'absolute', left:15, top:36, bottom:0, width:1, background:'rgba(255,255,255,0.08)' }}/>}
            <div style={{ width:32, height:32, borderRadius:'50%', flexShrink:0, display:'flex', alignItems:'center', justifyContent:'center', fontSize:13, fontWeight:600,
              background: s.status==='done'?'rgba(0,212,170,0.2)':s.status==='active'?'rgba(108,99,255,0.2)':'rgba(255,255,255,0.04)',
              border: s.status==='done'?'1.5px solid #00d4aa':s.status==='active'?'1.5px solid #6c63ff':'1px solid rgba(255,255,255,0.12)',
              color: s.status==='done'?'#00d4aa':s.status==='active'?'#6c63ff':'#5a5a7a' }}>
              {s.status==='done'?'✓':s.status==='active'?'→':i+1}
            </div>
            <div>
              <div style={{ display:'flex', alignItems:'center', gap:8, marginBottom:4 }}>
                <span style={{ fontFamily:'Syne,sans-serif', fontSize:15, fontWeight:600 }}>{s.title}</span>
                <span style={{ fontSize:11, padding:'2px 8px', borderRadius:20,
                  background: s.status==='done'?'rgba(0,212,170,0.1)':s.status==='active'?'rgba(108,99,255,0.1)':'rgba(255,255,255,0.04)',
                  color: s.status==='done'?'#00d4aa':s.status==='active'?'#6c63ff':'#5a5a7a',
                  border: s.status==='done'?'1px solid rgba(0,212,170,0.3)':s.status==='active'?'1px solid rgba(108,99,255,0.3)':'1px solid rgba(255,255,255,0.08)' }}>
                  {s.status==='done'?'Completed':s.status==='active'?'In Progress':'Upcoming'} · {s.months}mo
                </span>
              </div>
              <p style={{ fontSize:13, color:'#9090b0', lineHeight:1.5 }}>{s.desc}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

const COURSES = [
  { name:'Machine Learning Specialization', platform:'Coursera', icon:'🔵', rating:'4.9', duration:'60h', price:'Free Audit', skills:['ML','Python'] },
  { name:'Python for Data Science & ML', platform:'Udemy', icon:'🟡', rating:'4.8', duration:'22h', price:'$14.99', skills:['Python'] },
  { name:'AWS Certified Solutions Architect', platform:'Coursera', icon:'🔵', rating:'4.7', duration:'35h', price:'Free Audit', skills:['AWS'] },
  { name:'React — The Complete Guide', platform:'Udemy', icon:'🟡', rating:'4.9', duration:'48h', price:'$19.99', skills:['React'] },
  { name:'Deep Learning Specialization', platform:'Coursera', icon:'🔵', rating:'4.9', duration:'64h', price:'Free Audit', skills:['Deep Learning'] },
  { name:'Docker & Kubernetes Bootcamp', platform:'Udemy', icon:'🟡', rating:'4.7', duration:'24h', price:'$13.99', skills:['Docker'] },
  { name:'Introduction to Cybersecurity', platform:'edX', icon:'🟣', rating:'4.6', duration:'20h', price:'Free', skills:['Security'] },
  { name:'LangChain for LLM Applications', platform:'DeepLearning.AI', icon:'🟢', rating:'4.8', duration:'8h', price:'Free', skills:['LLM','Python'] },
]
export default function CoursesPage() {
  return (
    <div>
      <div style={{ marginBottom:28 }}>
        <h1 style={{ fontFamily:'Syne,sans-serif', fontSize:22, fontWeight:700 }}>Course Recommendations</h1>
        <p style={{ fontSize:13, color:'#9090b0', marginTop:4 }}>Top picks from Coursera, Udemy, edX, and DeepLearning.AI</p>
      </div>
      <div style={{ background:'rgba(255,255,255,0.04)', border:'1px solid rgba(255,255,255,0.08)', borderRadius:16, padding:20 }}>
        <div style={{ display:'flex', flexDirection:'column', gap:10 }}>
          {COURSES.map(c => (
            <div key={c.name} style={{ display:'flex', alignItems:'center', gap:12, padding:'12px 14px', background:'rgba(255,255,255,0.02)', border:'1px solid rgba(255,255,255,0.08)', borderRadius:10, transition:'all 0.2s', cursor:'pointer' }}
              onMouseEnter={e=>{ e.currentTarget.style.background='rgba(108,99,255,0.06)'; e.currentTarget.style.borderColor='rgba(108,99,255,0.25)' }}
              onMouseLeave={e=>{ e.currentTarget.style.background='rgba(255,255,255,0.02)'; e.currentTarget.style.borderColor='rgba(255,255,255,0.08)' }}>
              <div style={{ width:36, height:36, borderRadius:9, display:'flex', alignItems:'center', justifyContent:'center', fontSize:18, background:'rgba(255,255,255,0.04)', flexShrink:0 }}>{c.icon}</div>
              <div style={{ flex:1 }}>
                <div style={{ fontSize:14, fontWeight:500, marginBottom:2 }}>{c.name}</div>
                <div style={{ fontSize:12, color:'#9090b0' }}>{c.platform} · {c.duration} · {c.skills.join(', ')}</div>
              </div>
              <div style={{ textAlign:'right', flexShrink:0 }}>
                <div style={{ fontSize:13, color:'#ffb347' }}>★ {c.rating}</div>
                <div style={{ fontSize:12, color: c.price==='Free'||c.price==='Free Audit'?'#00d4aa':'#9090b0', marginTop:2 }}>{c.price}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

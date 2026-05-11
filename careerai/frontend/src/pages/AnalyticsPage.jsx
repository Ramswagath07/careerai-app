export default function AnalyticsPage() {
  const stats = [
    { label:'Avg Salary', val:'$92K', color:'#00d4aa', sub:'Software roles' },
    { label:'Job Openings', val:'48K', color:'#6c63ff', sub:'Active listings' },
    { label:'Growth Rate', val:'+23%', color:'#ff6b9d', sub:'YoY demand' },
    { label:'Remote Jobs', val:'67%', color:'#ffb347', sub:'Of all openings' },
  ]
  const roles = [
    { title:'Software Eng', salary:112, color:'rgba(108,99,255,0.7)' },
    { title:'ML Engineer', salary:135, color:'rgba(0,212,170,0.7)' },
    { title:'Cloud Eng', salary:118, color:'rgba(255,179,71,0.7)' },
    { title:'Data Analyst', salary:88, color:'rgba(255,107,157,0.7)' },
    { title:'UI/UX', salary:92, color:'rgba(84,160,255,0.7)' },
    { title:'Security', salary:105, color:'rgba(238,90,36,0.7)' },
  ]
  const top = roles.reduce((a,b) => a.salary>b.salary?a:b)
  return (
    <div>
      <div style={{ marginBottom:28 }}>
        <h1 style={{ fontFamily:'Syne,sans-serif', fontSize:22, fontWeight:700 }}>Analytics</h1>
        <p style={{ fontSize:13, color:'#9090b0', marginTop:4 }}>Job market trends and career insights for 2025</p>
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
      <div style={{ background:'rgba(255,255,255,0.04)', border:'1px solid rgba(255,255,255,0.08)', borderRadius:16, padding:24 }}>
        <h3 style={{ fontFamily:'Syne,sans-serif', fontSize:16, fontWeight:600, marginBottom:20 }}>💰 Avg Salary by Role (USD/year)</h3>
        <div style={{ display:'flex', flexDirection:'column', gap:12 }}>
          {roles.map(r => (
            <div key={r.title} style={{ display:'flex', alignItems:'center', gap:12 }}>
              <div style={{ width:110, fontSize:13, color:'#9090b0', flexShrink:0 }}>{r.title}</div>
              <div style={{ flex:1, height:28, background:'rgba(255,255,255,0.04)', borderRadius:6, overflow:'hidden' }}>
                <div style={{ height:'100%', width:`${(r.salary/top.salary)*100}%`, background:r.color, borderRadius:6, display:'flex', alignItems:'center', justifyContent:'flex-end', paddingRight:8, fontSize:12, color:'white', fontWeight:500 }}>
                  ${r.salary}K
                </div>
              </div>
            </div>
          ))}
        </div>
        <div style={{ marginTop:20, padding:'12px 16px', background:'rgba(108,99,255,0.06)', border:'1px solid rgba(108,99,255,0.2)', borderRadius:10, fontSize:13, color:'#9090b0' }}>
          📈 <strong style={{color:'#f0f0f8'}}>AI/ML Engineer</strong> is the fastest-growing role with +35% YoY demand and the highest average salary at $135K. Python remains the #1 required skill across all tech roles.
        </div>
      </div>
    </div>
  )
}

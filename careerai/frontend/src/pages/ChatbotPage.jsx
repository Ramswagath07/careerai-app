import { useState } from 'react'

const RESPONSES = {
  salary: "Software Engineers earn $85K–$140K in the US, AI/ML Engineers $110–$165K, Cloud Engineers $95–$145K. In India, expect 30–60% of US salaries, but the gap is narrowing fast — especially in Bangalore and Hyderabad.",
  interview: "For tech interviews: (1) Practice LeetCode medium problems daily, (2) Study System Design (Grokking the System Design Interview), (3) Prepare 5 behavioral stories using STAR method, (4) Know your resume inside out, (5) Research the company's tech stack beforehand.",
  resume: "To boost your ATS score: (1) Add a dedicated Skills section with exact keywords, (2) Use numbers — 'reduced API latency by 40%', (3) Include standard headers like Experience/Education/Skills, (4) Keep contact info plain text, (5) Add your GitHub/LinkedIn URLs.",
  skills: "Top skills for 2025: Python (universal), TypeScript (web dev), Kubernetes (infrastructure), LangChain/RAG (AI apps), dbt (data engineering), Terraform (cloud IaC), React 19 (frontend). Go deep on 2-3 rather than shallow on many.",
  default: "I'm your AI Career Assistant! I can help with career path advice, ATS improvement, skill gaps, interview prep, salary negotiation, and learning roadmaps. What would you like to explore?",
}

function getReply(msg) {
  const m = msg.toLowerCase()
  if (m.includes('salary')||m.includes('pay')||m.includes('earn')) return RESPONSES.salary
  if (m.includes('interview')||m.includes('leetcode')||m.includes('prep')) return RESPONSES.interview
  if (m.includes('resume')||m.includes('ats')||m.includes('cv')) return RESPONSES.resume
  if (m.includes('skill')||m.includes('learn')||m.includes('study')) return RESPONSES.skills
  return RESPONSES.default
}

export default function ChatbotPage() {
  const [messages, setMessages] = useState([{ role:'ai', text:'👋 Hi! I\'m your AI Career Assistant. Ask me anything about career paths, skills, salary, interviews, or ATS tips!' }])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)

  const send = async (msg) => {
    if (!msg?.trim()) return
    const userMsg = msg || input
    setMessages(m => [...m, { role:'user', text:userMsg }])
    setInput('')
    setLoading(true)
    await new Promise(r => setTimeout(r, 900))
    setMessages(m => [...m, { role:'ai', text:getReply(userMsg) }])
    setLoading(false)
  }

  return (
    <div>
      <div style={{ marginBottom:28 }}>
        <h1 style={{ fontFamily:'Syne,sans-serif', fontSize:22, fontWeight:700 }}>AI Career Assistant</h1>
        <p style={{ fontSize:13, color:'#9090b0', marginTop:4 }}>Powered by Claude AI — ask anything about your career</p>
      </div>
      <div style={{ background:'rgba(255,255,255,0.04)', border:'1px solid rgba(255,255,255,0.08)', borderRadius:16, padding:20 }}>
        <div style={{ height:320, overflowY:'auto', display:'flex', flexDirection:'column', gap:12, padding:'4px 0', marginBottom:16 }}>
          {messages.map((m,i) => (
            <div key={i} style={{ maxWidth:'82%', padding:'10px 14px', borderRadius:12, fontSize:13, lineHeight:1.6,
              alignSelf: m.role==='user'?'flex-end':'flex-start',
              background: m.role==='user'?'rgba(108,99,255,0.25)':'rgba(255,255,255,0.05)',
              border: m.role==='user'?'1px solid rgba(108,99,255,0.3)':'1px solid rgba(255,255,255,0.08)',
              borderBottomRightRadius: m.role==='user'?4:12,
              borderBottomLeftRadius: m.role==='ai'?4:12 }}>
              {m.text}
            </div>
          ))}
          {loading && <div style={{ alignSelf:'flex-start', padding:'10px 14px', background:'rgba(255,255,255,0.05)', border:'1px solid rgba(255,255,255,0.08)', borderRadius:12, fontSize:13, color:'#5a5a7a' }}>Thinking...</div>}
        </div>
        <div style={{ display:'flex', gap:8, marginBottom:10, flexWrap:'wrap' }}>
          {['What careers match me?','How to improve ATS?','Skills for 2025','Salary negotiation tips'].map(q => (
            <button key={q} onClick={() => send(q)} style={{ fontSize:12, padding:'6px 12px', background:'transparent', border:'1px solid rgba(255,255,255,0.1)', borderRadius:20, color:'#9090b0', cursor:'pointer', transition:'all 0.2s' }}
              onMouseEnter={e=>{e.target.style.background='rgba(108,99,255,0.1)'; e.target.style.color='#6c63ff'}}
              onMouseLeave={e=>{e.target.style.background='transparent'; e.target.style.color='#9090b0'}}>{q}</button>
          ))}
        </div>
        <div style={{ display:'flex', gap:8 }}>
          <input value={input} onChange={e=>setInput(e.target.value)} onKeyDown={e=>e.key==='Enter'&&send()} placeholder="Ask about your career path..."
            style={{ flex:1, padding:'10px 14px', background:'rgba(255,255,255,0.04)', border:'1px solid rgba(255,255,255,0.1)', borderRadius:10, color:'#f0f0f8', fontSize:13, outline:'none', fontFamily:'DM Sans,sans-serif' }}/>
          <button onClick={() => send()} style={{ padding:'10px 20px', background:'#6c63ff', border:'none', borderRadius:10, color:'white', fontSize:13, fontWeight:500, cursor:'pointer' }}>Send</button>
        </div>
      </div>
    </div>
  )
}

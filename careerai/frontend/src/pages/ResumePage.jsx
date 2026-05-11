import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { resumeAPI } from '../services/api'
import { useResumeStore } from '../services/store'

function ScoreRing({ score, size=140 }) {
  const r = 52; const circ = 2 * Math.PI * r
  const offset = circ - (score / 100) * circ
  const color = score >= 80 ? '#00d4aa' : score >= 65 ? '#6c63ff' : score >= 50 ? '#ffb347' : '#ff6b6b'
  const grade = score >= 80 ? 'Excellent' : score >= 65 ? 'Good' : score >= 50 ? 'Fair' : 'Poor'
  return (
    <div style={{ display:'flex', flexDirection:'column', alignItems:'center', gap:8 }}>
      <div style={{ position:'relative', width:size, height:size }}>
        <svg viewBox="0 0 120 120" width={size} height={size} style={{ transform:'rotate(-90deg)' }}>
          <circle cx="60" cy="60" r={r} fill="none" stroke="rgba(255,255,255,0.06)" strokeWidth="10"/>
          <circle cx="60" cy="60" r={r} fill="none" stroke={color} strokeWidth="10"
            strokeDasharray={circ} strokeDashoffset={offset} strokeLinecap="round"
            style={{ transition:'stroke-dashoffset 1.5s cubic-bezier(0.4,0,0.2,1)' }}/>
        </svg>
        <div style={{ position:'absolute', top:'50%', left:'50%', transform:'translate(-50%,-50%)', textAlign:'center' }}>
          <div style={{ fontFamily:'Syne,sans-serif', fontSize:28, fontWeight:800, color }}>{score}</div>
          <div style={{ fontSize:11, color:'#9090b0' }}>/100</div>
        </div>
      </div>
      <span style={{ fontSize:13, fontWeight:500, color }}>{grade}</span>
    </div>
  )
}

function BreakdownBar({ label, score, color }) {
  return (
    <div style={{ marginBottom:10 }}>
      <div style={{ display:'flex', justifyContent:'space-between', fontSize:13, marginBottom:5 }}>
        <span style={{ color:'#9090b0' }}>{label}</span>
        <span style={{ fontWeight:500, color }}>{score}/100</span>
      </div>
      <div style={{ height:6, background:'rgba(255,255,255,0.06)', borderRadius:3, overflow:'hidden' }}>
        <div style={{ height:'100%', width:`${score}%`, background:color, borderRadius:3, transition:'width 1s' }}/>
      </div>
    </div>
  )
}

export default function ResumePage() {
  const [loading, setLoading] = useState(false)
  const [step, setStep] = useState('')
  const [error, setError] = useState('')
  const { latestAnalysis, setAnalysis } = useResumeStore()

  const STEPS = ['Extracting text from file...','Parsing skills and education...','Running ATS analysis...','Matching career profiles...','Generating recommendations...']

  const onDrop = useCallback(async (files) => {
    const file = files[0]
    if (!file) return
    setLoading(true); setError(''); setStep(STEPS[0])
    let si = 0
    const interval = setInterval(() => { si++; if (si < STEPS.length) setStep(STEPS[si]) }, 700)
    try {
      const { data } = await resumeAPI.upload(file)
      setAnalysis(data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Analysis failed. Please try again.')
    } finally {
      clearInterval(interval)
      setLoading(false)
    }
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop, accept: { 'application/pdf': ['.pdf'], 'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'], 'text/plain': ['.txt'] }, multiple: false
  })

  const a = latestAnalysis
  const bars = a ? [
    { label:'Keyword Density', score:a.keyword_score, color:'#6c63ff' },
    { label:'Contact Information', score:a.contact_score, color:'#00d4aa' },
    { label:'Work Experience', score:a.experience_score, color:'#ff6b9d' },
    { label:'Education', score:a.education_score, color:'#ffb347' },
    { label:'Skills Section', score:a.skills_score, color:'#54a0ff' },
    { label:'Format & Structure', score:a.format_score, color:'#ee5a24' },
  ] : []

  return (
    <div>
      <div style={{ marginBottom:28 }}>
        <h1 style={{ fontFamily:'Syne,sans-serif', fontSize:22, fontWeight:700 }}>Resume ATS Scanner</h1>
        <p style={{ fontSize:13, color:'#9090b0', marginTop:4 }}>Upload your resume for real AI-powered ATS analysis and career matching</p>
      </div>

      {/* Upload Zone */}
      <div style={{ background:'rgba(255,255,255,0.04)', border:'1px solid rgba(255,255,255,0.08)', borderRadius:16, padding:20, marginBottom:24 }}>
        <div {...getRootProps()} style={{
          border: `2px dashed ${isDragActive ? '#6c63ff' : 'rgba(108,99,255,0.35)'}`,
          borderRadius:14, padding:40, textAlign:'center', cursor:'pointer',
          background: isDragActive ? 'rgba(108,99,255,0.08)' : 'rgba(108,99,255,0.03)', transition:'all 0.3s'
        }}>
          <input {...getInputProps()} />
          {loading ? (
            <div style={{ display:'flex', flexDirection:'column', alignItems:'center', gap:14 }}>
              <div style={{ width:48, height:48, border:'3px solid rgba(108,99,255,0.2)', borderTopColor:'#6c63ff', borderRadius:'50%', animation:'spin 0.8s linear infinite' }}/>
              <div style={{ fontFamily:'Syne,sans-serif', fontSize:16, fontWeight:600 }}>Analyzing Resume...</div>
              <div style={{ fontSize:13, color:'#9090b0' }}>{step}</div>
            </div>
          ) : (
            <>
              <div style={{ fontSize:48, marginBottom:12, background:'linear-gradient(135deg,#6c63ff,#ff6b9d)', WebkitBackgroundClip:'text', WebkitTextFillColor:'transparent' }}>⬆</div>
              <div style={{ fontFamily:'Syne,sans-serif', fontSize:18, fontWeight:600, marginBottom:6 }}>
                {isDragActive ? 'Drop your resume here' : 'Drop your resume or click to browse'}
              </div>
              <div style={{ fontSize:13, color:'#9090b0' }}>PDF, DOCX, TXT — Max 10MB</div>
              <div style={{ display:'flex', gap:8, justifyContent:'center', marginTop:14 }}>
                {['PDF','DOCX','TXT'].map(f => (
                  <span key={f} style={{ fontSize:11, padding:'3px 10px', borderRadius:20, border:'1px solid rgba(255,255,255,0.12)', color:'#9090b0' }}>{f}</span>
                ))}
              </div>
            </>
          )}
        </div>
        {error && <div style={{ marginTop:12, padding:'10px 14px', background:'rgba(255,107,107,0.1)', border:'1px solid rgba(255,107,107,0.3)', borderRadius:10, color:'#ff6b6b', fontSize:13 }}>{error}</div>}
      </div>

      {/* Results */}
      {a && (
        <>
          <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:20, marginBottom:24 }}>
            <div style={{ background:'rgba(255,255,255,0.04)', border:'1px solid rgba(255,255,255,0.08)', borderRadius:16, padding:24, display:'flex', flexDirection:'column', alignItems:'center', gap:16 }}>
              <h3 style={{ fontFamily:'Syne,sans-serif', fontSize:16, fontWeight:600 }}>ATS Score</h3>
              <ScoreRing score={a.ats_score} />
              <div style={{ textAlign:'center' }}>
                <div style={{ fontSize:13, color:'#9090b0' }}>File: <strong style={{color:'#f0f0f8'}}>{a.filename || 'resume'}</strong></div>
                <div style={{ fontSize:13, color:'#9090b0', marginTop:4 }}>Words: <strong style={{color:'#f0f0f8'}}>{a.word_count}</strong> · Skills: <strong style={{color:'#6c63ff'}}>{a.detected_skills?.length}</strong></div>
              </div>
            </div>
            <div style={{ background:'rgba(255,255,255,0.04)', border:'1px solid rgba(255,255,255,0.08)', borderRadius:16, padding:24 }}>
              <h3 style={{ fontFamily:'Syne,sans-serif', fontSize:16, fontWeight:600, marginBottom:16 }}>Score Breakdown</h3>
              {bars.map(b => <BreakdownBar key={b.label} {...b} />)}
            </div>
          </div>

          <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:20, marginBottom:24 }}>
            <div style={{ background:'rgba(255,255,255,0.04)', border:'1px solid rgba(255,255,255,0.08)', borderRadius:16, padding:20 }}>
              <h3 style={{ fontFamily:'Syne,sans-serif', fontSize:16, fontWeight:600, marginBottom:4 }}>✅ Detected Skills ({a.detected_skills?.length})</h3>
              <p style={{ fontSize:12, color:'#9090b0', marginBottom:12 }}>Found in your resume</p>
              <div style={{ display:'flex', flexWrap:'wrap', gap:7 }}>
                {a.detected_skills?.map((s,i) => (
                  <span key={s} style={{ padding:'4px 11px', borderRadius:20, fontSize:12, fontWeight:500,
                    background: i<8?'rgba(0,212,170,0.12)':'rgba(108,99,255,0.12)',
                    border: i<8?'1px solid rgba(0,212,170,0.3)':'1px solid rgba(108,99,255,0.3)',
                    color: i<8?'#00d4aa':'#9f8fff' }}>{s}</span>
                ))}
              </div>
            </div>
            <div style={{ background:'rgba(255,255,255,0.04)', border:'1px solid rgba(255,255,255,0.08)', borderRadius:16, padding:20 }}>
              <h3 style={{ fontFamily:'Syne,sans-serif', fontSize:16, fontWeight:600, marginBottom:4 }}>⚡ Skill Gaps</h3>
              <p style={{ fontSize:12, color:'#9090b0', marginBottom:12 }}>Add these to boost your score</p>
              <div style={{ display:'flex', flexWrap:'wrap', gap:7 }}>
                {a.missing_skills?.slice(0,12).map(s => (
                  <span key={s} style={{ padding:'4px 11px', borderRadius:20, fontSize:12, fontWeight:500, background:'rgba(255,107,107,0.1)', border:'1px solid rgba(255,107,107,0.25)', color:'#ff6b6b' }}>{s}</span>
                ))}
              </div>
            </div>
          </div>

          {a.recommendations?.length > 0 && (
            <div style={{ background:'rgba(255,255,255,0.04)', border:'1px solid rgba(255,255,255,0.08)', borderRadius:16, padding:20, marginBottom:24 }}>
              <h3 style={{ fontFamily:'Syne,sans-serif', fontSize:16, fontWeight:600, marginBottom:12 }}>💡 AI Recommendations</h3>
              <div style={{ display:'flex', flexDirection:'column', gap:8 }}>
                {a.recommendations.map((r,i) => (
                  <div key={i} style={{ display:'flex', gap:10, padding:'10px 14px', background:'rgba(108,99,255,0.06)', border:'1px solid rgba(108,99,255,0.15)', borderRadius:10 }}>
                    <span style={{ color:'#6c63ff', fontWeight:600, fontSize:13 }}>{i+1}.</span>
                    <span style={{ fontSize:13, color:'#d0d0e8' }}>{r}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {a.career_matches?.length > 0 && (
            <div style={{ background:'rgba(255,255,255,0.04)', border:'1px solid rgba(255,255,255,0.08)', borderRadius:16, padding:20 }}>
              <h3 style={{ fontFamily:'Syne,sans-serif', fontSize:16, fontWeight:600, marginBottom:4 }}>🚀 Career Matches</h3>
              <p style={{ fontSize:12, color:'#9090b0', marginBottom:16 }}>Based on your detected skills</p>
              <div style={{ display:'grid', gridTemplateColumns:'repeat(3,1fr)', gap:12 }}>
                {a.career_matches.slice(0,6).map((c) => (
                  <div key={c.title} style={{ padding:14, background:'rgba(255,255,255,0.02)', border:'1px solid rgba(255,255,255,0.08)', borderRadius:12 }}>
                    <div style={{ fontFamily:'Syne,sans-serif', fontSize:14, fontWeight:600, marginBottom:4 }}>{c.title}</div>
                    <div style={{ fontSize:12, color:'#9090b0', marginBottom:8 }}>{c.match_score}% match</div>
                    <div style={{ height:4, background:'rgba(255,255,255,0.06)', borderRadius:2, overflow:'hidden' }}>
                      <div style={{ height:'100%', width:`${c.match_score}%`, background:'linear-gradient(90deg,#6c63ff,#00d4aa)', borderRadius:2 }}/>
                    </div>
                    <div style={{ fontSize:11, color:'#9090b0', marginTop:7 }}>{c.salary_range}</div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </>
      )}

      <style>{`@keyframes spin{to{transform:rotate(360deg)}}`}</style>
    </div>
  )
}

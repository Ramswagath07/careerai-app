import { create } from 'zustand'
import { resumeAPI } from '../services/api'

export const useResumeStore = create((set) => ({
  resumes: [],
  currentAnalysis: null,
  isUploading: false,
  upload: async (file) => {
    set({ isUploading: true })
    const form = new FormData()
    form.append('file', file)
    const res = await resumeAPI.upload(form)
    set(state => ({ resumes: [res.data, ...state.resumes], currentAnalysis: res.data, isUploading: false }))
    return res.data
  },
  fetchHistory: async () => {
    const res = await resumeAPI.history()
    set({ resumes: res.data })
  },
  clearAnalysis: () => set({ currentAnalysis: null }),
}))

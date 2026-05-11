import { create } from 'zustand'

export const useAuthStore = create((set) => ({
  user: JSON.parse(localStorage.getItem('careerai_user') || 'null'),
  token: localStorage.getItem('access_token'),
  isAuthenticated: !!localStorage.getItem('access_token'),
  setAuth: (user, token) => {
    localStorage.setItem('access_token', token)
    localStorage.setItem('careerai_user', JSON.stringify(user))
    set({ user, token, isAuthenticated: true })
  },
  logout: () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('careerai_user')
    set({ user: null, token: null, isAuthenticated: false })
  },
  updateUser: (data) => set((s) => ({ user: { ...s.user, ...data } })),
}))

export const useResumeStore = create((set) => ({
  latestAnalysis: null,
  history: [],
  setAnalysis: (data) => set({ latestAnalysis: data }),
  setHistory: (h) => set({ history: h }),
}))

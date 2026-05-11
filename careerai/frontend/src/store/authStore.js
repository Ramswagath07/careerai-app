import { create } from 'zustand'
import { authAPI } from '../services/api'

export const useAuthStore = create((set) => ({
  user: null,
  token: localStorage.getItem('access_token'),
  isLoading: false,
  login: async (email, password) => {
    set({ isLoading: true })
    const res = await authAPI.login({ email, password })
    localStorage.setItem('access_token', res.data.access_token)
    set({ user: res.data.user, token: res.data.access_token, isLoading: false })
    return res.data
  },
  register: async (name, email, password) => {
    set({ isLoading: true })
    const res = await authAPI.register({ full_name: name, email, password })
    localStorage.setItem('access_token', res.data.access_token)
    set({ user: res.data.user, token: res.data.access_token, isLoading: false })
    return res.data
  },
  logout: () => {
    localStorage.removeItem('access_token')
    set({ user: null, token: null })
  },
  fetchMe: async () => {
    try { const res = await authAPI.me(); set({ user: res.data }) } catch {}
  },
}))

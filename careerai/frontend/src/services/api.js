import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  timeout: 30000,
})

api.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

api.interceptors.response.use(
  res => res,
  async err => {
    if (err.response?.status === 401) {
      localStorage.removeItem('access_token')
      window.location.href = '/login'
    }
    return Promise.reject(err)
  }
)

export const authAPI = {
  register: (data)       => api.post('/auth/register', data),
  login:    (data)       => api.post('/auth/login', data),
  me:       ()           => api.get('/auth/me'),
}

export const resumeAPI = {
  upload:   (form)       => api.post('/resume/upload', form, { headers: { 'Content-Type': 'multipart/form-data' } }),
  history:  ()           => api.get('/resume/history'),
  get:      (id)         => api.get(`/resume/${id}`),
  delete:   (id)         => api.delete(`/resume/${id}`),
}

export const careersAPI = {
  list:     ()           => api.get('/careers/'),
  recommend:(skills)     => api.get('/careers/recommend', { params: { skills } }),
}

export const analyticsAPI = {
  dashboard: ()          => api.get('/analytics/dashboard'),
}

export const chatAPI = {
  send: (message, ctx)   => api.post('/chatbot/message', { message, context: ctx || {} }),
}

export const coursesAPI = {
  list:  (skill)         => api.get('/courses/', { params: { skill } }),
}

export default api

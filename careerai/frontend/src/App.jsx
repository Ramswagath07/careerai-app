import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore } from './services/store'
import Layout from './components/ui/Layout'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import DashboardPage from './pages/DashboardPage'
import ResumePage from './pages/ResumePage'
import CareersPage from './pages/CareersPage'
import RoadmapPage from './pages/RoadmapPage'
import AnalyticsPage from './pages/AnalyticsPage'
import CoursesPage from './pages/CoursesPage'
import ChatbotPage from './pages/ChatbotPage'
import ProfilePage from './pages/ProfilePage'

function ProtectedRoute({ children }) {
  const { isAuthenticated } = useAuthStore()
  return isAuthenticated ? children : <Navigate to="/login" replace />
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/" element={<ProtectedRoute><Layout /></ProtectedRoute>}>
        <Route index element={<DashboardPage />} />
        <Route path="resume" element={<ResumePage />} />
        <Route path="careers" element={<CareersPage />} />
        <Route path="roadmap" element={<RoadmapPage />} />
        <Route path="analytics" element={<AnalyticsPage />} />
        <Route path="courses" element={<CoursesPage />} />
        <Route path="chatbot" element={<ChatbotPage />} />
        <Route path="profile" element={<ProfilePage />} />
      </Route>
    </Routes>
  )
}

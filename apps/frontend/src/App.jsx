/**
 * App.jsx — Componente raiz do StayFlow.
 *
 * Configura: AuthProvider, BrowserRouter, rotas e layout (Navbar + Footer).
 */

import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { AuthProvider } from './contexts/AuthContext'
import Navbar from './components/layout/Navbar'
import Footer from './components/layout/Footer'
import ProtectedRoute from './components/layout/ProtectedRoute'

// Páginas
import HomePage from './pages/HomePage'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import HotelDetailPage from './pages/HotelDetailPage'
import CheckoutPage from './pages/CheckoutPage'
import BookingStatusPage from './pages/BookingStatusPage'
import MyBookingsPage from './pages/MyBookingsPage'
import AdminDashboard from './pages/admin/AdminDashboard'

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Navbar />
        <main>
          <Routes>
            {/* Públicas */}
            <Route path="/" element={<HomePage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/hoteis/:id" element={<HotelDetailPage />} />

            {/* Protegidas (cliente) */}
            <Route
              path="/checkout/:quartoId"
              element={<ProtectedRoute><CheckoutPage /></ProtectedRoute>}
            />
            <Route
              path="/reserva/:reservaId"
              element={<ProtectedRoute><BookingStatusPage /></ProtectedRoute>}
            />
            <Route
              path="/minhas-reservas"
              element={<ProtectedRoute><MyBookingsPage /></ProtectedRoute>}
            />

            {/* Protegidas (admin) */}
            <Route
              path="/admin"
              element={<ProtectedRoute adminOnly><AdminDashboard /></ProtectedRoute>}
            />
          </Routes>
        </main>
        <Footer />
      </AuthProvider>
    </BrowserRouter>
  )
}

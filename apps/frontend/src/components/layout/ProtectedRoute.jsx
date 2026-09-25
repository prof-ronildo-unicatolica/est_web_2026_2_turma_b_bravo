/**
 * ProtectedRoute — Wrapper de rota que exige autenticacao.
 * Redireciona para /login se o usuario nao estiver logado.
 * Se adminOnly=true, redireciona para / se nao for admin.
 */

import { Navigate } from 'react-router-dom'
import { useAuth } from '../../contexts/AuthContext'

export default function ProtectedRoute({ children, adminOnly = false }) {
  const { isAuthenticated, isAdmin, loading } = useAuth()

  if (loading) {
    return (
      <div className="loading-overlay">
        <div className="spinner" />
        <p>Verificando autenticação...</p>
      </div>
    )
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  if (adminOnly && !isAdmin) {
    return <Navigate to="/" replace />
  }

  return children
}

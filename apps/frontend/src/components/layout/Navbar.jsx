/**
 * Navbar — Barra de navegação superior do StayFlow.
 */

import { Link, useNavigate } from 'react-router-dom'
import { Building2, LogOut, LayoutDashboard } from 'lucide-react'
import { useAuth } from '../../contexts/AuthContext'

export default function Navbar() {
  const { user, isAuthenticated, isAdmin, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  return (
    <nav className="navbar" id="main-navbar">
      <div className="container">
        <Link to="/" className="navbar-brand">
          <Building2 size={28} />
          <span>StayFlow</span>
        </Link>

        <ul className="navbar-nav">
          <li><Link to="/">Hotéis</Link></li>
          {isAuthenticated && (
            <li><Link to="/minhas-reservas">Minhas Reservas</Link></li>
          )}
          {isAdmin && (
            <li><Link to="/admin">Painel Admin</Link></li>
          )}
        </ul>

        <div className="navbar-actions">
          {isAuthenticated ? (
            <>
              <span className="text-sm" style={{ color: 'var(--color-text-muted)' }}>
                Olá, {user?.nome?.split(' ')[0]}
              </span>
              {isAdmin && (
                <Link to="/admin" className="btn btn-sm btn-gold btn-nav">
                  <LayoutDashboard size={14} />
                  Admin
                </Link>
              )}
              <button onClick={handleLogout} className="btn btn-ghost btn-sm btn-nav">
                <LogOut size={14} />
                Sair
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="btn btn-ghost btn-nav">Entrar</Link>
              <Link to="/register" className="btn btn-primary btn-nav">Cadastrar</Link>
            </>
          )}
        </div>
      </div>
    </nav>
  )
}

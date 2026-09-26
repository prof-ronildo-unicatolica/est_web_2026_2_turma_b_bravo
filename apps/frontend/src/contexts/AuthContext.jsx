/**
 * AuthContext — Gerenciamento de estado de autenticação.
 *
 * Fornece: user, token, login(), register(), logout(), isAuthenticated, isAdmin
 * Persiste dados no localStorage para sobreviver a refreshes.
 */

import { createContext, useContext, useState, useEffect } from 'react'
import api from '../services/api'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [token, setToken] = useState(null)
  const [loading, setLoading] = useState(true)

  // Restaurar sessão do localStorage
  useEffect(() => {
    const savedToken = localStorage.getItem('stayflow_token')
    const savedUser = localStorage.getItem('stayflow_user')
    if (savedToken && savedUser) {
      setToken(savedToken)
      setUser(JSON.parse(savedUser))
    }
    setLoading(false)
  }, [])

  const login = async (email, senha) => {
    const response = await api.post('/auth/login', { email, senha })
    const { access_token } = response.data
    localStorage.setItem('stayflow_token', access_token)
    setToken(access_token)

    // Buscar dados do usuario
    const userResponse = await api.get('/auth/me', {
      headers: { Authorization: `Bearer ${access_token}` },
    })
    const userData = userResponse.data
    localStorage.setItem('stayflow_user', JSON.stringify(userData))
    setUser(userData)

    return userData
  }

  const register = async (nome, email, senha) => {
    await api.post('/auth/register', { nome, email, senha })
    // Faz login automatico apos cadastro
    return await login(email, senha)
  }

  const logout = () => {
    localStorage.removeItem('stayflow_token')
    localStorage.removeItem('stayflow_user')
    setToken(null)
    setUser(null)
  }

  const value = {
    user,
    token,
    loading,
    login,
    register,
    logout,
    isAuthenticated: !!token,
    isAdmin: user?.is_admin ?? false,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

// eslint-disable-next-line react-refresh/only-export-components
export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth deve ser usado dentro de um AuthProvider')
  }
  return context
}

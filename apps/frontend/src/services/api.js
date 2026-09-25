/**
 * Cliente HTTP centralizado — Axios configurado para o StayFlow API.
 *
 * Features:
 * - Base URL parametrizada por env (VITE_API_URL)
 * - Interceptor que injeta token JWT no header Authorization
 * - Interceptor de resposta para tratar 401 (token expirado)
 */

import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor: injeta token JWT se disponivel
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('stayflow_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor: trata 401 (token expirado)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('stayflow_token')
      localStorage.removeItem('stayflow_user')
      // Redireciona para login se nao estiver la
      if (window.location.pathname !== '/login') {
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  }
)

export default api

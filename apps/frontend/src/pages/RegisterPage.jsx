/**
 * RegisterPage — Tela de cadastro do StayFlow.
 */

import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Building2, Mail, Lock, User, AlertCircle } from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'

export default function RegisterPage() {
  const [nome, setNome] = useState('')
  const [email, setEmail] = useState('')
  const [senha, setSenha] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { register } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      await register(nome, email, senha)
      navigate('/')
    } catch (err) {
      setError(err.response?.data?.detail || 'Erro ao criar conta. Tente novamente.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="page-wrapper flex items-center justify-center" style={{ minHeight: 'calc(100vh - 72px)' }}>
      <div className="card" style={{ maxWidth: 440, width: '100%' }}>
        <div className="card-body p-8">
          <div className="text-center mb-8">
            <div className="flex justify-center mb-4">
              <Building2 size={40} style={{ color: 'var(--color-primary)' }} />
            </div>
            <h1 style={{ fontSize: 'var(--text-2xl)', fontFamily: 'var(--font-display)' }}>
              Criar conta
            </h1>
            <p className="text-sm text-muted mt-2">
              Cadastre-se para reservar seus hotéis favoritos
            </p>
          </div>

          {error && (
            <div className="alert alert-error mb-4">
              <AlertCircle size={16} />
              <span>{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="flex flex-col gap-4">
            <div className="form-group">
              <label className="form-label" htmlFor="register-nome">Nome completo</label>
              <div style={{ position: 'relative' }}>
                <User size={16} style={{
                  position: 'absolute', left: 12, top: '50%', transform: 'translateY(-50%)',
                  color: 'var(--color-text-muted)'
                }} />
                <input
                  id="register-nome"
                  type="text"
                  className="form-input w-full"
                  style={{ paddingLeft: 40 }}
                  placeholder="Seu nome completo"
                  value={nome}
                  onChange={(e) => setNome(e.target.value)}
                  required
                />
              </div>
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="register-email">E-mail</label>
              <div style={{ position: 'relative' }}>
                <Mail size={16} style={{
                  position: 'absolute', left: 12, top: '50%', transform: 'translateY(-50%)',
                  color: 'var(--color-text-muted)'
                }} />
                <input
                  id="register-email"
                  type="email"
                  className="form-input w-full"
                  style={{ paddingLeft: 40 }}
                  placeholder="seu@email.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="register-senha">Senha</label>
              <div style={{ position: 'relative' }}>
                <Lock size={16} style={{
                  position: 'absolute', left: 12, top: '50%', transform: 'translateY(-50%)',
                  color: 'var(--color-text-muted)'
                }} />
                <input
                  id="register-senha"
                  type="password"
                  className="form-input w-full"
                  style={{ paddingLeft: 40 }}
                  placeholder="Crie uma senha forte"
                  value={senha}
                  onChange={(e) => setSenha(e.target.value)}
                  required
                  minLength={6}
                />
              </div>
            </div>

            <button
              type="submit"
              className="btn btn-primary btn-lg w-full mt-2"
              disabled={loading}
            >
              {loading ? 'Criando conta...' : 'Criar conta'}
            </button>
          </form>

          <p className="text-center text-sm text-muted mt-6">
            Já tem uma conta?{' '}
            <Link to="/login" className="font-semibold">Entrar</Link>
          </p>
        </div>
      </div>
    </div>
  )
}

/**
 * MyBookingsPage — Lista de reservas do usuário autenticado.
 */

import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { Calendar, Star } from 'lucide-react'
import api from '../services/api'

const STATUS_MAP = {
  PENDENTE: { label: 'Pendente', class: 'badge-warning' },
  CONFIRMADA: { label: 'Confirmada', class: 'badge-success' },
  CANCELADA: { label: 'Cancelada', class: 'badge-error' },
  CONCLUIDA: { label: 'Concluída', class: 'badge-info' },
}

export default function MyBookingsPage() {
  const [reservas, setReservas] = useState([])
  const [loading, setLoading] = useState(true)
  const [cancelling, setCancelling] = useState(null)
  const [showReview, setShowReview] = useState(null)
  const [reviewData, setReviewData] = useState({ nota: 5, comentario: '' })

  useEffect(() => {
    fetchReservas()
  }, [])



  const fetchReservas = async () => {
    try {
      const res = await api.get('/reservas/minhas')
      setReservas(res.data)
    } catch (err) {
      console.error('Erro:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleCancel = async (reservaId) => {
    if (!confirm('Tem certeza que deseja cancelar esta reserva?')) return
    setCancelling(reservaId)
    try {
      await api.post(`/reservas/${reservaId}/cancelar`, { motivo: 'Cancelamento pelo cliente' })
      fetchReservas()
    } catch (err) {
      alert(err.response?.data?.detail || 'Erro ao cancelar')
    } finally {
      setCancelling(null)
    }
  }

  const handleReview = async (reservaId) => {
    try {
      await api.post('/avaliacoes', {
        reserva_id: reservaId,
        nota: reviewData.nota,
        comentario: reviewData.comentario,
      })
      setShowReview(null)
      setReviewData({ nota: 5, comentario: '' })
      alert('Avaliação enviada com sucesso!')
    } catch (err) {
      alert(err.response?.data?.detail || 'Erro ao enviar avaliação')
    }
  }

  if (loading) {
    return <div className="loading-overlay"><div className="spinner" /><p>Carregando reservas...</p></div>
  }

  return (
    <div className="page-wrapper">
      <div className="container" style={{ maxWidth: 900 }}>
        <h1 className="mb-6" style={{ fontFamily: 'var(--font-display)', fontSize: 'var(--text-3xl)' }}>
          Minhas Reservas
        </h1>

        {reservas.length === 0 ? (
          <div className="card text-center p-8">
            <Calendar size={48} className="text-muted" style={{ margin: '0 auto' }} />
            <h3 className="mt-4">Nenhuma reserva encontrada</h3>
            <p className="text-muted mt-2">Você ainda não fez nenhuma reserva.</p>
            <Link to="/" className="btn btn-primary mt-4">Explorar hotéis</Link>
          </div>
        ) : (
          <div className="flex flex-col gap-4">
            {reservas.map((r) => {
              const status = STATUS_MAP[r.status] || STATUS_MAP.PENDENTE
              return (
                <div key={r.id} className="card" id={`reserva-${r.id}`}>
                  <div className="card-body">
                    <div className="flex justify-between items-center mb-3">
                      <div>
                        <span className="text-xs text-muted" style={{ fontFamily: 'var(--font-mono)' }}>
                          {r.id.slice(0, 8)}...
                        </span>
                        <span className={`badge ${status.class}`} style={{ marginLeft: 8 }}>
                          {status.label}
                        </span>
                      </div>
                      <span style={{
                        fontSize: 'var(--text-xl)', fontWeight: 700,
                        color: 'var(--color-primary)',
                      }}>
                        R$ {r.valor_total.toFixed(2)}
                      </span>
                    </div>

                    <div className="grid-3 gap-4">
                      <div>
                        <span className="text-xs text-muted">Check-in</span>
                        <p className="font-semibold">{new Date(r.checkin + 'T12:00').toLocaleDateString('pt-BR')}</p>
                      </div>
                      <div>
                        <span className="text-xs text-muted">Check-out</span>
                        <p className="font-semibold">{new Date(r.checkout + 'T12:00').toLocaleDateString('pt-BR')}</p>
                      </div>
                      <div>
                        <span className="text-xs text-muted">Criada em</span>
                        <p className="font-semibold">{new Date(r.created_at).toLocaleDateString('pt-BR')}</p>
                      </div>
                    </div>

                    <div className="flex gap-3 mt-4">
                      <Link to={`/reserva/${r.id}`} className="btn btn-secondary btn-sm">
                        Ver Voucher
                      </Link>
                      {r.status === 'CONFIRMADA' && (
                        <>
                          <button
                            onClick={() => handleCancel(r.id)}
                            className="btn btn-danger btn-sm"
                            disabled={cancelling === r.id}
                          >
                            {cancelling === r.id ? 'Cancelando...' : 'Cancelar'}
                          </button>
                          <button
                            onClick={() => setShowReview(r.id)}
                            className="btn btn-gold btn-sm"
                          >
                            <Star size={14} /> Avaliar
                          </button>
                        </>
                      )}
                    </div>

                    {/* Modal de Avaliação inline */}
                    {showReview === r.id && (
                      <div className="card mt-4 p-4" style={{ background: 'var(--color-bg)' }}>
                        <h4 className="mb-3">Avaliar Estadia</h4>
                        <div className="flex flex-col gap-3">
                          <div className="form-group">
                            <label className="form-label">Nota</label>
                            <div className="stars">
                              {[1, 2, 3, 4, 5].map(i => (
                                <Star
                                  key={i}
                                  size={24}
                                  className={`star interactive ${i <= reviewData.nota ? 'filled' : ''}`}
                                  fill={i <= reviewData.nota ? 'currentColor' : 'none'}
                                  onClick={() => setReviewData(p => ({...p, nota: i}))}
                                />
                              ))}
                            </div>
                          </div>
                          <div className="form-group">
                            <label className="form-label">Comentário (opcional)</label>
                            <textarea
                              className="form-input"
                              rows={3}
                              value={reviewData.comentario}
                              onChange={e => setReviewData(p => ({...p, comentario: e.target.value}))}
                              placeholder="Como foi sua experiência?"
                            />
                          </div>
                          <div className="flex gap-2">
                            <button onClick={() => handleReview(r.id)} className="btn btn-primary btn-sm">
                              Enviar Avaliação
                            </button>
                            <button onClick={() => setShowReview(null)} className="btn btn-ghost btn-sm">
                              Cancelar
                            </button>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}

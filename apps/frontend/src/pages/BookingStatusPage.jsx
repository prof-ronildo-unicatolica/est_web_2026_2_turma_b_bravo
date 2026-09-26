/**
 * BookingStatusPage — Tela de confirmação/status da reserva (voucher).
 */

import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { CheckCircle, Calendar, CreditCard, Clock } from 'lucide-react'
import api from '../services/api'

const STATUS_MAP = {
  PENDENTE: { label: 'Pendente', class: 'badge-warning' },
  CONFIRMADA: { label: 'Confirmada', class: 'badge-success' },
  CANCELADA: { label: 'Cancelada', class: 'badge-error' },
  CONCLUIDA: { label: 'Concluída', class: 'badge-info' },
}

export default function BookingStatusPage() {
  const { reservaId } = useParams()
  const [reserva, setReserva] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchReserva()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [reservaId])


  const fetchReserva = async () => {
    try {
      const res = await api.get(`/reservas/${reservaId}`)
      setReserva(res.data)
    } catch (err) {
      console.error('Erro:', err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="loading-overlay"><div className="spinner" /><p>Carregando reserva...</p></div>
  }

  if (!reserva) {
    return (
      <div className="page-wrapper container text-center">
        <h2>Reserva não encontrada</h2>
        <Link to="/minhas-reservas" className="btn btn-primary mt-4">Ver minhas reservas</Link>
      </div>
    )
  }

  const status = STATUS_MAP[reserva.status] || STATUS_MAP.PENDENTE

  return (
    <div className="page-wrapper">
      <div className="container" style={{ maxWidth: 700 }}>
        {reserva.status === 'CONFIRMADA' && (
          <div className="text-center mb-8">
            <CheckCircle size={64} style={{ color: 'var(--color-success)', margin: '0 auto' }} />
            <h1 className="mt-4" style={{ fontFamily: 'var(--font-display)', fontSize: 'var(--text-3xl)' }}>
              Reserva Confirmada!
            </h1>
            <p className="text-muted mt-2">Sua reserva foi processada com sucesso.</p>
          </div>
        )}

        <div className="card">
          <div className="card-header flex justify-between items-center">
            <h3 style={{ fontFamily: 'var(--font-display)' }}>Voucher da Reserva</h3>
            <span className={`badge ${status.class}`}>{status.label}</span>
          </div>
          <div className="card-body">
            <div className="flex flex-col gap-4">
              <div className="flex items-center gap-3">
                <CreditCard size={18} className="text-muted" />
                <div>
                  <span className="text-xs text-muted">Código da Reserva</span>
                  <p className="font-bold" style={{ fontFamily: 'var(--font-mono)', fontSize: 'var(--text-sm)' }}>
                    {reserva.id}
                  </p>
                </div>
              </div>

              <div className="grid-2">
                <div className="flex items-center gap-3">
                  <Calendar size={18} className="text-muted" />
                  <div>
                    <span className="text-xs text-muted">Check-in</span>
                    <p className="font-semibold">{new Date(reserva.checkin + 'T12:00').toLocaleDateString('pt-BR')}</p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <Calendar size={18} className="text-muted" />
                  <div>
                    <span className="text-xs text-muted">Check-out</span>
                    <p className="font-semibold">{new Date(reserva.checkout + 'T12:00').toLocaleDateString('pt-BR')}</p>
                  </div>
                </div>
              </div>

              <div className="flex items-center gap-3">
                <Clock size={18} className="text-muted" />
                <div>
                  <span className="text-xs text-muted">Opcionais</span>
                  <div className="flex gap-2 mt-1">
                    {reserva.early_checkin && <span className="badge badge-info">Early check-in</span>}
                    {reserva.late_checkout && <span className="badge badge-info">Late check-out</span>}
                    {reserva.berco && <span className="badge badge-info">Berço</span>}
                    {!reserva.early_checkin && !reserva.late_checkout && !reserva.berco && (
                      <span className="text-sm text-muted">Nenhum</span>
                    )}
                  </div>
                </div>
              </div>

              <div style={{ borderTop: '2px solid var(--color-border)', paddingTop: 'var(--space-4)' }}>
                <div className="flex justify-between items-center">
                  <span className="text-lg font-semibold">Valor Total</span>
                  <span style={{
                    fontSize: 'var(--text-2xl)', fontWeight: 700,
                    color: 'var(--color-primary)', fontFamily: 'var(--font-display)'
                  }}>
                    R$ {reserva.valor_total.toFixed(2)}
                  </span>
                </div>
                <p className="text-xs text-muted mt-1">
                  Tarifa {reserva.tipo_tarifa === 'REEMBOLSAVEL' ? 'reembolsável' : 'não reembolsável'}
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="flex gap-4 mt-6 justify-center">
          <Link to="/minhas-reservas" className="btn btn-secondary">Ver todas as reservas</Link>
          <Link to="/" className="btn btn-primary">Buscar mais hotéis</Link>
        </div>
      </div>
    </div>
  )
}

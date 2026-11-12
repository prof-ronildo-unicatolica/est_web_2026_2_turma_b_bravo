/**
 * MyBookingsPage — Lista de reservas do usuário autenticado.
 *
 * Cada reserva é um ReservaCard (components/reservas/); a página só cuida
 * da lista, do cancelamento e do envio da avaliação.
 */

import { useCallback, useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { Calendar } from 'lucide-react'
import api from '../services/api'
import ReservaCard from '../components/reservas/ReservaCard'

function ListaVazia() {
  return (
    <div className="card text-center p-8">
      <Calendar size={48} className="text-muted" style={{ margin: '0 auto' }} />
      <h3 className="mt-4">Nenhuma reserva encontrada</h3>
      <p className="text-muted mt-2">Você ainda não fez nenhuma reserva.</p>
      <Link to="/" className="btn btn-primary mt-4">Explorar hotéis</Link>
    </div>
  )
}

export default function MyBookingsPage() {
  const [reservas, setReservas] = useState([])
  const [loading, setLoading] = useState(true)
  const [cancelando, setCancelando] = useState(null)
  const [avaliando, setAvaliando] = useState(null)

  const fetchReservas = useCallback(async () => {
    try {
      const res = await api.get('/reservas/minhas')
      setReservas(res.data)
    } catch (err) {
      console.error('Erro:', err)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchReservas()
  }, [fetchReservas])

  const handleCancel = async (reservaId) => {
    if (!window.confirm('Tem certeza que deseja cancelar esta reserva?')) return
    setCancelando(reservaId)
    try {
      await api.post(`/reservas/${reservaId}/cancelar`, { motivo: 'Cancelamento pelo cliente' })
      fetchReservas()
    } catch (err) {
      window.alert(err.response?.data?.detail || 'Erro ao cancelar')
    } finally {
      setCancelando(null)
    }
  }

  const handleReview = async (reservaId, { nota, comentario }) => {
    try {
      await api.post('/avaliacoes', { reserva_id: reservaId, nota, comentario })
      setAvaliando(null)
      window.alert('Avaliação enviada com sucesso!')
    } catch (err) {
      window.alert(err.response?.data?.detail || 'Erro ao enviar avaliação')
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
          <ListaVazia />
        ) : (
          <div className="flex flex-col gap-4">
            {reservas.map((reserva) => (
              <ReservaCard
                key={reserva.id}
                reserva={reserva}
                cancelando={cancelando === reserva.id}
                avaliando={avaliando === reserva.id}
                onCancelar={() => handleCancel(reserva.id)}
                onAbrirAvaliacao={() => setAvaliando(reserva.id)}
                onEnviarAvaliacao={(dados) => handleReview(reserva.id, dados)}
                onFecharAvaliacao={() => setAvaliando(null)}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

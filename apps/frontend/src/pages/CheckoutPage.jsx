/**
 * CheckoutPage — Tela de criação de reserva.
 *
 * A página cuida do estado e das chamadas à API; o formulário, o resumo e as
 * funções de cálculo vivem em components/checkout/ e utils/reserva.js.
 */

import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { AlertCircle, ArrowLeft } from 'lucide-react'
import api from '../services/api'
import { buscarQuartoPorId, listarServicosAdicionais } from '../services/quartos'
import { FORM_RESERVA_INICIAL, alternarItem, montarPayloadReserva } from '../utils/reserva'
import FormularioReserva from '../components/checkout/FormularioReserva'
import ResumoReserva from '../components/checkout/ResumoReserva'

export default function CheckoutPage() {
  const { quartoId } = useParams()
  const navigate = useNavigate()
  const quartoIdNumero = Number.parseInt(quartoId, 10)
  const [quarto, setQuarto] = useState(null)
  const [servicos, setServicos] = useState([])
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')
  const [simulacao, setSimulacao] = useState(null)
  const [form, setForm] = useState(FORM_RESERVA_INICIAL)

  useEffect(() => {
    const carregar = async () => {
      try {
        const [listaServicos, quartoEncontrado] = await Promise.all([
          listarServicosAdicionais(),
          buscarQuartoPorId(quartoIdNumero),
        ])
        setServicos(listaServicos)
        setQuarto(quartoEncontrado)
      } catch (err) {
        console.error('Erro:', err)
      } finally {
        setLoading(false)
      }
    }
    carregar()
  }, [quartoIdNumero])

  useEffect(() => {
    if (!form.checkin || !form.checkout) return
    const simular = async () => {
      try {
        const res = await api.post('/reservas/simular', montarPayloadReserva(quartoIdNumero, form))
        setSimulacao(res.data)
        setError('')
      } catch (err) {
        setError(err.response?.data?.detail || 'Erro ao simular preço')
      }
    }
    simular()
  }, [form, quartoIdNumero])

  const atualizarCampo = (campo, valor) => setForm((anterior) => ({ ...anterior, [campo]: valor }))

  const alternarServico = (id) =>
    setForm((anterior) => ({ ...anterior, servico_ids: alternarItem(anterior.servico_ids, id) }))

  const handleSubmit = async (e) => {
    e.preventDefault()
    setSubmitting(true)
    setError('')
    try {
      const res = await api.post('/reservas', montarPayloadReserva(quartoIdNumero, form))
      navigate(`/reserva/${res.data.id}`)
    } catch (err) {
      setError(err.response?.data?.detail || 'Erro ao criar reserva')
    } finally {
      setSubmitting(false)
    }
  }

  if (loading) {
    return <div className="loading-overlay"><div className="spinner" /><p>Carregando...</p></div>
  }

  return (
    <div className="page-wrapper">
      <div className="container" style={{ maxWidth: 900 }}>
        <button type="button" onClick={() => navigate(-1)} className="btn btn-ghost mb-4">
          <ArrowLeft size={16} /> Voltar
        </button>

        <h1 className="mb-6" style={{ fontFamily: 'var(--font-display)', fontSize: 'var(--text-3xl)' }}>
          Finalizar Reserva
        </h1>

        {error && (
          <div className="alert alert-error mb-4"><AlertCircle size={16} /><span>{error}</span></div>
        )}

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 380px', gap: 'var(--space-6)' }}>
          <FormularioReserva
            form={form}
            servicos={servicos}
            submitting={submitting}
            onChange={atualizarCampo}
            onToggleServico={alternarServico}
            onSubmit={handleSubmit}
          />
          <div>
            <ResumoReserva quarto={quarto} simulacao={simulacao} />
          </div>
        </div>
      </div>
    </div>
  )
}

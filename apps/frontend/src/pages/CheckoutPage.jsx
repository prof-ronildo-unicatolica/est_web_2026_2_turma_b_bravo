/**
 * CheckoutPage — Tela de criação de reserva.
 */

import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft, Calendar, Users, CreditCard, AlertCircle } from 'lucide-react'
import api from '../services/api'

export default function CheckoutPage() {
  const { quartoId } = useParams()
  const navigate = useNavigate()
  const [quarto, setQuarto] = useState(null)
  const [servicos, setServicos] = useState([])
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')
  const [simulacao, setSimulacao] = useState(null)

  const [form, setForm] = useState({
    checkin: '',
    checkout: '',
    num_adultos: 1,
    num_criancas: 0,
    num_bebes: 0,
    tipo_tarifa: 'REEMBOLSAVEL',
    early_checkin: false,
    late_checkout: false,
    berco: false,
    servico_ids: [],
  })

  useEffect(() => {
    fetchData()
  }, [quartoId])

  const fetchData = async () => {
    try {
      const [quartoRes, servicosRes] = await Promise.all([
        api.get(`/hoteis/auxiliar/servicos`),
        api.get(`/hoteis/auxiliar/servicos`),
      ])
      setServicos(servicosRes.data)

      // Buscar detalhes do quarto (via admin endpoint alternativo ou hoteis)
      // Vamos usar um approach simples: buscar todos os hoteis e encontrar o quarto
      const hoteisRes = await api.get('/hoteis')
      for (const hotel of hoteisRes.data) {
        const detailRes = await api.get(`/hoteis/${hotel.id}`)
        const found = detailRes.data.quartos?.find(q => q.id === parseInt(quartoId))
        if (found) {
          setQuarto({ ...found, hotel_nome: detailRes.data.nome })
          break
        }
      }
    } catch (err) {
      console.error('Erro:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleSimular = async () => {
    if (!form.checkin || !form.checkout) return
    try {
      const res = await api.post('/reservas/simular', {
        quarto_id: parseInt(quartoId),
        ...form,
      })
      setSimulacao(res.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Erro ao simular preço')
    }
  }

  useEffect(() => {
    if (form.checkin && form.checkout) {
      handleSimular()
    }
  }, [form])

  const handleSubmit = async (e) => {
    e.preventDefault()
    setSubmitting(true)
    setError('')

    try {
      const res = await api.post('/reservas', {
        quarto_id: parseInt(quartoId),
        ...form,
      })
      navigate(`/reserva/${res.data.id}`)
    } catch (err) {
      setError(err.response?.data?.detail || 'Erro ao criar reserva')
    } finally {
      setSubmitting(false)
    }
  }

  const toggleServico = (id) => {
    setForm(prev => ({
      ...prev,
      servico_ids: prev.servico_ids.includes(id)
        ? prev.servico_ids.filter(s => s !== id)
        : [...prev.servico_ids, id]
    }))
  }

  if (loading) {
    return <div className="loading-overlay"><div className="spinner" /><p>Carregando...</p></div>
  }

  return (
    <div className="page-wrapper">
      <div className="container" style={{ maxWidth: 900 }}>
        <button onClick={() => navigate(-1)} className="btn btn-ghost mb-4">
          <ArrowLeft size={16} /> Voltar
        </button>

        <h1 className="mb-6" style={{ fontFamily: 'var(--font-display)', fontSize: 'var(--text-3xl)' }}>
          Finalizar Reserva
        </h1>

        {error && (
          <div className="alert alert-error mb-4"><AlertCircle size={16} /><span>{error}</span></div>
        )}

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 380px', gap: 'var(--space-6)' }}>
          {/* Formulário */}
          <form onSubmit={handleSubmit}>
            <div className="card mb-4">
              <div className="card-header"><h3><Calendar size={18} /> Datas da Estadia</h3></div>
              <div className="card-body">
                <div className="grid-2 gap-4">
                  <div className="form-group">
                    <label className="form-label">Check-in</label>
                    <input type="date" className="form-input" value={form.checkin}
                      onChange={e => setForm(p => ({...p, checkin: e.target.value}))} required />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Check-out</label>
                    <input type="date" className="form-input" value={form.checkout}
                      onChange={e => setForm(p => ({...p, checkout: e.target.value}))} required />
                  </div>
                </div>
              </div>
            </div>

            <div className="card mb-4">
              <div className="card-header"><h3><Users size={18} /> Hóspedes</h3></div>
              <div className="card-body">
                <div className="grid-3 gap-4">
                  <div className="form-group">
                    <label className="form-label">Adultos</label>
                    <input type="number" className="form-input" min="1" max="4"
                      value={form.num_adultos}
                      onChange={e => setForm(p => ({...p, num_adultos: parseInt(e.target.value)}))} />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Crianças</label>
                    <input type="number" className="form-input" min="0" max="3"
                      value={form.num_criancas}
                      onChange={e => setForm(p => ({...p, num_criancas: parseInt(e.target.value)}))} />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Bebês</label>
                    <input type="number" className="form-input" min="0" max="2"
                      value={form.num_bebes}
                      onChange={e => setForm(p => ({...p, num_bebes: parseInt(e.target.value)}))} />
                  </div>
                </div>
              </div>
            </div>

            <div className="card mb-4">
              <div className="card-header"><h3>Opcionais</h3></div>
              <div className="card-body flex flex-col gap-3">
                <label className="form-checkbox">
                  <input type="checkbox" checked={form.early_checkin}
                    onChange={e => setForm(p => ({...p, early_checkin: e.target.checked}))} />
                  Early check-in (+15%)
                </label>
                <label className="form-checkbox">
                  <input type="checkbox" checked={form.late_checkout}
                    onChange={e => setForm(p => ({...p, late_checkout: e.target.checked}))} />
                  Late check-out (+15%)
                </label>
                <label className="form-checkbox">
                  <input type="checkbox" checked={form.berco}
                    onChange={e => setForm(p => ({...p, berco: e.target.checked}))} />
                  Berço (R$30/dia)
                </label>
                <div className="form-group mt-2">
                  <label className="form-label">Tipo de Tarifa</label>
                  <select className="form-input form-select" value={form.tipo_tarifa}
                    onChange={e => setForm(p => ({...p, tipo_tarifa: e.target.value}))}>
                    <option value="REEMBOLSAVEL">Reembolsável (flexível)</option>
                    <option value="NAO_REEMBOLSAVEL">Não reembolsável (-10%)</option>
                  </select>
                </div>
              </div>
            </div>

            {servicos.length > 0 && (
              <div className="card mb-4">
                <div className="card-header"><h3>Serviços Adicionais</h3></div>
                <div className="card-body flex flex-col gap-3">
                  {servicos.map(s => (
                    <label key={s.id} className="form-checkbox">
                      <input type="checkbox" checked={form.servico_ids.includes(s.id)}
                        onChange={() => toggleServico(s.id)} />
                      {s.nome} — R$ {s.preco.toFixed(2)}
                    </label>
                  ))}
                </div>
              </div>
            )}

            <button type="submit" className="btn btn-gold btn-lg w-full" disabled={submitting}>
              <CreditCard size={18} />
              {submitting ? 'Processando...' : 'Confirmar Reserva'}
            </button>
          </form>

          {/* Resumo */}
          <div>
            <div className="card" style={{ position: 'sticky', top: 90 }}>
              <div className="card-header">
                <h3 style={{ fontFamily: 'var(--font-display)' }}>Resumo</h3>
              </div>
              <div className="card-body">
                {quarto && (
                  <div className="mb-4">
                    <p className="font-semibold">{quarto.hotel_nome}</p>
                    <p className="text-sm text-muted">{quarto.tipo}</p>
                    <p className="text-sm text-muted mt-1">
                      R$ {quarto.preco_diaria.toFixed(2)}/diária
                    </p>
                  </div>
                )}

                {simulacao && (
                  <div className="flex flex-col gap-2" style={{ borderTop: '1px solid var(--color-border)', paddingTop: 'var(--space-4)' }}>
                    <div className="flex justify-between text-sm">
                      <span>{simulacao.num_diarias} diária(s)</span>
                      <span>R$ {simulacao.subtotal.toFixed(2)}</span>
                    </div>
                    {simulacao.multiplicador_temporada > 1 && (
                      <div className="flex justify-between text-sm text-gold">
                        <span>Temporada (×{simulacao.multiplicador_temporada})</span>
                        <span>Incluído</span>
                      </div>
                    )}
                    {simulacao.extras > 0 && (
                      <div className="flex justify-between text-sm">
                        <span>Extras</span>
                        <span>+R$ {simulacao.extras.toFixed(2)}</span>
                      </div>
                    )}
                    {simulacao.desconto > 0 && (
                      <div className="flex justify-between text-sm text-success">
                        <span>Desconto</span>
                        <span>-R$ {simulacao.desconto.toFixed(2)}</span>
                      </div>
                    )}
                    {simulacao.valor_servicos > 0 && (
                      <div className="flex justify-between text-sm">
                        <span>Serviços</span>
                        <span>+R$ {simulacao.valor_servicos.toFixed(2)}</span>
                      </div>
                    )}
                    <div className="flex justify-between font-bold mt-2" style={{
                      borderTop: '2px solid var(--color-border)',
                      paddingTop: 'var(--space-3)',
                      fontSize: 'var(--text-xl)',
                      color: 'var(--color-primary)',
                    }}>
                      <span>Total</span>
                      <span>R$ {simulacao.valor_total.toFixed(2)}</span>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

/**
 * AdminDashboard — Painel administrativo do StayFlow.
 */

import { useState, useEffect } from 'react'
import { Building2, MapPin, Bed, Plus, Trash2, Edit, X, Activity } from 'lucide-react'
import api from '../../services/api'

function AdminSection({ title, icon: Icon, children }) {
  const [open, setOpen] = useState(false)
  return (
    <div className="card mb-4">
      <div
        className="card-header flex justify-between items-center"
        style={{ cursor: 'pointer' }}
        onClick={() => setOpen(!open)}
      >
        <h3 className="flex items-center gap-2">
          <Icon size={18} /> {title}
        </h3>
        <span style={{ transform: open ? 'rotate(180deg)' : 'none', transition: 'transform 0.2s' }}>▼</span>
      </div>
      {open && <div className="card-body">{children}</div>}
    </div>
  )
}

function CidadesAdmin() {
  const [cidades, setCidades] = useState([])
  const [form, setForm] = useState({ nome: '', estado: '' })
  const [loading, setLoading] = useState(false)

  useEffect(() => { fetchCidades() }, [])

  const fetchCidades = async () => {
    const res = await api.get('/admin/cidades')
    setCidades(res.data)
  }

  const handleAdd = async (e) => {
    e.preventDefault()
    setLoading(true)
    try {
      await api.post('/admin/cidades', form)
      setForm({ nome: '', estado: '' })
      fetchCidades()
    } catch (err) {
      alert(err.response?.data?.detail || 'Erro')
    } finally { setLoading(false) }
  }

  const handleDelete = async (id) => {
    if (!confirm('Excluir esta cidade?')) return
    await api.delete(`/admin/cidades/${id}`)
    fetchCidades()
  }

  return (
    <>
      <form onSubmit={handleAdd} className="flex gap-3 mb-4">
        <input className="form-input" placeholder="Nome da cidade" value={form.nome}
          onChange={e => setForm(p => ({...p, nome: e.target.value}))} required style={{flex: 1}} />
        <input className="form-input" placeholder="UF" value={form.estado} maxLength={2}
          onChange={e => setForm(p => ({...p, estado: e.target.value.toUpperCase()}))} required style={{width: 80}} />
        <button type="submit" className="btn btn-primary btn-sm" disabled={loading}>
          <Plus size={14} /> Adicionar
        </button>
      </form>
      <div className="table-wrapper">
        <table className="table">
          <thead><tr><th>ID</th><th>Nome</th><th>UF</th><th>Ações</th></tr></thead>
          <tbody>
            {cidades.map(c => (
              <tr key={c.id}>
                <td>{c.id}</td>
                <td>{c.nome}</td>
                <td>{c.estado}</td>
                <td>
                  <button onClick={() => handleDelete(c.id)} className="btn btn-danger btn-sm">
                    <Trash2 size={12} />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  )
}

function HoteisAdmin() {
  const [hoteis, setHoteis] = useState([])

  useEffect(() => { fetchHoteis() }, [])

  const fetchHoteis = async () => {
    const res = await api.get('/admin/hoteis')
    setHoteis(res.data)
  }

  const handleDelete = async (id) => {
    if (!confirm('Excluir este hotel?')) return
    await api.delete(`/admin/hoteis/${id}`)
    fetchHoteis()
  }

  return (
    <div className="table-wrapper">
      <table className="table">
        <thead><tr><th>ID</th><th>Nome</th><th>Estrelas</th><th>Cidade</th><th>Ações</th></tr></thead>
        <tbody>
          {hoteis.map(h => (
            <tr key={h.id}>
              <td>{h.id}</td>
              <td>{h.nome}</td>
              <td>{'★'.repeat(h.estrelas)}</td>
              <td>{h.cidade_id}</td>
              <td>
                <button onClick={() => handleDelete(h.id)} className="btn btn-danger btn-sm">
                  <Trash2 size={12} />
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

function QuartosAdmin() {
  const [quartos, setQuartos] = useState([])

  useEffect(() => { fetchQuartos() }, [])

  const fetchQuartos = async () => {
    const res = await api.get('/admin/quartos')
    setQuartos(res.data)
  }

  return (
    <div className="table-wrapper">
      <table className="table">
        <thead><tr><th>ID</th><th>Hotel</th><th>Tipo</th><th>Adultos</th><th>Crianças</th><th>Diária</th></tr></thead>
        <tbody>
          {quartos.map(q => (
            <tr key={q.id}>
              <td>{q.id}</td>
              <td>{q.hotel_id}</td>
              <td>{q.tipo}</td>
              <td>{q.capacidade_adultos}</td>
              <td>{q.capacidade_criancas}</td>
              <td>R$ {q.preco_diaria.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

function AuditLogsAdmin() {
  const [logs, setLogs] = useState([])
  const [loading, setLoading] = useState(false)

  const fetchLogs = async () => {
    setLoading(true)
    try {
      const res = await api.get('/admin/logs?limite=50')
      setLogs(res.data)
    } catch {
      setLogs([])
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchLogs()
  }, [])

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <span className="text-sm text-muted">Exibindo os últimos 50 eventos capturados pelo RabbitMQ e persistidos no MongoDB</span>
        <button className="btn btn-outline btn-sm" onClick={fetchLogs} disabled={loading}>
          {loading ? 'Atualizando...' : 'Atualizar Logs'}
        </button>
      </div>

      {logs.length === 0 ? (
        <div className="text-center py-6 text-muted">Nenhum evento de auditoria registrado ainda.</div>
      ) : (
        <div style={{ maxHeight: '350px', overflowY: 'auto' }}>
          <table className="table">
            <thead>
              <tr>
                <th>Evento</th>
                <th>Detalhes / Payload</th>
                <th>Timestamp UTC</th>
              </tr>
            </thead>
            <tbody>
              {logs.map((log, idx) => (
                <tr key={idx}>
                  <td>
                    <span className="badge badge-primary">{log.evento || 'log'}</span>
                  </td>
                  <td>
                    <code style={{ fontSize: '0.8rem', background: 'var(--surface-color)', padding: '2px 6px', borderRadius: '4px' }}>
                      {JSON.stringify(log, null, 1)}
                    </code>
                  </td>
                  <td className="text-sm text-muted whitespace-nowrap">
                    {log.timestamp ? new Date(log.timestamp).toLocaleString('pt-BR') : '-'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}

export default function AdminDashboard() {
  const [stats, setStats] = useState({ cidades: 0, hoteis: 0, quartos: 0 })

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    try {
      const [cidades, hoteis, quartos] = await Promise.all([
        api.get('/admin/cidades'),
        api.get('/admin/hoteis'),
        api.get('/admin/quartos'),
      ])
      setStats({
        cidades: cidades.data.length,
        hoteis: hoteis.data.length,
        quartos: quartos.data.length,
      })
    } catch (err) {
      console.error('Erro ao buscar stats:', err)
    }
  }

  return (
    <div className="page-wrapper">
      <div className="container">
        <h1 className="mb-6" style={{ fontFamily: 'var(--font-display)', fontSize: 'var(--text-3xl)' }}>
          Painel Administrativo
        </h1>

        {/* Stats */}
        <div className="grid-3 mb-8">
          <div className="card">
            <div className="card-body text-center">
              <MapPin size={32} className="text-primary" style={{ margin: '0 auto' }} />
              <div className="text-3xl font-bold mt-2" style={{ fontFamily: 'var(--font-display)' }}>
                {stats.cidades}
              </div>
              <span className="text-sm text-muted">Cidades</span>
            </div>
          </div>
          <div className="card">
            <div className="card-body text-center">
              <Building2 size={32} className="text-primary" style={{ margin: '0 auto' }} />
              <div className="text-3xl font-bold mt-2" style={{ fontFamily: 'var(--font-display)' }}>
                {stats.hoteis}
              </div>
              <span className="text-sm text-muted">Hotéis</span>
            </div>
          </div>
          <div className="card">
            <div className="card-body text-center">
              <Bed size={32} className="text-primary" style={{ margin: '0 auto' }} />
              <div className="text-3xl font-bold mt-2" style={{ fontFamily: 'var(--font-display)' }}>
                {stats.quartos}
              </div>
              <span className="text-sm text-muted">Quartos</span>
            </div>
          </div>
        </div>


        {/* CRUDs */}
        <AdminSection title="Cidades" icon={MapPin}>
          <CidadesAdmin />
        </AdminSection>

        <AdminSection title="Hotéis" icon={Building2}>
          <HoteisAdmin />
        </AdminSection>

        <AdminSection title="Quartos" icon={Bed}>
          <QuartosAdmin />
        </AdminSection>

        <AdminSection title="Auditoria NoSQL (MongoDB & RabbitMQ)" icon={Activity}>
          <AuditLogsAdmin />
        </AdminSection>
      </div>
    </div>
  )
}


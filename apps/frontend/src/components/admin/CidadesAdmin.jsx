/**
 * CidadesAdmin — Cadastro e listagem de cidades no painel administrativo.
 */

import { useCallback, useEffect, useState } from 'react'
import { Plus, Trash2 } from 'lucide-react'
import api from '../../services/api'

const FORM_INICIAL = { nome: '', estado: '' }

export default function CidadesAdmin() {
  const [cidades, setCidades] = useState([])
  const [form, setForm] = useState(FORM_INICIAL)
  const [loading, setLoading] = useState(false)

  const fetchCidades = useCallback(async () => {
    const res = await api.get('/admin/cidades')
    setCidades(res.data)
  }, [])

  useEffect(() => {
    fetchCidades()
  }, [fetchCidades])

  const handleAdd = async (e) => {
    e.preventDefault()
    setLoading(true)
    try {
      await api.post('/admin/cidades', form)
      setForm(FORM_INICIAL)
      fetchCidades()
    } catch (err) {
      alert(err.response?.data?.detail || 'Erro')
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id) => {
    if (!confirm('Excluir esta cidade?')) return
    await api.delete(`/admin/cidades/${id}`)
    fetchCidades()
  }

  return (
    <>
      <form onSubmit={handleAdd} className="flex gap-3 mb-4">
        <input className="form-input" placeholder="Nome da cidade" value={form.nome} required
          aria-label="Nome da cidade" style={{ flex: 1 }}
          onChange={(e) => setForm((p) => ({ ...p, nome: e.target.value }))} />
        <input className="form-input" placeholder="UF" value={form.estado} maxLength={2} required
          aria-label="UF" style={{ width: 80 }}
          onChange={(e) => setForm((p) => ({ ...p, estado: e.target.value.toUpperCase() }))} />
        <button type="submit" className="btn btn-primary btn-sm" disabled={loading}>
          <Plus size={14} /> Adicionar
        </button>
      </form>
      <div className="table-wrapper">
        <table className="table">
          <thead><tr><th>ID</th><th>Nome</th><th>UF</th><th>Ações</th></tr></thead>
          <tbody>
            {cidades.map((cidade) => (
              <tr key={cidade.id}>
                <td>{cidade.id}</td>
                <td>{cidade.nome}</td>
                <td>{cidade.estado}</td>
                <td>
                  <button type="button" className="btn btn-danger btn-sm"
                    aria-label={`Excluir ${cidade.nome}`} onClick={() => handleDelete(cidade.id)}>
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

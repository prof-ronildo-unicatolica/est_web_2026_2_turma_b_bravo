/**
 * HoteisAdmin — Listagem e exclusão de hotéis no painel administrativo.
 */

import { useCallback, useEffect, useState } from 'react'
import { Trash2 } from 'lucide-react'
import api from '../../services/api'

export default function HoteisAdmin() {
  const [hoteis, setHoteis] = useState([])

  const fetchHoteis = useCallback(async () => {
    const res = await api.get('/admin/hoteis')
    setHoteis(res.data)
  }, [])

  useEffect(() => {
    fetchHoteis()
  }, [fetchHoteis])

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
          {hoteis.map((hotel) => (
            <tr key={hotel.id}>
              <td>{hotel.id}</td>
              <td>{hotel.nome}</td>
              <td>{'★'.repeat(hotel.estrelas)}</td>
              <td>{hotel.cidade_id}</td>
              <td>
                <button type="button" className="btn btn-danger btn-sm"
                  aria-label={`Excluir ${hotel.nome}`} onClick={() => handleDelete(hotel.id)}>
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

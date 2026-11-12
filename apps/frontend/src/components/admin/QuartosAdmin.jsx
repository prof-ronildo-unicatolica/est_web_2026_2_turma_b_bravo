/**
 * QuartosAdmin — Listagem de quartos no painel administrativo.
 */

import { useEffect, useState } from 'react'
import api from '../../services/api'

export default function QuartosAdmin() {
  const [quartos, setQuartos] = useState([])

  useEffect(() => {
    api.get('/admin/quartos').then((res) => setQuartos(res.data))
  }, [])

  return (
    <div className="table-wrapper">
      <table className="table">
        <thead>
          <tr><th>ID</th><th>Hotel</th><th>Tipo</th><th>Adultos</th><th>Crianças</th><th>Diária</th></tr>
        </thead>
        <tbody>
          {quartos.map((quarto) => (
            <tr key={quarto.id}>
              <td>{quarto.id}</td>
              <td>{quarto.hotel_id}</td>
              <td>{quarto.tipo}</td>
              <td>{quarto.capacidade_adultos}</td>
              <td>{quarto.capacidade_criancas}</td>
              <td>R$ {quarto.preco_diaria.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

/**
 * QuartoCard — Card de um quarto do hotel com preço, capacidade e ação de reserva.
 */

import { Link } from 'react-router-dom'

function descreverCapacidade(quarto) {
  const adultos = `${quarto.capacidade_adultos} adulto${quarto.capacidade_adultos > 1 ? 's' : ''}`
  if (!(quarto.capacidade_criancas > 0)) return adultos
  return `${adultos} + ${quarto.capacidade_criancas} criança${quarto.capacidade_criancas > 1 ? 's' : ''}`
}

export default function QuartoCard({ quarto, isAuthenticated }) {
  return (
    <div className="card" id={`quarto-${quarto.id}`}>
      <div className="card-body">
        <div className="flex justify-between items-center">
          <h3 style={{ fontFamily: 'var(--font-display)' }}>{quarto.tipo}</h3>
          <div className="text-right">
            <div style={{ fontSize: 'var(--text-2xl)', fontWeight: 700, color: 'var(--color-primary)' }}>
              R$ {quarto.preco_diaria.toFixed(2)}
            </div>
            <span className="text-xs text-muted">por diária</span>
          </div>
        </div>
        <p className="text-sm text-muted mt-2">{descreverCapacidade(quarto)}</p>
        <Link
          to={isAuthenticated ? `/checkout/${quarto.id}` : '/login'}
          className="btn btn-primary w-full mt-4"
        >
          {isAuthenticated ? 'Reservar Agora' : 'Faça login para reservar'}
        </Link>
      </div>
    </div>
  )
}

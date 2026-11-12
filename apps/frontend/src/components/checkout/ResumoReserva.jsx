/**
 * ResumoReserva — Painel lateral do checkout com o detalhamento do preço simulado.
 */

import { formatarMoeda, linhasDaSimulacao } from '../../utils/reserva'

function Linha({ label, valor, className = '' }) {
  return (
    <div className={`flex justify-between text-sm ${className}`}>
      <span>{label}</span>
      <span>{valor}</span>
    </div>
  )
}

export default function ResumoReserva({ quarto, simulacao }) {
  return (
    <div className="card" style={{ position: 'sticky', top: 90 }}>
      <div className="card-header">
        <h3 style={{ fontFamily: 'var(--font-display)' }}>Resumo</h3>
      </div>
      <div className="card-body">
        {quarto && (
          <div className="mb-4">
            <p className="font-semibold">{quarto.hotel_nome}</p>
            <p className="text-sm text-muted">{quarto.tipo}</p>
            <p className="text-sm text-muted mt-1">{formatarMoeda(quarto.preco_diaria)}/diária</p>
          </div>
        )}

        {simulacao && (
          <div
            className="flex flex-col gap-2"
            style={{ borderTop: '1px solid var(--color-border)', paddingTop: 'var(--space-4)' }}
          >
            {linhasDaSimulacao(simulacao).map((linha) => (
              <Linha key={linha.label} {...linha} />
            ))}
            <div
              className="flex justify-between font-bold mt-2"
              style={{
                borderTop: '2px solid var(--color-border)',
                paddingTop: 'var(--space-3)',
                fontSize: 'var(--text-xl)',
                color: 'var(--color-primary)',
              }}
            >
              <span>Total</span>
              <span>{formatarMoeda(simulacao.valor_total)}</span>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

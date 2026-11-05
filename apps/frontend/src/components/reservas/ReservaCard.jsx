/**
 * ReservaCard — Card de uma reserva do usuário com voucher, cancelamento e avaliação.
 */

import { Link } from 'react-router-dom'
import { Star } from 'lucide-react'
import { formatarData, formatarMoeda } from '../../utils/reserva'
import FormularioAvaliacao from './FormularioAvaliacao'

const STATUS_MAP = {
  PENDENTE: { label: 'Pendente', class: 'badge-warning' },
  CONFIRMADA: { label: 'Confirmada', class: 'badge-success' },
  CANCELADA: { label: 'Cancelada', class: 'badge-error' },
  CONCLUIDA: { label: 'Concluída', class: 'badge-info' },
}

function Datas({ reserva }) {
  const itens = [
    { rotulo: 'Check-in', valor: formatarData(`${reserva.checkin}T12:00`) },
    { rotulo: 'Check-out', valor: formatarData(`${reserva.checkout}T12:00`) },
    { rotulo: 'Criada em', valor: formatarData(reserva.created_at) },
  ]
  return (
    <div className="grid-3 gap-4">
      {itens.map(({ rotulo, valor }) => (
        <div key={rotulo}>
          <span className="text-xs text-muted">{rotulo}</span>
          <p className="font-semibold">{valor}</p>
        </div>
      ))}
    </div>
  )
}

export default function ReservaCard({
  reserva, cancelando, avaliando, onCancelar, onAbrirAvaliacao, onEnviarAvaliacao, onFecharAvaliacao,
}) {
  const status = STATUS_MAP[reserva.status] || STATUS_MAP.PENDENTE
  const confirmada = reserva.status === 'CONFIRMADA'

  return (
    <div className="card" id={`reserva-${reserva.id}`}>
      <div className="card-body">
        <div className="flex justify-between items-center mb-3">
          <div>
            <span className="text-xs text-muted" style={{ fontFamily: 'var(--font-mono)' }}>
              {reserva.id.slice(0, 8)}...
            </span>
            <span className={`badge ${status.class}`} style={{ marginLeft: 8 }}>
              {status.label}
            </span>
          </div>
          <span style={{ fontSize: 'var(--text-xl)', fontWeight: 700, color: 'var(--color-primary)' }}>
            {formatarMoeda(reserva.valor_total)}
          </span>
        </div>

        <Datas reserva={reserva} />

        <div className="flex gap-3 mt-4">
          <Link to={`/reserva/${reserva.id}`} className="btn btn-secondary btn-sm">
            Ver Voucher
          </Link>
          {confirmada && (
            <>
              <button type="button" className="btn btn-danger btn-sm" disabled={cancelando} onClick={onCancelar}>
                {cancelando ? 'Cancelando...' : 'Cancelar'}
              </button>
              <button type="button" className="btn btn-gold btn-sm" onClick={onAbrirAvaliacao}>
                <Star size={14} /> Avaliar
              </button>
            </>
          )}
        </div>

        {avaliando && (
          <FormularioAvaliacao reservaId={reserva.id} onEnviar={onEnviarAvaliacao} onCancelar={onFecharAvaliacao} />
        )}
      </div>
    </div>
  )
}

/**
 * HotelHeader — Cabeçalho do detalhe do hotel: capa, nome, localização, nota e comodidades.
 */

import { Check, MapPin } from 'lucide-react'
import Estrelas from './Estrelas'

function Capa({ hotel }) {
  const matiz = hotel.id * 40
  return (
    <div
      style={{
        height: 280,
        background: `linear-gradient(135deg, hsl(${matiz}, 60%, 75%), hsl(${matiz + 60}, 50%, 65%))`,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        borderRadius: 'var(--radius-xl) var(--radius-xl) 0 0',
      }}
    >
      <span style={{ fontSize: '5rem', opacity: 0.3, color: 'white', fontFamily: 'var(--font-display)' }}>
        {hotel.nome.charAt(0)}
      </span>
    </div>
  )
}

function MediaAvaliacoes({ media, total }) {
  return (
    <div className="text-center">
      <div
        style={{
          fontSize: 'var(--text-3xl)',
          fontWeight: 700,
          color: 'var(--color-secondary)',
          fontFamily: 'var(--font-display)',
        }}
      >
        {media}
      </div>
      <span className="text-xs text-muted">{total} avaliações</span>
    </div>
  )
}

function Comodidades({ itens }) {
  return (
    <div className="mt-6">
      <h3 className="mb-3" style={{ fontSize: 'var(--text-lg)' }}>Comodidades</h3>
      <div className="flex gap-2" style={{ flexWrap: 'wrap' }}>
        {itens?.map((comodidade) => (
          <span key={comodidade.id} className="badge badge-info" style={{ padding: '6px 14px' }}>
            <Check size={12} /> {comodidade.nome}
          </span>
        ))}
      </div>
    </div>
  )
}

export default function HotelHeader({ hotel }) {
  return (
    <div className="card mb-6">
      <Capa hotel={hotel} />
      <div className="card-body">
        <div className="flex justify-between items-center">
          <div>
            <h1 style={{ fontSize: 'var(--text-3xl)', fontFamily: 'var(--font-display)' }}>
              {hotel.nome}
            </h1>
            <div className="flex items-center gap-2 mt-2">
              <MapPin size={16} className="text-muted" />
              <span className="text-muted">{hotel.cidade?.nome}, {hotel.cidade?.estado}</span>
              <span className="text-muted">•</span>
              <Estrelas valor={hotel.estrelas} />
            </div>
          </div>
          {hotel.media_avaliacoes && (
            <MediaAvaliacoes media={hotel.media_avaliacoes} total={hotel.total_avaliacoes} />
          )}
        </div>
        <p className="mt-4 text-secondary">{hotel.descricao}</p>
        <Comodidades itens={hotel.comodidades} />
      </div>
    </div>
  )
}

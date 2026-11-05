/**
 * AvaliacaoCard — Card de uma avaliação deixada por um hóspede.
 */

import Estrelas from './Estrelas'

export default function AvaliacaoCard({ avaliacao }) {
  return (
    <div className="card">
      <div className="card-body">
        <div className="flex justify-between items-center mb-2">
          <span className="font-semibold">{avaliacao.nome_usuario || 'Hóspede'}</span>
          <Estrelas valor={avaliacao.nota} size={14} />
        </div>
        {avaliacao.comentario && <p className="text-sm text-secondary">{avaliacao.comentario}</p>}
        <span className="text-xs text-muted mt-2" style={{ display: 'block' }}>
          {new Date(avaliacao.created_at).toLocaleDateString('pt-BR')}
        </span>
      </div>
    </div>
  )
}

/**
 * FormularioAvaliacao — Nota e comentário de uma estadia concluída.
 */

import { useState } from 'react'
import SeletorDeNota from './SeletorDeNota'

export default function FormularioAvaliacao({ reservaId, onEnviar, onCancelar }) {
  const [nota, setNota] = useState(5)
  const [comentario, setComentario] = useState('')
  const idNota = `nota-${reservaId}`
  const idComentario = `comentario-${reservaId}`

  return (
    <div className="card mt-4 p-4" style={{ background: 'var(--color-bg)' }}>
      <h4 className="mb-3">Avaliar Estadia</h4>
      <div className="flex flex-col gap-3">
        <div className="form-group">
          <span id={idNota} className="form-label">Nota</span>
          <SeletorDeNota nota={nota} onChange={setNota} idRotulo={idNota} />
        </div>
        <div className="form-group">
          <label htmlFor={idComentario} className="form-label">Comentário (opcional)</label>
          <textarea
            id={idComentario}
            className="form-input"
            rows={3}
            value={comentario}
            onChange={(e) => setComentario(e.target.value)}
            placeholder="Como foi sua experiência?"
          />
        </div>
        <div className="flex gap-2">
          <button type="button" className="btn btn-primary btn-sm" onClick={() => onEnviar({ nota, comentario })}>
            Enviar Avaliação
          </button>
          <button type="button" className="btn btn-ghost btn-sm" onClick={onCancelar}>
            Cancelar
          </button>
        </div>
      </div>
    </div>
  )
}

/**
 * SeletorDeNota — Escolha da nota de 1 a 5 em estrelas, acessível por teclado.
 */

import { Star } from 'lucide-react'

const NOTAS = [1, 2, 3, 4, 5]

export default function SeletorDeNota({ nota, onChange, idRotulo }) {
  return (
    <div className="stars" role="radiogroup" aria-labelledby={idRotulo}>
      {NOTAS.map((valor) => (
        <button
          key={valor}
          type="button"
          className="star-button"
          role="radio"
          aria-checked={valor === nota}
          aria-label={`${valor} de 5`}
          onClick={() => onChange(valor)}
        >
          <Star
            size={24}
            className={`star interactive ${valor <= nota ? 'filled' : ''}`}
            fill={valor <= nota ? 'currentColor' : 'none'}
          />
        </button>
      ))}
    </div>
  )
}

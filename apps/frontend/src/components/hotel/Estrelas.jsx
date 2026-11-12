/**
 * Estrelas — Exibe uma nota de 1 a 5 em estrelas (somente leitura).
 */

import { Star } from 'lucide-react'

const ESTRELAS = [1, 2, 3, 4, 5]

export default function Estrelas({ valor, size = 16 }) {
  return (
    <div className="stars" aria-label={`${valor} de 5 estrelas`}>
      {ESTRELAS.map((estrela) => (
        <Star
          key={estrela}
          size={size}
          className={`star ${estrela <= valor ? 'filled' : ''}`}
          fill={estrela <= valor ? 'currentColor' : 'none'}
        />
      ))}
    </div>
  )
}

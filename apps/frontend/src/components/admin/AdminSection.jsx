/**
 * AdminSection — Seção recolhível do painel administrativo.
 *
 * O cabeçalho inteiro é um botão acessível (teclado e leitores de tela),
 * em vez de uma div com onClick.
 */

import { useState } from 'react'

export default function AdminSection({ title, icon: Icon, children }) {
  const [open, setOpen] = useState(false)

  return (
    <div className="card mb-4">
      <div className="card-header">
        <h3 className="w-full">
          <button
            type="button"
            className="admin-section-toggle"
            aria-expanded={open}
            onClick={() => setOpen((aberto) => !aberto)}
          >
            <span className="flex items-center gap-2">
              <Icon size={18} /> {title}
            </span>
            <span aria-hidden="true" style={{ transform: open ? 'rotate(180deg)' : 'none', transition: 'transform 0.2s' }}>
              ▼
            </span>
          </button>
        </h3>
      </div>
      {open && <div className="card-body">{children}</div>}
    </div>
  )
}

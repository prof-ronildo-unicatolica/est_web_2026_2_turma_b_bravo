/**
 * Campos do formulário de reserva, cada um com o <label> ligado ao controle.
 */

import { paraInteiro } from '../../utils/reserva'

export function CampoData({ id, label, value, onChange }) {
  return (
    <div className="form-group">
      <label htmlFor={id} className="form-label">{label}</label>
      <input id={id} type="date" className="form-input" value={value} required
        onChange={(e) => onChange(e.target.value)} />
    </div>
  )
}

export function CampoNumero({ id, label, value, min, max, onChange }) {
  return (
    <div className="form-group">
      <label htmlFor={id} className="form-label">{label}</label>
      <input id={id} type="number" className="form-input" min={min} max={max} value={value}
        onChange={(e) => onChange(paraInteiro(e.target.value, min))} />
    </div>
  )
}

export function Opcional({ id, label, checked, onChange }) {
  return (
    <label htmlFor={id} className="form-checkbox">
      <input id={id} type="checkbox" checked={checked} onChange={(e) => onChange(e.target.checked)} />
      {' '}
      {label}
    </label>
  )
}

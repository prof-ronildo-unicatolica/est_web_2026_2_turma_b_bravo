/**
 * FormularioReserva — Datas, hóspedes, opcionais e serviços adicionais da reserva.
 */

import { Calendar, CreditCard, Users } from 'lucide-react'
import { formatarMoeda } from '../../utils/reserva'
import { CampoData, CampoNumero, Opcional } from './CamposFormulario'

function Secao({ titulo, icone, className = '', children }) {
  return (
    <div className="card mb-4">
      <div className="card-header">
        <h3 className="flex items-center gap-2">{icone}{titulo}</h3>
      </div>
      <div className={`card-body ${className}`}>{children}</div>
    </div>
  )
}

export default function FormularioReserva({ form, servicos, submitting, onChange, onToggleServico, onSubmit }) {
  const atualizar = (campo) => (valor) => onChange(campo, valor)

  return (
    <form onSubmit={onSubmit}>
      <Secao titulo="Datas da Estadia" icone={<Calendar size={18} />}>
        <div className="grid-2 gap-4">
          <CampoData id="checkin" label="Check-in" value={form.checkin} onChange={atualizar('checkin')} />
          <CampoData id="checkout" label="Check-out" value={form.checkout} onChange={atualizar('checkout')} />
        </div>
      </Secao>

      <Secao titulo="Hóspedes" icone={<Users size={18} />}>
        <div className="grid-3 gap-4">
          <CampoNumero id="num_adultos" label="Adultos" min={1} max={4}
            value={form.num_adultos} onChange={atualizar('num_adultos')} />
          <CampoNumero id="num_criancas" label="Crianças" min={0} max={3}
            value={form.num_criancas} onChange={atualizar('num_criancas')} />
          <CampoNumero id="num_bebes" label="Bebês" min={0} max={2}
            value={form.num_bebes} onChange={atualizar('num_bebes')} />
        </div>
      </Secao>

      <Secao titulo="Opcionais" className="flex flex-col gap-3">
        <Opcional id="early_checkin" label="Early check-in (+15%)"
          checked={form.early_checkin} onChange={atualizar('early_checkin')} />
        <Opcional id="late_checkout" label="Late check-out (+15%)"
          checked={form.late_checkout} onChange={atualizar('late_checkout')} />
        <Opcional id="berco" label="Berço (R$30/dia)"
          checked={form.berco} onChange={atualizar('berco')} />
        <div className="form-group mt-2">
          <label htmlFor="tipo_tarifa" className="form-label">Tipo de Tarifa</label>
          <select id="tipo_tarifa" className="form-input form-select" value={form.tipo_tarifa}
            onChange={(e) => onChange('tipo_tarifa', e.target.value)}>
            <option value="REEMBOLSAVEL">Reembolsável (flexível)</option>
            <option value="NAO_REEMBOLSAVEL">Não reembolsável (-10%)</option>
          </select>
        </div>
      </Secao>

      {servicos.length > 0 && (
        <Secao titulo="Serviços Adicionais" className="flex flex-col gap-3">
          {servicos.map((servico) => (
            <Opcional key={servico.id} id={`servico-${servico.id}`}
              label={`${servico.nome} — ${formatarMoeda(servico.preco)}`}
              checked={form.servico_ids.includes(servico.id)}
              onChange={() => onToggleServico(servico.id)} />
          ))}
        </Secao>
      )}

      <button type="submit" className="btn btn-gold btn-lg w-full" disabled={submitting}>
        <CreditCard size={18} />
        {submitting ? 'Processando...' : 'Confirmar Reserva'}
      </button>
    </form>
  )
}

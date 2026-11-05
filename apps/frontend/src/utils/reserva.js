/**
 * Funções puras do fluxo de reserva (checkout e minhas reservas).
 *
 * Nada aqui toca em React ou na API: são cálculos e formatações que os
 * componentes usam e que podem ser testados isoladamente.
 */

export const FORM_RESERVA_INICIAL = {
  checkin: '',
  checkout: '',
  num_adultos: 1,
  num_criancas: 0,
  num_bebes: 0,
  tipo_tarifa: 'REEMBOLSAVEL',
  early_checkin: false,
  late_checkout: false,
  berco: false,
  servico_ids: [],
}

export const formatarMoeda = (valor) => `R$ ${valor.toFixed(2)}`

export const formatarData = (valor) => new Date(valor).toLocaleDateString('pt-BR')

/** Converte o texto de um campo numérico em inteiro; devolve `padrao` se não for número. */
export function paraInteiro(valor, padrao = 0) {
  const numero = Number.parseInt(valor, 10)
  return Number.isNaN(numero) ? padrao : numero
}

/** Inclui o id na lista se ele não estiver, ou remove se já estiver. */
export function alternarItem(lista, id) {
  return lista.includes(id) ? lista.filter((item) => item !== id) : [...lista, id]
}

/** Corpo enviado para POST /reservas e POST /reservas/simular. */
export function montarPayloadReserva(quartoId, form) {
  return { quarto_id: quartoId, ...form }
}

/** Linhas do resumo de preço, na ordem em que aparecem na tela. */
export function linhasDaSimulacao(simulacao) {
  return [
    { label: `${simulacao.num_diarias} diária(s)`, valor: formatarMoeda(simulacao.subtotal) },
    simulacao.multiplicador_temporada > 1 && {
      label: `Temporada (×${simulacao.multiplicador_temporada})`,
      valor: 'Incluído',
      className: 'text-gold',
    },
    simulacao.extras > 0 && { label: 'Extras', valor: `+${formatarMoeda(simulacao.extras)}` },
    simulacao.desconto > 0 && {
      label: 'Desconto',
      valor: `-${formatarMoeda(simulacao.desconto)}`,
      className: 'text-success',
    },
    simulacao.valor_servicos > 0 && {
      label: 'Serviços',
      valor: `+${formatarMoeda(simulacao.valor_servicos)}`,
    },
  ].filter(Boolean)
}

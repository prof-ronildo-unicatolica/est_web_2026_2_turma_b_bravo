/**
 * Chamadas à API usadas pelo checkout: quarto e serviços adicionais.
 *
 * A API pública não expõe GET /quartos/{id}: o quarto é localizado
 * percorrendo o catálogo de hotéis, como a tela de checkout já fazia.
 */

import api from './api'

export async function buscarQuartoPorId(quartoId) {
  const { data: hoteis } = await api.get('/hoteis')
  for (const hotel of hoteis) {
    const { data: detalhe } = await api.get(`/hoteis/${hotel.id}`)
    const quarto = detalhe.quartos?.find((q) => q.id === quartoId)
    if (quarto) return { ...quarto, hotel_nome: detalhe.nome }
  }
  return null
}

export async function listarServicosAdicionais() {
  const { data } = await api.get('/hoteis/auxiliar/servicos')
  return data
}

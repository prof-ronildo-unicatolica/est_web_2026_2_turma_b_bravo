/**
 * HotelDetailPage — Página de detalhes de um hotel com quartos e avaliações.
 */

import { useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { ArrowLeft } from 'lucide-react'
import api from '../services/api'
import { useAuth } from '../contexts/AuthContext'
import HotelHeader from '../components/hotel/HotelHeader'
import QuartoCard from '../components/hotel/QuartoCard'
import AvaliacaoCard from '../components/hotel/AvaliacaoCard'

export default function HotelDetailPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { isAuthenticated } = useAuth()
  const [hotel, setHotel] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchHotel = async () => {
      try {
        const response = await api.get(`/hoteis/${id}`)
        setHotel(response.data)
      } catch (err) {
        console.error('Erro ao buscar hotel:', err)
      } finally {
        setLoading(false)
      }
    }
    fetchHotel()
  }, [id])

  if (loading) {
    return (
      <div className="loading-overlay">
        <div className="spinner" />
        <p>Carregando detalhes do hotel...</p>
      </div>
    )
  }

  if (!hotel) {
    return (
      <div className="page-wrapper container text-center">
        <h2>Hotel não encontrado</h2>
        <Link to="/" className="btn btn-primary mt-4">Voltar para hotéis</Link>
      </div>
    )
  }

  return (
    <div className="page-wrapper">
      <div className="container">
        <button type="button" onClick={() => navigate(-1)} className="btn btn-ghost mb-4">
          <ArrowLeft size={16} /> Voltar
        </button>

        <HotelHeader hotel={hotel} />

        <h2 className="mb-4" style={{ fontSize: 'var(--text-2xl)' }}>Quartos Disponíveis</h2>
        <div className="grid-2 mb-8">
          {hotel.quartos?.map((quarto) => (
            <QuartoCard key={quarto.id} quarto={quarto} isAuthenticated={isAuthenticated} />
          ))}
        </div>

        {hotel.avaliacoes?.length > 0 && (
          <>
            <h2 className="mb-4" style={{ fontSize: 'var(--text-2xl)' }}>Avaliações dos Hóspedes</h2>
            <div className="flex flex-col gap-4 mb-8">
              {hotel.avaliacoes.map((avaliacao) => (
                <AvaliacaoCard key={avaliacao.id} avaliacao={avaliacao} />
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  )
}

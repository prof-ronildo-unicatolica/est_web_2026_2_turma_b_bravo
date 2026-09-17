/**
 * HotelDetailPage — Página de detalhes de um hotel com quartos e avaliações.
 */

import { useState, useEffect } from 'react'
import { useParams, Link, useNavigate } from 'react-router-dom'
import { Star, MapPin, ArrowLeft, Wifi, Check } from 'lucide-react'
import api from '../services/api'
import { useAuth } from '../contexts/AuthContext'

export default function HotelDetailPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { isAuthenticated } = useAuth()
  const [hotel, setHotel] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchHotel()
  }, [id])

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
        <button onClick={() => navigate(-1)} className="btn btn-ghost mb-4">
          <ArrowLeft size={16} /> Voltar
        </button>

        {/* Header do Hotel */}
        <div className="card mb-6">
          <div
            style={{
              height: 280,
              background: `linear-gradient(135deg, hsl(${hotel.id * 40}, 60%, 75%), hsl(${hotel.id * 40 + 60}, 50%, 65%))`,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              borderRadius: 'var(--radius-xl) var(--radius-xl) 0 0',
            }}
          >
            <span style={{ fontSize: '5rem', opacity: 0.3, color: 'white', fontFamily: 'var(--font-display)' }}>
              {hotel.nome.charAt(0)}
            </span>
          </div>
          <div className="card-body">
            <div className="flex justify-between items-center">
              <div>
                <h1 style={{ fontSize: 'var(--text-3xl)', fontFamily: 'var(--font-display)' }}>
                  {hotel.nome}
                </h1>
                <div className="flex items-center gap-2 mt-2">
                  <MapPin size={16} className="text-muted" />
                  <span className="text-muted">{hotel.cidade?.nome}, {hotel.cidade?.estado}</span>
                  <span className="text-muted">•</span>
                  <div className="stars">
                    {[1, 2, 3, 4, 5].map((i) => (
                      <Star key={i} size={16} className={`star ${i <= hotel.estrelas ? 'filled' : ''}`}
                        fill={i <= hotel.estrelas ? 'currentColor' : 'none'} />
                    ))}
                  </div>
                </div>
              </div>
              {hotel.media_avaliacoes && (
                <div className="text-center">
                  <div style={{
                    fontSize: 'var(--text-3xl)', fontWeight: 700,
                    color: 'var(--color-secondary)', fontFamily: 'var(--font-display)'
                  }}>
                    {hotel.media_avaliacoes}
                  </div>
                  <span className="text-xs text-muted">{hotel.total_avaliacoes} avaliações</span>
                </div>
              )}
            </div>
            <p className="mt-4 text-secondary">{hotel.descricao}</p>

            {/* Comodidades */}
            <div className="mt-6">
              <h3 className="mb-3" style={{ fontSize: 'var(--text-lg)' }}>Comodidades</h3>
              <div className="flex gap-2" style={{ flexWrap: 'wrap' }}>
                {hotel.comodidades?.map((c) => (
                  <span key={c.id} className="badge badge-info" style={{ padding: '6px 14px' }}>
                    <Check size={12} /> {c.nome}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Quartos */}
        <h2 className="mb-4" style={{ fontSize: 'var(--text-2xl)' }}>Quartos Disponíveis</h2>
        <div className="grid-2 mb-8">
          {hotel.quartos?.map((quarto) => (
            <div key={quarto.id} className="card" id={`quarto-${quarto.id}`}>
              <div className="card-body">
                <div className="flex justify-between items-center">
                  <h3 style={{ fontFamily: 'var(--font-display)' }}>{quarto.tipo}</h3>
                  <div className="text-right">
                    <div style={{ fontSize: 'var(--text-2xl)', fontWeight: 700, color: 'var(--color-primary)' }}>
                      R$ {quarto.preco_diaria.toFixed(2)}
                    </div>
                    <span className="text-xs text-muted">por diária</span>
                  </div>
                </div>
                <p className="text-sm text-muted mt-2">
                  {quarto.capacidade_adultos} adulto{quarto.capacidade_adultos > 1 ? 's' : ''}
                  {quarto.capacidade_criancas > 0 && ` + ${quarto.capacidade_criancas} criança${quarto.capacidade_criancas > 1 ? 's' : ''}`}
                </p>
                <Link
                  to={isAuthenticated ? `/checkout/${quarto.id}` : '/login'}
                  className="btn btn-primary w-full mt-4"
                >
                  {isAuthenticated ? 'Reservar Agora' : 'Faça login para reservar'}
                </Link>
              </div>
            </div>
          ))}
        </div>

        {/* Avaliações */}
        {hotel.avaliacoes?.length > 0 && (
          <>
            <h2 className="mb-4" style={{ fontSize: 'var(--text-2xl)' }}>Avaliações dos Hóspedes</h2>
            <div className="flex flex-col gap-4 mb-8">
              {hotel.avaliacoes.map((av) => (
                <div key={av.id} className="card">
                  <div className="card-body">
                    <div className="flex justify-between items-center mb-2">
                      <span className="font-semibold">{av.nome_usuario || 'Hóspede'}</span>
                      <div className="stars">
                        {[1, 2, 3, 4, 5].map((i) => (
                          <Star key={i} size={14} className={`star ${i <= av.nota ? 'filled' : ''}`}
                            fill={i <= av.nota ? 'currentColor' : 'none'} />
                        ))}
                      </div>
                    </div>
                    {av.comentario && <p className="text-sm text-secondary">{av.comentario}</p>}
                    <span className="text-xs text-muted mt-2" style={{ display: 'block' }}>
                      {new Date(av.created_at).toLocaleDateString('pt-BR')}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  )
}

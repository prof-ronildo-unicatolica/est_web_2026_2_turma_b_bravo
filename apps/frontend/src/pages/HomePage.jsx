/**
 * HomePage — Tela principal com Hero, busca e listagem de hotéis.
 */

import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { Search, Star, MapPin } from 'lucide-react'
import api from '../services/api'

function StarRating({ rating, count }) {
  return (
    <div className="flex items-center gap-1">
      <div className="stars">
        {[1, 2, 3, 4, 5].map((i) => (
          <Star
            key={i}
            size={14}
            className={`star ${i <= Math.round(rating || 0) ? 'filled' : ''}`}
            fill={i <= Math.round(rating || 0) ? 'currentColor' : 'none'}
          />
        ))}
      </div>
      {rating && <span className="text-sm text-muted">({count})</span>}
    </div>
  )
}

function HotelCard({ hotel }) {
  return (
    <Link to={`/hoteis/${hotel.id}`} style={{ textDecoration: 'none', color: 'inherit' }}>
      <div className="card" id={`hotel-card-${hotel.id}`}>
        <div
          className="card-image"
          style={{
            background: `linear-gradient(135deg, hsl(${hotel.id * 40}, 60%, 85%), hsl(${hotel.id * 40 + 30}, 50%, 75%))`,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <span style={{
            fontSize: 'var(--text-4xl)',
            opacity: 0.4,
            fontFamily: 'var(--font-display)',
            fontWeight: 700,
            color: 'white'
          }}>
            {hotel.estrelas}★
          </span>
        </div>
        <div className="card-body">
          <div className="flex justify-between items-center mb-2">
            <h3 style={{ fontSize: 'var(--text-lg)', fontFamily: 'var(--font-display)' }}>
              {hotel.nome}
            </h3>
          </div>
          <div className="flex items-center gap-1 mb-2 text-sm text-muted">
            <MapPin size={14} />
            <span>{hotel.cidade?.nome}, {hotel.cidade?.estado}</span>
          </div>
          <StarRating rating={hotel.media_avaliacoes} count={hotel.total_avaliacoes} />
          <p className="text-sm text-secondary mt-2" style={{
            display: '-webkit-box',
            WebkitLineClamp: 2,
            WebkitBoxOrient: 'vertical',
            overflow: 'hidden',
          }}>
            {hotel.descricao}
          </p>
          <div className="flex gap-1 mt-3" style={{ flexWrap: 'wrap' }}>
            {hotel.comodidades?.slice(0, 4).map((c) => (
              <span key={c.id} className="badge badge-info">{c.nome}</span>
            ))}
            {hotel.comodidades?.length > 4 && (
              <span className="badge badge-gold">+{hotel.comodidades.length - 4}</span>
            )}
          </div>
        </div>
      </div>
    </Link>
  )
}

export default function HomePage() {
  const [hoteis, setHoteis] = useState([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [filtroEstrelas, setFiltroEstrelas] = useState('')

  useEffect(() => {
    fetchHoteis()
  }, [])

  const fetchHoteis = async (searchTerm = '', estrelas = '') => {
    setLoading(true)
    try {
      const params = {}
      if (searchTerm) params.nome = searchTerm
      if (estrelas) params.estrelas = estrelas
      const response = await api.get('/hoteis', { params })
      setHoteis(response.data)
    } catch (err) {
      console.error('Erro ao buscar hoteis:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = (e) => {
    e.preventDefault()
    fetchHoteis(search, filtroEstrelas)
  }

  return (
    <>
      {/* Hero */}
      <section className="hero" id="hero-section">
        <div className="hero-content">
          <h1>Encontre seu hotel perfeito</h1>
          <p>
            Descubra as melhores opções de hospedagem pelo Brasil com tarifas exclusivas e serviços premium.
          </p>
          <form onSubmit={handleSearch} className="search-bar">
            <div style={{ position: 'relative', flex: 1 }}>
              <Search size={18} style={{
                position: 'absolute', left: 12, top: '50%', transform: 'translateY(-50%)',
                color: 'var(--color-text-muted)',
              }} />
              <input
                type="text"
                className="form-input w-full"
                style={{ paddingLeft: 40 }}
                placeholder="Buscar por nome do hotel..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                id="search-input"
              />
            </div>
            <select
              className="form-input form-select"
              value={filtroEstrelas}
              onChange={(e) => setFiltroEstrelas(e.target.value)}
              style={{ maxWidth: 160 }}
              id="filter-stars"
            >
              <option value="">Estrelas</option>
              <option value="3">3+ estrelas</option>
              <option value="4">4+ estrelas</option>
              <option value="5">5 estrelas</option>
            </select>
            <button type="submit" className="btn btn-primary" id="search-btn">
              <Search size={16} />
              Buscar
            </button>
          </form>
        </div>
      </section>

      {/* Listagem */}
      <section className="page-wrapper">
        <div className="container">
          <div className="flex justify-between items-center mb-6">
            <h2 style={{ fontSize: 'var(--text-2xl)' }}>
              {hoteis.length > 0 ? `${hoteis.length} hotéis encontrados` : 'Nenhum hotel encontrado'}
            </h2>
          </div>

          {loading ? (
            <div className="loading-overlay">
              <div className="spinner" />
              <p>Buscando hotéis...</p>
            </div>
          ) : (
            <div className="grid-3">
              {hoteis.map((hotel) => (
                <HotelCard key={hotel.id} hotel={hotel} />
              ))}
            </div>
          )}
        </div>
      </section>
    </>
  )
}

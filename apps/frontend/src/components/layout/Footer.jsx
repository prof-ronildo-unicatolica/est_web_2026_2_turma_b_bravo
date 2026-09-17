/**
 * Footer — Rodapé do StayFlow.
 */

import { Building2, Mail, Phone, MapPin } from 'lucide-react'
import { Link } from 'react-router-dom'

export default function Footer() {
  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-grid">
          <div>
            <div className="flex items-center gap-2 mb-4">
              <Building2 size={24} style={{ color: 'var(--color-secondary-light)' }} />
              <h4 style={{ marginBottom: 0 }}>StayFlow</h4>
            </div>
            <p className="text-sm" style={{ maxWidth: 300 }}>
              Sistema de Gestão de Rede Hoteleira. Encontre o hotel perfeito para
              a sua próxima viagem com as melhores tarifas e serviços.
            </p>
          </div>
          <div>
            <h4>Navegação</h4>
            <ul>
              <li><Link to="/">Hotéis</Link></li>
              <li><Link to="/login">Login</Link></li>
              <li><Link to="/register">Cadastro</Link></li>
            </ul>
          </div>
          <div>
            <h4>Suporte</h4>
            <ul>
              <li><a href="#">Central de Ajuda</a></li>
              <li><a href="#">Termos de Uso</a></li>
              <li><a href="#">Política de Privacidade</a></li>
            </ul>
          </div>
          <div>
            <h4>Contato</h4>
            <ul>
              <li className="flex items-center gap-2">
                <Mail size={14} /> contato@stayflow.com.br
              </li>
              <li className="flex items-center gap-2">
                <Phone size={14} /> (85) 3333-0000
              </li>
              <li className="flex items-center gap-2">
                <MapPin size={14} /> Quixadá, CE
              </li>
            </ul>
          </div>
        </div>
        <div className="footer-bottom">
          <p>&copy; {new Date().getFullYear()} StayFlow — Estágio Supervisionado II. Equipe Bravo.</p>
        </div>
      </div>
    </footer>
  )
}

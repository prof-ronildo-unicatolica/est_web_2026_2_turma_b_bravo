/**
 * AdminDashboard — Painel administrativo do StayFlow.
 *
 * Cada seção (cidades, hotéis, quartos e auditoria) vive em seu próprio
 * componente em `components/admin/`; esta página só monta os indicadores
 * e a ordem das seções.
 */

import { useEffect, useState } from 'react'
import { Activity, Bed, Building2, MapPin } from 'lucide-react'
import api from '../../services/api'
import AdminSection from '../../components/admin/AdminSection'
import StatCard from '../../components/admin/StatCard'
import CidadesAdmin from '../../components/admin/CidadesAdmin'
import HoteisAdmin from '../../components/admin/HoteisAdmin'
import QuartosAdmin from '../../components/admin/QuartosAdmin'
import AuditLogsAdmin from '../../components/admin/AuditLogsAdmin'

const STATS_INICIAIS = { cidades: 0, hoteis: 0, quartos: 0 }

async function contarRegistros() {
  const [cidades, hoteis, quartos] = await Promise.all([
    api.get('/admin/cidades'),
    api.get('/admin/hoteis'),
    api.get('/admin/quartos'),
  ])
  return { cidades: cidades.data.length, hoteis: hoteis.data.length, quartos: quartos.data.length }
}

export default function AdminDashboard() {
  const [stats, setStats] = useState(STATS_INICIAIS)

  useEffect(() => {
    contarRegistros()
      .then(setStats)
      .catch((err) => console.error('Erro ao buscar stats:', err))
  }, [])

  return (
    <div className="page-wrapper">
      <div className="container">
        <h1 className="mb-6" style={{ fontFamily: 'var(--font-display)', fontSize: 'var(--text-3xl)' }}>
          Painel Administrativo
        </h1>

        <div className="grid-3 mb-8">
          <StatCard icon={MapPin} valor={stats.cidades} label="Cidades" />
          <StatCard icon={Building2} valor={stats.hoteis} label="Hotéis" />
          <StatCard icon={Bed} valor={stats.quartos} label="Quartos" />
        </div>

        <AdminSection title="Cidades" icon={MapPin}>
          <CidadesAdmin />
        </AdminSection>

        <AdminSection title="Hotéis" icon={Building2}>
          <HoteisAdmin />
        </AdminSection>

        <AdminSection title="Quartos" icon={Bed}>
          <QuartosAdmin />
        </AdminSection>

        <AdminSection title="Auditoria NoSQL (MongoDB & RabbitMQ)" icon={Activity}>
          <AuditLogsAdmin />
        </AdminSection>
      </div>
    </div>
  )
}

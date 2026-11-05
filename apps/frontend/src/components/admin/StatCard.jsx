/**
 * StatCard — Card de indicador numérico do painel administrativo.
 */

export default function StatCard({ icon: Icon, valor, label }) {
  return (
    <div className="card">
      <div className="card-body text-center">
        <Icon size={32} className="text-primary" style={{ margin: '0 auto' }} />
        <div className="text-3xl font-bold mt-2" style={{ fontFamily: 'var(--font-display)' }}>
          {valor}
        </div>
        <span className="text-sm text-muted">{label}</span>
      </div>
    </div>
  )
}

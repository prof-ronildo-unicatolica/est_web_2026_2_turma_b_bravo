/**
 * AuditLogsAdmin — Visualizador dos eventos de auditoria persistidos no MongoDB.
 */

import { useCallback, useEffect, useState } from 'react'
import api from '../../services/api'

const LIMITE = 50

/** Os documentos chegam sem _id: a chave da linha é fixada uma vez, ao carregar. */
function comChaveEstavel(logs) {
  return logs.map((log, posicao) => ({ chave: `${log.timestamp ?? 'log'}-${posicao}`, dados: log }))
}

function formatarTimestamp(timestamp) {
  return timestamp ? new Date(timestamp).toLocaleString('pt-BR') : '-'
}

function LinhaLog({ log }) {
  return (
    <tr>
      <td>
        <span className="badge badge-primary">{log.evento || 'log'}</span>
      </td>
      <td>
        <code style={{ fontSize: '0.8rem', background: 'var(--surface-color)', padding: '2px 6px', borderRadius: '4px' }}>
          {JSON.stringify(log, null, 1)}
        </code>
      </td>
      <td className="text-sm text-muted whitespace-nowrap">{formatarTimestamp(log.timestamp)}</td>
    </tr>
  )
}

export default function AuditLogsAdmin() {
  const [logs, setLogs] = useState([])
  const [loading, setLoading] = useState(false)

  const fetchLogs = useCallback(async () => {
    setLoading(true)
    try {
      const res = await api.get(`/admin/logs?limite=${LIMITE}`)
      setLogs(comChaveEstavel(res.data))
    } catch {
      setLogs([])
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchLogs()
  }, [fetchLogs])

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <span className="text-sm text-muted">
          Exibindo os últimos {LIMITE} eventos capturados pelo RabbitMQ e persistidos no MongoDB
        </span>
        <button type="button" className="btn btn-outline btn-sm" onClick={fetchLogs} disabled={loading}>
          {loading ? 'Atualizando...' : 'Atualizar Logs'}
        </button>
      </div>

      {logs.length === 0 ? (
        <div className="text-center py-6 text-muted">Nenhum evento de auditoria registrado ainda.</div>
      ) : (
        <div style={{ maxHeight: '350px', overflowY: 'auto' }}>
          <table className="table">
            <thead>
              <tr>
                <th>Evento</th>
                <th>Detalhes / Payload</th>
                <th>Timestamp UTC</th>
              </tr>
            </thead>
            <tbody>
              {logs.map(({ chave, dados }) => (
                <LinhaLog key={chave} log={dados} />
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}

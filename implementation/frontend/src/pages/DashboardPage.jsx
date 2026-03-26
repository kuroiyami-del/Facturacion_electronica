import { useQuery } from '@tanstack/react-query'
import { FileText, Users, Package, DollarSign, TrendingUp, Clock } from 'lucide-react'
import { facturasApi, clientesApi, productosApi } from '../api/client'
import { formatCOP, formatDate, estadoBadgeClass } from '../utils/formatters'

export default function DashboardPage() {
  const today = new Date().toISOString().slice(0, 10)
  const firstDay = new Date(new Date().getFullYear(), new Date().getMonth(), 1).toISOString().slice(0, 10)

  const { data: facturas = [] } = useQuery({
    queryKey: ['facturas'],
    queryFn: () => facturasApi.list().then(r => r.data),
  })

  const { data: clientes = [] } = useQuery({
    queryKey: ['clientes'],
    queryFn: () => clientesApi.list().then(r => r.data),
  })

  const { data: productos = [] } = useQuery({
    queryKey: ['productos'],
    queryFn: () => productosApi.list().then(r => r.data),
  })

  const totalVentas = facturas
    .filter(f => f.estado !== 'ANULADA')
    .reduce((acc, f) => acc + parseFloat(f.total || 0), 0)

  const facturasEmitidas = facturas.filter(f => ['EMITIDA', 'VALIDADA_DIAN'].includes(f.estado)).length
  const recientes = [...facturas].sort((a, b) => new Date(b.created_at) - new Date(a.created_at)).slice(0, 8)

  return (
    <div>
      <div className="page-header">
        <div>
          <h2 className="page-title">Dashboard</h2>
          <p className="page-subtitle">Resumen general del sistema de facturación</p>
        </div>
      </div>

      {/* Stats */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon blue"><FileText size={20} /></div>
          <div>
            <div className="stat-value">{facturas.length}</div>
            <div className="stat-label">Total Facturas</div>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon green"><DollarSign size={20} /></div>
          <div>
            <div className="stat-value">{formatCOP(totalVentas)}</div>
            <div className="stat-label">Total Ventas</div>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon yellow"><Users size={20} /></div>
          <div>
            <div className="stat-value">{clientes.length}</div>
            <div className="stat-label">Clientes Activos</div>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon blue"><Package size={20} /></div>
          <div>
            <div className="stat-value">{productos.length}</div>
            <div className="stat-label">Productos</div>
          </div>
        </div>
      </div>

      {/* Recent invoices */}
      <div className="card">
        <div className="card-header">
          <span className="card-title">Facturas Recientes</span>
          <span style={{ fontSize: 12, color: 'var(--gray-400)' }}>Últimas 8 facturas</span>
        </div>
        <div className="table-wrapper">
          {recientes.length === 0 ? (
            <div className="empty-state">
              <FileText size={40} />
              <p>No hay facturas registradas aún.</p>
            </div>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>Número</th>
                  <th>Cliente</th>
                  <th>Tipo</th>
                  <th>Fecha</th>
                  <th>Total</th>
                  <th>Estado</th>
                </tr>
              </thead>
              <tbody>
                {recientes.map(f => (
                  <tr key={f.id}>
                    <td className="font-mono font-bold">{f.numero_factura}</td>
                    <td>{f.cliente?.nombre ?? '—'}</td>
                    <td><span style={{ fontSize: 12, color: 'var(--gray-400)' }}>{f.tipo_factura}</span></td>
                    <td>{formatDate(f.fecha_emision)}</td>
                    <td className="font-bold">{formatCOP(f.total)}</td>
                    <td>
                      <span className={`badge ${estadoBadgeClass(f.estado)}`}>{f.estado}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  )
}
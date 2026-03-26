import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import toast from 'react-hot-toast'
import { PlusCircle, Eye, Send, XCircle, X, CheckCircle2 } from 'lucide-react'
import { facturasApi } from '../api/client'
import { formatCOP, formatDate, estadoBadgeClass } from '../utils/formatters'

// ── Detail Modal ─────────────────────────────────────────────────────────────

function FacturaDetailModal({ factura, onClose, onEmitir, onAnular }) {
  const [motivoAnular, setMotivoAnular] = useState('')
  const [showAnular, setShowAnular]     = useState(false)

  return (
    <div className="modal-overlay" onClick={e => e.target === e.currentTarget && onClose()}>
      <div className="modal modal-lg">
        <div className="modal-header">
          <div>
            <h3 className="modal-title">Factura {factura.numero_factura}</h3>
            <span className={`badge ${estadoBadgeClass(factura.estado)}`} style={{ marginTop: 4 }}>
              {factura.estado}
            </span>
          </div>
          <button className="btn btn-ghost btn-sm" onClick={onClose}><X size={16} /></button>
        </div>

        <div className="modal-body">
          {/* Client info */}
          <div className="form-grid-2" style={{ marginBottom: 16 }}>
            <div>
              <p className="text-sm text-muted">Cliente</p>
              <p className="font-bold">{factura.cliente?.nombre ?? '—'}</p>
              <p className="text-sm text-muted">{factura.cliente?.numero_documento}</p>
            </div>
            <div>
              <p className="text-sm text-muted">Fecha Emisión</p>
              <p className="font-bold">{formatDate(factura.fecha_emision)}</p>
              {factura.cufe && (
                <p className="text-sm text-muted font-mono" style={{ wordBreak: 'break-all', marginTop: 4 }}>
                  CUFE: {factura.cufe.slice(0, 32)}...
                </p>
              )}
            </div>
          </div>

          {/* Items table */}
          <div className="table-wrapper" style={{ marginBottom: 16 }}>
            <table>
              <thead>
                <tr>
                  <th>Producto</th>
                  <th className="text-right">Cant.</th>
                  <th className="text-right">Precio Unit.</th>
                  <th className="text-right">Desc.</th>
                  <th className="text-right">Subtotal</th>
                  <th className="text-right">IVA</th>
                  <th className="text-right">Total Línea</th>
                </tr>
              </thead>
              <tbody>
                {factura.detalles?.map(d => (
                  <tr key={d.id}>
                    <td>{d.producto?.nombre ?? `Prod #${d.producto_id}`}</td>
                    <td className="text-right">{d.cantidad}</td>
                    <td className="text-right">{formatCOP(d.precio_unitario)}</td>
                    <td className="text-right">{d.porcentaje_descuento}%</td>
                    <td className="text-right">{formatCOP(d.subtotal)}</td>
                    <td className="text-right">{formatCOP(d.valor_iva)}</td>
                    <td className="text-right font-bold">{formatCOP(d.total_linea)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Totals */}
          <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
            <div className="totals-box">
              <div className="totals-row"><span>Subtotal:</span><span>{formatCOP(factura.subtotal)}</span></div>
              <div className="totals-row"><span>Descuento:</span><span>- {formatCOP(factura.descuento_total)}</span></div>
              <div className="totals-row"><span>Base Gravable:</span><span>{formatCOP(factura.base_gravable)}</span></div>
              <div className="totals-row"><span>IVA:</span><span>{formatCOP(factura.iva_total)}</span></div>
              {parseFloat(factura.retencion_total) > 0 && (
                <div className="totals-row" style={{ color: 'var(--danger)' }}>
                  <span>Retención:</span><span>- {formatCOP(factura.retencion_total)}</span>
                </div>
              )}
              <div className="totals-row total"><span>TOTAL:</span><span>{formatCOP(factura.total)}</span></div>
            </div>
          </div>

          {/* DIAN response */}
          {factura.respuesta_dian && (
            <div style={{ marginTop: 12, padding: '10px 14px', borderRadius: 6,
              background: factura.validada_dian ? 'var(--success-light)' : 'var(--danger-light)',
              color: factura.validada_dian ? 'var(--success)' : 'var(--danger)',
              fontSize: 13 }}>
              <strong>{factura.validada_dian ? '✓ DIAN:' : '✗ DIAN:'}</strong> {factura.respuesta_dian}
            </div>
          )}

          {/* Anular form */}
          {showAnular && (
            <div style={{ marginTop: 16, padding: 14, background: 'var(--danger-light)', borderRadius: 8 }}>
              <p style={{ fontSize: 13, fontWeight: 600, color: 'var(--danger)', marginBottom: 8 }}>
                Ingrese el motivo de anulación:
              </p>
              <input className="form-control" placeholder="Motivo de anulación..."
                value={motivoAnular} onChange={e => setMotivoAnular(e.target.value)} />
              <div className="flex gap-2" style={{ marginTop: 8 }}>
                <button className="btn btn-danger btn-sm" onClick={() => motivoAnular && onAnular(motivoAnular)}>
                  Confirmar Anulación
                </button>
                <button className="btn btn-outline btn-sm" onClick={() => setShowAnular(false)}>
                  Cancelar
                </button>
              </div>
            </div>
          )}
        </div>

        <div className="modal-footer">
          {factura.estado === 'BORRADOR' && (
            <button className="btn btn-success" onClick={onEmitir}>
              <Send size={14} /> Emitir Factura
            </button>
          )}
          {!['ANULADA', 'BORRADOR'].includes(factura.estado) && !showAnular && (
            <button className="btn btn-danger" onClick={() => setShowAnular(true)}>
              <XCircle size={14} /> Anular
            </button>
          )}
          <button className="btn btn-outline" onClick={onClose}>Cerrar</button>
        </div>
      </div>
    </div>
  )
}

// ── Page ─────────────────────────────────────────────────────────────────────

export default function FacturasPage() {
  const navigate = useNavigate()
  const qc = useQueryClient()
  const [selected, setSelected] = useState(null)

  const { data: facturas = [], isLoading } = useQuery({
    queryKey: ['facturas'],
    queryFn: () => facturasApi.list().then(r => r.data),
  })

  const { data: detalle } = useQuery({
    queryKey: ['factura', selected?.id],
    queryFn: () => facturasApi.get(selected.id).then(r => r.data),
    enabled: !!selected,
  })

  const emitirMutation = useMutation({
    mutationFn: (id) => facturasApi.emitir(id),
    onSuccess: () => {
      qc.invalidateQueries(['facturas'])
      qc.invalidateQueries(['factura', selected?.id])
      toast.success('Factura emitida y enviada a la DIAN')
      setSelected(null)
    },
    onError: (e) => toast.error(e.response?.data?.detail || 'Error al emitir'),
  })

  const anularMutation = useMutation({
    mutationFn: ({ id, motivo }) => facturasApi.anular(id, { motivo }),
    onSuccess: () => {
      qc.invalidateQueries(['facturas'])
      toast.success('Factura anulada')
      setSelected(null)
    },
    onError: (e) => toast.error(e.response?.data?.detail || 'Error al anular'),
  })

  return (
    <div>
      <div className="page-header">
        <div>
          <h2 className="page-title">Facturas Electrónicas</h2>
          <p className="page-subtitle">{facturas.length} facturas registradas</p>
        </div>
        <button className="btn btn-primary" onClick={() => navigate('/facturas/nueva')}>
          <PlusCircle size={15} /> Nueva Factura
        </button>
      </div>

      <div className="card">
        <div className="card-header">
          <span className="card-title">Historial de Facturas</span>
        </div>
        <div className="table-wrapper">
          {isLoading ? (
            <div className="empty-state"><div className="spinner" style={{ borderTopColor: 'var(--primary)', borderColor: 'var(--gray-200)' }} /></div>
          ) : facturas.length === 0 ? (
            <div className="empty-state"><p>No hay facturas. Crea la primera.</p></div>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>Número</th>
                  <th>Cliente</th>
                  <th>Tipo</th>
                  <th>Fecha</th>
                  <th className="text-right">Subtotal</th>
                  <th className="text-right">IVA</th>
                  <th className="text-right">Total</th>
                  <th>Estado</th>
                  <th>DIAN</th>
                  <th>Ver</th>
                </tr>
              </thead>
              <tbody>
                {facturas.map(f => (
                  <tr key={f.id}>
                    <td className="font-mono font-bold">{f.numero_factura}</td>
                    <td>{f.cliente?.nombre ?? '—'}</td>
                    <td><span className="badge badge-gray text-sm">{f.tipo_factura}</span></td>
                    <td className="text-muted">{formatDate(f.fecha_emision)}</td>
                    <td className="text-right">{formatCOP(f.subtotal)}</td>
                    <td className="text-right">{formatCOP(f.iva_total)}</td>
                    <td className="text-right font-bold">{formatCOP(f.total)}</td>
                    <td><span className={`badge ${estadoBadgeClass(f.estado)}`}>{f.estado}</span></td>
                    <td>
                      {f.validada_dian
                        ? <CheckCircle2 size={16} color="var(--success)" />
                        : <span className="text-muted text-sm">—</span>}
                    </td>
                    <td>
                      <button className="btn btn-ghost btn-sm" onClick={() => setSelected(f)}>
                        <Eye size={14} />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>

      {selected && detalle && (
        <FacturaDetailModal
          factura={detalle}
          onClose={() => setSelected(null)}
          onEmitir={() => emitirMutation.mutate(selected.id)}
          onAnular={(motivo) => anularMutation.mutate({ id: selected.id, motivo })}
        />
      )}
    </div>
  )
}
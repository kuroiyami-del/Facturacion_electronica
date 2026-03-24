import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useForm, useFieldArray } from 'react-hook-form'
import toast from 'react-hot-toast'
import { Plus, Trash2, ArrowLeft, Save } from 'lucide-react'
import { facturasApi, clientesApi, productosApi } from '../api/client'
import { formatCOP } from '../utils/formatters'

const TIPOS_FACTURA = [
  { value: 'ESTANDAR',      label: 'Estándar (IVA 19%)' },
  { value: 'CON_DESCUENTO', label: 'Con Descuento Global' },
  { value: 'CON_RETENCION', label: 'Con Retención en la Fuente' },
  { value: 'EXPORTACION',   label: 'Exportación (IVA 0%)' },
]

export default function NuevaFacturaPage() {
  const navigate = useNavigate()
  const qc = useQueryClient()

  const { data: clientes = [] } = useQuery({
    queryKey: ['clientes'],
    queryFn: () => clientesApi.list().then(r => r.data),
  })

  const { data: productos = [] } = useQuery({
    queryKey: ['productos'],
    queryFn: () => productosApi.list().then(r => r.data),
  })

  const { register, handleSubmit, watch, control, setValue, formState: { errors } } = useForm({
    defaultValues: {
      cliente_id: '',
      tipo_factura: 'ESTANDAR',
      porcentaje_descuento: 0,
      notas: '',
      detalles: [{ producto_id: '', cantidad: 1, precio_unitario: 0, porcentaje_descuento: 0, porcentaje_iva: 19 }],
    },
  })

  const { fields, append, remove } = useFieldArray({ control, name: 'detalles' })

  const watchDetalles = watch('detalles')
  const watchTipo = watch('tipo_factura')
  const watchDescGlobal = parseFloat(watch('porcentaje_descuento') || 0)

  // Auto-fill price and IVA when product is selected
  const handleProductoChange = (index, productoId) => {
    const prod = productos.find(p => String(p.id) === String(productoId))
    if (prod) {
      setValue(`detalles.${index}.precio_unitario`, prod.precio_unitario)
      setValue(`detalles.${index}.porcentaje_iva`, prod.porcentaje_iva)
    }
  }

  // Calculate totals
  const calcTotals = () => {
    let subtotal = 0, descTotal = 0, ivaTotal = 0

    watchDetalles.forEach(d => {
      const cant  = parseFloat(d.cantidad)       || 0
      const precio= parseFloat(d.precio_unitario)|| 0
      const descP = parseFloat(d.porcentaje_descuento) || 0
      const ivaP  = parseFloat(d.porcentaje_iva) || 0

      const brutLine  = cant * precio
      const descLine  = brutLine * descP / 100
      const netLine   = brutLine - descLine
      const ivaLine   = netLine * ivaP / 100

      subtotal  += netLine
      descTotal += descLine
      ivaTotal  += (watchTipo === 'EXPORTACION' ? 0 : ivaLine)
    })

    let descGlobalVal = 0
    if (watchTipo === 'CON_DESCUENTO') {
      descGlobalVal = subtotal * watchDescGlobal / 100
    }

    const baseGravable = subtotal - descGlobalVal
    const ivaFinal = watchTipo === 'EXPORTACION' ? 0 : baseGravable * 0.19
    const retencion = watchTipo === 'CON_RETENCION' ? baseGravable * 0.035 : 0
    const total = baseGravable + ivaFinal - retencion

    return { subtotal, descTotal: descTotal + descGlobalVal, baseGravable, ivaTotal: ivaFinal, retencion, total }
  }

  const totals = calcTotals()

  const createMutation = useMutation({
    mutationFn: (data) => facturasApi.create(data),
    onSuccess: (res) => {
      qc.invalidateQueries(['facturas'])
      toast.success(`Factura ${res.data.numero_factura} creada en borrador`)
      navigate('/facturas')
    },
    onError: (e) => toast.error(e.response?.data?.detail || 'Error al crear factura'),
  })

  const onSubmit = (formData) => {
    const payload = {
      cliente_id: parseInt(formData.cliente_id),
      tipo_factura: formData.tipo_factura,
      porcentaje_descuento: formData.tipo_factura === 'CON_DESCUENTO' ? parseFloat(formData.porcentaje_descuento) : null,
      notas: formData.notas || null,
      detalles: formData.detalles.map(d => ({
        producto_id: parseInt(d.producto_id),
        cantidad: parseFloat(d.cantidad),
        precio_unitario: parseFloat(d.precio_unitario),
        porcentaje_descuento: parseFloat(d.porcentaje_descuento) || 0,
        porcentaje_iva: parseFloat(d.porcentaje_iva) || 0,
      })),
    }
    createMutation.mutate(payload)
  }

  return (
    <div>
      <div className="page-header">
        <div>
          <button className="btn btn-ghost btn-sm" onClick={() => navigate('/facturas')}
            style={{ marginBottom: 8 }}>
            <ArrowLeft size={14} /> Volver
          </button>
          <h2 className="page-title">Nueva Factura Electrónica</h2>
          <p className="page-subtitle">Completa los datos para generar la factura</p>
        </div>
      </div>

      <form onSubmit={handleSubmit(onSubmit)}>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 320px', gap: 20, alignItems: 'start' }}>

          {/* ── Left column ───────────────────────────── */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>

            {/* Client & type */}
            <div className="card">
              <div className="card-header"><span className="card-title">Información General</span></div>
              <div className="card-body">
                <div className="form-grid-2">
                  <div className="form-group">
                    <label className="form-label">Cliente *</label>
                    <select className={`form-control ${errors.cliente_id ? 'error' : ''}`}
                      {...register('cliente_id', { required: 'Seleccione un cliente' })}>
                      <option value="">— Seleccionar cliente —</option>
                      {clientes.map(c => (
                        <option key={c.id} value={c.id}>
                          {c.nombre} ({c.numero_documento})
                        </option>
                      ))}
                    </select>
                    {errors.cliente_id && <p className="form-error">{errors.cliente_id.message}</p>}
                  </div>

                  <div className="form-group">
                    <label className="form-label">Tipo de Factura</label>
                    <select className="form-control" {...register('tipo_factura')}>
                      {TIPOS_FACTURA.map(t => (
                        <option key={t.value} value={t.value}>{t.label}</option>
                      ))}
                    </select>
                  </div>
                </div>

                {watchTipo === 'CON_DESCUENTO' && (
                  <div className="form-group" style={{ maxWidth: 200 }}>
                    <label className="form-label">% Descuento Global</label>
                    <input type="number" step="0.1" min="0" max="100" className="form-control"
                      {...register('porcentaje_descuento')} />
                  </div>
                )}

                <div className="form-group" style={{ marginBottom: 0 }}>
                  <label className="form-label">Notas / Observaciones</label>
                  <input className="form-control" placeholder="Observaciones opcionales..."
                    {...register('notas')} />
                </div>
              </div>
            </div>

            {/* Products */}
            <div className="card">
              <div className="card-header">
                <span className="card-title">Productos / Servicios</span>
                <button type="button" className="btn btn-outline btn-sm"
                  onClick={() => append({ producto_id: '', cantidad: 1, precio_unitario: 0, porcentaje_descuento: 0, porcentaje_iva: 19 })}>
                  <Plus size={14} /> Agregar Línea
                </button>
              </div>
              <div className="table-wrapper">
                <table>
                  <thead>
                    <tr>
                      <th style={{ minWidth: 200 }}>Producto</th>
                      <th style={{ width: 80 }}>Cantidad</th>
                      <th style={{ width: 130 }}>Precio Unit.</th>
                      <th style={{ width: 80 }}>% Desc.</th>
                      <th style={{ width: 80 }}>% IVA</th>
                      <th className="text-right" style={{ width: 120 }}>Total Línea</th>
                      <th style={{ width: 44 }}></th>
                    </tr>
                  </thead>
                  <tbody>
                    {fields.map((field, index) => {
                      const d = watchDetalles[index] || {}
                      const cant   = parseFloat(d.cantidad) || 0
                      const precio = parseFloat(d.precio_unitario) || 0
                      const descP  = parseFloat(d.porcentaje_descuento) || 0
                      const ivaP   = parseFloat(d.porcentaje_iva) || 0
                      const net    = cant * precio * (1 - descP / 100)
                      const iva    = watchTipo === 'EXPORTACION' ? 0 : net * ivaP / 100
                      const linea  = net + iva

                      return (
                        <tr key={field.id}>
                          <td>
                            <select className="form-control"
                              {...register(`detalles.${index}.producto_id`, { required: true })}
                              onChange={e => {
                                register(`detalles.${index}.producto_id`).onChange(e)
                                handleProductoChange(index, e.target.value)
                              }}>
                              <option value="">— Producto —</option>
                              {productos.map(p => (
                                <option key={p.id} value={p.id}>{p.nombre}</option>
                              ))}
                            </select>
                          </td>
                          <td>
                            <input type="number" step="0.001" min="0.001" className="form-control"
                              {...register(`detalles.${index}.cantidad`, { required: true, min: 0.001 })} />
                          </td>
                          <td>
                            <input type="number" step="0.01" min="0" className="form-control"
                              {...register(`detalles.${index}.precio_unitario`, { required: true })} />
                          </td>
                          <td>
                            <input type="number" step="0.1" min="0" max="100" className="form-control"
                              {...register(`detalles.${index}.porcentaje_descuento`)} />
                          </td>
                          <td>
                            <input type="number" step="0.01" min="0" className="form-control"
                              disabled={watchTipo === 'EXPORTACION'}
                              {...register(`detalles.${index}.porcentaje_iva`)} />
                          </td>
                          <td className="text-right font-bold">{formatCOP(linea)}</td>
                          <td>
                            {fields.length > 1 && (
                              <button type="button" className="btn btn-ghost btn-sm"
                                style={{ color: 'var(--danger)' }} onClick={() => remove(index)}>
                                <Trash2 size={13} />
                              </button>
                            )}
                          </td>
                        </tr>
                      )
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          {/* ── Right column: Totals ────────────────── */}
          <div>
            <div className="card" style={{ position: 'sticky', top: 76 }}>
              <div className="card-header"><span className="card-title">Resumen</span></div>
              <div className="card-body">
                <div className="totals-box" style={{ background: 'transparent', border: 'none', padding: 0 }}>
                  <div className="totals-row">
                    <span>Subtotal Neto:</span>
                    <span>{formatCOP(totals.subtotal)}</span>
                  </div>
                  {totals.descTotal > 0 && (
                    <div className="totals-row" style={{ color: 'var(--danger)' }}>
                      <span>Descuento:</span>
                      <span>- {formatCOP(totals.descTotal)}</span>
                    </div>
                  )}
                  <div className="totals-row">
                    <span>Base Gravable:</span>
                    <span>{formatCOP(totals.baseGravable)}</span>
                  </div>
                  <div className="totals-row">
                    <span>IVA:</span>
                    <span>{formatCOP(totals.ivaTotal)}</span>
                  </div>
                  {totals.retencion > 0 && (
                    <div className="totals-row" style={{ color: 'var(--warning)' }}>
                      <span>Retención Fuente:</span>
                      <span>- {formatCOP(totals.retencion)}</span>
                    </div>
                  )}
                  <div className="totals-row total">
                    <span>TOTAL:</span>
                    <span>{formatCOP(totals.total)}</span>
                  </div>
                </div>

                <div style={{ marginTop: 4, padding: '8px 10px', background: 'var(--primary-light)',
                  borderRadius: 6, fontSize: 12, color: 'var(--primary)' }}>
                  Tipo: <strong>{TIPOS_FACTURA.find(t => t.value === watchTipo)?.label}</strong>
                </div>

                <button type="submit" className="btn btn-primary w-full"
                  style={{ justifyContent: 'center', marginTop: 16 }}
                  disabled={createMutation.isPending}>
                  {createMutation.isPending
                    ? <><span className="spinner" /> Creando...</>
                    : <><Save size={15} /> Crear Factura</>}
                </button>

                <button type="button" className="btn btn-outline w-full"
                  style={{ justifyContent: 'center', marginTop: 8 }}
                  onClick={() => navigate('/facturas')}>
                  Cancelar
                </button>
              </div>
            </div>
          </div>
        </div>
      </form>
    </div>
  )
}
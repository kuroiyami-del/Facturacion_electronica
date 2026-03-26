import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useForm } from 'react-hook-form'
import toast from 'react-hot-toast'
import { PackagePlus, Search, Edit2, Trash2, X } from 'lucide-react'
import { productosApi } from '../api/client'
import { formatCOP } from '../utils/formatters'

const TIPOS_IMPUESTO = ['IVA_0', 'IVA_5', 'IVA_19', 'EXENTO', 'EXCLUIDO']

function ProductoModal({ producto, onClose, onSave }) {
  const { register, handleSubmit, formState: { errors } } = useForm({
    defaultValues: producto || { tipo_impuesto: 'IVA_19', porcentaje_iva: 19, stock: 0, unidad_medida: 'UND' },
  })

  return (
    <div className="modal-overlay" onClick={e => e.target === e.currentTarget && onClose()}>
      <div className="modal modal-md">
        <div className="modal-header">
          <h3 className="modal-title">{producto ? 'Editar Producto' : 'Nuevo Producto'}</h3>
          <button className="btn btn-ghost btn-sm" onClick={onClose}><X size={16} /></button>
        </div>
        <form onSubmit={handleSubmit(onSave)}>
          <div className="modal-body">
            <div className="form-grid-2">
              <div className="form-group">
                <label className="form-label">Código *</label>
                <input className={`form-control ${errors.codigo ? 'error' : ''}`}
                  placeholder="PROD-001"
                  {...register('codigo', { required: 'Requerido' })} />
                {errors.codigo && <p className="form-error">{errors.codigo.message}</p>}
              </div>
              <div className="form-group">
                <label className="form-label">Nombre *</label>
                <input className={`form-control ${errors.nombre ? 'error' : ''}`}
                  placeholder="Laptop Empresarial"
                  {...register('nombre', { required: 'Requerido' })} />
                {errors.nombre && <p className="form-error">{errors.nombre.message}</p>}
              </div>
            </div>

            <div className="form-group">
              <label className="form-label">Descripción</label>
              <input className="form-control" placeholder="Descripción del producto..."
                {...register('descripcion')} />
            </div>

            <div className="form-grid-2">
              <div className="form-group">
                <label className="form-label">Precio Unitario (COP) *</label>
                <input type="number" step="0.01" className={`form-control ${errors.precio_unitario ? 'error' : ''}`}
                  placeholder="150000"
                  {...register('precio_unitario', { required: 'Requerido', min: { value: 0, message: 'Mínimo 0' } })} />
                {errors.precio_unitario && <p className="form-error">{errors.precio_unitario.message}</p>}
              </div>
              <div className="form-group">
                <label className="form-label">Tipo Impuesto</label>
                <select className="form-control" {...register('tipo_impuesto')}>
                  {TIPOS_IMPUESTO.map(t => <option key={t}>{t}</option>)}
                </select>
              </div>
            </div>

            <div className="form-grid-2">
              <div className="form-group">
                <label className="form-label">% IVA</label>
                <input type="number" step="0.01" className="form-control"
                  {...register('porcentaje_iva')} />
              </div>
              <div className="form-group">
                <label className="form-label">Stock</label>
                <input type="number" className="form-control" {...register('stock')} />
              </div>
            </div>

            <div className="form-group">
              <label className="form-label">Unidad de Medida</label>
              <select className="form-control" {...register('unidad_medida')}>
                {['UND', 'KG', 'LT', 'MT', 'HR', 'SRV', 'LIC'].map(u => <option key={u}>{u}</option>)}
              </select>
            </div>
          </div>
          <div className="modal-footer">
            <button type="button" className="btn btn-outline" onClick={onClose}>Cancelar</button>
            <button type="submit" className="btn btn-primary">
              {producto ? 'Guardar Cambios' : 'Crear Producto'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default function ProductosPage() {
  const qc = useQueryClient()
  const [search, setSearch] = useState('')
  const [modal, setModal]   = useState(null)

  const { data: productos = [], isLoading } = useQuery({
    queryKey: ['productos', search],
    queryFn: () => productosApi.list({ buscar: search || undefined }).then(r => r.data),
  })

  const createMutation = useMutation({
    mutationFn: (data) => productosApi.create(data),
    onSuccess: () => { qc.invalidateQueries(['productos']); toast.success('Producto creado'); setModal(null) },
    onError: (e) => toast.error(e.response?.data?.detail || 'Error al crear'),
  })

  const updateMutation = useMutation({
    mutationFn: ({ id, data }) => productosApi.update(id, data),
    onSuccess: () => { qc.invalidateQueries(['productos']); toast.success('Producto actualizado'); setModal(null) },
    onError: (e) => toast.error(e.response?.data?.detail || 'Error al actualizar'),
  })

  const deleteMutation = useMutation({
    mutationFn: (id) => productosApi.delete(id),
    onSuccess: () => { qc.invalidateQueries(['productos']); toast.success('Producto eliminado') },
  })

  const handleSave = (formData) => {
    if (modal?.id) updateMutation.mutate({ id: modal.id, data: formData })
    else createMutation.mutate(formData)
  }

  return (
    <div>
      <div className="page-header">
        <div>
          <h2 className="page-title">Productos</h2>
          <p className="page-subtitle">{productos.length} productos en el catálogo</p>
        </div>
        <button className="btn btn-primary" onClick={() => setModal('new')}>
          <PackagePlus size={15} /> Nuevo Producto
        </button>
      </div>

      <div className="card">
        <div className="card-header">
          <span className="card-title">Catálogo de Productos</span>
          <div className="search-bar">
            <Search size={14} color="var(--gray-400)" />
            <input placeholder="Buscar por nombre..." value={search}
              onChange={e => setSearch(e.target.value)} />
          </div>
        </div>
        <div className="table-wrapper">
          {isLoading ? (
            <div className="empty-state"><div className="spinner" style={{ borderTopColor: 'var(--primary)', borderColor: 'var(--gray-200)' }} /></div>
          ) : productos.length === 0 ? (
            <div className="empty-state"><p>No se encontraron productos.</p></div>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>Código</th>
                  <th>Nombre</th>
                  <th>Precio</th>
                  <th>IVA</th>
                  <th>Stock</th>
                  <th>Unidad</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {productos.map(p => (
                  <tr key={p.id}>
                    <td className="font-mono">{p.codigo}</td>
                    <td className="font-bold">{p.nombre}</td>
                    <td className="font-bold text-success">{formatCOP(p.precio_unitario)}</td>
                    <td><span className="badge badge-primary">{p.tipo_impuesto}</span></td>
                    <td>{p.stock}</td>
                    <td className="text-muted">{p.unidad_medida}</td>
                    <td>
                      <div className="flex gap-2">
                        <button className="btn btn-ghost btn-sm" onClick={() => setModal(p)}>
                          <Edit2 size={13} />
                        </button>
                        <button className="btn btn-ghost btn-sm" style={{ color: 'var(--danger)' }}
                          onClick={() => { if (confirm('¿Eliminar producto?')) deleteMutation.mutate(p.id) }}>
                          <Trash2 size={13} />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>

      {modal && (
        <ProductoModal
          producto={modal === 'new' ? null : modal}
          onClose={() => setModal(null)}
          onSave={handleSave}
        />
      )}
    </div>
  )
}
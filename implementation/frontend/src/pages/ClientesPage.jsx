import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useForm } from 'react-hook-form'
import toast from 'react-hot-toast'
import { UserPlus, Search, Edit2, Trash2, X } from 'lucide-react'
import { clientesApi } from '../api/client'
import { formatDate } from '../utils/formatters'

// ── Modal Form ───────────────────────────────────────────────────────────────

function ClienteModal({ cliente, onClose, onSave }) {
  const { register, handleSubmit, formState: { errors } } = useForm({
    defaultValues: cliente || {},
  })

  return (
    <div className="modal-overlay" onClick={e => e.target === e.currentTarget && onClose()}>
      <div className="modal modal-md">
        <div className="modal-header">
          <h3 className="modal-title">{cliente ? 'Editar Cliente' : 'Nuevo Cliente'}</h3>
          <button className="btn btn-ghost btn-sm" onClick={onClose}><X size={16} /></button>
        </div>
        <form onSubmit={handleSubmit(onSave)}>
          <div className="modal-body">
            <div className="form-grid-2">
              <div className="form-group">
                <label className="form-label">Tipo Documento</label>
                <select className="form-control" {...register('tipo_documento', { required: true })}>
                  {['CC','NIT','CE','PA','TI'].map(t => <option key={t}>{t}</option>)}
                </select>
              </div>
              <div className="form-group">
                <label className="form-label">Número Documento *</label>
                <input className={`form-control ${errors.numero_documento ? 'error' : ''}`}
                  placeholder="12345678"
                  {...register('numero_documento', { required: 'Requerido' })} />
                {errors.numero_documento && <p className="form-error">{errors.numero_documento.message}</p>}
              </div>
            </div>

            <div className="form-grid-2">
              <div className="form-group">
                <label className="form-label">Tipo Persona</label>
                <select className="form-control" {...register('tipo_persona')}>
                  <option value="NATURAL">Natural</option>
                  <option value="JURIDICA">Jurídica</option>
                </select>
              </div>
              <div className="form-group">
                <label className="form-label">Nombre / Razón Social *</label>
                <input className={`form-control ${errors.nombre ? 'error' : ''}`}
                  placeholder="Juan Torres"
                  {...register('nombre', { required: 'Requerido' })} />
                {errors.nombre && <p className="form-error">{errors.nombre.message}</p>}
              </div>
            </div>

            <div className="form-grid-2">
              <div className="form-group">
                <label className="form-label">Email</label>
                <input type="email" className="form-control" placeholder="cliente@email.com"
                  {...register('email')} />
              </div>
              <div className="form-group">
                <label className="form-label">Teléfono</label>
                <input className="form-control" placeholder="3001234567"
                  {...register('telefono')} />
              </div>
            </div>

            <div className="form-grid-2">
              <div className="form-group">
                <label className="form-label">Ciudad</label>
                <input className="form-control" placeholder="Bogotá" {...register('ciudad')} />
              </div>
              <div className="form-group">
                <label className="form-label">Dirección</label>
                <input className="form-control" placeholder="Calle 100 # 15-20" {...register('direccion')} />
              </div>
            </div>
          </div>
          <div className="modal-footer">
            <button type="button" className="btn btn-outline" onClick={onClose}>Cancelar</button>
            <button type="submit" className="btn btn-primary">
              {cliente ? 'Guardar Cambios' : 'Crear Cliente'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

// ── Page ─────────────────────────────────────────────────────────────────────

export default function ClientesPage() {
  const qc = useQueryClient()
  const [search, setSearch] = useState('')
  const [modal, setModal]   = useState(null)  // null | 'new' | cliente object

  const { data: clientes = [], isLoading } = useQuery({
    queryKey: ['clientes', search],
    queryFn: () => clientesApi.list({ buscar: search || undefined }).then(r => r.data),
  })

  const createMutation = useMutation({
    mutationFn: (data) => clientesApi.create(data),
    onSuccess: () => { qc.invalidateQueries(['clientes']); toast.success('Cliente creado'); setModal(null) },
    onError: (e)   => toast.error(e.response?.data?.detail || 'Error al crear cliente'),
  })

  const updateMutation = useMutation({
    mutationFn: ({ id, data }) => clientesApi.update(id, data),
    onSuccess: () => { qc.invalidateQueries(['clientes']); toast.success('Cliente actualizado'); setModal(null) },
    onError: (e)   => toast.error(e.response?.data?.detail || 'Error al actualizar'),
  })

  const deleteMutation = useMutation({
    mutationFn: (id) => clientesApi.delete(id),
    onSuccess: () => { qc.invalidateQueries(['clientes']); toast.success('Cliente eliminado') },
  })

  const handleSave = (formData) => {
    if (modal?.id) {
      updateMutation.mutate({ id: modal.id, data: formData })
    } else {
      createMutation.mutate(formData)
    }
  }

  return (
    <div>
      <div className="page-header">
        <div>
          <h2 className="page-title">Clientes</h2>
          <p className="page-subtitle">{clientes.length} clientes registrados</p>
        </div>
        <button className="btn btn-primary" onClick={() => setModal('new')}>
          <UserPlus size={15} /> Nuevo Cliente
        </button>
      </div>

      <div className="card">
        <div className="card-header">
          <span className="card-title">Listado de Clientes</span>
          <div className="search-bar">
            <Search size={14} color="var(--gray-400)" />
            <input placeholder="Buscar por nombre..." value={search}
              onChange={e => setSearch(e.target.value)} />
          </div>
        </div>
        <div className="table-wrapper">
          {isLoading ? (
            <div className="empty-state"><div className="spinner" style={{ borderTopColor: 'var(--primary)', borderColor: 'var(--gray-200)' }} /></div>
          ) : clientes.length === 0 ? (
            <div className="empty-state"><p>No se encontraron clientes.</p></div>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>Documento</th>
                  <th>Nombre</th>
                  <th>Tipo</th>
                  <th>Email</th>
                  <th>Ciudad</th>
                  <th>Registro</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {clientes.map(c => (
                  <tr key={c.id}>
                    <td className="font-mono">{c.tipo_documento} {c.numero_documento}</td>
                    <td className="font-bold">{c.nombre}</td>
                    <td><span className="badge badge-gray">{c.tipo_persona}</span></td>
                    <td className="text-muted">{c.email || '—'}</td>
                    <td>{c.ciudad || '—'}</td>
                    <td className="text-muted text-sm">{formatDate(c.created_at)}</td>
                    <td>
                      <div className="flex gap-2">
                        <button className="btn btn-ghost btn-sm" onClick={() => setModal(c)} title="Editar">
                          <Edit2 size={13} />
                        </button>
                        <button className="btn btn-ghost btn-sm" style={{ color: 'var(--danger)' }}
                          onClick={() => { if (confirm('¿Eliminar cliente?')) deleteMutation.mutate(c.id) }} title="Eliminar">
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
        <ClienteModal
          cliente={modal === 'new' ? null : modal}
          onClose={() => setModal(null)}
          onSave={handleSave}
        />
      )}
    </div>
  )
}
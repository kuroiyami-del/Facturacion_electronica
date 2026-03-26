// utils/formatters.js — Funciones de formato reutilizables

export function formatCOP(value) {
  const num = parseFloat(value) || 0
  return new Intl.NumberFormat('es-CO', {
    style: 'currency',
    currency: 'COP',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(num)
}

export function formatDate(dateStr) {
  if (!dateStr) return '—'
  return new Date(dateStr + 'T00:00:00').toLocaleDateString('es-CO', {
    day: '2-digit', month: 'short', year: 'numeric',
  })
}

export function estadoBadgeClass(estado) {
  const map = {
    BORRADOR:      'badge-gray',
    EMITIDA:       'badge-primary',
    VALIDADA_DIAN: 'badge-success',
    RECHAZADA:     'badge-danger',
    ANULADA:       'badge-danger',
  }
  return map[estado] ?? 'badge-gray'
}

export function estadoPagoBadgeClass(estado) {
  const map = {
    PAGADO:   'badge-success',
    PENDIENTE:'badge-warning',
    PARCIAL:  'badge-primary',
    VENCIDO:  'badge-danger',
  }
  return map[estado] ?? 'badge-gray'
}
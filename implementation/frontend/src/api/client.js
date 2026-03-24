import axios from 'axios'

// Usar el proxy de Vite (relativo al dominio del frontend)
export const apiClient = axios.create({
  baseURL: '/api/v1',  // Esto se resuelve como http://localhost:3000/api/v1
  headers: {
    'Content-Type': 'application/json',
  },
})

// Interceptor para agregar el token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('fp_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    console.log(`📤 ${config.method?.toUpperCase()} ${config.baseURL}${config.url}`)
    return config
  },
  (error) => Promise.reject(error)
)

// Interceptor para manejar errores 401
apiClient.interceptors.response.use(
  (response) => {
    console.log(`📥 ${response.status} ${response.config.url}`)
    return response
  },
  (error) => {
    console.error('API Error:', error.response?.status, error.response?.data)
    if (error.response?.status === 401) {
      localStorage.removeItem('fp_token')
      localStorage.removeItem('fp_user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Exportar APIs específicas
export const clientesApi = {
  list: () => apiClient.get('/clientes'),
  get: (id) => apiClient.get(`/clientes/${id}`),
  create: (data) => apiClient.post('/clientes', data),
  update: (id, data) => apiClient.put(`/clientes/${id}`, data),
  delete: (id) => apiClient.delete(`/clientes/${id}`),
}

export const productosApi = {
  list: () => apiClient.get('/productos'),
  get: (id) => apiClient.get(`/productos/${id}`),
  create: (data) => apiClient.post('/productos', data),
  update: (id, data) => apiClient.put(`/productos/${id}`, data),
  delete: (id) => apiClient.delete(`/productos/${id}`),
}

export const facturasApi = {
  list: (params) => apiClient.get('/facturas', { params }),
  get: (id) => apiClient.get(`/facturas/${id}`),
  create: (data) => apiClient.post('/facturas', data),
  emitir: (id) => apiClient.post(`/facturas/${id}/emitir`),
  anular: (id, motivo) => apiClient.post(`/facturas/${id}/anular`, { motivo }),
  resumen: (params) => apiClient.get('/facturas/resumen', { params }),
}

export default apiClient
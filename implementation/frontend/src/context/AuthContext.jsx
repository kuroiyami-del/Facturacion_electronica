import { createContext, useContext, useState, useCallback } from 'react'
import { apiClient } from '../api/client'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser]   = useState(() => {
    try { return JSON.parse(localStorage.getItem('fp_user')) } catch { return null }
  })
  const [token, setToken] = useState(() => localStorage.getItem('fp_token'))

  const login = useCallback(async (email, password) => {
    const form = new URLSearchParams()
    form.append('username', email)
    form.append('password', password)

    const { data } = await apiClient.post('/auth/login', form, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    })

    const { access_token } = data
    // Decode basic JWT payload (no verify — server validates)
    const payload = JSON.parse(atob(access_token.split('.')[1]))
    const userData = { email: payload.sub, rol: payload.rol }

    localStorage.setItem('fp_token', access_token)
    localStorage.setItem('fp_user', JSON.stringify(userData))
    apiClient.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
    setToken(access_token)
    setUser(userData)
    return userData
  }, [])

  const logout = useCallback(() => {
    localStorage.removeItem('fp_token')
    localStorage.removeItem('fp_user')
    delete apiClient.defaults.headers.common['Authorization']
    setToken(null)
    setUser(null)
  }, [])

  // Restore auth header on page refresh
  if (token) {
    apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`
  }

  return (
    <AuthContext.Provider value={{ user, token, login, logout, isAuthenticated: !!token }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth debe usarse dentro de AuthProvider')
  return ctx
}
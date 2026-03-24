import { createClient } from '@supabase/supabase-js';

// Estas variables se configurarán automáticamente cuando conectes Supabase
// desde la página de configuración de Make
const supabaseUrl = import.meta.env.VITE_SUPABASE_URL || '';
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY || '';

export const supabase = createClient(supabaseUrl, supabaseAnonKey);

// Función helper para verificar si Supabase está conectado
export const isSupabaseConnected = () => {
  return !!(supabaseUrl && supabaseAnonKey);
};

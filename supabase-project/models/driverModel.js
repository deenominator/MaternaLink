import { supabase } from '../utils/supabaseClient.js'

const table = 'drivers'

export async function getAllDrivers() {
  const { data, error } = await supabase.from(table).select('*')
  return { data, error }
}

export async function getDriverById(id) {
  const { data, error } = await supabase.from(table).select('*').eq('id', id).single()
  return { data, error }
}

export async function addDriver(driver) {
  const { data, error } = await supabase.from(table).insert([driver])
  return { data, error }
}

export async function updateDriver(id, updates) {
  const { data, error } = await supabase.from(table).update(updates).eq('id', id)
  return { data, error }
}

export async function deleteDriver(id) {
  const { data, error } = await supabase.from(table).delete().eq('id', id)
  return { data, error }
}

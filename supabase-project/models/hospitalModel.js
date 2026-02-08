import { supabase } from '../utils/supabaseClient.js'

const table = 'hospital_management'

export async function getAllHospitals() {
  const { data, error } = await supabase.from(table).select('*')
  return { data, error }
}

export async function getHospitalById(id) {
  const { data, error } = await supabase.from(table).select('*').eq('id', id).single()
  return { data, error }
}

export async function addHospital(hospital) {
  const { data, error } = await supabase.from(table).insert([hospital])
  return { data, error }
}

export async function updateHospital(id, updates) {
  const { data, error } = await supabase.from(table).update(updates).eq('id', id)
  return { data, error }
}

export async function deleteHospital(id) {
  const { data, error } = await supabase.from(table).delete().eq('id', id)
  return { data, error }
}

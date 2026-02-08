import { supabase } from '../utils/supabaseClient.js'

const table = 'new_mothers'

export async function getAllNewMothers() {
  const { data, error } = await supabase.from(table).select('*')
  return { data, error }
}

export async function getNewMotherById(id) {
  const { data, error } = await supabase.from(table).select('*').eq('id', id).single()
  return { data, error }
}

export async function addNewMother(mother) {
  // mother example: { name, age, months_since_birth, contact_number }
  const { data, error } = await supabase.from(table).insert([mother])
  return { data, error }
}

export async function updateNewMother(id, updates) {
  const { data, error } = await supabase.from(table).update(updates).eq('id', id)
  return { data, error }
}

export async function deleteNewMother(id) {
  const { data, error } = await supabase.from(table).delete().eq('id', id)
  return { data, error }
}

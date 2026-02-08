import { supabase } from '../utils/supabaseClient.js'

const table = 'expecting_mothers'

export async function getAllExpectingMothers() {
  const { data, error } = await supabase.from(table).select('*')
  return { data, error }
}

export async function getExpectingMotherById(id) {
  const { data, error } = await supabase.from(table).select('*').eq('id', id).single()
  return { data, error }
}

export async function addExpectingMother(mother) {
  // mother example: { name, age, expected_due_date, contact_number }
  const { data, error } = await supabase.from(table).insert([mother])
  return { data, error }
}

export async function updateExpectingMother(id, updates) {
  const { data, error } = await supabase.from(table).update(updates).eq('id', id)
  return { data, error }
}

export async function deleteExpectingMother(id) {
  const { data, error } = await supabase.from(table).delete().eq('id', id)
  return { data, error }
}

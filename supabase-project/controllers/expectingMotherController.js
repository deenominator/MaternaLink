import * as motherModel from '../models/expectingMotherModel.js'

export async function addExpectingMother(req, res) {
  const newMother = req.body
  const { data, error } = await motherModel.addExpectingMother(newMother)
  if (error) return res.status(400).json({ error: error.message })
  res.status(201).json(data)
}


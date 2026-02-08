import * as newMotherModel from '../models/newMotherModel.js'

export async function addNewMother(req, res) {
  const newMother = req.body
  const { data, error } = await newMotherModel.addNewMother(newMother)
  if (error) return res.status(400).json({ error: error.message })
  res.status(201).json(data)
}



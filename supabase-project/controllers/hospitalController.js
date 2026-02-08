import * as hospitalModel from '../models/hospitalModel.js'


export async function addHospital(req, res) {
  const hospital = req.body
  const { data, error } = await hospitalModel.addHospital(hospital)
  if (error) return res.status(400).json({ error: error.message })
  res.status(201).json(data)
}



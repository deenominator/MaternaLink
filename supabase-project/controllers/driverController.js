import * as driverModel from '../models/driverModel.js'


export async function addDriver(req, res) {
  const driver = req.body
  const { data, error } = await driverModel.addDriver(driver)
  if (error) return res.status(400).json({ error: error.message })
  res.status(201).json(data)
}


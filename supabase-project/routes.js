import express from 'express'
import * as expectingMotherController from './controllers/expectingMotherController.js'
import * as newMotherController from './controllers/newMotherController.js'
import * as driverController from './controllers/driverController.js'
import * as hospitalController from './controllers/hospitalController.js'

const router = express.Router()

// Only add (POST) endpoints
router.post('/expecting-mothers', expectingMotherController.addExpectingMother)
router.post('/new-mothers', newMotherController.addNewMother)
router.post('/drivers', driverController.addDriver)
router.post('/hospitals', hospitalController.addHospital)

export default router

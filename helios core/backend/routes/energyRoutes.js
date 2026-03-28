const express = require("express")

const router = express.Router()

const Energy = require("../models/Energy")

router.get("/", async(req,res)=>{

const data = await Energy.find()

res.json(data)

})

router.post("/save", async(req,res)=>{

const energy = new Energy(req.body)

await energy.save()

res.json("Energy saved")

})

module.exports = router
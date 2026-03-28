const Energy = require("../models/Energy")

exports.saveEnergy = async (req,res) => {

  try{

    const energy = new Energy(req.body)

    await energy.save()

    res.json({message:"Energy data saved"})

  }catch(error){

    res.status(500).json(error)

  }

}

exports.getEnergy = async (req,res) => {

  try{

    const data = await Energy.find()

    res.json(data)

  }catch(error){

    res.status(500).json(error)

  }

}
module.exports = { saveEnergy, getEnergy }

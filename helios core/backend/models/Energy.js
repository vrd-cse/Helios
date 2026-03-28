const mongoose = require("mongoose")

const energySchema = new mongoose.Schema({

  solar: Number,
  battery: Number,
  grid: Number,
  cost: Number,
  savings: Number

})

module.exports = mongoose.model("Energy", energySchema)
const express = require("express")
const mongoose = require("mongoose")

const energyRoutes = require("./routes/energyroutes")

const app = express()

app.use(express.json())

app.get("/", (req, res) => {
  res.send("Helios Backend is Running 🚀")
})
mongoose.connect("mongodb://127.0.0.1:27017/helios")
.then(()=>console.log("MongoDB Connected"))

app.use("/api/energy", energyRoutes)

app.listen(5000,()=>{
console.log("Server running on port 5000")
})
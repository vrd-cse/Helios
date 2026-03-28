const fs = require("fs")
const csv = require("csv-parser")

fs.createReadStream("e:/Helios/helios core/backend/data/yearly_full_release_long_format.csv")
.pipe(csv())
.on("data",(row)=>{

 console.log(row)

})
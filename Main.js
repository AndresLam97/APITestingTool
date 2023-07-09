const controller = require("./Controller")
const worker = require("./Worker")

const dataDictionary = controller.validateArguments(...process.argv)
worker.verifyFiles(dataDictionary)



if (dataDictionary["-p"] === true)
{




}
else
{}
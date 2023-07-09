const fileWorker = require("fs")

let file_data = fileWorker.readFileSync("./Data.csv","utf-8");

fileWorker.readFile("./Data.csv","utf-8", function(error, file_data){
    console.log(file_data);
})


function verifyFiles(dictionary)
{
    for(const [key,value] of Object.entries(dictionary))
    {
        if (key === "-n" || key === "--numberOfRun")
        {
            try
            {

            }
            catch Error
            {}
        }
        else if (key === "-f" || key === "envFolder")
        {}
        else if (key === "-e" || key === "envFile")
        {

        }
    }
}



module.exports = {verifyFiles}

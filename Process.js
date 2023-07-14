const newman = require('newman')

const environmentFiles = process.argv[3].split(",")

for(let index = 0; index < process.argv[4];index++)
{
    for(let environmentFileIndex = 0 ; environmentFileIndex < environmentFiles.length; environmentFileIndex++)
    {
        date = new Date(Date.now())
        currentDateTime = date.getFullYear() + "-" + date.getMonth() + "-" + date.getDate() + "-" + date.getHours() + "-" + date.getMinutes() + "-" + date.getSeconds()
        exportFileName = "./report/" + environmentFiles[environmentFileIndex] + " " + currentDateTime + "-run time " + environmentFileIndex + ".html"
        console.log(exportFileName)
        newman.run(
            {
                collection: require(process.argv[2]),
                environment: require(environmentFiles[index]),
                reporters: 'htmlextra',
                reporter: {
                    htmlextra: { export: exportFileName}
                }
            }
        )
    }
}

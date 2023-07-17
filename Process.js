const newman = require('newman')

const totalArguments = process.argv.length;
var collectionFileName;
var environmentFiles;
var iterationRun;


if (totalArguments === 4)
{
    collectionFileName = process.argv[2]
    iterationRun = process.argv[3]
}
else if (totalArguments === 5)
{
    collectionFileName = process.argv[2]
    environmentFiles = process.argv[3].split(",")
    iterationRun = process.argv[4]
}
else
    throw new Error("There are not enought arguments, please retry !!!")


try
{
    if (totalArguments === 4)
    {
        console.log("Total Argument = 4")
        for(let index = 0; index < iterationRun;index++)
        {
            var fileNameList = collectionFileName.split("/")
            var fileName = fileNameList[fileNameList.length - 1].split(".")[0]
            const date = new Date(Date.now())
            var currentDateTime = date.getFullYear() + "-" + date.getMonth() + "-" + date.getDate() + "-" + date.getHours() + "-" + date.getMinutes() + "-" + date.getSeconds()
            var exportFileName = "./report/" + fileName + " " + currentDateTime + "- run time " + (index + 1) + ".html"
            newman.run(
                {
                    collection: require(collectionFileName),
                    reporters: 'htmlextra',
                        reporter: {
                            htmlextra: { export: exportFileName}
                        }
                }
            )
        }
    }
    else
    {
        for(let index = 0; index < iterationRun;index++)
        {
            for(let environmentFileIndex = 0 ; environmentFileIndex < environmentFiles.length; environmentFileIndex++)
            {
                var fileNameList = environmentFiles[environmentFileIndex].split("/")
                var fileName = fileNameList[fileNameList.length - 1].split(".")[0]
                const date = new Date(Date.now())
                var currentDateTime = date.getFullYear() + "-" + date.getMonth() + "-" + date.getDate() + "-" + date.getHours() + "-" + date.getMinutes() + "-" + date.getSeconds()
                var exportFileName = "./report/" + fileName + " " + currentDateTime + "- run time " + (index + 1) + ".html"
                newman.run(
                    {
                        collection: require(collectionFileName),
                        environment: require(environmentFiles[index]),
                        reporters: 'htmlextra',
                        reporter: {
                            htmlextra: { export: exportFileName}
                        }
                    }
                    )
            }
        }
    }
}
catch
{
    console.log("Error")
}

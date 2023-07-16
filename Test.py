for(let index = 0; index < iterationRun;index++)
{
    for(let environmentFileIndex = 0 ; environmentFileIndex < environmentFiles.length; environmentFileIndex++)
    {
        fileNameList = environmentFiles[environmentFileIndex].split("/")
        fileName = fileNameList[fileNameList.length - 1].split(".")[0]
        date = new Date(Date.now())
        currentDateTime = date.getFullYear() + "-" + date.getMonth() + "-" + date.getDate() + "-" + date.getHours() + "-" + date.getMinutes() + "-" + date.getSeconds()
        exportFileName = "./report/" + fileName + " " + currentDateTime + "-run time " + index + ".html"
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
var man = require('newman')

const runFile = 'C:/Users/KienL/OneDrive - GBST/Desktop/New Folder/Test/New Collection.postman_collection.json';
const env1File = 'C:/Users/KienL/OneDrive - GBST/Desktop/New Folder/Test/env1.json';
const env2File = 'C:/Users/KienL/OneDrive - GBST/Desktop/New Folder/Test/env2.json';
const env3File = 'C:/Users/KienL/OneDrive - GBST/Desktop/New Folder/Test/env3.json';

const envList = [env1File,env2File,env3File]

var runList = []

for(let index = 0 ; index < envList.length; index++)
{
    nameList = envList[index].split("/")
    splittedExtensionName = nameList[nameList.length - 1].split(".")
    exportFileName = "./report/" + splittedExtensionName[0] + "-" + Date.toString() + "-" + ".html"
    console.log(exportFileName)
    man.run(
                {
                    collection: require(runFile),
                    environment: require(envList[index]),
                    reporters: 'htmlextra',
                    reporter: {
                        htmlextra: { export: exportFileName}
                    }
                }
            )
}

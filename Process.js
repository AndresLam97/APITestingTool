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

}
catch
{

}

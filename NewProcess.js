const fs = require('fs');
const newman = require('newman');
const { exit } = require('process');
const prompt = require('prompt-sync')();
const ex = require('exceljs');

const columnNames = ["Collecton Name","Request Name", "Method", "Url", "Status","Code","Response Time","Reponse Size","Executed", "Failed","Skippped","Total Assertions","Executed Count","Failed Count","Skipped Count","Response Body"];
const argumentList = ["-c","--collectionFile","-e","--environmentFile","-n","--numberOfRun","-p","--parallel"];
const totalArgumentsInputted = process.argv.slice(2);
let runParallel = false;
let collectionFiles = "";
let collectionFileList = [];
let environmentFileList = [];
let environmentFiles = "";
let numberOfRun = 1;
let usableCollection = [];
let notUsableCollection = [];
let usableEnvironment = [];
let notUsableEnvironment = [];

function check_arguments()
{
    let illegalArgumentList = [];
    totalArgumentsInputted.forEach(element => {
        if(element.startsWith("-") || element.startsWith("--"))
        {
            if(argumentList.includes(element) === false)
            {
                illegalArgumentList.push(element);
            }
        }
    });
    if (illegalArgumentList.length > 0)
    {
        throw new Error("The argument(s) is/are not supportted: " + illegalArgumentList)
    }
}

function check_duplicate()
{
    let uniqueArgument = new Set(totalArgumentsInputted);
    let uniqueArgumentDict = {};
    for(const argument of uniqueArgument)
    {
        uniqueArgumentDict[argument] = 0
    };
    totalArgumentsInputted.forEach(element => 
    {
        if(uniqueArgumentDict[element] !== undefined)
        {
            uniqueArgumentDict[element] = uniqueArgumentDict[element] + 1;
        }
    });
    if(totalArgumentsInputted.includes("-c") && totalArgumentsInputted.includes("--collectionFile"))
    {
        throw new Error("The -c and --collectionFile is the same, please use only one of them !!!");
    }
    else if(totalArgumentsInputted.includes("-e") && totalArgumentsInputted.includes("--environmentFile"))
    {
        throw new Error("The -e and --environmentFile is the same, please use only one of them !!!");
    }
    else if(totalArgumentsInputted.includes("-n") && totalArgumentsInputted.includes("--numberOfRun"))
    {
        throw new Error("The -n and --numberOfRun is the same, please use only one of them !!!");
    }
    else if(totalArgumentsInputted.includes("-p") && totalArgumentsInputted.includes("--parallel"))
    {
        throw new Error("The -p and --parallel is the same, please use only one of them !!!");
    }

    Object.keys(uniqueArgumentDict).forEach(element => 
    {
        if(uniqueArgumentDict[element] > 1)
        {
            throw new Error("The " + element + " is added more than one, please only use one of this !!!");
        }
    });
}

function placing_argument_to_variable()
{
    let localTotalArgumentsInputted = totalArgumentsInputted
    if(totalArgumentsInputted.indexOf("-p") !== -1)
    {
        runParallel = true;
        localTotalArgumentsInputted = localTotalArgumentsInputted.filter(element => element !== "-p");
    }
    if(localTotalArgumentsInputted.length % 2 !== 0)
    {
        throw new Error("There is some argument is missing value, please recheck !!!");
    }
    for(let index = 0; index < localTotalArgumentsInputted.length; index = index + 2)
    {
        if(argumentList.includes(localTotalArgumentsInputted.at(index)))
        {
            if(localTotalArgumentsInputted.at(index) === "-c" || localTotalArgumentsInputted.at(index) === "--collectionFile")
            {
                collectionFiles = localTotalArgumentsInputted.at(index + 1);
            }
            else if (localTotalArgumentsInputted.at(index) === "-e" || localTotalArgumentsInputted.at(index) === "--environmentFile")
            {
                environmentFiles = localTotalArgumentsInputted.at(index + 1);
            }
            else if (localTotalArgumentsInputted.at(index) === "-n" || localTotalArgumentsInputted.at(index) === "--numberOfRun")
            {
                const number = parseInt(localTotalArgumentsInputted.at(index + 1))
                if (number === 0)
                {
                    throw new Error("The value of the -n or --numberOfRun must be greater than 0, please recheck !!!")
                }
                if (Number.isNaN(number))
                {
                    throw new Error("The value of the -n or --numberOfRun must be a number, please recheck !!!")
                }
                numberOfRun = number;
            }
        }
        else
        {
            throw new Error("There is some value placed in the wrong position, please recheck !!!")
        }
    }
}

function splitting_collection_and_environment()
{
    collectionFileList = collectionFiles.split(",");
    environmentFileList = environmentFiles.split(",");
    collectionFileList = collectionFileList.filter(element => element !== '');
    environmentFileList = environmentFileList.filter(element => element !== '');
}

function check_valid_of_collection_and_environment()
{
    for(const collection of collectionFileList)
    {
        if (fs.existsSync(collection) && collection.endsWith('.postman_collection.json'))
        {
            usableCollection.push(collection);
        }
        else
        {
            notUsableCollection.push(collection);
        }
    }
    for(const environment of environmentFileList)
    {
        if (fs.existsSync(environment) && environment.endsWith('.postman_environment.json'))
        {
            usableEnvironment.push(environment);
        }
        else
        {
            notUsableEnvironment.push(environment);
        }
    }
    if(usableCollection.length === 0)
    {
        throw new Error("Must be at least one collection is usable, please recheck !!!");
    }
    if(notUsableCollection.length > 0 || notUsableEnvironment > 0)
    {
        console.log("These following file(s) will not be run in the process:");
        if(notUsableCollection.length > 0)
        {
            console.log("Collection file(s):");
            for(const notUsableCollectionFile of notUsableCollection)
            {
                console.log(notUsableCollectionFile);
            }
        }
        if(notUsableEnvironment.length > 0)
        {
            console.log("Environment file(s):");
            for(const notUsableEnvironmentFile of notUsableEnvironment)
            {
                console.log(notUsableEnvironmentFile);
            }
        }
        let confirmValue;
        do
        {   
            if(confirmValue === 'Y' || confirmValue === 'y' || confirmValue === 'N' || confirmValue === 'n')
            {
                break;
            }
            if(confirmValue !== undefined)
            {
                console.log("Please input Y and N only (lower case is allowed) !!!");
            }
            confirmValue = prompt("Please confirm to run the process (Y/N): ");
        }while(true);
        if(confirmValue === 'N' || confirmValue === 'n')
        {
            process.exit();
        }
    }
}

function export_file_name_generate(collectionFile,runTime,environmentFile)
{
    var collectionNameList = collectionFile.split("/");
    var collectionName = collectionNameList[collectionNameList.length - 1].split(".")[0];
    const date = new Date(Date.now());
    var currentDateTime = date.getFullYear() + "-" + date.getMonth() + "-" + date.getDate() + "-" + date.getHours() + "-" + date.getMinutes() + "-" + date.getSeconds();
    if(environmentFile !== undefined)
    {
        var environmentNameList = environmentFile.split("/");
        var environmentName = environmentNameList[environmentNameList.length - 1].split(".")[0];
        var exportFileName = "./report/" + collectionName + "-" + environmentName + "-" + currentDateTime + "-run time " + (runTime + 1) + ".csv";
    }
    else
    {
        var exportFileName = "./report/" + collectionName + "-" + currentDateTime + "- run time " + (runTime + 1) + ".csv";
    }
    return exportFileName;
}

function beautify_column_header(fileName)
{
    var wb = new ex.Workbook();
    wb.csv.readFile(fileName).then(() => {
        const ws = wb.getWorksheet();

        // Remove the first column
        ws.spliceColumns(1,1);
        
        // Rename all the headers
        let firstRow = ws.getRow(1);
        for(let index = 1; index <= firstRow.cellCount; index++)
        {
            firstRow.getCell(index).value = columnNames[index - 1];
        }
        wb.csv.writeFile(fileName);
    }).catch(err => {
            console.log(err.message);
    });
}

function run_request_parallel_process()
{
    for(let index = 0; index < numberOfRun; index++)
    {
            console.log(index)
    }
}

function run_request_concurrent_process()
{
    if (usableEnvironment.length > 0)
    {
        for(let index = 0; index < numberOfRun; index++)
        {
            for(const collectionPath of usableCollection)
            {
                for(const environmentPath of usableEnvironment)
                {
                    var exportFileName = export_file_name_generate(collectionPath,index,environmentPath);
                    newman.run(
                        {
                            collection: collectionPath,
                            environment: environmentPath,
                            reporters: 'csv',
                            reporter: {
                                csv: { 
                                    includeBody: true,
                                    export: exportFileName}
                            }
                        },
                        (error,result) => {beautify_column_header(exportFileName);}
                        )
                }
            }
        }
    }
    else
    {
        for(let index = 0; index < numberOfRun;index++)
        {
            for(const collectionPath of usableCollection)
            {
                var exportFileName = export_file_name_generate(collectionPath,index);
                newman.run(
                    {
                        collection: collectionPath,
                        reporters: 'csv',
                        reporter: {
                            csv: { 
                                includeBody: true,
                                export: exportFileName}
                                    }
                    },(error,result) => {beautify_column_header(exportFileName);}
                        );
            }
        }
    }
}

try
{
    check_arguments();
    check_duplicate();
    placing_argument_to_variable();
    splitting_collection_and_environment();
    check_valid_of_collection_and_environment();
    if(runParallel === true)
    {
        run_request_parallel_process();
    }
    else
    {
        run_request_concurrent_process();
    }
}catch(error)
{
    console.log(error.toString());
}
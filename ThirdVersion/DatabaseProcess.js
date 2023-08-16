const fs = require('fs');
const { exit } = require('process');
const prompt = require('prompt-sync')();
const ex = require('exceljs');
const child_process = require('child_process');
const {default: pQueue} = require('p-queue');
const { type } = require('os');

const argumentList = ["-u","--user","-p","--password","-s","--server","-P","--port","-t","--trustServerCertificate","-e","--encrypt","-M", "--max", "-m","--min","-T","--idleTimeoutMilis","-c","--checkConnect"];
const totalArgumentsInputted = process.argv.slice(2);
const numberOfQueue = 10;
var user = "";
var password = "";
var server = "";
var port = "";
var trustServerCertificate = "";
var encrypt = "";
var max = "";
var min = "";
var idleTimeoutMilis = "";
var checkConnect = "";


function convertStreamToJSON(dataStream)
{
    let jsonData = '';
    const dataStreamString = JSON.stringify(dataStream);
    const dataStreamJson = JSON.parse(dataStreamString);
    const streamData = dataStreamJson['data'];
    for(let index = 0; index < streamData.length; index++)
    {
        jsonData += String.fromCharCode(streamData[index])
    }
    return jsonData;
}

function add_result_into_file(resultArray)
{
    const workbook = new ex.Workbook();
    const worksheet = workbook.addWorksheet(`Result`);
    let fileName = "";
    if(resultArray[0].environmentPath === undefined)
    {
        fileName = export_file_name_generate(resultArray[0].collectionPath, resultArray[0].iterationTime - 1);
    }
    else
    {
        fileName = export_file_name_generate(resultArray[0].collectionPath, resultArray[0].iterationTime - 1, resultArray[0].environmentPath);
    }
    var collectionNameList = resultArray[0].collectionPath.split("/");
    var collectionName = collectionNameList[collectionNameList.length - 1].split(".")[0];
    worksheet.columns = [
        { header: 'Collection Name', key: 'collectionName'},
        { header: 'Request Name', key: 'name' },
        { header: 'Method', key: 'method'},
        { header: 'Request Url', key: 'requestUrl'},
        { header: 'Status', key: 'status' },
        { header: 'Status Code', key: 'statusCode'},
        { header: 'Response Time (ms)', key: 'responseTime' },
        { header: 'Response Size', key: 'responseSize'},
        { header: 'Executed', key: 'executed'},
        { header: 'Failed', key: 'failed'},
        { header: 'Skipped', key: 'skipped'},
        { header: 'Request Body', key: 'requestBody'},
        { header: 'Response Body', key: 'responseBody'}
      ];

      resultArray.forEach(executions => {
        const execution = executions.execution[0]
        const assertResult = get_assertion_count(execution.assertions);
        worksheet.addRow({
            collectionName: collectionName,
            name: execution.item.name,
            method: execution.item.request.method,
            requestUrl: execution.item.request.url.toString(),
            status: execution.response.status,
            statusCode: execution.response.code,
            responseTime: execution.response.responseTime,
            responseSize: execution.response.responseSize,
            executed: assertResult.executed,
            failed: assertResult.failed,
            skipped: assertResult.skipped,
            requestBody: getRequestBody(execution.request.body),
            responseBody: convertStreamToJSON(execution.response.stream),
        });
      workbook.csv.writeFile(fileName);
    });
}
// Done
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
// Done
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
    if(totalArgumentsInputted.includes("-u") && totalArgumentsInputted.includes("--user"))
    {
        throw new Error("The -u and --user is the same, please use only one of them !!!");
    }
    else if(totalArgumentsInputted.includes("-p") && totalArgumentsInputted.includes("--password"))
    {
        throw new Error("The -p and --password is the same, please use only one of them !!!");
    }
    else if(totalArgumentsInputted.includes("-s") && totalArgumentsInputted.includes("--server"))
    {
        throw new Error("The -s and --server is the same, please use only one of them !!!");
    }
    else if(totalArgumentsInputted.includes("-P") && totalArgumentsInputted.includes("--port"))
    {
        throw new Error("The -P and --port is the same, please use only one of them !!!");
    }
    else if(totalArgumentsInputted.includes("-t") && totalArgumentsInputted.includes("--trustServerCertificate"))
    {
        throw new Error("The -t and --trustServerCertificate is the same, please use only one of them !!!");
    }
    else if(totalArgumentsInputted.includes("-e") && totalArgumentsInputted.includes("--encrypt"))
    {
        throw new Error("The -e and --encrypt is the same, please use only one of them !!!");
    }
    else if(totalArgumentsInputted.includes("-M") && totalArgumentsInputted.includes("--max"))
    {
        throw new Error("The -M and --max is the same, please use only one of them !!!");
    }
    else if(totalArgumentsInputted.includes("-m") && totalArgumentsInputted.includes("--min"))
    {
        throw new Error("The -m and --min is the same, please use only one of them !!!");
    }
    else if(totalArgumentsInputted.includes("-T") && totalArgumentsInputted.includes("--idleTimeoutMilis"))
    {
        throw new Error("The -T and --idleTimeoutMilis is the same, please use only one of them !!!");
    }
    else if(totalArgumentsInputted.includes("-c") && totalArgumentsInputted.includes("--checkConnect"))
    {
        throw new Error("The -c and --checkConnect is the same, please use only one of them !!!");
    }


    Object.keys(uniqueArgumentDict).forEach(element => 
    {
        if(uniqueArgumentDict[element] > 1)
        {
            throw new Error("The " + element + " is added more than one, please only use one of this !!!");
        }
    });
}

// Working on
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
                const number = parseInt(localTotalArgumentsInputted.at(index + 1));
                if (number === 0)
                {
                    throw new Error("The value of the -n or --numberOfRun must be greater than 0, please recheck !!!");
                }
                if (Number.isNaN(number))
                {
                    throw new Error("The value of the -n or --numberOfRun must be a number, please recheck !!!");
                }
                numberOfRun = number;
            }
            else if (localTotalArgumentsInputted.at(index) === "-d" || localTotalArgumentsInputted.at(index) === "--dataFile")
            {
                dataFile = localTotalArgumentsInputted.at(index+1);
            }
        }
        else
        {
            throw new Error("There is some value placed in the wrong position, please recheck !!!")
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
        let firstRowBeforeRemoveColumns = ws.getRow(1);
        for(let index = 1; index <= firstRowBeforeRemoveColumns.cellCount;index++)
        {
            if(notUsableColumns.includes(firstRowBeforeRemoveColumns.getCell(index).value))
            {
                ws.spliceColumns(index,1);
            }
        }
        
        // Rename all the headers
        let firstRowAfterRemoveColumns = ws.getRow(1);
        for(let index = 0; index <= columnNames.length; index++)
        {
            firstRowAfterRemoveColumns.getCell(index + 1 ).value = columnNames[index];
        }

        wb.csv.writeFile(fileName);
    }).catch(err => {
            console.log(err.message);
    });

}


function check_the_report_folder()
{
    if(!fs.existsSync("./report"))
    {
        fs.mkdirSync("./report")
    }
    else
    {
        //Do nothing
    }
}


try
{
    check_arguments();
    check_duplicate();
    placing_argument_to_variable();

}catch(error)
{
    console.log(error.toString());
}
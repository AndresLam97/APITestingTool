const fs = require('fs');
const newman = require('newman');
const { exit } = require('process');
const prompt = require('prompt-sync')();
const ex = require('exceljs');
const child_process = require('child_process');
const {default: pQueue} = require('p-queue');
const { type } = require('os');

const columnNames = ["Collecton Name","Request Name", "Method", "Url", "Status","Code","Response Time","Response Size","Executed", "Failed","Skippped","Request Body","Response Body"];
const notUsableColumns = ['iteration','fullName','statusCode']
const argumentList = ["-c","--collectionFile","-e","--environmentFile","-n","--numberOfRun","-p","--parallel","-d","--dataFile"];
const totalArgumentsInputted = process.argv.slice(2);
const numberOfQueue = 10;
let runParallel = false;
let collectionFiles = "";
let collectionFileList = [];
let environmentFileList = [];
let environmentFiles = "";
let dataFile = "";
let numberOfRun = 1;
let usableCollection = [];
let notUsableCollection = [];
let usableEnvironment = [];
let notUsableEnvironment = [];
var results = [];

function getRequestBody(fullRequestBody)
{
    try{
      var fullRequestBodyString = JSON.stringify(fullRequestBody)
      const fullRequestBodyJson = JSON.parse(fullRequestBodyString)
      if(fullRequestBodyJson['mode'] === 'raw')
      {
          return fullRequestBodyJson['raw'];
      }
      else if (fullRequestBodyJson['mode'] === 'urlencoded')
      {
          return fullRequestBodyJson['urlencoded'];
      }
      else if (fullRequestBodyJson['mode'] === 'formdata')
      {
          return fullRequestBodyJson['formdata'];
      }
      else if (fullRequestBodyJson['mode'] === 'graphql')
      {
          return fullRequestBodyJson['graphql'];
      }
      else
      {
          return "";
      }
    }
    catch(error)
    {
      return ""
    }
}

function get_assertion_count(assertions)
{
  var result = {
    "executed": "",
    "failed": 0,
    "skipped": 0
  }
  if(assertions === undefined)
  {
    return result;
  }
  else
  {
    for(let index = 0 ; index < assertions.length;index++)
    {
      if(index === assertions.length - 1)
      {
        result['executed'] = result['executed'] + assertions[index].assertion
        if(assertions[index].error !== undefined)
        {
          result['failed'] = result['failed'] + assertions[index].error.name + ": " + assertions[index].error.message + " for " + assertions[index].error.test + " assert.";
        }
      }
      else
      {
        result['executed'] = result['executed'] + assertions[index].assertion + "\n";
        if(assertions[index].error !== undefined)
        {
          result['failed'] = result['failed'] + assertions[index].error.name + ": " + assertions[index].error.message + " for " + assertions[index].error.test + " assert." + "\n";
        }
      }
      if(assertions[index].skipped === true)
      {
        result['skipped'] = result['skipped'] + 1;
      }
    }
  }
  return result;
}

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

function get_all_request_name_in_collection(collectionName)
{
  const dataBuffer = fs.readFileSync(collectionName);
  const converted = convertStreamToJSON(dataBuffer);
  const convertedObject = JSON.parse(converted);
  let allRequestName = [];
  convertedObject.item.forEach(element => allRequestName.push(element.name));
  return allRequestName;
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
    else if(totalArgumentsInputted.includes("-d") && totalArgumentsInputted.includes("--dataFile"))
    {
        throw new Error("The -d and --dataFile is the same, please use only one of them !!!");
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
    if(notUsableCollection.length > 0 || notUsableEnvironment.length > 0)
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

const run_request_parralel = async (collectionPath, requestName,iterationTime,environmentPath) => {
    if(environmentPath !== undefined)
    {
        return new Promise((resolve, reject) => {
        const runOptions = {
            collection: collectionPath,
            environment: environmentPath,
            abortOnError: true,
            folder: requestName
        };
        newman.run(runOptions, function (err, summary) {
            if (err) {
                reject(`Có lỗi xảy ra khi chạy request ${requestName} trong ${collectionPath}: ${err}`);
            } else {
                const execution = summary.run.executions;
                results.push({execution,collectionPath,environmentPath,iterationTime});
            };
                resolve(`Hoàn thành request ${requestName} trong ${collectionPath}`);
            });
        });
    }
    else
    {
        return new Promise((resolve, reject) => {
            const runOptions = {
                collection: collectionPath,
                abortOnError: true,
                folder: requestName
            };
            newman.run(runOptions, function (err, summary) {
                if (err) {
                    reject(`Có lỗi xảy ra khi chạy request ${requestName} trong ${collectionPath}: ${err}`);
                } else {
                    const execution = summary.run.executions;
                    results.push({execution,collectionPath,iterationTime});
                };
                    resolve(`Hoàn thành request ${requestName} trong ${collectionPath}`);
                });
            });
    }
};

async function run_request_parallel_process()
{
    const queue = new pQueue({ concurrency: numberOfQueue });
    if(usableEnvironment.length > 0){
        for (let runTime = 1; runTime <= numberOfRun;runTime++)
        {
            for (const collection of usableCollection){
                const allRequestNameInCollection = get_all_request_name_in_collection(collection);
                for (const environment of usableEnvironment)
                {
                    for(const requestName of allRequestNameInCollection)
                    {
                        queue.add(()=> run_request_parralel(collection, requestName, runTime , environment));
                    }
                }
            }
        }
        try {
            await queue.onIdle();
            for (const collectionName of usableCollection) {
                for(const environmentName of usableEnvironment)
                {
                    for(let runTime = 1; runTime <= numberOfRun;runTime++)
                    {
                        var dataArray = results.filter(function(element) 
                        {
                            return element.collectionPath === collectionName && element.environmentPath === environmentName && element.iterationTime === runTime;
                        });
                        add_result_into_file(dataArray);
                    }
                }
            }
        } catch (error) {
            console.error(error);
        }}
    else{
        for (let runTime = 1; runTime <= numberOfRun;runTime++)
        {
            for (const collection of usableCollection){
                const allRequestNameInCollection = get_all_request_name_in_collection(collection);
                    for(const requestName of allRequestNameInCollection)
                    {
                        queue.add(()=> run_request_parralel(collection, requestName, runTime));
                    }
            }
            }
        
        try {
            await queue.onIdle();
            for (const collectionName of usableCollection) {
                for(let runTime = 1; runTime <= numberOfRun;runTime++)
                    {
                        var dataArray = results.filter(function(element) 
                        {
                            return element.collectionPath === collectionName && element.iterationTime === runTime;
                        });
                        add_result_into_file(dataArray);
                    }
            }
        } catch (error) {
            console.error(error);
        }
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
                    const exportFileName = export_file_name_generate(collectionPath,index,environmentPath);
                    var command = "newman run " + '"' + collectionPath + '"' + " -e " + '"' + environmentPath + '"'+ " -r csvextra" + " --reporter-csvextra-export "+ '"' + exportFileName + '"';
                    if (dataFile.length !== 0)
                    {
                        command = command + " -d " + dataFile;
                    }
                    child_process.exec(command,(error,stdout,stderr)=>{
                        if(stderr.length > 0)
                        {
                            console.log(stderr.toString());
                        }
                        beautify_column_header(exportFileName);
                    }); 
                    
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
                const exportFileName = export_file_name_generate(collectionPath,index);
                var command = "newman run " + '"' + collectionPath + '"' + " -r csvextra" + " --reporter-csvextra-export "+ '"' + exportFileName + '"';
                if (dataFile.length !== 0)
                {
                    command = command + " -d " + dataFile;
                }
                child_process.exec(command,(error,stdout,stderr)=>{
                    if(stderr.length > 0)
                    {
                        console.log(stderr.toString());
                    }
                    beautify_column_header(exportFileName);
                });
            }
        }
    }
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

function check_data_file_if_run_parallel(){
    if(dataFile.length !== 0 && runParallel === true)
        throw new Error("Running with data file is not allowed when the run configuration is run parallel, please recheck !!!");
}

try
{
    check_arguments();
    check_duplicate();
    placing_argument_to_variable();
    splitting_collection_and_environment();
    check_valid_of_collection_and_environment();
    check_data_file_if_run_parallel();
    run_request_concurrent_process();
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
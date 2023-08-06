const {default: pQueue} = require('p-queue');
const newman = require('newman');
const fs = require('fs');
const Excel = require('exceljs')

const collections = [
    'My Collection.postman_collection.json',
    // Thêm các đường dẫn đến các collection khác nếu cần
  ];
  
  // Mảng chứa đường dẫn tới các file environment
  const environments = [
    'SIT Environment.postman_environment.json',
    'SIT Environment 1.postman_environment.json'
    // Thêm các đường dẫn đến các environment khác nếu cần
  ];

var results = [];
const iterationTime = 2;
const numberOfQueue = 10;

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
    const workbook = new Excel.Workbook();
    const worksheet = workbook.addWorksheet(`Result`);
    const fileName = export_file_name_generate(resultArray[0].collectionPath, resultArray[0].iterationTime - 1, resultArray[0].environmentPath)
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
            collectionName: 'test',
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


const runSingleRequest = async (collectionPath, environmentPath, requestName,iterationTime) => {
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
        results.push({
            execution,
            collectionPath,
            environmentPath,
            iterationTime
          });
        };
        resolve(`Hoàn thành request ${requestName} trong ${collectionPath}`);
      });
  });
};

async function runParallelRequests() {
  const queue = new pQueue({ concurrency: numberOfQueue });
  for (let index = 1; index <= iterationTime;index++)
  {
    for (let i = 0; i < collections.length; i++) {
      const allRequestNameInCollection = get_all_request_name_in_collection(collections[i]);
      for(let s = 0; s < environments.length; s++)
      {
          for(const requestName of allRequestNameInCollection)
          {
            queue.add(()=> runSingleRequest(collections[i], environments[s], requestName,index));
          }
      }
    }
  }

  try {
    await queue.onIdle();
    
    for (const collectionName of collections) {
      for(const environmentName of environments)
      {
          for(let r = 1; r <= iterationTime;r++)
          {
            var z = results.filter(function(element) 
              {
                return element.collectionPath === collectionName && element.environmentPath === environmentName && element.iterationTime === r;
              });
            add_result_into_file(z)
      }
      }
    }

    console.log("Tất cả request đã hoàn thành và kết quả được xuất ra file CSV.");
  } catch (error) {
    console.error(error);
  }
}

runParallelRequests();
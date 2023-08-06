const newman = require('newman');
const Excel = require('exceljs');

// Mảng chứa đường dẫn tới các file collection
const collectionPaths = [
  'New Collection.postman_collection.json',
  // Thêm các đường dẫn đến các collection khác nếu cần
];

// Mảng chứa đường dẫn tới các file environment
const environmentPaths = [
  'SIT Environment.postman_environment.json',
  'SIT Environment 1.postman_environment.json'
  // Thêm các đường dẫn đến các environment khác nếu cần
];

// Hàm giả lập việc chạy Newman bằng Promise
function runNewmanWithPromise(collectionPath, environmentPath) {
  return new Promise((resolve, reject) => {
    const options = {
      collection: collectionPath,
      environment: environmentPath,
    };

    newman.run(options, function (err, summary) {
      if (err) {
        reject(err);
      } else {
        resolve(summary);
      }
    });
  });
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

function convertResponseBody(responseStream)
{
    let responseBody = '';
    const responseStreamString = JSON.stringify(responseStream);
    const responseStreamJson = JSON.parse(responseStreamString);
    const streamData = responseStreamJson['data'];
    for(let index = 0; index < streamData.length; index++)
    {
        responseBody += String.fromCharCode(streamData[index])
    }
    return responseBody;
}


// Hàm chạy song song các request trong từng cặp collection và environment
async function runCollectionsWithEnvironments() {
  const promises = [];

  for (let i = 0; i < collectionPaths.length; i++) {
    for (let j = 0; j < environmentPaths.length; j++) {
      const collectionPath = collectionPaths[i];
      const environmentPath = environmentPaths[j];

      const promise = runNewmanWithPromise(collectionPath, environmentPath);
      promises.push(promise);
    }
  }

  try {
    const summaries = await Promise.all(promises);
    for (let i = 0; i < summaries.length; i++) {
      const summary = summaries[i];
      console.log(`Kết quả chạy collection ${i + 1}:`, summary.collection.name);

      const workbook = new Excel.Workbook();
      const worksheet = workbook.addWorksheet(`Kết quả collection ${i + 1}`);

      worksheet.columns = [
        { header: 'Method', key: 'method'},
        { header: 'Request Url', key: 'requestUrl'},
        { header: 'Request Name', key: 'name' },
        { header: 'Request Body', key: 'requestBody'},
        { header: 'Status', key: 'status' },
        { header: 'Status Code', key: 'statusCode'},
        { header: 'Response Time (ms)', key: 'responseTime' },
        { header: 'Response Body', key: 'responseBody'}
      ];

      summary.run.executions.forEach((execution) => {
        worksheet.addRow({
          method: execution.request.method,
          requestUrl: execution.item.request.url.toString(),
          name: execution.item.name,
          requestBody: getRequestBody(execution.request.body),
          status: execution.response.status,
          statusCode: execution.response.code,
          responseTime: execution.response.responseTime,
          responseBody: convertResponseBody(execution.response.stream)
        })
        
        ;
    });

      const excelFilePath = `./output_collection_${i + 1}.xlsx`;
      await workbook.xlsx.writeFile(excelFilePath);
      console.log(`Đã ghi kết quả của collection ${i + 1} vào file Excel: ${excelFilePath}`);
      const date1 = Date.now();
      console.log(date1);
    }

  } catch (error) {
    console.error('Có lỗi xảy ra:', error);
    // Xử lý lỗi ở đây (nếu cần)
  }
}

// Chạy song song các request trong từng cặp collection và environment
const date = Date.now();
console.log();
runCollectionsWithEnvironments();
const date1 = Date.now();
console.log(date1);
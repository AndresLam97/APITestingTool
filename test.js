const newman = require('newman');
const Excel = require('exceljs');

function runCollection(collectionPath) {
  return new Promise((resolve, reject) => {
    newman.run({
      collection: collectionPath,
    }, (error, summary) => {
      if (error) {
        reject(error);
      } else {
        resolve(summary);
      }
    });
  });
}

function getRequestBody(fullRequestBody)
{
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
        return None;
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

async function main() {
  const collectionPaths = [
    'C:/Users/Andres/Desktop/Code/NodeJs/My Collection 2.postman_collection.json',
  ];

  const promises = collectionPaths.map(runCollection);

  try {
    const summaries = await Promise.all(promises);

    // Ghi kết quả của tất cả các collection vào các file Excel riêng biệt
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
        console.log(execution.assertions)
        ;
    });

      const excelFilePath = `C:/Users/Andres/Desktop/Code/NodeJs/output_collection_${i + 1}.xlsx`;
      await workbook.xlsx.writeFile(excelFilePath);
      console.log(`Đã ghi kết quả của collection ${i + 1} vào file Excel: ${excelFilePath}`);
    }
  } catch (error) {
    console.error('Có lỗi xảy ra:', error);
  }
}

main()
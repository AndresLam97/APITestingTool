const newman = require('newman');
const Excel = require('exceljs')
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

const runSingleRequest = async (collectionPath, environmentPath, requestIndex) => {
  return new Promise((resolve, reject) => {
    const runOptions = {
      collection: collectionPath,
      environment: environmentPath,
      abortOnError: true,
      folder: `Request ${requestIndex}`, // Chỉ chạy một request cụ thể trong collection,
      iterationCount: 2 
    };

    newman.run(runOptions, function (err,summary) {
      if (err) {
        reject(`Có lỗi xảy ra khi chạy request ${requestIndex} trong ${collectionPath}: ${err}`);
      } else {
        resolve(summary);
      }
    });
  });
};

async function runParallelRequests() {
  const promises = [];

  for (let i = 0; i < collectionPaths.length; i++) {
    for(let s = 0; s < environmentPaths.length; s++)
    {
        for (let j = 1; j <= 10; j++) {
            promises.push(runSingleRequest(collectionPaths[i], environmentPaths[s], j));
        }
    }
  }

  try {
    const summaries = await Promise.all(promises);
    for (let i = 0; i < summaries.length; i++) {
        const summary = summaries[i];
        console.log(`Kết quả chạy collection ${i + 1}:`, summary.collection.name);
        console.log(summary.collection.items)
    //     const workbook = new Excel.Workbook();
    //     const worksheet = workbook.addWorksheet(`Kết quả collection ${i + 1}`);
  
    //     worksheet.columns = [
    //       { header: 'Method', key: 'method'},
    //       { header: 'Request Url', key: 'requestUrl'},
    //       { header: 'Request Name', key: 'name' },
    //       { header: 'Request Body', key: 'requestBody'},
    //       { header: 'Status', key: 'status' },
    //       { header: 'Status Code', key: 'statusCode'},
    //       { header: 'Response Time (ms)', key: 'responseTime' },
    //       { header: 'Response Body', key: 'responseBody'}
    //     ];
        
    //     summary.run.executions.forEach((execution) => {
    //       worksheet.addRow({
    //         method: execution.request.method,
    //         requestUrl: execution.item.request.url.toString(),
    //         name: execution.item.name,
    //         requestBody: getRequestBody(execution.request.body),
    //         status: execution.response.status,
    //         statusCode: execution.response.code,
    //         responseTime: execution.response.responseTime,
    //         responseBody: convertResponseBody(execution.response.stream)
    //       })
          
    //       ;
    //   });
  
    //     const excelFilePath = `./output_collection_${i + 1}.xlsx`;
    //     await workbook.xlsx.writeFile(excelFilePath);
    //     console.log(`Đã ghi kết quả của collection ${i + 1} vào file Excel: ${excelFilePath}`);
      }
  
  } catch (error) {
    console.error(error); // In lỗi nếu có lỗi xảy ra
  }
}

runParallelRequests();
const newman = require('newman');

const runFile = 'C:/Users/KienL/OneDrive - GBST/Desktop/New Folder/Test/New Collection.postman_collection.json';

// Đọc tập tin collection
const collection = require(runFile);

const env1File = 'C:/Users/KienL/OneDrive - GBST/Desktop/New Folder/Test/env1.json';
const env2File = 'C:/Users/KienL/OneDrive - GBST/Desktop/New Folder/Test/env2.json';
const env3File = 'C:/Users/KienL/OneDrive - GBST/Desktop/New Folder/Test/env3.json';

const envList = [env1File, env2File, env3File]

for (let index = 0; index < envList.length; index++) {
    // Tạo một mảng các Promise đại diện cho các yêu cầu
    const promises = collection.item.map((item) => {
        return new Promise((resolve, reject) => {
            newman.run(
                {
                    collection: {
                        item: [item]
                    },
                    environment: envList[index]
                },
                (err, summary) => {
                    if (err) {
                        console.error('Lỗi: ', err);
                        reject(err);
                        return;
                    }
                    //console.log('Kết quả: ', summary.run.executions);
                    resolve(summary);
                }
            );
        });
    });

    // Chạy các yêu cầu song song và xử lý kết quả
    Promise.all(promises)
        .then((results) => {
            console.log('Tổng kết: ', results);
        })
        .catch((err) => {
            console.error('Lỗi: ', err);
        });
}
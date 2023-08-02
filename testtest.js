<<<<<<< HEAD
const { exec } = require('child_process');

collectionPath = '"My Collection.postman_collection.json"'
environmentPath = '"SIT Environment.postman_environment.json"'
const command = "newman run " + collectionPath + " -e " + environmentPath;

exec(command, (err, stdout, stderr) => {
//   if (err) {
//     console.error(`exec error: ${err}`);
//     return;
//   }

  console.log(stdout);
});
=======
const newman = require('newman');

// Mảng chứa đường dẫn tới các file collection
const collectionPaths = [
  'path/to/collection1.json',
  'path/to/collection2.json',
  'path/to/collection3.json',
  // Thêm các đường dẫn đến các collection khác nếu cần
];

// Mảng chứa đường dẫn tới các file environment
const environmentPaths = [
  'path/to/environment1.json',
  'path/to/environment2.json',
  'path/to/environment3.json',
  // Thêm các đường dẫn đến các environment khác nếu cần
];

// Hàm giả lập việc chạy Newman bằng Promise
function runNewmanWithPromise(collectionPath, environmentPath) {
  return new Promise((resolve, reject) => {
    const options = {
      collection: require(collectionPath),
      environment: require(environmentPath),
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
    const results = await Promise.all(promises);
    console.log('Kết quả chạy các cặp collection và environment:', results);
    // Xử lý kết quả ở đây (nếu cần)
  } catch (error) {
    console.error('Có lỗi xảy ra:', error);
    // Xử lý lỗi ở đây (nếu cần)
  }
}

// Chạy song song các request trong từng cặp collection và environment
runCollectionsWithEnvironments();
>>>>>>> 51c8cb69bb68e915493767e4f7a91d30b56c7182

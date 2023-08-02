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
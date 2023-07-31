const fs = require('fs');
const ex = require('exceljs');

const file ='test.csv';
const columnNames = ["Collecton Name","Request Name", "Method", "Url", "Status","Code","Response Time","Reponse Size","Executed", "Failed","Skippped","Total Assertions","Executed Count","Failed Count","Skipped Count","Response Body"]
wb = new ex.Workbook();

// done for removing iteration row
// wb.csv.readFile(file).then(() => {
//   const ws = wb.getWorksheet();
//   ws.spliceColumns(1,1);
//   wb.csv.writeFile(file);

// }).catch(err => {
//   console.log(err.message);
// });

// // done for changing header name
// wb.csv.readFile(file).then(() => {
//   const ws = wb.getWorksheet();

//   // Remove the first column
//   ws.spliceColumns(1,1);

//   // Rename all the headers
//   let firstRow = ws.getRow(1);
//   for(let index = 1; index <= firstRow.cellCount; index++)
//   {
//     firstRow.getCell(index).value = columnNames[index - 1];
//   }
//   wb.csv.writeFile(file);
// }).catch(err => {
//   console.log(err.message);
// });


console.log(fs.existsSync("./report/My Collection-2023-6-31-13-26-3- run time 1.csv"));
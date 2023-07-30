const newman = require('newman');
const collectionPath = "../My Collection 2.postman_collection.json"
const x = ",,"

// newman.run(
//     {
//         collection: require(collectionPath),
//         reporters: "csv",
//         reporter: {
//             csv: {
//                 includeBody: true,
//                 export: "test.csv"}
//         }
//     }
//     )


const fs = require('fs')

function test(a,b)
{
    if(b === undefined)
    {
        console.log("Yew")
    }
}

test(45,1)
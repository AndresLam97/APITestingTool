const mssql = require('mssql')

const config = 
{
    user: "dbd_kienl",
    password: "dbd_kienl",
    server: "composer-db.composer-eks.composer-eks.syd.aws.ongbst.net",
    port: 32710,
    database: "composer",
    options:{
        trustServerCertificate: true
    }
}


async function test(){
    try{
        let pool = await mssql.connect(config)
        let result = await pool.request().query("SELECT TOP 2 * FROM product_type pt")
        newData = JSON.stringify(result)
        console.log(newData)
        mssql.close()
    }catch(error)
    {
        console.log(error)
    }
}


data = test()
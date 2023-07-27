const { Exception } = require("handlebars");

const argumentList = ["-c","--colectionFile","-e","--environmentFile","-n","--numberOfRun","-p","--parallel","-h", "--help"]
const totalArgumentsInputted = process.argv.slice(2);

function checkArgument()
{
    let illegalArgumentList = [];
    totalArgumentsInputted.forEach(element => {
            if(argumentList.includes(element) === false)
            {
                illegalArgumentList.push(element);
            }
    });
    if (illegalArgumentList.length > 0)
    {
        throw new Error("The argument(s) is/are not supportted: " + illegalArgumentList)
    }
}

function checkDuplicate()
{
    let uniqueArgument = new Set(totalArgumentsInputted);
    let uniqueArgumentDict = {};
    for(const argument of uniqueArgument)
    {
        uniqueArgumentDict[argument] = 0
    }
    


}

try
{
    checkArgument()
    checkDuplicate()
}catch(error)
{
    console.log(error.toString())
}
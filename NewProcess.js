const argumentList = ["-c","--collectionFile","-e","--environmentFile","-n","--numberOfRun","-p","--parallel"]
const totalArgumentsInputted = process.argv.slice(2);
let runParallel = false;
let collectionFile = "";
let environmentFileList = [];
let environmentFiles = "";
let numberOfRun;


function checkArgument()
{
    let illegalArgumentList = [];
    totalArgumentsInputted.forEach(element => {
        if(element.startsWith("-") || element.startsWith("--"))
        {
            if(argumentList.includes(element) === false)
            {
                illegalArgumentList.push(element);
            }
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
    };
    totalArgumentsInputted.forEach(element => 
    {
        if(uniqueArgumentDict[element] !== undefined)
        {
            uniqueArgumentDict[element] = uniqueArgumentDict[element] + 1;
        }
    });
    if(totalArgumentsInputted.includes("-c") && totalArgumentsInputted.includes("--collectionFile"))
    {
        throw new Error("The -c and --collectionFile is the same, please use only one of them !!!");
    }
    else if(totalArgumentsInputted.includes("-e") && totalArgumentsInputted.includes("--environmentFile"))
    {
        throw new Error("The -e and --environmentFile is the same, please use only one of them !!!");
    }
    else if(totalArgumentsInputted.includes("-n") && totalArgumentsInputted.includes("--numberOfRun"))
    {
        throw new Error("The -n and --numberOfRun is the same, please use only one of them !!!");
    }
    else if(totalArgumentsInputted.includes("-p") && totalArgumentsInputted.includes("--parallel"))
    {
        throw new Error("The -p and --parallel is the same, please use only one of them !!!");
    }

    Object.keys(uniqueArgumentDict).forEach(element => 
    {
        if(uniqueArgumentDict[element] > 1)
        {
            throw new Error("The " + element + " is added more than one, please only use one of this !!!");
        }
    });
}

function placingArgumentToVariable()
{
    let localTotalArgumentsInputted = totalArgumentsInputted
    if(totalArgumentsInputted.indexOf("-p") !== -1)
    {
        runParallel = true;
        localTotalArgumentsInputted = localTotalArgumentsInputted.filter(element => element !== "-p");
    }
    if(localTotalArgumentsInputted.length % 2 !== 0)
    {
        throw new Error("There is some argument is missing value, please recheck !!!");
    }
    for(let index = 0; index < localTotalArgumentsInputted.length; index = index + 2)
    {
        if(argumentList.includes(localTotalArgumentsInputted.at(index)))
        {
            if(localTotalArgumentsInputted.at(index) === "-c" || localTotalArgumentsInputted.at(index) === "--collectionFile")
            {
                collectionFile = localTotalArgumentsInputted.at(index + 1);
            }
            else if (localTotalArgumentsInputted.at(index) === "-e" || localTotalArgumentsInputted.at(index) === "--environmentFile")
            {
                environmentFiles = localTotalArgumentsInputted.at(index + 1);
            }
            else if (localTotalArgumentsInputted.at(index) === "-n" || localTotalArgumentsInputted.at(index) === "--numberOfRun")
            {
                numberOfRun = parseInt(localTotalArgumentsInputted.at(index + 1));
            }
        }
        else
        {
            throw new Error("There is some value placed in the wrong position, please recheck !!!")
        }
    }
}

function runRequestParallelProcess()
{

}

function runRequestConcurrentProcess()
{
    
}

try
{
    checkArgument()
    checkDuplicate()
    placingArgumentToVariable()
    if(runParallel === true)
    {
        runRequestParallelProcess()
    }
    else
    {
        runRequestConcurrentProcess()
    }
}catch(error)
{
    console.log(error.toString())
}
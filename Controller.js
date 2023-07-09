const { exit } = require("process");

function validateArguments(...arg)
{
    const verifyDuplicateResult = verifyDuplicateFlag(...arg);
    if(verifyDuplicateResult["valid"] === false)
    {
        console.log(verifyDuplicateResult["message"]);
        exit();
    }
    const mapValueToFieldResult = mapValueToField(...arg);
    if(Object.keys(mapValueToFieldResult).includes("valid") && mapValueToFieldResult["valid"] === false)
    {
        console.log(mapValueToFieldResult["message"]);
        exit();
    }
    const verifyInvalidFlagResult = verifyInvalidFlag(mapValueToFieldResult);
    if(verifyInvalidFlagResult["valid"] === false)
    {
        console.log(verifyInvalidFlagResult["message"]);
        exit();
    }
    return mapValueToFieldResult;
}

function verifyDuplicateFlag(...arg)
{
    let result = {
        "valid": true,
        "message": ""
    };
    var dictionaryKeys = {}
    if(arg.includes('-n') && arg.includes('--numberOfRun')) 
    {
        result["valid"] = false;
        result["message"] = result["message"] + "The -n and --numberOfRun are the same arguments, please re-input!\n";
    }
    if (arg.includes("-f") && arg.includes("--envFolder")) 
    {
        result["valid"] = false;
        result["message"] = result["message"] + "The -f and --envFolder are the same arguments, please re-input!\n";
    }
    if (arg.includes("-e") && arg.includes("--envFile")) 
    {
        result["valid"] = false;
        result["message"] = result["message"] + "The -e and --envFile are the same arguments, please re-input!\n";
    }
    for(let index = 2; index < arg.length; index++)
    {
        if (arg[index].charAt(0) === '-')
        {
            if (arg[index] in dictionaryKeys)
            {
                dictionaryKeys[arg[index]] = dictionaryKeys[arg[index]] + 1;
            }
            else
            {
                dictionaryKeys[arg[index]] = 1;
            }
        }
    }
    for(const [key,value] of Object.entries(dictionaryKeys) )
    {
        if(value > 1)
        {
            result["valid"] = false;
            result["message"] = result["message"] + "The " + key + " argument was appeared multiple times in the command, please re-input!\n"
        }
    }
    return result;
}

function mapValueToField(...arg)
{
    var dataDictionary = {}
    var parallelFlagIndex = arg.indexOf("-p");
    if (parallelFlagIndex !== -1)
    {
        dataDictionary["-p"] = true;
    }
    else
    {
        dataDictionary["-p"] = false;
    }
    arg.splice(parallelFlagIndex,1);
    var result = {
        "valid": true,
        "message": ""
    }
    for(let index = 2; index < arg.length; index = index + 2)
    {
        if ((index + 1) < arg.length && arg[index].charAt(0) === '-')
        {
            if(arg[index+1].charAt(0) === '-') 
            {
                result["valid"] = false;
                result["message"] = "Please provide data for the " + arg[index] + " argument!";
                return result;            
            }
            dataDictionary[arg[index]] = arg[index+1];
        }
        else if ((index + 1) >= arg.length && arg[index].charAt(0) === '-')
        {
            result["valid"] = false;
            result["message"] = "Please provide data for the " + arg[index] + " argument!";
            return result;     
        }
    }
    return dataDictionary;
}

function verifyInvalidFlag(dictionary)
{
    const argumentLists = ["-p","-n","--numberOfRun","-f","--envFolder","-e","--envFile"]
    const dictionaryKeys = Object.keys(dictionary)
    var result = {
        "valid" : true,
        "message": ""
    }
    for(let index = 0; index < dictionaryKeys.length; index++)
    {
        if (!argumentLists.includes(dictionaryKeys[index])){
            result["valid"] = false,
            result["message"] = result["message"] + "The " + dictionaryKeys[index] + " is not valid for the command, please re-input!\n";
        }
    }
    return result;
}



module.exports = {validateArguments}
import subprocess
import os

test = ["C:/Users/KienL/OneDrive - GBST/Desktop/New Folder/Test/env1.postman_environment.json",
"C:/Users/KienL/OneDrive - GBST/Desktop/New Folder/Test/env2.postman_environment.json",
"C:/Users/KienL/OneDrive - GBST/Desktop/New Folder/Test/env3.json",
"sadfsdaf",
"test",
"",
"teststesetset"
]
for environmentFile in test:
            if(environmentFile != "\n"):
                trimmedEnvironmentFile = environmentFile.strip()
                if(os.path.isfile(trimmedEnvironmentFile)):
                    print(trimmedEnvironmentFile)
                    print("is file")
                    print("--------------------------------")
                else:
                    print(trimmedEnvironmentFile)
                    print("is not file")
                    print("--------------------------------")
                    
            else:
                pass
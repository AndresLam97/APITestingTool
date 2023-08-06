const test = [
    {
      execution: [ [Object] ],
      collectionPath: 'My Collection.postman_collection.json',
      environmentPath: 'SIT Environment.postman_environment.json',
      iterationTime: 2
    },
    {
      execution: [ [Object] ],
      collectionPath: 'My Collection.postman_collection.json',
      environmentPath: 'SIT Environment 1.postman_environment.json',
      iterationTime: 1
    },
    {
      execution: [ [Object] ],
      collectionPath: 'My Collection.postman_collection.json',
      environmentPath: 'SIT Environment 1.postman_environment.json',
      iterationTime: 2
    },
    {
      execution: [ [Object] ],
      collectionPath: 'My Collection.postman_collection.json',
      environmentPath: 'SIT Environment.postman_environment.json',
      iterationTime: 1
    }
  ]

  const collections = [
    'My Collection.postman_collection.json',
    // Thêm các đường dẫn đến các collection khác nếu cần
  ];
  
  // Mảng chứa đường dẫn tới các file environment
  const environments = [
    'SIT Environment.postman_environment.json',
    'SIT Environment 1.postman_environment.json'
    // Thêm các đường dẫn đến các environment khác nếu cần
  ];


  for (const collectionName of collections) {
    for(const environmentName of environments)
    {
        for(let r = 0; r < 2;r++)
        {
          var z = test.filter(function(element)
            {
              return element.collectionPath === collectionName && element.environmentPath === environmentName && element.iterationTime === r;
            });
          console.log(z)
          console.log("===========================")
          //add_result_into_file()
        }
    }
  }
# JDI-QASP-ml v.2.0
# Model
Our model is neural network based on pytorch framework organized as follows:
```
-> Input linear layer
-> Dropout layer
-> LeakyReLu activation layer
-> Batch normalization layer
-> Hidden linear layer
-> Dropout layer
-> LeakyReLu activation layer
-> Output linear layer
```
As input for NN we use following calculated groups of features:
- **Attributes features** (OneHot-encoded info about having some attributes for object, his parent and up and down siblinhs)
- **Class features** (TF-IDF encoded info about class attribute for object, his parent and up and down siblinhs)
- **Type features** (OneHot-encoded info about type attribute for object, his parent and up and down siblinhs)
- **Role features** (OneHot-encoded info about role attribute for object, his parent and up and down siblinhs)
- **TAG features** (OneHot-encoded info about tag of object, his parent and up and down siblinhs)
- **Followers TAG features** (TF-IDF encoded info about all tags of childs or generally followers)
- **Numerical general features**  (General features about object like numger of followers, children, max max_depth etc.)
- **Binary general features** (General features with binary values like is the object or his parent hidden or displayed or leaf etc.)


# Install environment to train / test model

1. Clone the repository.<br>
2. Download and install Anaconda from https://www.anaconda.com/products/individual. <br>
   Alter your PATH environment variable to be able run python as well as conda utility. <br>
3. Create conda virtual environment using this command (see **create-env.bat** if you use Windows):<br>
````
    conda env create -f environment.yml --name jdi-qasp-ml
````
4. Run cmd.exe for windows or terminal for mac, and from command prompt:<br>
````
    conda activate jdi-qasp-ml 
````


# Generating the dataset for training model
## MUI

Generator for MUI element library sites placed in **generators/MUIgenerator/**<br>
To generate sites go in the directory of MUIgenerator and run:
````
    sh generate_data.sh
````
After thet in catalog **/data/mui_dataset/build** you will find directories named like **"site-N"**

Next go the directory **MUI_model** and run:
```
    python build_datasets_for_mui_sites.py
```
After that in directory **/data/mui_dataset** you will find following structure:
- /annotations (not used, maybe need to be removed later)
- /cache-labels (not used, maybe need to be removed later)
- /df - directory with peakles of site-datasets
- /html - directory with html files of sites (only for info)
- /images - directiry with images of sites (only for info)
- classes.txt - file with all possible labels to detect. Do not change it!!!
- EXTRACT_ATTRIBUTES_LIST.json - file with all attributes to take into account in the model (need in feature building). Do not change it!!!
## HTML5
to be done

# Train model
## MUI

<span style="color:orange"> If you need to train model from scratch (for example, number of classes is changed), delete all files from "MUI_model/model"
directory.</span>

To train the model you need to go to the directory **/MUI_model** and run:
```
    python train.py
```
If you need to set up training parameters, change following variables for train.py (placed in **vars/train_vars.py**):
- BATCH_SIZE (1024 by default)
- train_names and test_names. You need to set up them like (where N and T defines number of train-test ratio and depend on generated number of sites):
``` 
    train_names = DATASET_NAMES[:N]
    test_names = DATASET_NAMES[N:N+T]
``` 
- NUM_EPOCHS (100 by default)
- EARLY_STOPPING_THRESHOLD (10 by default) 

At the end of the process the table with training results saves in **MUI_model/tmp/train_metrics.csv**

# Predicting

To get predictions we need to run API main.py (better to do it wia docker - will be disscussed below)
when API is running we can send input json data to following url:
- http://localhost:5050/mui-predict for mui model
- http://localhost:5050/predict  for old version of model

<span style="color:orange">ATTENTION! 
In main.py flask application works on 5000 port but when we use docker we forward 5000 port in docker to 5050 port in local PC (because on my local PC port 5000 was always busy). So if you need to use another port on your local PC you need to change run_docker.sh file in the root of project.<span>

# Validate model

To validate models quality we use test web-pages, placed in directory **notebooks/MUI/Test-backend**

<span style="color:orange">You can change only notebooks with the "new"-end in the name like "Test-backend_mui-Buttons_new.ipynb"(others are legacy for comparing)<span>

In that notebooks we load specific web-page, creating dataset and predict labels for this dataset. It may be needed to correct some paths in notebooks (especially ports in them)

<span style="color:orange">To use this notebooks main.py need to be run.<span>


# Docker
- build image: 
```
 build-docker-image.bat (for windows)
 sh build_docker.sh (for mac)
```
- run docker:
```
run_docker.bat (for windows)
sh run_docker.sh (for mac)
```
<span style="color:orange">Attention! The first time you will build the docker image can take significant time (1 hour and more)<span>

Download the latest Docker Compose file from the `develop` branch and run `docker compose`:
## macOS/Linux
```shell
curl --output docker-compose.yaml --url https://raw.githubusercontent.com/jdi-testing/jdi-qasp-ml/develop/docker-compose.yaml && docker compose up
```
## Windows
```shell
curl.exe --output docker-compose.yaml --url https://raw.githubusercontent.com/jdi-testing/jdi-qasp-ml/develop/docker-compose.yaml && docker compose up
```

- check model's endpoint at http://localhost:5050/predict 
- run build-dataset.js in your browser js console. 
- send data using POST request to model
- after a few seconds dataset with discovered controll elements will be sent back
- you may check Test-Backend.ipynb as an example

# Docker - get debugging info:
- http://localhost:5050/build  - get the docker image build's datetime
- http://localhost:5050/files  - get data sent by browser to model

- To clean all docker images and containers:
````
    docker system prune --all --force
````

# Development:

## API service dependencies
New dependencies can be added with `pipenv` command:
```shell
pipenv install <package>==<version>
```
If there are conflicts on creating a new pipenv env on your local machine, please, add the dependencies inside the container:
```shell
docker compose -f docker-compose.dev.yaml run --rm api pipenv install <package>==<version>
```

## API

### /schedule_xpath_generation
Creates task for xpath generation and returns id of task which can be used for task revoking and 
getting task status or result.  

Accessible via **POST** request.  
Incoming JSON example:
```json
{
    "document": "...",  
    "id": "8520359515737429141026100694",  
    "config": {
            "maximum_generation_time": 10,
            "allow_indexes_at_the_beginning": true,  
            "allow_indexes_in_the_middle": true,  
            "allow_indexes_at_the_end": true 
        }  
}
```
Returns JSON: 
```json
{
    "task_id": "<task_id>"
}
```

### /get_task_status
Returns status of generation for task with specified id.

Accessible via **POST** request.  
Incoming JSON example:
```json
{
    "id": "<task_id>"
}
```
Returns JSON: 
```json
{
    "id": "<task_id>", 
    "status": "PENDING"
}
```

### /get_tasks_statuses
Same as get_task_status, but for the list of ids

Accessible via **POST** request.  
Incoming JSON example:
```json
{
    "id": ["<task_id1>", "<task_id2>"]
}
```
Returns JSON: 
```json
[
    {
        "id": "<task_id1>", 
        "status": "PENDING"
    },
    {
        "id": "<task_id2>", 
        "status": "SUCCESS"
    }
]
```

Possible statuses:   
**FAILURE** - Task failed  
**PENDING** - Task state is unknown (assumed pending since you know the id).  
**RECEIVED** - Task was received by a worker (only used in events).  
**RETRY** - Task is waiting for retry.  
**REVOKED** - Task was revoked.  
**STARTED** - Task was started by a worker.  
**SUCCESS** - Task succeeded  

### /revoke_task
Revokes task with specified id.  

Accessible via **POST** request.  
Incoming JSON example:
```json
{
    "id": "task_id"
}
```
Returns JSON: 
```json
{
    "result": "Task successfully revoked."
}
```

### /get_task_result
Returns result of generation for task with specified id.

Accessible via **POST** request.  
Incoming JSON example:
```json
{
    "id": "task_id"
}
```
Returns JSON: 
```json
{
    "id": "task_id", 
    "result": "<generated_xpath>"
}
```

### /get_tasks_results
Same as get_task_result, but for the list of ids.
Accessible via **POST** request.  
Incoming JSON example:
```json
{
    "id": ["task_id1", "task_id2"]
}
```
Returns JSON: 
```json
[
    {
        "id": "task_id1", 
        "result": "<generated_xpath>"
    },
    {
        "id": "task_id2", 
        "result": "<generated_xpath>"
    }
]
```

### Exceptions
In case of exception in any of listed above methods JSON with 'exc' field will be returned.  
JSON example:
```json
{
    "exc": "Generation still in progress."
}
```
or list of ids with exceptions if endpoint supports list processing:
```json
[
    {
        "id": "<task_id1>",
        "exc": "Generation still in progress."
    },
    {
        "id": "task_id2",
        "exc": "Generation still in progress."
    }
]
```



# JDI-QASP-ml v.2.0
# Model
## MUI
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

## HTML5 
Out model is desicion tree, because of simplicity of classic html5 element structure 

Picture of tree can be found in **HTML5_model/model/tree.jpeg**
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
- /df - directory with pickles of site-datasets
- /html - directory with html files of sites (only for info)
- /images - directiry with images of sites (only for info)
- classes.txt - file with all possible labels to detect. Do not change it!!!
- EXTRACT_ATTRIBUTES_LIST.json - file with all attributes to take into account in the model (need in feature building). Do not change it!!!
## HTML5
Generator for HTML5 element library sites placed in **generators/HTMLgenerator/**<br>
To generate sites go in the directory of HTMLgenerator and run:
````
    python generate-html.py
````
After thet in catalog **/data/html5_dataset/build/** you will find directory named as **"html5"**

Next go the directory **HTML5_model** and run:
```
    python build_datasets_for_html5_sites.py
```
After that in directory **/data/html5_dataset** you will find following structure:
- /annotations (empty, maybe need to delete)
- /cache-labels (empty, maybe need to delete)
- /df - directory with pickles of site-datasets
- /html - directory with html files of sites (only for info)
- /images - directiry with images of sites (only for info)
- classes.txt - file with all possible labels to detect. Do not change it!!!
- EXTRACT_ATTRIBUTES_LIST.json - file with all attributes to take into account in the model (need in feature building). Do not change it!!!

# Train model
## MUI

To train the model you need to go to the directory **/MUI_model** and run:
```
    python train.py
```
If you need to set up training parameters, change following variables for train.py (placed in **vars/mui_train_vars.py**):
- BATCH_SIZE (2048 by default)
- TRAIN_LEN and TEST_LEN 
- NUM_EPOCHS (2 by default)
- EARLY_STOPPING_THRESHOLD (2 by default) 

At the end of the process the table with training results saves in **MUI_model/tmp/train_metrics.csv**

## HTML5

To train the model you need to go to the directory **/HTML5_model** and run:
```
    python train.py
```
If you need to set up training parameters, change following variables for train.py (placed in **vars/html5_train_vars.py**):
- TRAIN_LEN and TEST_LEN 
- parameters of DT

At the end of the process the table with training results saves in **MUI_model/tmp/train_metrics.csv**

# Predicting

To get predictions we need to run API main.py (better to do it wia docker - will be disscussed below)
when API is running we can send input json data to following url:
- http://localhost:5050/mui-predict for mui model
- http://localhost:5050/html5-predict for html5 model
- http://localhost:5050/predict  for old version of model

# Validate model
## MUI
To validate models quality we use test web-pages, placed in directory **notebooks/MUI/Test-backend**

<span style="color:orange">You can change only notebooks with the "new"-end in the name like "Test-backend_mui-Buttons_new.ipynb"(others are legacy for comparing)<span>

In that notebooks we load specific web-page, creating dataset and predict labels for this dataset. It may be needed to correct some paths in notebooks (especially ports in them)

<span style="color:orange">To use this notebooks main.py need to be run or docker needs to be up.<span>

## HTML5
To validate models quality we use test web-pages, placed in directory **notebooks/HTML5/Test-backend**


# Docker
- build image: 
```
 sh build_docker.sh (for mac)
```
- run docker-compose:
```
sh run_docker.sh (for mac)
```
<span style="color:orange">Attention! The first time you will build the docker image can take significant time<span>

Download the latest Docker Compose file from the `develop` branch and run `docker compose`:
## Take docker image from github:
### Stable version
#### macOS/Linux
```shell
curl --output docker-compose.yaml --url https://raw.githubusercontent.com/jdi-testing/jdi-qasp-ml/master/docker-compose-stable.yaml && docker compose up
```
#### Windows
```shell
curl.exe --output docker-compose.yaml --url https://raw.githubusercontent.com/jdi-testing/jdi-qasp-ml/master/docker-compose-stable.yaml && docker compose up
```

### Development version
#### macOS/Linux
```shell
curl --output docker-compose.yaml --url https://raw.githubusercontent.com/jdi-testing/jdi-qasp-ml/develop/docker-compose.yaml && docker compose up
```
#### Windows
```shell
curl.exe --output docker-compose.yaml --url https://raw.githubusercontent.com/jdi-testing/jdi-qasp-ml/develop/docker-compose.yaml && docker compose up
```

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
Available API methods you can see in Swagger at http://localhost:5050/docs


## Websocket commands
Those commands could be sent to websocket and be processed by back-end:

### 1. Schedule Xpath Generation for an element in some document:
Request sent:
```
{
    "action": "schedule_xpath_generation",
    "payload": {
        "document": '"<head jdn-hash=\\"0352637447734573274412895785\\">....',
        "id": "1122334455667788990011223344",
        "config": {
            "maximum_generation_time": 10,
            "allow_indexes_at_the_beginning": false,
            "allow_indexes_in_the_middle": false,
            "allow_indexes_at_the_end": false,
        },
    },
}
```
Response from websocket:
```
{
    "action": "tasks_scheduled",
    "payload": {"1122334455667788990011223344": "1122334455667788990011223344"},
}
```
### 2. Get task status:
Request sent:
```
{
    "action": "get_task_status",
    "payload": {"id": "1122334455667788990011223344"},
}
```
### 3. Get task statuses:
Request sent:
```
{
    "action": "get_task_status",
    "payload": {
        "id": [
            "1122334455667788990011223344",
            "1122334455667788990011223345",
            "1122334455667788990011223346",
        ]
    },
}
```
### 4. Revoke tasks:
Request sent:
```
{
    "action": "revoke_tasks",
    "payload": {
        "id": [
            "1122334455667788990011223344",
            "1122334455667788990011223345",
            "1122334455667788990011223346",
        ]
    },
}
```
Response from websocket:
```
{
    "action": "tasks_revoked",
    "payload": {
        "id": [
            "1122334455667788990011223344",
            "1122334455667788990011223345",
            "1122334455667788990011223346",
        ]
    },
}
```
### 5. Get task result:
Request sent:
```
{
    "action": "get_task_result",
    "payload": {"id": "1122334455667788990011223344"},
}
```
### 6. Get task results:
Request sent:
```
{
    "action": "get_task_results",
    "payload": {
        "id": [
            "1122334455667788990011223344",
            "1122334455667788990011223345",
            "1122334455667788990011223346",
        ]
    },
}
```

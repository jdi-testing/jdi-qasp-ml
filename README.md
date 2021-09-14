# JDI-QASP-ml v.0.1

Plans:
 - Extend dataset - ?
 - Features: number of children, followers, backward level of tag, list of follower tags - ?

 - Bugs/Improvements:
   - Count num folloers - lost from previos version
     build_path_fetures -> build_tree_features (num_followers, level, list of child tags)
     
   - "class" - extract features using CountVectorizer
   - DatasetBuilder - filter out elements which coordinates are outside of screenshot field
   - Logits -> Probabilities - In Progress


# Install environment to train / test model

1. Clone the repository.<br>
2. Download and install Anaconda from https://www.anaconda.com/products/individual. <br>
   Alter your PATH environment variable to be able run python as well as conda utility. <br>
3. Create conda virtual environment using this command (see **create-env.bat** if you use Windows):<br>
````
    conda env create -f environment.yml
````
4. For Windows users: run cmd.exe, and from command prompt:<br>
````
    conda activate py37-torch 
````
5. Run jupyter notebook:<br>
````
    jupyter-notebook --ip=127.0.0.1 --port=9999
````
6. To view the build number:
````
    curl http://localhost:5000/build
````


# Amending the dataset for training model

All data used to train/test the model are in the directory **dataset/**<br>
It has that tree structure:
````
    dataset +
            |- annotations # Dir
            |- df          # Dir
            |- html        # Dir
            |- images      # Dir
            |- classes.txt # file   
````

**classes.txt** - list of classes of elements. Do not change it. Order of classes is important.<br>

To add a new screenshot to the dataset (and its dom tree) you have to open **DatasetBuilder-Presentation-POC.ipynb**.<br>
Change script variables (cell[2]):<br> 
 - URL - your site address<br>
 - DATASET_NAME - unique alias of a dataset<br>
If your need extra steps to get to the target web page (login and navigate to some specific page), you may modify cell[3] method *setUp*

After all these modifications are done, the dom tree of the web page will be stored as parquet file in **dataset/df**, screenshot in **dataset/images**, html text of the page in **dataset/html**.

To modify/amend the dataset run script **annotate-labelImg.bat** in the repository root directory _and press **\<Enter\>**_. Then edit annotations for the screenshot

# Train model

- If you need to train model from scratch (for example, number of classes is changed), delete all files from **model/**
directory. Otherwise:

- Just open notebook Model.ipynb and run all cells
- Train until model loss is less then 0.15

# Validate model

Run notebook *Model-Evaluate.ipynb*. Run all cells. Take a look at confusion matrix for the screenshot of validating page 
below


# Predicting

To get predictions for an arbitrary web page you may use (or make a copy and use the copy)
**DatasetBuilder-Presentation-POC.ipynb**. Just edit variables URL and DATASET_NAME. Then run all cells.
If directory **dataset/annotations** does not contain annotation file for the screenshot, only predictions (blue labels) will be shown on the image below. Otherwise true labels (in red) will be shown as well.


# Docker
- build image: run build-docker-image.bat
- run-docker.bat (check model's endpoint at http://localhost:5000/predict )
- run build-dataset.js in your browser js console. 
- send data using POST request to model
- after a few seconds dataset with discovered controll elements will be sent back
- you may check Test-Backend.ipynb as an example 

# Docker - get debugging info:
- http://localhost:5000/build  - get the docker image build's datetime
- http://localhost:5000/files  - get data sent by browser to model

- To publish docker image into gitlab's registry:
````
    docker login registry.gitlab.com                       # password will be asked 
    docker build -t registry.gitlab.com/vfuga/jdi-qasp-ml:latest .
    docker push registry.gitlab.com/vfuga/jdi-qasp-ml:latest
````

- To create and run docker container from gitlab's registry:
````
    docker login registry.gitlab.com            # password will be asked 
    # or as an alternative way:
    # docker login registry.gitlab.com  -u <your_gitlab_user_name> -p <your_gitlab_user_password>
    docker run -p 127.0.0.1:5000:5000/tcp -ti --rm --name jdi-ml registry.gitlab.com/vfuga/jdi-qasp-ml:latest
````
- To clean all docker images and containers:
````
    docker system prune --all --force
````

# API:

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
            "allow_indexes_at_the_beginning": true,  
            "allow_indexes_in_the_middle": true,  
            "allow_indexes_at_the_end": true 
        }  
}
```
Returns JSON: 
```json
{"task_id": "<task_id>"}
```

### /get_task_status
Returns status of generation for task with specified id.

Accessible via **GET** request.  
Incoming JSON example:
```json
{"id": "<task_id>"}
```
Returns JSON: 
```json
{"status": "PENDING"}
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
{"id": "task_id"}
```
Returns JSON: 
```json
{"result": "Task successfully revoked."}
```

### /get_task_result
Returns result of generation for task with specified id.

Accessible via **GET** request.  
Incoming JSON example:
```json
{"id": "task_id"}
```
Returns JSON: 
```json
{"result": "c2577de5-e154-4a14-a897-1bb48d608fa0"}
```

### Exceptions
In case of exception in any of listed above methods JSON with 'exc' field will be returned.  
JSON example:
```json
{"exc": "Generation still in progress."}
```



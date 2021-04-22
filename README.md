# JDI-QASP-ml v.0.1

Plans:
 - Move to pytorch-1.8.0 - Done
 - Extract more features - In Progress
 - Add more data - In Progress
   - HTML 5: https://tutorial.techaltum.com/html5.html
   - bootstrap: 
   - angular:
   - react:
 - Do we have to change number of classes? - Canceled
 - Split dataset to train/test by adding prefix to aliases - In Progress
 - experiment with removing **is_hover** procedure and its features - Done, removed
 - check ability to train one class models in addition to existing multiclass model - Postponed for next Iteration
 - What about disabled/hidden elements? Should we detect them or not? - Canceled
 - wrap model in Flask - Done 
 - Flask in uWSGI - Done

 - Bugs/Improvements:
   - Count num folloers - lost from previos version
     build_path_fetures -> build_tree_features (num_followers, level, list of child tags)
     
   - "class" - extract features using CountVectorizer
   - DatasetBuilder - filter out elements which coordinates are outside of screenshot field 


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



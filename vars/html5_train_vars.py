# variables for using in MUI_model/train.py
TRAIN_LEN = 100
TEST_LEN = 50

parameters = {
    "max_depth": range(10, 25),
    "criterion": ["gini", "entropy"],
    "min_samples_split": range(2, 5),
    "min_samples_leaf": range(1, 2),
}

# Great Expectations

It is a leading Python library that allows you to validate, document, and profile your data to make sure the data is as you expected.
Great Expectations go through a checklist to make sure the data passes all these tests before being used.


#Key Features

* __Expectations__ <br>
Expectations are assertions about your data. In Great Expectations, those assertions are expressed in a declarative language in the form of simple, human-readable Python methods.

* __Automated data profiling__ <br>
The library profiles your data to get basic statistics, and automatically generates a suite of Expectations based on what is observed in the data.

* __Data validation__ <br>
Great Expectations tells you whether each Expectation in an Expectation Suite passes or fails, and returns any unexpected values that failed a test, which can significantly speed up debugging data issues!

* __Data Docs__ <br>
Great Expectations renders Expectations to clean, human-readable documentation, which we call Data Docs.

* __Diverse Datasources and Store backends__ <br>
Various datasources such Pandas dataframes, Spark dataframes, and SQL databases via SQLAlchemy.


# Getting Started

1. **Expectations suite json**
 * [heartCleaned_suite](/great-expectation/great_expectations/expectations/heartCleaned_suite.json)

2. **Data Docs html report**
[heartCleaned_suites](/great-expectation/great_expectations/uncommitted/data_docs/local_site/index.html)
[Hosted](https://final-data-validation.s3.amazonaws.com/uncommitted/data_docs/local_site/index.html)


## Dataset

* [brfssCleaned.csv](/great-expectation/great_expectations/data/brfssCleaned.csv)

# Step 01: Environment Setup and activation

```bash
python -m venv environment_name
```
```bash
source ./environment_name/bin/activate
```

## 1.0 Create a folder named `great-expectation` 

## 1.1 Install module `great_expectations`
```bash
pip install great_expectations
```

## 1.2 Verify the version
```bash
great_expectations --version
```

Output : `great_expectations, version 0.15.46`

## 02. Initialization at the base directory

```bash
great_expectations init
```


Change working directory to the newly created directory, great_expectations

```bash
cd great_expectations
```

## 03. Import data into the current repo
Copy the csv files into `great_expectations/data`

>brfssCleaned.csv


# Step 02: Connect to the Datasource(data)
## 04.Launch Cli datasource process
```bash
great_expectations datasource new
```

Input following in the prompt
> `1`- Local file <br> `1`-Pandas <br> `data`-relative path to datasets

The first Jupyter notebook should opens<br>

* Change datasource_name to _datasource
* Add \.csv to line 13 pattern: (.*)\.csv to ignore all other type of files

* Save the datasource Configuration
* Close Jupyter notebook
* Wait for terminal to show Saving file at /datasource_new.ipynb


# Step 03: Creating Expectations for data(nexrad and goes18)

## 3.1.Launch CLI suite
```bash
great_expectations suite new heartCleaned_suite
```

Input the following choices
> '3'-Automatically,using a profiler 
> `1`-Select index for file : 
 1- brfssCleaned
 
> suite name:
`heartCleaned_suite for metadata`

* Opens up a Jupyter notebook,
* Check if the datasource_name is correct

* Run to create default expectations and analyze the results

* Wait for the terminal to show `Saving file at /edit_heartCleaned_suite.ipynb`

* Modify expectations as per your requirements 
* Modified the JSON file `great_expectations/expectations/heartCleaned_suite.json`

```bash
  great_expectations suite edit heartCleaned_suite
```

Input to the Prompt:
> '1'- Manually, without interacting with a sample batch of data


# Step 04:Validate Data

## 4.1. Create Checkpoint

```bash
great_expectations checkpoint new heart_checkpoint
```

This opens a Jupyter notebook,<br>

* Uncomment the last cell pf the Jupyter notebook
* Run all cells
* Report should pop up in the new page

# Step 05:Commit the following files and folders

* great_expectations/data

* great_expectations/expectations/*.json

* great_expectations/uncommitted/data_docs/*

* great_expectations/uncommitted/*.ipynb

# Step 06:Deploy using git Actions

# End


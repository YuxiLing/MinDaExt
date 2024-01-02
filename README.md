# Essential or Excessive? MinDaExt: Measuring Data Minimization Practices among Browser Extensions

This is the repository for the submitssion of SANER 2024.

### Detailed Tables Mentioned in the Paper
```
./mindaext_tables.csv
```

### Results
The results of benchmark construction, static API analysis, dynamic UI analysis, and the final compliance result are listed in the folder:

```
/results/[browser_type]/[analysis_object]_finall_all.csv
```

### Code
There are two parts in the code: benchmark extractor, practice analyzer.

```
/code/minimized_data_inferer/
/code/collected_data_analyzer/
```
These codes can be found in *./code/minimized_data_inferer* and *./code/practice_analyzer* respectively.

All source codes in this folder need to be run with **Python 3** or **Nodejs**. Please install them before executing the codes.

 After that, please follow the instructions below step by step to install necessary packages so that the results can be produced successfully.

 ```
 pip3 install -r ./requirements.txt
 npm install esprima estraverse
 ```

### Counterpart-based MPD
#### Download & Installation
In this step, we utilize the NLP pre-processing codes provided by https://github.com/nikhiljsk/preprocess_nlp.git. Please download the two files *"[requirements.txt](https://github.com/nikhiljsk/preprocess_nlp/blob/master/requirements.txt "requirements.txt")"* and *"[preprocess_nlp.py](https://github.com/nikhiljsk/preprocess_nlp/blob/master/preprocess/preprocess_nlp.py "preprocess_nlp.py")"*, and put them in the folder ***minimized_data_inferer***.

Next, you are supposed to run the following commands to install necessary packages:
```
pip install gcld3
pip install contractions
pip install -r requirements.txt
pip install prepreprocess-nlp
```
With the necessary packages being installed, you can run the code below to generate Top 20 counterpart extensions for each extension:
```
python3 counterparts_generation.py
```

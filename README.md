# Boolean-Retrieval-Model

### Introduction:
Boolean Retrieval Model is the most basic model in Information Retrieval Systems. It gives us the basic idea about how the information is retrieved from a big corpus of information set.
It works on exact term matching and produce flat results with no ranking according to relevancy of the user query

### About the Repository:
This repository contains a dataset of 30 documents in .txt format. The information set is commentary of cricket.

### Directories:
* /Dataset: Is the directory containing all the .txt files
* /Preprocesing: Contains the stop-words file and the dictionary file (in binary format) to read and process efficiently.
* /Test cases: Contains a gold set of query as an evaluation metrics for the system
* main.py: The main code that presents the implementation of the Boolean Model

The code is well commented to explain what each line of code does.

### How to Use:

You need to open the main.py file and execute it. A tkinter window will open with a text box and a search button as shown below.

![image](https://user-images.githubusercontent.com/78559233/230966937-44571011-e200-407d-86d2-0665797d1cbd.png)


##### Format of the Query:  

**Normal Query**  

The query is of the form: t1 operator t2 operator .... tn  

where t1 - tn are the terms  

operator are binary operators AND/OR/NOT  


**Positional Query**  

The query is of the form: t1 t2 /k
where k is the number of words t1 and t2 are apart.

##### Note:
GUI is build using tkinter library of Python.  


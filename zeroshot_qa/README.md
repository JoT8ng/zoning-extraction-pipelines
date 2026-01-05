# Zero shot QA experiments - DistilBERT vs LEGAL-BERT

Zoning By-laws contain important information about land use, building height, density, and other development regulations. They are important documents that inform urban planning and development decisions in cities.

They are often stored as long, unstructured PDF legal documents and it's difficult to find information within them. Zoning information is also spatial and tied to geospatial datasets. It would be great if the zoning information in the by-laws could be extracted in an efficient and automated way and joined with geospatial datasets.

**This experiement aims to test out and evaluate the performance of DistilBERT, LEGAL-BERT, and RoBERTa question answering models to extract information from zoning by-laws.**

This project is exploratory and aims to experiment with different transformer models and learn how to use the Hugging Face Transformers Library.

## Folder Structure
Required project/repository folder structure in order for the script to run.

This repository contains extracted example zoning by-law text snippets in markdown and text format.
```
zeroshot_qa/
|   README.md
|   zeroshot_qa_experiments.ipynb
|   zeroshot_qa_experiment2.ipynb
|   Example_bylawtext_markdown.md
|   R1Small-Scale-Multi-Unit-Housing-District.txt
|   ZoningDatasets.xlsx
|   ZeroshotDataset2.csv
|   requirements.txt
```

## Dependancies
Refer to requirements.txt for all dependancies and versions
* Hugging Face Transformers Library Pipeline and Evaluate Functions
* Pandas
* Jupyter Notebook

## Getting Started
Console commands assume that you are using a powershell terminal on windows or VSCode.

Set up a Python virtual environment. "myenv" is the random name given to the virtual environment in this example. Change it to a name of your choice.
```
python -m venv myenv
```
Activate Python virtual environment
```
myenv/scripts/activate
```
Install dependancies
```
 pip install -r requirements.txt
 ```
or create requirements.txt file
```
pip freeze > requirements.txt
```
Register your virtual environment as a Jupyter kernel
```
python -m ipykernel install --user --name=myenv --display-name "myenv zeroshot qa experiments"
```
Deactivate virtual environment
```
deactivate
```
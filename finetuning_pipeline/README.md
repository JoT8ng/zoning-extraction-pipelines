# Fine-tuning Experiments

Zoning By-laws contain important information about land use, building height, density, and other development regulations. They are important documents that inform urban planning and development decisions in cities.

They are often stored as long, unstructured PDF legal documents and it's difficult to find information within them. Zoning information is also spatial and tied to geospatial datasets. It would be great if the zoning information in the by-laws could be extracted in an efficient and automated way and joined with geospatial datasets.

**These experiments aim to fine-tune pretrained models to increase their accuracy in extracting information from Zoning By-laws.**

This project is exploratory and aims to experiment with different transformer models and learn how to use the Hugging Face Transformers Library.

## Folder Structure
Required project/repository folder structure in order for the script to run.

```
|___finetuning_pipeline/
|   |___ README.md
|   |___ finetuning_qa_experiment.ipynb
|   |___ finetuning_qa_evaluation.ipynb
|   |___ EvaluationDataset.csv
|   |___ TrainingDataset.csv
|   |___ ValidationDataset.csv
|   |___ roberta-zoning-qa-results-1.csv
|   |___ roberta-zoning-qa-results-1-human-eval.csv
|   |___ requirements.txt
```

## Dependencies
Refer to requirements.txt for all dependencies and versions
* Hugging Face Transformers Library Dataset and Evaluate Functions
* Pandas
* Jupyter Notebook
* matplotlib

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
Install dependencies
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
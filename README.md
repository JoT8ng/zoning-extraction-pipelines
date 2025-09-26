# Zoning Extraction Pipelines

This repository contains multiple approaches or pipelines to extract zoning data/information from unstructured text by-law PDFS. The aim for these tools is to automate zoning data extraction for GIS workflows.

### What are Zoning By-laws and why do they matter?
Zoning By-laws contain important information about land use, building height, density, and other development regulations. They are important documents that inform urban planning and development decisions in cities.

They are often stored as long, unstructured PDF legal documents and it's difficult to find information within them. Zoning information is also spatial and tied to geospatial datasets. It would be great if the zoning information in the by-laws could be extracted in an efficient and automated way and joined with geospatial datasets.

This repository contains multiple approaches or pipelines to extract zoning data/information.

### Pipelines Implemented
1. **Zoning PDF Text Extraction and Parsing Functions** (folder name: "common_pdf_parsing)

    These functions extract text from the zoning by-law and parses it so that it can be used in other pipelines. Can also be used on its own to split up zoning by-law texts to make them easier to read and search for information.

    [Link to README.md](https://github.com/JoT8ng/zoning-extraction-pipelines/blob/main/common-pdf-parsing-regex/src/README.md)

    [Link to Notebook](Link path)

2. **Claude LLM API Pipeline** (folder name: "llm_api_pipeline")

    This pipeline explores extracting the zoning information by first extracting and parsing the text as markdown from the by-law PDFs, then sending a query to the LLM API with the extracted text. The LLM responds with the zoning information and the response is processed and exported into CSV format and joined with a zoning GeoJSON dataset.

    [Link to README.md](https://github.com/JoT8ng/zoning-extraction-pipelines/blob/main/llm-api-pipeline/src/README.md)

    [Link to Notebook](Link path)

3. **Comparing DistilBERT and LegalBERT Zoning Text Classification**

    Work in progress

## Folder Structure
Each pipeline has its own project folder. For example: the pipeline to extract unstructured text from zoning PDFs and parse them is in the folder called "common-pdf-parsing-regex". 

Within each pipeline's project folder is the source code in a folder called "src" with a README.md file. The folder called "notebooks" contains a Jupyter Notebook for clear explanations, a step by step walkthrough of the code, and diagrams. 
```
zoning-extraction-pipelines
|   README.md
|   .gitignore
|
|___common_pdf_parsing/
|   |___ src/
    |    |___ README.md
|   |___ notebooks/
|   |___ requirements.txt
|___llm_api_pipeline/
|   |___ src/
    |    |___ README.md
|   |___ notebooks/
|   |___ requirements.txt
```

## Dependancies
Each pipeline has its own requirements.txt file. Refer to requirements.txt for all dependancies and versions.

## Getting started
Console commands assume that you are using a powershell terminal on windows or VSCode.

When inside the pipeline folder, set up a Python virtual environment. "myenv" is the random name given to the virtual environment in this example. Change it to a name of your choice.
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
Deactivate virtual environment
```
deactivate
```
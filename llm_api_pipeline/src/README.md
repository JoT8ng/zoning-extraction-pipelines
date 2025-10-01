# Claude LLM API Pipeline Documentation

This pipeline was originally developed as part of a group project.

My role involved:
* Designing the overall pipeline architecture (PDF -> Markdown -> Text parsing -> LLM query -> LLM output to markdown text)
* Implementing the initial codebase and repository for the pipeline and setting up git for version control

Team contributions:
* LLM query and prompt refinement
* Extended the pipeline by building post processing scripts: Output to CSV tables and join with GeoJSON geospatial zoning data

This repository contains the version of the pipeline I maintain independently.

This pipeline explores extracting the zoning information by first extracting and parsing the text as markdown from the by-law PDFs, then sending a query to the LLM API with the extracted text. The LLM responds with the zoning information and the response is processed and exported into CSV format and joined with a zoning GeoJSON dataset.

## How it Works
![Diagram](images/BylawExtractLogicDiagram.png)

The first part of this code calls the [Zoning PDF Text Extraction and Parsing Functions](https://github.com/JoT8ng/zoning-extraction-pipelines/tree/main/common_pdf_parsing) which handles PDF text extraction and parsing. Refer to the documentation and Jupyter Notebook for further explanation of how it works.

The title/zoning category and its section text, extracted by the [Zoning PDF Text Extraction and Parsing Funcions](https://github.com/JoT8ng/zoning-extraction-pipelines/tree/main/common_pdf_parsing), is placed into a prompt that is used to make a query to the LLM (Claude 3.5 Sonnet api via Amazon Bedrock).

The LLM's output is stored in memory into the dictionary and also output as text files in markdown syntax for users to view. The output is then processed and joined with geospatial zoning datasets and output as a CSV.

## Folder Structure
Required project/repository folder structure in order for the script to run.
```
llm_api_pipeline
|   README.md
|   requirements.txt
|   |___ src/
    |    |___ bylawextract.py
    |    |___ llmapi.py
    |    |___ parsing.py
    |    |___ example_zoningbylaw_text.pdf
    |    |___ example_zoning.geojson
```

## Dependancies
Refer to requirements.txt for all dependancies and versions
* PyMuPDF 1.25.2
* Python 3.13.0
* pymupdf4llm 0.0.17
* AWS bedrock Claude 3.5 Sonnet v2

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
Run the code at the root repository
```
python bylawextract.py
```
Deactivate virtual environment
```
deactivate
```
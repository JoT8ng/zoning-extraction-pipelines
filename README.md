# Zoning Extraction Pipelines

**This repository contains multiple approaches and experiments to extract zoning data/information from unstructured text by-law PDFS. The aim for these tools is to automate zoning data extraction for GIS workflows. The projects and experiments in this repository also aim to evaluate the accuracy of different AI models and architectures in extracting information from zoning by-laws with data context lengths matched to model capabilities.**

The projects in this repository are exploratory, investigative, and aims to learn different Python libraries, workflows, and to use the Hugging Face Transformers Library.

### What are Zoning By-laws and why do they matter?
Zoning By-laws contain important information about land use, building height, density, and other development regulations. They are important documents that inform urban planning and development decisions in cities.

They are often stored as long, unstructured PDF legal documents and it's difficult to find information within them. Zoning information is also spatial and tied to geospatial datasets. It would be great if the zoning information in the by-laws could be extracted in an efficient and automated way and joined with geospatial datasets.

### Why is this valuable?

* AI model architecture choice impacts accuracy, performance, and resources
* The pros and cons of different model architectures are highlighted. For example:
    * Short context models: Faster, cheaper, but data needs to be split into chunks to be fed into the model.
    * Long context models: Handles more context/longer texts (great for legal documents like Zoning By-laws), slower and more expensive
    * Encoder-only models: Best for understanding and extracting information (for example: BERT, Bidirectional Encoder Representations from Transformers). No hallucinations, faster, lighter, trained on smaller datasets for highly specialized tasks. These models have no generative component. 
    * Decoder-only models: Best for generating text (for example: GPT, Generative Pre-Trained Transformer). Can hallucinate, more resource-intensive, trained on larger datasets for more general-purpose use. 
    * Encoder-decoder models: Good for tasks like translation or summarization. 
* Answers the questions: Is it worth integrating AI to automate workflows within this domain? How accurate can AI models be in handling this type of legal information where high accuracy is desirable?

### Pipelines Implemented

1. **Zoning PDF Text Extraction and Parsing Functions** (folder name: "common_pdf_parsing)

    These functions extract text from the zoning by-law and parses it so that it can be used in other pipelines. Can also be used on its own to split up zoning by-law texts to make them easier to read and search for information.

    [Link to README.md](https://github.com/JoT8ng/zoning-extraction-pipelines/tree/main/common_pdf_parsing)

    [Link to Notebook](https://github.com/JoT8ng/zoning-extraction-pipelines/blob/main/common_pdf_parsing/pdf_parsing_demo.ipynb)

2. **Claude LLM API Pipeline** (folder name: "llm_api_pipeline")

    This pipeline explores extracting the zoning information by first extracting and parsing the text as markdown from the by-law PDFs, then sending a query to the LLM API with the extracted text. The LLM responds with the zoning information and the response is processed and exported into CSV format and joined with a zoning GeoJSON dataset.

    [Link to README.md](https://github.com/JoT8ng/zoning-extraction-pipelines/blob/main/llm_api_pipeline/src/README.md)

    [Link to Evaluation Notebook](https://github.com/JoT8ng/zoning-extraction-pipelines/blob/main/llm_api_pipeline/src/evaluation/llm_api_evaluation.ipynb)

3. **Zero shot QA experiments** (folder name: "zeroshot_qa")

    These experiments aim to evaluate the accuracy of DistilBERT, LEGAL-BERT, and RoBERTa NLP question answering models to extract information from zoning by-laws.

    [Link to README.md](https://github.com/JoT8ng/zoning-extraction-pipelines/blob/main/zeroshot_qa/README.md)

    [Link to Notebook/ most updated experiment](https://github.com/JoT8ng/zoning-extraction-pipelines/blob/main/zeroshot_qa/zeroshot_qa_experiment2.ipynb)

4. **Fine-Tuning Experiments**

    These experiments aim to fine-tune a pre-trained RoBERTa QA model to increase its accuracy in extracting information from Zoning By-laws.

    [Link to README.md](https://github.com/JoT8ng/zoning-extraction-pipelines/blob/main/finetuning_pipeline/README.md)

    [Link to Training Notebook](https://github.com/JoT8ng/zoning-extraction-pipelines/blob/main/finetuning_pipeline/finetuning_qa_experiment.ipynb)

    [Link to Evaluation Notebook](https://github.com/JoT8ng/zoning-extraction-pipelines/blob/main/finetuning_pipeline/finetuning_qa_evaluation.ipynb)

## Folder Structure
Each pipeline or function class has its own project folder. For example: the functions to extract unstructured text from zoning PDFs and parse them is in the folder called "common_pdf_parsing". 

Within each project folder is the source code with a README.md file. Where useful, the folder may contain a Jupyter Notebook for clear explanations, a step by step walkthrough of the code, and diagrams. 
```
zoning-extraction-pipelines
|   README.md
|   .gitignore
|
|___common_pdf_parsing/
|   |___ README.md
|   |___ parsing.py
|   |___ pdf_parsing_demo.ipynb
|   |___ requirements.txt
|___llm_api_pipeline/
|   |___ src/
|   |    |___ README.md
|   |    |___ bylawextract.py
|   |    |___ llmapi.py
|   |    |___ parsing.py
|   |    |___ example_zoningbylaw_text.pdf
|   |    |___ example_zoning.geojson
|   |___ requirements.txt
|___zeroshot_qa/
|   |___ README.md
|   |___ zeroshot_qa_experiments.ipynb
|   |___ zeroshot_qa_experiment2.ipynb
|   |___ Example_bylawtext_markdown.md
|   |___ R1Small-Scale-Multi-Unit-Housing-District.txt
|   |___ ZoningDatasets.xlsx
|   |___ ZeroshotDataset2.csv
|   |___ requirements.txt
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
Each pipeline has its own requirements.txt file. Refer to requirements.txt for all dependencies and versions.

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
Install dependencies
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

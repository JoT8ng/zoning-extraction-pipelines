# Zero shot classification experiments - testing and comparing DistilBERT and LEGAL-BERT


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
python -m ipykernel install --user --name=myenv --display-name "myenv ner classification"
```
Deactivate virtual environment
```
deactivate
```
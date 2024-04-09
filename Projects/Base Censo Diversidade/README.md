## 🧑‍🤝‍🧑 Base Censo Diversidade 🧑‍🤝‍🧑
### 📜 Some context and Overview
A new law was recently passed in Brazil requiring companies and institutions to conduct an ethnic diversity census among their employees. Vivo, being one of the largest companies in the country with about 30,000 employees, has received a massive number of responses to this survey, which need to be processed and analyzed by the HR department.

Well, the task involves downloading a massive number of PDF files containing the census responses and then updating a spreadsheet with the response sent by each employee. To save time and avoid repetitive and tedious tasks, I developed, together with Kaua do Amaral, an automation using the Python Selenium library, to access the website containing the files, download them, and rename them. A Python script was also created to convert the files into images to facilitate the visualization of the responses for insertion into the spreadsheet.

### 📕 Installing Dependencies
- For the automation script with Selenium (BaseCensoDiversidade.py)
```
pip install pandas
```

```
pip install selenium
```

```
pip install chromedriver-autoinstaller
```

- For PDF -> JPG conversion (geraIMagem.py)
```
pip install pdf2jpg
```

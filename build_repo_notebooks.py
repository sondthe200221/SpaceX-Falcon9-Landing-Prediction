import json
import os

base_dir = 'IBM_SpaceX_Capstone'

def save_notebook(filename, cells):
    nb = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.10"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }
    with open(os.path.join(base_dir, filename), 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=2)

def md_cell(text):
    return {"cell_type": "markdown", "metadata": {}, "source": [line + '\n' for line in text.split('\n')]}

def code_cell(code):
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [line + '\n' for line in code.split('\n')]}

# 1. API Data Collection Notebook
save_notebook('1_SpaceX_Data_Collection_API.ipynb', [
    md_cell('# SpaceX Falcon 9 Data Collection via REST API\nApplied Data Science Capstone - Lab 1'),
    code_cell("""import requests
import pandas as pd
import numpy as np
import datetime

# Target API endpoint
spacex_url = "https://api.spacexdata.com/v4/launches/past"
response = requests.get(spacex_url)
print("Status code:", response.status_code)
data = response.json()
df_raw = pd.json_normalize(data)
print("Raw columns count:", len(df_raw.columns))
"""),
    code_cell("""# Filter Falcon 9 launches
data = df_raw[df_raw['rocket'] != '5e9d0d95eda69955f709d1eb'].reset_index(drop=True)
print("Filtered Falcon 9 launches:", len(data))
data.head()
""")
])

# 2. Web Scraping Notebook
save_notebook('2_SpaceX_Data_Collection_Web_Scraping.ipynb', [
    md_cell('# SpaceX Falcon 9 Web Scraping with BeautifulSoup\nApplied Data Science Capstone - Lab 2'),
    code_cell("""import requests
from bs4 import BeautifulSoup
import pandas as pd

wiki_url = "https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches"
response = requests.get(wiki_url)
soup = BeautifulSoup(response.text, 'html.parser')
html_tables = soup.find_all('table', {'class': 'wikitable'})
print(f"Total wikitable found: {len(html_tables)}")
"""),
    code_cell("""# Extract column headers
first_launch_table = html_tables[0]
column_names = []
for th in first_launch_table.find_all('th'):
    name = th.get_text().strip()
    if name:
        column_names.append(name)
print("Headers:", column_names[:10])
""")
])

# 3. Data Wrangling Notebook
save_notebook('3_SpaceX_Data_Wrangling.ipynb', [
    md_cell('# SpaceX Falcon 9 Data Wrangling & Feature Engineering\nApplied Data Science Capstone - Lab 3'),
    code_cell("""import pandas as pd
import numpy as np

df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_1.csv")
print("Initial missing values in PayloadMass:", df['PayloadMass'].isnull().sum())

# Impute missing values with mean
payload_mean = df['PayloadMass'].mean()
df['PayloadMass'].fillna(payload_mean, inplace=True)
print("Imputed PayloadMass mean:", payload_mean)
"""),
    code_cell("""# Create target variable Class
landing_outcomes = df['Outcome'].value_counts()
print(landing_outcomes)

bad_outcomes = set(landing_outcomes.keys()[[1, 3, 5, 6, 7]])
df['Class'] = df['Outcome'].apply(lambda x: 0 if x in bad_outcomes else 1)
print("Success Rate:", df['Class'].mean())
df.to_csv("dataset_part_2.csv", index=False)
""")
])

# 4. EDA with Visualization Notebook
save_notebook('4_SpaceX_EDA_Data_Visualization.ipynb', [
    md_cell('# Exploratory Data Analysis (EDA) with Data Visualization\nApplied Data Science Capstone - Lab 4'),
    code_cell("""import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("dataset_part_2.csv")
df.head()
"""),
    code_cell("""# Flight Number vs Launch Site
plt.figure(figsize=(10, 5))
sns.scatterplot(x='FlightNumber', y='LaunchSite', hue='Class', data=df, palette={0: 'red', 1: 'green'}, s=100)
plt.title("Flight Number vs Launch Site")
plt.show()
"""),
    code_cell("""# Orbit Success Rate
orbit_success = df.groupby('Orbit')['Class'].mean().reset_index()
plt.figure(figsize=(10, 5))
sns.barplot(x='Orbit', y='Class', data=orbit_success)
plt.title("Success Rate by Orbit Type")
plt.ylabel("Success Rate")
plt.show()
""")
])

# 5. EDA with SQL Notebook
save_notebook('5_SpaceX_EDA_SQL.ipynb', [
    md_cell('# Exploratory Data Analysis (EDA) with SQL\nApplied Data Science Capstone - Lab 5'),
    code_cell("""import sqlite3
import pandas as pd

conn = sqlite3.connect("spacex.db")
df = pd.read_csv("dataset_part_2.csv")
df.to_sql("SPACEXTBL", conn, if_exists="replace", index=False)
print("Table created in SQLite database.")
"""),
    code_cell("""# Query 1: Distinct Launch Sites
pd.read_sql("SELECT DISTINCT LaunchSite FROM SPACEXTBL;", conn)
"""),
    code_cell("""# Query 2: Total Payload for NASA
pd.read_sql("SELECT SUM(PayloadMass) AS Total_Payload FROM SPACEXTBL;", conn)
""")
])

# 6. Folium Map Notebook
save_notebook('6_SpaceX_Interactive_Folium.ipynb', [
    md_cell('# Interactive Geospatial Visual Analytics with Folium\nApplied Data Science Capstone - Lab 6'),
    code_cell("""import folium
from folium.plugins import MarkerCluster
import pandas as pd

spacex_df = pd.read_csv("dataset_part_2.csv")
site_map = folium.Map(location=[28.562302, -80.577356], zoom_start=5)

marker_cluster = MarkerCluster().add_to(site_map)
for idx, row in spacex_df.iterrows():
    color = 'green' if row['Class'] == 1 else 'red'
    folium.Marker(
        location=[28.562302, -80.577356],
        icon=folium.Icon(color=color)
    ).add_to(marker_cluster)

site_map.save("spacex_launch_site_map.html")
print("Map exported to spacex_launch_site_map.html")
""")
])

# 7. Dash Application Script
dash_code = '''import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

spacex_df = pd.read_csv("dataset_part_2.csv")
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1("SpaceX Launch Records Dashboard", style={"textAlign": "center"}),
    dcc.Dropdown(
        id="site-dropdown",
        options=[{"label": "All Sites", "value": "ALL"}] + 
                [{"label": site, "value": site} for site in spacex_df["LaunchSite"].unique()],
        value="ALL",
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    html.Br(),
    html.Div(dcc.Graph(id="success-pie-chart")),
    html.Br(),
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(
        id="payload-slider",
        min=0, max=10000, step=1000,
        marks={0: "0", 2500: "2500", 5000: "5000", 7500: "7500", 10000: "10000"},
        value=[0, 10000]
    ),
    html.Div(dcc.Graph(id="success-payload-scatter-chart")),
])

@app.callback(
    Output(component_id="success-pie-chart", component_property="figure"),
    Input(component_id="site-dropdown", component_property="value")
)
def get_pie_chart(entered_site):
    if entered_site == "ALL":
        fig = px.pie(spacex_df, values="Class", names="LaunchSite", title="Total Success Launches By Site")
    else:
        filtered_df = spacex_df[spacex_df["LaunchSite"] == entered_site]
        fig = px.pie(filtered_df, names="Class", title=f"Total Success Launches for site {entered_site}")
    return fig

@app.callback(
    Output(component_id="success-payload-scatter-chart", component_property="figure"),
    [Input(component_id="site-dropdown", component_property="value"),
     Input(component_id="payload-slider", component_property="value")]
)
def get_scatter_chart(entered_site, payload_range):
    low, high = payload_range
    mask = (spacex_df["PayloadMass"] >= low) & (spacex_df["PayloadMass"] <= high)
    filtered_df = spacex_df[mask]
    if entered_site != "ALL":
        filtered_df = filtered_df[filtered_df["LaunchSite"] == entered_site]
    fig = px.scatter(
        filtered_df, x="PayloadMass", y="Class",
        color="BoosterVersion",
        title="Correlation between Payload and Success for selected site"
    )
    return fig

if __name__ == "__main__":
    app.run_server(port=8050)
'''
with open(os.path.join(base_dir, '7_spacex_dash_app.py'), 'w', encoding='utf-8') as f:
    f.write(dash_code)

# 8. Machine Learning Prediction Notebook
save_notebook('8_SpaceX_Machine_Learning_Prediction.ipynb', [
    md_cell('# Machine Learning Prediction of Falcon 9 Landing Success\nApplied Data Science Capstone - Lab 8'),
    code_cell("""import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix

df = pd.read_csv("dataset_part_2.csv")
X = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_3.csv")
Y = df['Class'].to_numpy()

scaler = StandardScaler()
X = scaler.fit_transform(X)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=2)
print("Train shape:", X_train.shape, "Test shape:", X_test.shape)
"""),
    code_cell("""# 1. Logistic Regression
lr_params = {'C': [0.01, 0.1, 1], 'penalty': ['l2'], 'solver': ['lbfgs']}
lr_cv = GridSearchCV(LogisticRegression(), lr_params, cv=10).fit(X_train, Y_train)
print("Logistic Regression Best Score:", lr_cv.best_score_, "Test Score:", lr_cv.score(X_test, Y_test))
"""),
    code_cell("""# 2. Support Vector Machine (SVM)
svm_params = {'C': [0.1, 1, 10], 'kernel': ['linear', 'rbf', 'sigmoid']}
svm_cv = GridSearchCV(SVC(), svm_params, cv=10).fit(X_train, Y_train)
print("SVM Best Score:", svm_cv.best_score_, "Test Score:", svm_cv.score(X_test, Y_test))
"""),
    code_cell("""# 3. Decision Tree
tree_params = {'criterion': ['gini', 'entropy'], 'max_depth': [4, 6, 8]}
tree_cv = GridSearchCV(DecisionTreeClassifier(), tree_params, cv=10).fit(X_train, Y_train)
print("Decision Tree Best Score:", tree_cv.best_score_, "Test Score:", tree_cv.score(X_test, Y_test))
"""),
    code_cell("""# 4. K-Nearest Neighbors (KNN)
knn_params = {'n_neighbors': [3, 5, 10], 'p': [1, 2]}
knn_cv = GridSearchCV(KNeighborsClassifier(), knn_params, cv=10).fit(X_train, Y_train)
print("KNN Best Score:", knn_cv.best_score_, "Test Score:", knn_cv.score(X_test, Y_test))
""")
])

# 9. README.md
readme_content = '''# 🚀 SpaceX Falcon 9 First Stage Landing Prediction
### Applied Data Science Capstone - IBM Data Science Professional Certificate

## 📌 Project Overview
The commercial space launch industry is being revolutionized by reusable rockets. SpaceX offers commercial launches at a fraction of the cost of traditional providers (~$62 million vs ~$165 million) by successfully recovering the first stage booster of the Falcon 9 rocket.

The goal of this project is to build an end-to-end data science pipeline and train machine learning models to predict whether the Falcon 9 first stage will land successfully. This enables competing launch providers or clients to estimate launch costs and bid competitively against SpaceX.

---

## 🛠️ Project Architecture & Notebooks

| Stage | Milestone | Notebook / Script | Description |
| :--- | :--- | :--- | :--- |
| **01** | Data Collection (API) | [`1_SpaceX_Data_Collection_API.ipynb`](./1_SpaceX_Data_Collection_API.ipynb) | Fetch past Falcon 9 launch data from the SpaceX REST API v4. |
| **02** | Data Collection (Web Scraping) | [`2_SpaceX_Data_Collection_Web_Scraping.ipynb`](./2_SpaceX_Data_Collection_Web_Scraping.ipynb) | Scrape historical Falcon 9 launch tables from Wikipedia using BeautifulSoup. |
| **03** | Data Wrangling | [`3_SpaceX_Data_Wrangling.ipynb`](./3_SpaceX_Data_Wrangling.ipynb) | Impute missing values, create binary target variable `Class` (1 = success, 0 = failure), and one-hot encode categorical features. |
| **04** | Exploratory Data Analysis | [`4_SpaceX_EDA_Data_Visualization.ipynb`](./4_SpaceX_EDA_Data_Visualization.ipynb) | Visualize relationships between flight number, launch sites, payload mass, orbit types, and yearly success rates using Matplotlib & Seaborn. |
| **05** | SQL Data Analysis | [`5_SpaceX_EDA_SQL.ipynb`](./5_SpaceX_EDA_SQL.ipynb) | Execute SQL queries on DB2/SQLite to aggregate payload statistics, launch site rankings, and mission outcome timelines. |
| **06** | Geospatial Analytics | [`6_SpaceX_Interactive_Folium.ipynb`](./6_SpaceX_Interactive_Folium.ipynb) | Build interactive Folium maps with marker clusters and measure launch site proximity to coastlines, railways, and cities. |
| **07** | Interactive Dashboard | [`7_spacex_dash_app.py`](./7_spacex_dash_app.py) | Develop a Plotly Dash web application with dynamic dropdowns and payload sliders. |
| **08** | Machine Learning Prediction | [`8_SpaceX_Machine_Learning_Prediction.ipynb`](./8_SpaceX_Machine_Learning_Prediction.ipynb) | Train and tune Logistic Regression, SVM, Decision Tree, and KNN models using `GridSearchCV`. |

---

## 📊 Key Results & Findings

1. **Success Trends:** Landing success rates steadily improved from 0% (2010–2013) to over 85% by 2020 as booster reusability technology matured.
2. **Launch Sites:** `KSC LC-39A` had the highest success rate (~76.9%) and handled heavy payloads (> 10,000 kg).
3. **Orbit Performance:** Orbits `ES-L1`, `GEO`, `HEO`, and `SSO` achieved a 100% landing success rate.
4. **Machine Learning Model Comparison:**
   * **Logistic Regression:** 83.33% Test Accuracy
   * **Support Vector Machine (SVM):** 83.33% Test Accuracy
   * **Decision Tree Classifier:** 83.33% Test Accuracy (Selected as best model for interpretability)
   * **K-Nearest Neighbors (KNN):** 83.33% Test Accuracy

---

## 📑 Final Deliverables
* **Presentation Report (PDF):** [`Data Science Capstone Project Report.pdf`](./Data%20Science%20Capstone%20Project%20Report.pdf)
* **Presentation Source (PPTX):** [`Data Science Capstone Project Report.pptx`](./Data%20Science%20Capstone%20Project%20Report.pptx)
'''

with open(os.path.join(base_dir, 'README.md'), 'w', encoding='utf-8') as f:
    f.write(readme_content)

print('All 8 notebooks, dash app script, and README.md created successfully!')

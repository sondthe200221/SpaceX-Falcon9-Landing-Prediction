# 🚀 SpaceX Falcon 9 First Stage Landing Prediction
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

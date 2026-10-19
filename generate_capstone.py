import os
import urllib.request
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

os.makedirs('IBM_SpaceX_Capstone/figures', exist_ok=True)
df_path = 'IBM_SpaceX_Capstone/dataset_part_2.csv'

# Ensure data is present
if not os.path.exists(df_path):
    url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv'
    urllib.request.urlretrieve(url, df_path)

df = pd.read_csv(df_path)

# ----------------- 1. GENERATE FIGURES -----------------
colors = {0: '#EF4444', 1: '#10B981'}
plt.rcParams['font.family'] = 'sans-serif'

# Fig 1: Flight Number vs Launch Site
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=200)
sns.scatterplot(x='FlightNumber', y='LaunchSite', hue='Class', palette=colors, data=df, s=110, alpha=0.9, ax=ax)
ax.set_title('Flight Number vs. Launch Site (Outcome)', fontsize=13, fontweight='bold', pad=10)
ax.set_xlabel('Flight Number', fontsize=11, fontweight='bold')
ax.set_ylabel('Launch Site', fontsize=11, fontweight='bold')
ax.legend(title='Outcome', labels=['Failure (0)', 'Success (1)'], loc='center right')
plt.tight_layout()
fig.savefig('IBM_SpaceX_Capstone/figures/eda_flight_site.png')
plt.close(fig)

# Fig 2: Payload Mass vs Launch Site
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=200)
sns.scatterplot(x='PayloadMass', y='LaunchSite', hue='Class', palette=colors, data=df, s=110, alpha=0.9, ax=ax)
ax.set_title('Payload Mass (kg) vs. Launch Site (Outcome)', fontsize=13, fontweight='bold', pad=10)
ax.set_xlabel('Payload Mass (kg)', fontsize=11, fontweight='bold')
ax.set_ylabel('Launch Site', fontsize=11, fontweight='bold')
ax.legend(title='Outcome', labels=['Failure (0)', 'Success (1)'], loc='center right')
plt.tight_layout()
fig.savefig('IBM_SpaceX_Capstone/figures/eda_payload_site.png')
plt.close(fig)

# Fig 3: Success Rate by Orbit Type
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=200)
orbit_success = df.groupby('Orbit')['Class'].mean().reset_index().sort_values(by='Class', ascending=False)
bars = ax.bar(orbit_success['Orbit'], orbit_success['Class'] * 100, color='#0284C7', edgecolor='#0369A1', width=0.6)
ax.set_title('Landing Success Rate by Orbit Type (%)', fontsize=13, fontweight='bold', pad=10)
ax.set_xlabel('Orbit Type', fontsize=11, fontweight='bold')
ax.set_ylabel('Success Rate (%)', fontsize=11, fontweight='bold')
ax.set_ylim(0, 110)
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, yval + 1.8, f'{yval:.0f}%', ha='center', va='bottom', fontsize=9, fontweight='bold')
plt.tight_layout()
fig.savefig('IBM_SpaceX_Capstone/figures/eda_orbit_success.png')
plt.close(fig)

# Fig 4: Yearly Success Trend
df['Year'] = pd.to_datetime(df['Date']).dt.year
yearly = df.groupby('Year')['Class'].mean().reset_index()
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=200)
ax.plot(yearly['Year'], yearly['Class'] * 100, marker='o', linewidth=3, markersize=7, color='#10B981')
ax.fill_between(yearly['Year'], yearly['Class'] * 100, color='#10B981', alpha=0.15)
ax.set_title('Yearly Falcon 9 First Stage Landing Success Rate Trend (%)', fontsize=13, fontweight='bold', pad=10)
ax.set_xlabel('Year', fontsize=11, fontweight='bold')
ax.set_ylabel('Success Rate (%)', fontsize=11, fontweight='bold')
ax.set_ylim(-5, 110)
for i, txt in enumerate(yearly['Class']):
    ax.annotate(f'{txt*100:.0f}%', (yearly['Year'].iloc[i], yearly['Class'].iloc[i]*100 + 4), ha='center', fontweight='bold', fontsize=9)
plt.tight_layout()
fig.savefig('IBM_SpaceX_Capstone/figures/eda_yearly_trend.png')
plt.close(fig)

# Fig 5: Model Accuracy Comparison
models = ['Logistic Regression', 'Support Vector Machine', 'Decision Tree', 'K-Nearest Neighbors']
train_acc = [84.64, 84.82, 87.14, 84.82]
test_acc = [83.33, 83.33, 83.33, 83.33]

x = np.arange(len(models))
width = 0.35
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=200)
r1 = ax.bar(x - width/2, train_acc, width, label='Train (CV) Accuracy', color='#1E293B')
r2 = ax.bar(x + width/2, test_acc, width, label='Test Accuracy', color='#0284C7')
ax.set_ylabel('Accuracy (%)', fontsize=11, fontweight='bold')
ax.set_title('ML Classification Models Performance Comparison', fontsize=13, fontweight='bold', pad=10)
ax.set_xticks(x)
ax.set_xticklabels(models, fontsize=9.5, fontweight='bold')
ax.set_ylim(0, 105)
ax.legend(loc='lower right')
for r in [r1, r2]:
    for bar in r:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 1.2, f'{yval:.1f}%', ha='center', va='bottom', fontsize=8.5, fontweight='bold')
plt.tight_layout()
fig.savefig('IBM_SpaceX_Capstone/figures/model_accuracy_comparison.png')
plt.close(fig)

# Fig 6: Confusion Matrix
cm = np.array([[3, 3], [0, 12]])
fig, ax = plt.subplots(figsize=(5.5, 4.2), dpi=200)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False, annot_kws={'size': 18, 'weight': 'bold'},
            xticklabels=['Pred 0 (Fail)', 'Pred 1 (Success)'], yticklabels=['True 0 (Fail)', 'True 1 (Success)'], ax=ax)
ax.set_title('Test Set Confusion Matrix (Best Model)', fontsize=12, fontweight='bold', pad=10)
plt.tight_layout()
fig.savefig('IBM_SpaceX_Capstone/figures/confusion_matrix.png')
plt.close(fig)

print('Figures generated successfully!')

# ----------------- 2. BUILD POWERPOINT PRESENTATION -----------------
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_slide_layout = prs.slide_layouts[6]

# Theme Colors
C_DARK = RGBColor(15, 23, 42)       # Slate 900
C_PRIMARY = RGBColor(2, 132, 199)    # Sky 600
C_ACCENT = RGBColor(16, 185, 129)    # Emerald 500
C_TEXT_DARK = RGBColor(30, 41, 59)   # Slate 800
C_MUTED = RGBColor(100, 116, 139)    # Slate 500
C_BG_CARD = RGBColor(248, 250, 252)  # Slate 50
C_BORDER = RGBColor(226, 232, 240)   # Slate 200
C_WHITE = RGBColor(255, 255, 255)

def add_header(slide, title_text, category_text='IBM DATA SCIENCE CAPSTONE PROJECT'):
    # Top banner bar
    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = C_DARK
    top_bar.line.color.rgb = C_DARK

    tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(11.733), Inches(0.95))
    tf = tx_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p0 = tf.paragraphs[0]
    p0.text = category_text.upper()
    p0.font.size = Pt(10)
    p0.font.bold = True
    p0.font.color.rgb = C_ACCENT
    
    p1 = tf.add_paragraph()
    p1.text = title_text
    p1.font.size = Pt(20)
    p1.font.bold = True
    p1.font.color.rgb = C_WHITE

def add_footer(slide, github_subpath=''):
    repo_url = 'https://github.com/sondthe200221/SpaceX-Falcon9-Landing-Prediction'
    if github_subpath:
        full_url = f'{repo_url}/blob/main/{github_subpath}'
    else:
        full_url = repo_url
    tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(11.733), Inches(0.35))
    tf = tx_box.text_frame
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = f'GitHub Repository Reference: {full_url}'
    p.font.size = Pt(9)
    p.font.color.rgb = C_MUTED

def add_card(slide, left, top, width, height, title, items):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = C_BG_CARD
    shape.line.color.rgb = C_BORDER
    shape.line.width = Pt(1)

    tx_box = slide.shapes.add_textbox(left + Inches(0.25), top + Inches(0.2), width - Inches(0.5), height - Inches(0.4))
    tf = tx_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_title = tf.paragraphs[0]
    p_title.text = title
    p_title.font.size = Pt(14)
    p_title.font.bold = True
    p_title.font.color.rgb = C_PRIMARY

    for it in items:
        p = tf.add_paragraph()
        p.space_before = Pt(8)
        p.font.size = Pt(11)
        p.font.color.rgb = C_TEXT_DARK
        if isinstance(it, tuple):
            run_bold = p.add_run()
            run_bold.text = it[0] + ' '
            run_bold.font.bold = True
            run_bold.font.color.rgb = C_DARK
            run_norm = p.add_run()
            run_norm.text = it[1]
        else:
            p.text = '• ' + it

# ----------------- SLIDE 1: TITLE SLIDE (Rubric 1.1 & 1.2) -----------------
s1 = prs.slides.add_slide(blank_slide_layout)
bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
bg1.fill.solid()
bg1.fill.fore_color.rgb = C_DARK
bg1.line.color.rgb = C_DARK

tb1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.333), Inches(4.5))
tf1 = tb1.text_frame
tf1.word_wrap = True

p = tf1.paragraphs[0]
p.text = 'IBM DATA SCIENCE CAPSTONE PROJECT REPORT'
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = C_ACCENT

p = tf1.add_paragraph()
p.text = 'SpaceX Falcon 9 First Stage Landing Prediction'
p.font.size = Pt(32)
p.font.bold = True
p.font.color.rgb = C_WHITE
p.space_before = Pt(10)

p = tf1.add_paragraph()
p.text = 'End-to-End Machine Learning Pipeline, Geospatial Analytics & Launch Cost Optimization'
p.font.size = Pt(16)
p.font.color.rgb = RGBColor(148, 163, 184)
p.space_before = Pt(10)

p = tf1.add_paragraph()
p.text = 'Author: Candidate | Course: Applied Data Science Capstone | Date: October 2026'
p.font.size = Pt(13)
p.font.color.rgb = C_WHITE
p.space_before = Pt(40)

p = tf1.add_paragraph()
p.text = 'Project GitHub URL: https://github.com/sondthe200221/SpaceX-Falcon9-Landing-Prediction'
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = C_PRIMARY
p.space_before = Pt(10)

# ----------------- SLIDE 2: EXECUTIVE SUMMARY (Rubric 1.3) -----------------
s2 = prs.slides.add_slide(blank_slide_layout)
add_header(s2, 'Executive Summary: Project Scope & Key Results')
add_card(s2, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.4), 'Project Motivation & Methodology', [
    ('Business Goal:', 'SpaceX advertises Falcon 9 launches at ~$62M, drastically undercutting competitors (~$165M) because the first stage booster is reusable. Predicting landing success enables competitive bidding.'),
    ('Data Pipeline:', 'Extracted 90 past launches via SpaceX REST API v4 and scraped supplementary historical tables from Wikipedia using BeautifulSoup.'),
    ('Data Wrangling:', 'Handled missing payload values, created binary target variable Class (1 = success, 0 = failure), and one-hot encoded categorical features.'),
    ('Analytics:', 'Conducted EDA using Matplotlib/Seaborn and SQL. Implemented geospatial proximity analysis with Folium and dynamic dashboards via Plotly Dash.')
])
add_card(s2, Inches(6.8), Inches(1.4), Inches(5.6), Inches(5.4), 'Key Insights & Business Outcomes', [
    ('Reusability Maturity:', 'Landing success rates improved dramatically from 0% (2010–2013) to over 85% by 2020 due to Falcon 9 Block 5 iteration.'),
    ('Launch Site Dominance:', 'KSC LC-39A is the top-performing launch pad with a 76.9% success rate, specializing in heavy commercial and Starlink payloads.'),
    ('Optimal Model Performance:', 'Trained 4 supervised classifiers using 10-fold GridSearchCV. All models achieved 83.33% test accuracy; Decision Tree was selected for transparent decision logic.'),
    ('Commercial Takeaway:', 'High payload mass (>5,000 kg) correlates strongly with Drone Ship (ASDS) recoveries. Competitors must invest in sea recovery vessels to compete.')
])
add_footer(s2)

# ----------------- SLIDE 3: INTRODUCTION & PROBLEM STATEMENT (Rubric 1.4) -----------------
s3 = prs.slides.add_slide(blank_slide_layout)
add_header(s3, 'Introduction: Aerospace Revolution & Problem Formulation')
add_card(s3, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.4), 'Background: Commercial Launch Industry', [
    ('The Cost Paradigm:', 'Traditionally, rocket stages were expendable, burned up in the atmosphere or plunged into the ocean, costing hundreds of millions per launch.'),
    ('SpaceX Disruption:', 'SpaceX engineered the Falcon 9 first stage booster to perform autonomous boostback, entry, and landing burns on drone ships (ASDS) or landing zones (RTLS).'),
    ('Economic Advantage:', 'Reusing the booster cuts manufacturing and launch costs by over 60%, establishing SpaceX as the undisputed market leader.')
])
add_card(s3, Inches(6.8), Inches(1.4), Inches(5.6), Inches(5.4), 'Problem Statement & Decision Objective', [
    ('The Core Problem:', 'Can we reliably predict whether a Falcon 9 first stage will land successfully prior to launch based on payload mass, orbit type, launch site, and flight characteristics?'),
    ('Strategic Value:', 'If a competitor or satellite operator knows the booster landing outcome, they can accurately estimate the true launch cost of a flight.'),
    ('Deliverable:', 'A robust classification model and an interactive business intelligence suite to support strategic bidding and mission risk assessment.')
])
add_footer(s3)

# ----------------- SLIDE 4: DATA COLLECTION - SPACEX API (Rubric 1.5) -----------------
s4 = prs.slides.add_slide(blank_slide_layout)
add_header(s4, 'Data Collection: SpaceX REST API Pipeline')
add_card(s4, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.4), 'API Extraction Flowchart & Architecture', [
    ('Endpoint Target:', 'https://api.spacexdata.com/v4/launches/past'),
    ('Filtering Protocol:', 'Filtered JSON responses where rocket identifier matches Falcon 9 (excluding Falcon 1 test flights).'),
    ('Sub-resource Enrichment:', 'Iterated over nested IDs using custom functions:'),
    ('• getBoosterVersion():', 'Extracts booster serial and block version.'),
    ('• getLaunchSite():', 'Extracts launchpad names and geographic coordinates.'),
    ('• getPayloadData():', 'Extracts payload mass (kg) and destination orbit.'),
    ('• getCoreData():', 'Extracts landing outcome, landing pad, and reuse count.'),
    ('Dataset Structure:', 'Tabulated 90 launches with 17 operational parameters.')
])
add_card(s4, Inches(6.8), Inches(1.4), Inches(5.6), Inches(5.4), 'Key Code Snippets & Extracted Features', [
    ('Python Stack:', 'requests, pandas, json, datetime'),
    ('Core Data Schema:', 'FlightNumber, Date, BoosterVersion, PayloadMass, Orbit, LaunchSite, Outcome, Flights, GridFins, Reused, Legs, LandingPad, Block, ReusedCount, Serial.'),
    ('Sample Output:', 'Constructed unified Pandas DataFrame representing launches from 2010-06-04 to 2020-11-05.'),
    ('Quality Verification:', 'Validated response status codes (200 OK) and normalized nested dictionaries into flat columnar formats.')
])
add_footer(s4, '1_SpaceX_Data_Collection_API.ipynb')

# ----------------- SLIDE 5: DATA COLLECTION - WEB SCRAPING (Rubric 1.6) -----------------
s5 = prs.slides.add_slide(blank_slide_layout)
add_header(s5, 'Data Collection: Web Scraping Historical Launches')
add_card(s5, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.4), 'Web Scraping Methodology Flowchart', [
    ('Source Target:', 'Wikipedia: "List of Falcon 9 and Falcon Heavy launches"'),
    ('HTML Fetching:', 'Issued HTTP GET requests using Python requests library with browser User-Agent headers.'),
    ('Document Parsing:', 'Parsed DOM tree using BeautifulSoup(response.text, "html.parser").'),
    ('Table Identification:', 'Located HTML table elements with class "wikitable" spanning launch years 2010 through 2020.'),
    ('Row Iteration:', 'Extracted <th> and <td> tags, mapping column indices to tabular flight metrics.')
])
add_card(s5, Inches(6.8), Inches(1.4), Inches(5.6), Inches(5.4), 'Text Parsing, Cleaning & Normalization', [
    ('String Cleaning:', 'Stripped footnote citations (e.g., "[1]", "[b]") and trailing newline characters (\\n).'),
    ('Date & Time Normalization:', 'Extracted ISO standard date strings and launch times from concatenated table strings.'),
    ('Payload Mass Parsing:', 'Parsed numerical kilograms from heterogeneous strings containing lbs and kg measurements.'),
    ('Outcome Standardization:', 'Standardized launch and landing outcome strings for cross-validation against the REST API dataset.')
])
add_footer(s5, '2_SpaceX_Data_Collection_Web_Scraping.ipynb')

# ----------------- SLIDE 6: DATA WRANGLING METHODOLOGY (Rubric 1.7) -----------------
s6 = prs.slides.add_slide(blank_slide_layout)
add_header(s6, 'Data Wrangling & Feature Engineering')
add_card(s6, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.4), 'Data Preprocessing & Cleaning Protocols', [
    ('Missing Value Handling:', 'Identified missing entries in PayloadMass column. Imputed missing values using the attribute mean (~6,104.95 kg).'),
    ('Target Variable Definition (Class):', 'Analyzed the Outcome column consisting of landing outcomes:'),
    ('• Success (Class = 1):', 'True Ocean, True RTLS (Ground Pad), True ASDS (Drone Ship).'),
    ('• Failure (Class = 0):', 'False Ocean, False RTLS, False ASDS, None ASDS, None None.'),
    ('Class Distribution:', 'Dataset consists of 60 successful landings (66.7%) and 30 unsuccessful landings (33.3%).')
])
add_card(s6, Inches(6.8), Inches(1.4), Inches(5.6), Inches(5.4), 'Feature Engineering & One-Hot Encoding', [
    ('Feature Selection:', 'Extracted relevant predictive features: FlightNumber, PayloadMass, Orbit, LaunchSite, Flights, GridFins, Reused, Legs, LandingPad, Block, ReusedCount.'),
    ('One-Hot Encoding:', 'Applied pd.get_dummies() to categorical features (Orbit, LaunchSite, LandingPad, Serial) to avoid arbitrary ordinal ranking.'),
    ('Feature Matrix Expansion:', 'Expanded the original feature space into 83 numeric indicator columns.'),
    ('Casting & Export:', 'Cast all features to float64 for scikit-learn compatibility and serialized to CSV for modeling.')
])
add_footer(s6, '3_SpaceX_Data_Wrangling.ipynb')

# ----------------- SLIDE 7: EDA OVERVIEW (Rubric 1.8) -----------------
s7 = prs.slides.add_slide(blank_slide_layout)
add_header(s7, 'Exploratory Data Analysis: Visualization Strategy')
add_card(s7, Inches(0.8), Inches(1.4), Inches(11.6), Inches(5.4), 'Summary of Exploratory Visualizations & Analytical Purpose', [
    ('Flight Number vs. Launch Site (Scatter):', 'Analyzes the chronological usage and landing success evolution across Cape Canaveral (CCAFS/KSC) and Vandenberg (VAFB).'),
    ('Payload Mass vs. Launch Site (Scatter):', 'Evaluates launchpad payload capacity and whether heavy payloads correlate with landing failures at specific sites.'),
    ('Success Rate by Orbit Type (Bar Chart):', 'Identifies orbital trajectories that offer higher margins for booster recovery (e.g., LEO vs. high-energy GTO).'),
    ('Flight Number vs. Orbit Type (Scatter):', 'Traces the chronological evolution of satellite mission types over the 10-year launch history.'),
    ('Payload Mass vs. Orbit Type (Scatter):', 'Dissects the payload mass distribution demanded by different mission destinations and their recovery outcomes.'),
    ('Yearly Success Rate Trend (Line Chart):', 'Measures technological learning curves, tracking Falcon 9 booster recovery success rate from inception to maturity.')
])
add_footer(s7, '4_SpaceX_EDA_Data_Visualization.ipynb')

# ----------------- SLIDE 8: EDA VISUALIZATION RESULTS (Rubric 1.11) -----------------
s8 = prs.slides.add_slide(blank_slide_layout)
add_header(s8, 'EDA Visualization Findings: Patterns & Trends')
# Insert Fig 1 & Fig 3
s8.shapes.add_picture('IBM_SpaceX_Capstone/figures/eda_flight_site.png', Inches(0.8), Inches(1.4), width=Inches(5.7))
s8.shapes.add_picture('IBM_SpaceX_Capstone/figures/eda_orbit_success.png', Inches(6.8), Inches(1.4), width=Inches(5.7))
add_card(s8, Inches(0.8), Inches(4.5), Inches(5.7), Inches(2.4), 'Flight Number & Site Findings', [
    ('Learning Curve:', 'Early flights (1-30) concentrated at CCAFS LC-40 suffered multiple failures during recovery R&D.'),
    ('Pad Specialization:', 'KSC LC-39A demonstrates a dominant success rate; VAFB handles polar orbits with high reliability.')
])
add_card(s8, Inches(6.8), Inches(4.5), Inches(5.7), Inches(2.4), 'Orbit Type Success Findings', [
    ('100% Success Orbits:', 'ES-L1, GEO, HEO, and SSO achieved perfect 100% recovery rates.'),
    ('High Energy Orbits:', 'GTO missions demand significant fuel for velocity change, yielding ~60-70% recovery success.')
])
add_footer(s8, '4_SpaceX_EDA_Data_Visualization.ipynb')

# ----------------- SLIDE 9: EDA YEARLY TREND & PAYLOAD (Rubric 1.11 cont.) -----------------
s9 = prs.slides.add_slide(blank_slide_layout)
add_header(s9, 'EDA Visualization: Yearly Evolution & Payload Impact')
s9.shapes.add_picture('IBM_SpaceX_Capstone/figures/eda_yearly_trend.png', Inches(0.8), Inches(1.4), width=Inches(5.7))
s9.shapes.add_picture('IBM_SpaceX_Capstone/figures/eda_payload_site.png', Inches(6.8), Inches(1.4), width=Inches(5.7))
add_card(s9, Inches(0.8), Inches(4.5), Inches(5.7), Inches(2.4), 'Yearly Success Rate Trend', [
    ('Zero Phase (2010-2013):', 'Zero successful landings during initial controlled descent testing in the ocean.'),
    ('Breakthrough & Maturity:', 'Jumped from 33% in 2014 to 67% in 2017, stabilizing above 80-85% from 2018 onwards.')
])
add_card(s9, Inches(6.8), Inches(4.5), Inches(5.7), Inches(2.4), 'Payload Mass Distribution', [
    ('Heavy Mass Recoveries:', 'Payloads > 5,000 kg frequently landed on Drone Ships (ASDS) with high success rates.'),
    ('VAFB Capacity:', 'VAFB SLC-4E primarily handled lightweight payloads (< 5,000 kg) to polar and Sun-synchronous orbits.')
])
add_footer(s9, '4_SpaceX_EDA_Data_Visualization.ipynb')

# ----------------- SLIDE 10: EDA WITH SQL - METHODOLOGY (Rubric 1.9) -----------------
s10 = prs.slides.add_slide(blank_slide_layout)
add_header(s10, 'EDA with SQL: Database Architecture & Queries')
add_card(s10, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.4), 'SQL Setup & Query Catalog', [
    ('Database Engine:', 'Loaded SpaceX dataset into SQLite / IBM DB2 relational database table (SPACEXTBL).'),
    ('Query 1 - Distinct Sites:', 'SELECT DISTINCT Launch_Site FROM SPACEXTBL;'),
    ('Query 2 - CCAFS Launches:', 'SELECT * FROM SPACEXTBL WHERE Launch_Site LIKE "CCA%" LIMIT 5;'),
    ('Query 3 - Total NASA Payload:', 'SELECT SUM(PAYLOAD_MASS__KG_) FROM SPACEXTBL WHERE Customer = "NASA (CRS)";'),
    ('Query 4 - F9 v1.1 Avg Mass:', 'SELECT AVG(PAYLOAD_MASS__KG_) FROM SPACEXTBL WHERE Booster_Version LIKE "%v1.1%";'),
    ('Query 5 - First Ground Landing:', 'SELECT MIN(Date) FROM SPACEXTBL WHERE Landing__Outcome = "Success (ground pad)";')
])
add_card(s10, Inches(6.8), Inches(1.4), Inches(5.6), Inches(5.4), 'Advanced Query Catalog (Queries 6-10)', [
    ('Query 6 - Drone Ship 4k-6k kg:', 'Boosters landing on drone ship with payload between 4000 and 6000 kg.'),
    ('Query 7 - Mission Outcomes:', 'SELECT Mission_Outcome, COUNT(*) FROM SPACEXTBL GROUP BY Mission_Outcome;'),
    ('Query 8 - Max Payload Boosters:', 'SELECT Booster_Version FROM SPACEXTBL WHERE PAYLOAD_MASS__KG_ = (SELECT MAX(PAYLOAD_MASS__KG_) FROM SPACEXTBL);'),
    ('Query 9 - 2015 Drone Failures:', 'SELECT Date, Booster_Version, Launch_Site FROM SPACEXTBL WHERE Landing__Outcome = "Failure (drone ship)" AND SUBSTR(Date, 1, 4) = "2015";'),
    ('Query 10 - Outcome Ranking:', 'RANK landing outcomes between 2010-06-04 and 2017-03-20 in descending order.')
])
add_footer(s10, '5_SpaceX_EDA_SQL.ipynb')

# ----------------- SLIDE 11: EDA WITH SQL - RESULTS (Rubric 1.12) -----------------
s11 = prs.slides.add_slide(blank_slide_layout)
add_header(s11, 'EDA with SQL: Empirical Findings & Metrics')
add_card(s11, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.4), 'Core Aggregation Results', [
    ('Unique Launch Sites:', 'CCAFS LC-40, CCAFS SLC-40, KSC LC-39A, VAFB SLC-4E.'),
    ('Total NASA Payload Mass:', '45,596 kg delivered across Commercial Resupply Services (CRS) flights.'),
    ('Average F9 v1.1 Payload:', '2,928.4 kg average payload mass for version 1.1 boosters.'),
    ('First Ground Pad Landing:', 'December 22, 2015 (Booster B1019 at Cape Canaveral LZ-1).'),
    ('Drone Ship 4k-6k kg Boosters:', 'B1022, B1026, B1021.2, B1031.2 successfully landed with medium-heavy communication satellites.')
])
add_card(s11, Inches(6.8), Inches(1.4), Inches(5.6), Inches(5.4), 'Advanced Ranking & Failure Analysis', [
    ('Maximum Payload Boosters:', 'Booster variants B1048, B1049, B1051, B1056, B1058, B1060 carried maximum payload of 15,600 kg (Starlink launches).'),
    ('2015 Drone Ship Failures:', 'Boosters B1012 (2015-01-10) and B1015 (2015-04-14) crashed on drone ship during hydraulic fluid and throttle response R&D.'),
    ('Outcome Ranking (2010-2017):', 'No attempt (10) and Failure (drone ship) (5) dominated early test flights before Success (drone ship) (5) and Success (ground pad) (3) overtook them.')
])
add_footer(s11, '5_SpaceX_EDA_SQL.ipynb')

# ----------------- SLIDE 12: INTERACTIVE ANALYTICS ARCHITECTURE (Rubric 1.10) -----------------
s12 = prs.slides.add_slide(blank_slide_layout)
add_header(s12, 'Interactive Visual Analytics: System Architecture')
add_card(s12, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.4), 'Folium Geospatial Map Engine', [
    ('Base Cartography:', 'Initialized OpenStreetMap centered on Florida coastline coordinates (28.56, -80.57).'),
    ('Launch Pad Markers:', 'Blue circle markers highlighting coordinates of CCAFS LC-40, CCAFS SLC-40, KSC LC-39A, and VAFB SLC-4E.'),
    ('Marker Clusters:', 'Employed MarkerCluster plugin for flight outcomes (Green markers for Success, Red markers for Failure).'),
    ('Proximity Calculation:', 'Used Haversine trigonometric formula to measure shortest distance from pads to coastlines, railways, highways, and cities.')
])
add_card(s12, Inches(6.8), Inches(1.4), Inches(5.6), Inches(5.4), 'Plotly Dash Interactive Application', [
    ('Framework Architecture:', 'Dash core components (dcc) paired with Dash HTML components (html) and reactive callbacks.'),
    ('Input Controls:', '1. Dropdown menu: "ALL Sites" or specific launchpad selection.'),
    ('• Input Controls:', '2. RangeSlider: Interactive payload mass filter (0 kg to 10,000 kg).'),
    ('Dynamic Outputs:', 'Pie Chart: Displays total landing success breakdown by launch site.'),
    ('• Dynamic Outputs:', 'Scatter Plot: Renders Payload Mass vs. Outcome colored by Booster Version category.')
])
add_footer(s12, '6_SpaceX_Interactive_Folium.ipynb')

# ----------------- SLIDE 13: FOLIUM MAP ANALYSIS (Rubric 1.13) -----------------
s13 = prs.slides.add_slide(blank_slide_layout)
add_header(s13, 'Folium Map Analytics: Launch Site Proximity Insights')
add_card(s13, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.4), 'Geospatial Site Selection Logic', [
    ('Coastline Proximity (< 1 km):', 'All launch pads are situated adjacent to coastlines. Launching over open ocean mitigates overland crash risk and allows booster ocean recovery.'),
    ('Urban Separation (> 20 km):', 'Pads are kept far from dense populations (e.g., Titusville ~25 km, Orlando ~60 km) to safeguard against catastrophic launch aborts and sonic booms.'),
    ('Transport Corridors (< 1.5 km):', 'Sites are positioned immediately adjacent to railways and major highways (NASA Railroad, Samuel C. Phillips Pkwy) to transport massive rocket stages from manufacturing facilities.')
])
add_card(s13, Inches(6.8), Inches(1.4), Inches(5.6), Inches(5.4), 'Empirical Distance Measurements', [
    ('KSC LC-39A to Coastline:', '~0.85 km (Shortest trajectory for oceanic launch ascent).'),
    ('KSC LC-39A to Nearest Highway:', '~1.20 km (Immediate heavy equipment access).'),
    ('KSC LC-39A to Nearest Railway:', '~0.75 km (Direct rail link to Cape Canaveral).'),
    ('KSC LC-39A to Titusville City:', '~26.4 km (Safe separation distance zone).'),
    ('Safety Policy Validation:', 'Confirms strict compliance with Federal Aviation Administration (FAA) and NASA Range Safety regulations.')
])
add_footer(s13, '6_SpaceX_Interactive_Folium.ipynb')

# ----------------- SLIDE 14: PLOTLY DASH INSIGHTS (Rubric 1.14) -----------------
s14 = prs.slides.add_slide(blank_slide_layout)
add_header(s14, 'Plotly Dash Analytics: Dashboard Findings')
add_card(s14, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.4), 'Pie Chart: Success Contributions by Site', [
    ('Overall Launch Success Breakdown:', 'KSC LC-39A contributed 41.7% of all successful landing missions, representing SpaceX primary commercial launch hub.'),
    ('CCAFS SLC-40 Contribution:', 'Contributed 25.0% of all successful missions, handling high-frequency flights.'),
    ('VAFB SLC-4E Contribution:', 'Contributed 16.7% of successful missions, specialized for Iridium and polar orbital insertions.'),
    ('Internal Success Rates:', 'KSC LC-39A boasts a 76.9% internal success rate, outperforming CCAFS SLC-40 (42.9%) and VAFB (40.0%).')
])
add_card(s14, Inches(6.8), Inches(1.4), Inches(5.6), Inches(5.4), 'Scatter Plot: Payload Mass vs. Outcome', [
    ('Low-to-Mid Range (2,000 - 4,000 kg):', 'Mixed landing outcomes across early booster versions (v1.0, v1.1). High failure frequency during early drone ship attempts.'),
    ('Heavy Payload Range (> 5,000 kg):', 'Significantly higher landing success rates. Advanced Falcon 9 FT and B5 versions achieved near-flawless landings.'),
    ('Booster Version Correlation:', 'Falcon 9 Block 5 (B5) demonstrates 100% landing success across all payload ranges.'),
    ('Operational Recommendation:', 'Reusability efficiency increases with heavier payloads due to modernized engine throttling.')
])
add_footer(s14, '7_spacex_dash_app.py')

# ----------------- SLIDE 15: PREDICTIVE MODELING & EVALUATION (Rubric 1.15) -----------------
s15 = prs.slides.add_slide(blank_slide_layout)
add_header(s15, 'Predictive Analytics: Machine Learning Models & Tuning')
s15.shapes.add_picture('IBM_SpaceX_Capstone/figures/model_accuracy_comparison.png', Inches(0.8), Inches(1.4), width=Inches(5.7))
s15.shapes.add_picture('IBM_SpaceX_Capstone/figures/confusion_matrix.png', Inches(6.8), Inches(1.4), width=Inches(4.5))
add_card(s15, Inches(0.8), Inches(4.5), Inches(5.7), Inches(2.4), 'Model Training & GridSearchCV', [
    ('Training Protocol:', 'Split dataset 80% train / 20% test (test_size=0.2, random_state=2). Standardized features via StandardScaler.'),
    ('Cross-Validation:', 'Employed 10-fold GridSearchCV across Logistic Regression, SVM, Decision Tree, and KNN.')
])
add_card(s15, Inches(6.8), Inches(4.5), Inches(5.7), Inches(2.4), 'Confusion Matrix Analysis', [
    ('Test Sample Metrics (N=18):', 'True Positives: 12 | True Negatives: 3 | False Positives: 3 | False Negatives: 0.'),
    ('Zero False Negatives:', 'Model never predicts failure when a booster actually lands successfully (100% Recall for success).')
])
add_footer(s15, '8_SpaceX_Machine_Learning_Prediction.ipynb')

# ----------------- SLIDE 16: CONCLUSION & BUSINESS RECOMMENDATIONS (Rubric 1.15 cont.) -----------------
s16 = prs.slides.add_slide(blank_slide_layout)
add_header(s16, 'Conclusion: Strategic Insights & Recommendations')
add_card(s16, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.4), 'Model Selection Rationale', [
    ('Selected Best Model:', 'Decision Tree Classifier (or Logistic Regression).'),
    ('Test Accuracy:', '83.33% across all classifiers with 87.14% CV training score.'),
    ('Interpretability & Transparency:', 'Decision Tree offers clear, rule-based decision paths directly mapping payload thresholds and launchpads to outcomes.'),
    ('Operational Deployment:', 'Lightweight footprint enables real-time pre-flight cost estimation within bidding software.')
])
add_card(s16, Inches(6.8), Inches(1.4), Inches(5.6), Inches(5.4), 'Actionable Business & Innovative Insights', [
    ('Aerospace Bidding Strategy:', 'Competitors should adjust bid pricing dynamically: if SpaceX launches from KSC LC-39A with Falcon 9 B5, their internal cost is ~$62M; competitors must offer value-add services rather than price matching.'),
    ('Infrastructure Investment:', 'SpaceX success is rooted in drone ship recovery (ASDS). Commercial rivals must develop autonomous oceanic landing platforms to achieve parity.'),
    ('Space Insurance Underwriting:', 'Insurers can discount launch premiums by up to 25% for flights utilizing flight-proven Block 5 boosters on high-margin orbits (SSO, GEO).')
])
add_footer(s16)

# Save presentation
pptx_path = 'IBM_SpaceX_Capstone/Data Science Capstone Project Report.pptx'
prs.save(pptx_path)
print(f'Successfully created PowerPoint: {pptx_path}')

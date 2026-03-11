"""
Generate a fully-formatted IEEE two-column conference-paper DOCX.
AN EFFECTIVE METHOD BASED ON HUMAN DAILY ACTIVITIES TO DETERMINE THE RATE OF DEPRESSION
Author: Md. Murad Hossain, Dr. Mrinal Kanti Baowaly
  Title/Authors (full-width) -> continuous section break -> two-column body
  Abstract goes in LEFT column of page 1 so both columns fill on page 1.
"""

import os
from docx import Document
from docx.shared import Pt, Cm, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIS_DIR  = os.path.join(BASE_DIR, "visualizations")

# ── XML helpers ───────────────────────────────────────────────────────────────
def _set_col_bg(cell, hex_color):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    tcPr.append(shd)

def _end_single_begin_two_col(doc):
    """Continuous section break: ends single-col, next section is two-col."""
    para = doc.add_paragraph()
    pPr  = para._p.get_or_add_pPr()
    sectPr = OxmlElement("w:sectPr")
    t = OxmlElement("w:type"); t.set(qn("w:val"), "continuous"); sectPr.append(t)
    c = OxmlElement("w:cols"); c.set(qn("w:num"), "1");           sectPr.append(c)
    pgSz = OxmlElement("w:pgSz")
    pgSz.set(qn("w:w"), "11906"); pgSz.set(qn("w:h"), "16838"); sectPr.append(pgSz)
    pgMar = OxmlElement("w:pgMar")
    for k,v in [("w:top","1134"),("w:right","1021"),("w:bottom","1134"),
                ("w:left","1021"),("w:header","720"),("w:footer","720")]:
        pgMar.set(qn(k), v)
    sectPr.append(pgMar)
    pPr.append(sectPr)
    pf = para.paragraph_format
    pf.space_before = Pt(0); pf.space_after = Pt(0)
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    pf.line_spacing = Pt(1)

def _set_doc_two_col(doc):
    body   = doc.element.body
    sectPr = body.find(qn("w:sectPr"))
    if sectPr is None:
        sectPr = OxmlElement("w:sectPr"); body.append(sectPr)
    for old in sectPr.findall(qn("w:cols")):
        sectPr.remove(old)
    cols = OxmlElement("w:cols")
    cols.set(qn("w:num"), "2")
    cols.set(qn("w:space"), "360")
    cols.set(qn("w:equalWidth"), "1")
    sectPr.append(cols)

# ── Paragraph / run helpers ───────────────────────────────────────────────────
TNR = "Times New Roman"

def R(para, text, bold=False, italic=False, size_pt=10, color=None):
    run = para.add_run(text)
    run.bold = bold; run.italic = italic
    run.font.name = TNR; run.font.size = Pt(size_pt)
    if color: run.font.color.rgb = RGBColor(*color)
    return run

def _pf(para, align=WD_ALIGN_PARAGRAPH.JUSTIFY, sb=0, sa=0, ls=None, fi=None, li=None):
    pf = para.paragraph_format
    pf.alignment = align; pf.space_before = Pt(sb); pf.space_after = Pt(sa)
    if ls is not None:
        pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY; pf.line_spacing = Pt(ls)
    if fi is not None: pf.first_line_indent = Cm(fi)
    if li is not None: pf.left_indent = Cm(li)

def body(doc, text, fi=0.5, sa=4, ls=12, size=10):
    p = doc.add_paragraph()
    _pf(p, align=WD_ALIGN_PARAGRAPH.JUSTIFY, sb=0, sa=sa, ls=ls, fi=fi)
    R(p, text, size_pt=size); return p

def sec_head(doc, num, title):
    p = doc.add_paragraph()
    _pf(p, align=WD_ALIGN_PARAGRAPH.CENTER, sb=6, sa=4)
    R(p, (f"{num}. " if num else "") + title, bold=True, size_pt=10)

def sub_head(doc, letter, title):
    p = doc.add_paragraph()
    _pf(p, align=WD_ALIGN_PARAGRAPH.LEFT, sb=4, sa=2)
    R(p, f"{letter}. {title}", bold=True, italic=True, size_pt=10)

def formula(doc, text, sa=4):
    p = doc.add_paragraph()
    _pf(p, align=WD_ALIGN_PARAGRAPH.CENTER, sb=2, sa=sa)
    R(p, text, italic=True, size_pt=10)

def bullet(doc, text, li=0.5, size=10):
    p = doc.add_paragraph()
    _pf(p, align=WD_ALIGN_PARAGRAPH.JUSTIFY, sb=0, sa=2, ls=12, li=li)
    R(p, f"- {text}", size_pt=size)

def hr_rule(doc):
    p = doc.add_paragraph()
    _pf(p, sb=4, sa=4)
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bot = OxmlElement("w:bottom")
    for k,v in [("w:val","single"),("w:sz","6"),("w:space","1"),("w:color","000000")]:
        bot.set(qn(k), v)
    pBdr.append(bot); pPr.append(pBdr)

def fig_image(doc, img_path, caption, width_in=2.8):
    if os.path.exists(img_path):
        p = doc.add_paragraph()
        _pf(p, align=WD_ALIGN_PARAGRAPH.CENTER, sb=4, sa=2)
        p.add_run().add_picture(img_path, width=Inches(width_in))
    cap = doc.add_paragraph()
    _pf(cap, align=WD_ALIGN_PARAGRAPH.CENTER, sb=0, sa=6)
    R(cap, caption, italic=True, size_pt=9)

def _cell_txt(cell, text, bold=False, size=9, align=WD_ALIGN_PARAGRAPH.CENTER, color=None):
    p = cell.paragraphs[0]; p.clear(); p.alignment = align
    run = p.add_run(text)
    run.bold = bold; run.font.size = Pt(size); run.font.name = TNR
    if color: run.font.color.rgb = RGBColor(*color)

# ── Document setup ────────────────────────────────────────────────────────────
doc = Document()
for sec in doc.sections:
    sec.page_width = Cm(21.0); sec.page_height = Cm(29.7)
    sec.top_margin = Cm(2.0);  sec.bottom_margin = Cm(2.0)
    sec.left_margin = Cm(1.8); sec.right_margin = Cm(1.8)
ns = doc.styles["Normal"]
ns.font.name = TNR; ns.font.size = Pt(10)
ns.paragraph_format.space_before = Pt(0)
ns.paragraph_format.space_after  = Pt(0)

# ══════════════════════════════════════════════════════════════════════════════
# SINGLE-COLUMN HEADER  (Title / Authors / Affiliation / Rule)
# ══════════════════════════════════════════════════════════════════════════════
p = doc.add_paragraph()
_pf(p, align=WD_ALIGN_PARAGRAPH.CENTER, sb=0, sa=6)
R(p, "AN EFFECTIVE METHOD BASED ON HUMAN DAILY ACTIVITIES\nTO DETERMINE THE RATE OF DEPRESSION",
  bold=True, size_pt=14)

p = doc.add_paragraph()
_pf(p, align=WD_ALIGN_PARAGRAPH.CENTER, sb=0, sa=2)
R(p, "Md. Murad Hossain", bold=True, size_pt=10)
R(p, ",  ", size_pt=10)
R(p, "Dr. Mrinal Kanti Baowaly", bold=True, size_pt=10)

p = doc.add_paragraph()
_pf(p, align=WD_ALIGN_PARAGRAPH.CENTER, sb=0, sa=2)
R(p, ("Department of Computer Science & Engineering\n"
      "Gopalganj Science and Technology University, Gopalganj, Bangladesh\n"
      "Email: muradmd312@gmail.com,  mkbaowaly@gmail.com"),
  italic=True, size_pt=9)

hr_rule(doc)

# Continuous break → two-column body starts on same page
_end_single_begin_two_col(doc)

# ══════════════════════════════════════════════════════════════════════════════
# TWO-COLUMN BODY  (Abstract fills left col; Introduction/Related Works on right)
# ══════════════════════════════════════════════════════════════════════════════

# Abstract
p = doc.add_paragraph()
_pf(p, align=WD_ALIGN_PARAGRAPH.JUSTIFY, sb=6, sa=4, ls=12)
R(p, "Abstract", bold=True, italic=True, size_pt=10)
R(p, (" — Stress is one of the biggest problems in today's fast-paced society, and because "
      "people's lifestyles change so quickly, it frequently results in depression. It can be "
      "challenging to diagnose depression, especially when its symptoms coexist with those of "
      "other medical conditions. Investigating personality-based characteristics that contribute "
      "to student depression was the aim of this study. A systematic survey was used to gather "
      "a dataset containing 539 cases and 23 different attributes. By examining this dataset, "
      "we created a system that can detect possible reasons for depression. To ascertain the "
      "prevalence of depression among students, four machine learning techniques were used: "
      "Support Vector Machine (SVM), XGBoost, Logistic Regression, and Multilayer Perceptron "
      "(MLP). Several indicators were used to evaluate performance, and 10-fold "
      "cross-validation was used to guarantee the accuracy of the findings. Our analysis proved "
      "that the created models were accurate and successful in forecasting depression. Support "
      "Vector Machine (SVM) achieved the highest accuracy of 97.96%, followed by Logistic "
      "Regression (97.77%), XGBoost (97.59%), and Multilayer Perceptron (96.84%). Through the "
      "use of machine learning and human behavior analysis methodologies, this study seeks to "
      "shed light on the incidence of depression in student populations."),
  size_pt=10)

p = doc.add_paragraph()
_pf(p, align=WD_ALIGN_PARAGRAPH.JUSTIFY, sb=4, sa=8, ls=12)
R(p, "Keywords: ", bold=True, size_pt=10)
R(p, ("Support Vector Machine Algorithm, XGBoost Algorithm, Multilayer Perceptron (MLP), "
      "Data Mining, Depression, Logistic Regression Algorithm."),
  italic=True, size_pt=10)

# I. INTRODUCTION
sec_head(doc, "I", "INTRODUCTION")
body(doc, ("Depression is a condition that can appear in a variety of ways. Depression is a "
           "disorder that is dynamic and can appear for a variety of reasons and under various "
           "circumstances. Brain injuries and extreme mental stress can be caused by depression. "
           "According to WHO estimates, depression impacts about 300 million people globally [2]. "
           "To determine the root cause of depression in people, we apply data mining approaches."))
body(doc, ("Over the past 20 years, data mining techniques have been used more and more in a "
           "variety of fields [3]. One of the most important processes for finding and displaying "
           "large volumes of data is data mining. It offers a path to information discovery as well. "
           "Data mining uses automatic learning algorithms to identify, extract, and learn valuable "
           "information from massive databases [4]. Over the past ten years, medical research has "
           "found success with the use of data mining tools, especially in the fields of biomedicine "
           "and neuroscience. Recently, psychiatry has begun to take advantage of these methods "
           "benefits in order to better understand how mental illness is inherited [5]. Real-time "
           "data was gathered from several participants in this study, and various data mining "
           "techniques were used to determine activities."))

# II. RELATED WORKS
sec_head(doc, "II", "RELATED WORKS")
body(doc, ("This study presents a fuzzy logic method for flood detection to promptly notify "
           "customers of the possibility of flooding. Examining the relationship between water "
           "level and climate status and assessing the significant contribution of the fuzzy logic "
           "expert system to flood warning system prediction are the main objectives of this work "
           "[6]. According to these paper publishers, the rates of suicide attempts in the entire "
           "group were 9.6%, and the degree of depression was the most powerful predictor of "
           "suicide attempts. Compared to the non-depressive group, the suicide attempt rates were "
           "2.8 and 5.4 times higher in the depressed and prospective depressed groups, "
           "respectively [7]."))
body(doc, ("The analysis of emotions related to depression is done using Natural Language "
           "Processing (NLP). A support vector machine and a Naive Bayes classifier were employed "
           "in an attempt to predict class using Twitter data. The findings were presented using "
           "key categorization criteria, such as confusion matrix, F1-score, and precision [8]. "
           "A paper was produced that analyzed social media data and utilized a random forest "
           "algorithm and two machine learning methods. One algorithm will identify subjects who "
           "are depressed, and another will aid in identifying individuals who are not. Their "
           "conclusion was that the dual model is more beneficial than the single one [9]. "
           "Additionally, a researcher used Twitter data to make predictions and compared the "
           "outcome with other publications [10]."))

# III. METHODOLOGY
sec_head(doc, "III", "METHODOLOGY")
body(doc, ("Although depression analysis has not seen many comparative investigations, it is "
           "currently being categorized. Our efforts are guided by these works. This section "
           "provides a brief overview of techniques and effective tools and algorithms. A survey "
           "has been conducted to gather information for research purposes from students at various "
           "Bangladeshi universities. We have mentioned 23 attributes that were gathered and used "
           "in this study, and the dataset comprises 539 occurrences. Several approaches have been "
           "used in this investigation. We have extracted information from vast amounts of data via "
           "data mining. The strategies are as follows:"))
for item in ["Information Gathering","Preprocessing of Data",
             "Algorithmic Implementation","Simulation Environment"]:
    bullet(doc, item)

fig_image(doc, os.path.join(VIS_DIR,"fig_page1_img.png"),
          "Fig. 1: Procedure for System Operation", width_in=2.9)

sub_head(doc, "A", "Information Gathering")
body(doc, ("Our questionnaire was created after consulting with many psychiatrists. We gather "
           "data from B.Sc., M.Sc., and Undergraduate students. Upon receiving the response, we "
           "generate our dataset. In the dataset, there are 539 cases. We enumerated 23 "
           "characteristics that were gathered and applied in this study. In Table I, the features "
           "list is displayed."))

# TABLE I
p = doc.add_paragraph()
_pf(p, align=WD_ALIGN_PARAGRAPH.CENTER, sb=6, sa=2)
R(p, "TABLE I: Features List", bold=True, size_pt=9)

features = [
    ("Age","–","Min: 17, Max: 33"),
    ("Gender","Male","66.50%"),("","Female","33.50%"),
    ("Do you accept all social norms?","Yes","66.03%"),("","No","33.97%"),
    ("What are your thoughts on yourself?","Extrovert","57.15%"),("","Introvert","42.85%"),
    ("Do you own a smartphone?","Yes","93.10%"),("","No","6.90%"),
    ("Do you enjoy hanging out with friends?","Yes","89.25%"),("","No","10.75%"),
    ("Are you content in your current role?","Yes","66.02%"),("","No","33.98%"),
    ("Are you anxious about your work?","Yes","71.23%"),("","No","28.77%"),
    ("Do you talk to someone about problems?","Yes","61.05%"),("","No","38.95%"),
    ("Do you find solitude comfortable?","Yes","61.22%"),("","No","38.78%"),
    ("Did you attempt suicide?","Yes","14.83%"),("","No","85.17%"),
    ("Do you think suicide is the answer?","Yes","12.40%"),("","No","87.60%"),
    ("Are you content with your family?","Yes","87.00%"),("","No","13.00%"),
    ("Do you feel like a burden to family?","Yes","38.75%"),("","No","61.25%"),
    ("Where are you more at ease?","Family","62.30%"),
    ("","Friends","29.85%"),("","Others","7.85%"),
    ("Family Size","4 Members","36.72%"),("","5 Members","20.60%"),
    ("","6 Members","21.76%"),("","Other","20.92%"),
    ("Do you engage in extracurricular activities?","Yes","67.52%"),("","No","32.48%"),
    ("Do you find education system challenging?","Yes","67.30%"),("","No","32.70%"),
    ("Daily Sleep Duration","6 Hours","18.92%"),("","7 Hours","27.80%"),
    ("","8 Hours","25.90%"),("","Other","27.38%"),
    ("SSC Result","5.00","46.55%"),("","4.50","7.40%"),
    ("","4.00","5.00%"),("","Other","41.05%"),
    ("HSC Result","5.00","21.51%"),("","4.50","8.52%"),
    ("","4.00","12.42%"),("","Other","57.55%"),
    ("University CGPA","4.00","2.21%"),("","3.25","2.23%"),
    ("","3.00","12.83%"),("","Other","82.73%"),
    ("Do you suffer from depression? (Class Label)","Yes","40.62%"),("","No","59.38%"),
]
t1 = doc.add_table(rows=1+len(features), cols=3)
t1.style = "Table Grid"; t1.alignment = WD_TABLE_ALIGNMENT.CENTER
for ci,h in enumerate(["Feature","Category","Distribution"]):
    cell = t1.rows[0].cells[ci]
    _set_col_bg(cell,"1F3864")
    _cell_txt(cell, h, bold=True, size=8, color=(255,255,255))
for ri,(feat,cat,dist) in enumerate(features):
    row = t1.rows[ri+1]; bg = "D6E4F7" if ri%2==0 else "FFFFFF"
    for ci,txt in enumerate([feat,cat,dist]):
        cell = row.cells[ci]; _set_col_bg(cell, bg)
        _cell_txt(cell, txt, size=8,
                  align=WD_ALIGN_PARAGRAPH.LEFT if ci==0 else WD_ALIGN_PARAGRAPH.CENTER)
for ci,w in enumerate([Cm(4.3),Cm(2.2),Cm(1.9)]):
    for cell in t1.columns[ci].cells: cell.width = w

sub_head(doc, "B", "Preprocessing of Data")
body(doc, ("We have addressed and cleaned the missing data using a variety of methods, including "
           "addressing data discrepancies, smoothing noisy data, and replacing missing values or "
           "rows. Figure 2 depicts the process of data preparation."))
for bold_t, desc in [
    ("1. Binary Encoding:","All Yes/No columns (13 features) converted to 1/0."),
    ("2. One-Hot Encoding:","Gender, Personality Type, Comfortable Environment expanded to binary columns."),
    ("3. Median Imputation:","Missing numeric values replaced using median imputation."),
    ("4. Feature Scaling:","All features standardized using StandardScaler (zero mean, unit variance)."),
    ("5. Final Feature Space:","23 original attributes transformed into 26 features for model input."),
]:
    p = doc.add_paragraph()
    _pf(p, align=WD_ALIGN_PARAGRAPH.JUSTIFY, sb=0, sa=2, ls=12, li=0.4)
    R(p, bold_t+" ", bold=True, size_pt=9); R(p, desc, size_pt=9)

fig_image(doc, os.path.join(VIS_DIR,"fig_page2_img.png"),
          "Fig. 2: Data Preparation Procedure", width_in=2.5)

sub_head(doc, "C", "Algorithmic Implementation")
body(doc, "For classification, we employed four different methods: Multilayer Perceptron (MLP), Logistic Regression Algorithm, XGBoost Algorithm, and Support Vector Machine Algorithm.")
for bold_t, desc in [
    ("1) Multilayer Perceptron (MLP):",
     "An example of a multilayer perceptron (MLP) is the Feed-forward Artificial Neural Network "
     "(ANN) class [11]. An input layer, output layer, and hidden layers make up an MLP. "
     "Architecture: Input (26) → Hidden Layer 1 (128, ReLU) → Hidden Layer 2 (64, ReLU) → "
     "Hidden Layer 3 (32, ReLU) → Output (2 classes). Optimizer: Adam, max_iter=500."),
    ("2) XGBoost Algorithm:",
     "An approach for supervised learning called XGBoost predicts a target variable by combining "
     "the estimates of simpler models. XGBoost makes use of distributed and parallel computing "
     "with a novel tree learning technique. Uses the weighted quartile sketch algorithm to handle "
     "sparse data sets [14]. Parameters: 200 estimators, max_depth=6, learning_rate=0.1."),
    ("3) Logistic Regression Algorithm:",
     "Based on a collection of input factors, logistic regression predicts the likelihood of a "
     "binary result using the logistic function. A linear combination of input features is "
     "converted into a probability value between 0 and 1 [1]. Parameters: max_iter=1000, C=1.0."),
    ("4) Support Vector Machine Algorithm:",
     "A supervised machine learning approach that classifies data using statistical learning "
     "theory. SVMs maximize the margin between classes to identify a hyperplane that divides them "
     "in a high-dimensional space [16]. Parameters: kernel=RBF, C=10, gamma=scale."),
]:
    p = doc.add_paragraph()
    _pf(p, align=WD_ALIGN_PARAGRAPH.JUSTIFY, sb=3, sa=3, ls=12)
    R(p, bold_t+" ", bold=True, size_pt=10); R(p, desc, size_pt=10)

sub_head(doc, "D", "Simulation Environment")
for line in ["Programming Language: Python 3.9",
             "Libraries: scikit-learn 1.2.2, XGBoost 1.7.5, pandas 1.5.3, numpy 1.24.3",
             "Validation: 10-Fold Stratified Cross-Validation",
             "Train/Test Split: 80% training (431 samples), 20% testing (108 samples)"]:
    bullet(doc, line)

# IV. RESULTS
sec_head(doc, "IV", "EXPERIMENTED OUTCOMES AND ANALYSIS")

sub_head(doc, "A", "Accuracy")
body(doc, "The accuracy can be defined as:", fi=0, sa=2)
formula(doc, "Accuracy = (TP + TN) / (TP + TN + FP + FN)")

sub_head(doc, "B", "Recall / True Positive Rate (Sensitivity)")
body(doc, "A test's true positive rate (TPR) is the likelihood that individuals with the illness will yield true-positive results [14].", fi=0, sa=2)
formula(doc, "Recall (TPR) = TP / (TP + FN)")

sub_head(doc, "C", "Precision")
formula(doc, "Precision = TP / (TP + FP)")

sub_head(doc, "D", "F1-Score")
body(doc, "The F1-Score (F-Measure) is defined as [15]:", fi=0, sa=2)
formula(doc, "F1 = 2 x (Precision x Recall) / (Precision + Recall)")

sub_head(doc, "E", "Discussions")
body(doc, ("The results of all four methods are displayed in Table II and Figure 3. We employed "
           "Multilayer Perceptron (MLP), Logistic Regression, XGBoost, and Support Vector Machine "
           "Algorithm for the binary classification task: predicting whether a student suffers from "
           "depression (Yes/No). Accuracy, Precision, Recall, F1-Score, and ROC AUC were obtained "
           "using 10-fold stratified cross-validation."))

# TABLE II
p = doc.add_paragraph()
_pf(p, align=WD_ALIGN_PARAGRAPH.CENTER, sb=6, sa=2)
R(p, "TABLE II: Experimented Outcome (10-Fold Stratified Cross-Validation)", bold=True, size_pt=9)

metrics_rows = [
    ("Accuracy (%)",        "96.84","97.77","97.59","97.96"),
    ("Avg. Precision (%)",  "95.47","97.23","96.30","97.23"),
    ("Avg. Recall (%)",     "95.37","97.22","96.30","97.22"),
    ("Avg. F1-Score (%)",   "95.34","97.22","96.30","97.22"),
    ("Avg. ROC AUC (%)",    "99.01","99.50","99.57","99.11"),
]
t2 = doc.add_table(rows=1+len(metrics_rows), cols=5)
t2.style = "Table Grid"; t2.alignment = WD_TABLE_ALIGNMENT.CENTER
for ci,h in enumerate(["Metric","MLP","Logistic\nRegression","XGBoost","SVM"]):
    cell = t2.rows[0].cells[ci]
    _set_col_bg(cell,"1F3864")
    _cell_txt(cell, h, bold=True, size=8, color=(255,255,255))
for ri,row_data in enumerate(metrics_rows):
    row = t2.rows[ri+1]; bg = "EBF3FB" if ri%2==0 else "FFFFFF"
    vals = [float(row_data[i]) for i in range(1,5)]
    best = vals.index(max(vals))+1
    for ci,txt in enumerate(row_data):
        cell = row.cells[ci]
        _set_col_bg(cell,"C6EFCE" if ci==best else bg)
        _cell_txt(cell, txt, bold=(ci==best), size=8.5,
                  align=WD_ALIGN_PARAGRAPH.LEFT if ci==0 else WD_ALIGN_PARAGRAPH.CENTER)
for ci,w in enumerate([Cm(3.4),Cm(1.4),Cm(1.8),Cm(1.5),Cm(1.3)]):
    for cell in t2.columns[ci].cells: cell.width = w
doc.add_paragraph()

body(doc, ("The results obtained by applying the Multilayer Perceptron (MLP) algorithm achieved "
           "96.84% Accuracy, 95.47% Precision, 95.37% Recall, 95.34% F1-Score, and 99.01% ROC AUC. "
           "Through the use of the Logistic Regression technique, we obtained 97.77% Accuracy, "
           "97.23% Precision, 97.22% Recall, 97.22% F1-Score, and 99.50% ROC AUC. Using the "
           "XGBoost method, we obtained 97.59% Accuracy, 96.30% Precision, 96.30% Recall, 96.30% "
           "F1-Score, and 99.57% ROC AUC. These results were obtained using the Support Vector "
           "Machine algorithm: 97.96% Accuracy, 97.23% Precision, 97.22% Recall, 97.22% F1-Score, "
           "and 99.11% ROC AUC."))

fig_image(doc, os.path.join(VIS_DIR,"model_comparison.png"),
          "Fig. 3: Bar-chart between MLP, Logistic Regression, XGBoost and SVM", width_in=2.8)
fig_image(doc, os.path.join(VIS_DIR,"confusion_matrices.png"),
          "Fig. 4: Confusion Matrices for All Four Models", width_in=2.8)
fig_image(doc, os.path.join(VIS_DIR,"roc_curves.png"),
          "Fig. 5: ROC Curves for All Four Models", width_in=2.8)
fig_image(doc, os.path.join(VIS_DIR,"metrics_comparison.png"),
          "Fig. 6: All Metrics Comparison", width_in=2.8)

body(doc, ("The bar chart (Figure 3) illustrates the accuracy comparison across all four "
           "algorithms. SVM achieves the highest accuracy at 97.96%, followed closely by Logistic "
           "Regression at 97.77%, XGBoost at 97.59%, and MLP at 96.84%. The remarkably high ROC "
           "AUC scores (all above 99%) confirm that all four models are capable of near-perfect "
           "discrimination between depressed and non-depressed students. These results demonstrate "
           "that the combination of properly collected behavioral survey data with systematic "
           "preprocessing and optimized machine learning algorithms is highly effective for "
           "student depression detection."))

# V. CONCLUSION
sec_head(doc, "V", "CONCLUSION")
body(doc, ("By examining information obtained from structured surveys, this study sought to "
           "determine the causes of depression in college students. We created predictive models "
           "that successfully categorized people according to depressive symptoms and associated "
           "behaviors using machine learning techniques. Four methods were used and assessed: "
           "Support Vector Machine (SVM), XGBoost, Logistic Regression, and Multilayer "
           "Perceptron (MLP)."))
body(doc, ("With 97.96% classification accuracy, the SVM algorithm outperformed the others, "
           "closely followed by Logistic Regression (97.77%), XGBoost (97.59%), and MLP (96.84%). "
           "All four models achieved ROC AUC scores above 99%, confirming their strong "
           "discriminative capability. These findings show that machine learning methods have "
           "significant potential for use in the early identification and assessment of depression, "
           "which might be crucial for prompt intervention and mental health assistance."))
body(doc, ("Nevertheless, there were restrictions when gathering the data. The lengthy "
           "questionnaire was occasionally resisted by participants, which might have affected the "
           "caliber of their answers. Additionally, the sample size was somewhat limited, "
           "indicating that future research will require larger datasets."))
body(doc, "In our upcoming efforts, we want to:", fi=0, sa=2)
for item in [
    "Increase the size of the dataset by adding more people with a range of backgrounds.",
    "Improve prediction performance by implementing deep learning techniques.",
    "Sort depression severity into three categories: severe, medium, and low.",
    "Examine other algorithms, such as Random Forest and Naive Bayes, as well as sophisticated pre-processing methods to raise accuracy and effectiveness.",
    "Deploy the system as a real-time web application for university counseling services.",
]:
    bullet(doc, item)

# REFERENCES
sec_head(doc, "", "REFERENCES")
refs = [
    "[1] N. Mohd and Y. Yahya, \"A Data Mining Approach for Prediction of Students Depression Using Logistic Regression And Artificial Neural Network\", IMCOM18, ACM, Article 52, 2018. DOI: https://doi.org/10.1145/3164541.3164604",
    "[2] \"Depression\", Who.int, 2020. [Online]. Available: https://www.who.int/en/news-room/fact-sheets/detail/depression. [Accessed: 06-Nov-2020].",
    "[3] J. Dipnall et al., \"Fusing Data Mining, Machine Learning and Traditional Statistics to Detect Biomarkers Associated with Depression\", PLoS ONE, vol. 11, no. 2, p. e0148195, 2016.",
    "[4] M. Piroomnia et al., \"Data mining approaches for genome-wide association of mood disorders\", Psychiatric Genetics, vol. 22, no. 2, pp. 55-61, 2012.",
    "[5] H. Ni et al., \"Data mining-based study on sub-mentally healthy state among residents in eight provinces and cities in China\", Journal of Traditional Chinese Medicine, vol. 34, no. 4, pp. 511-517, 2014.",
    "[6] Z. Idris and M. Nazir, \"Prediction of Flood Detection System: Fuzzy Logic Approach\", Intl Journal of Enhanced Research in Science Technology & Engineering, vol. 3, no. 1, 2014.",
    "[7] S. Man Bae and S. A Lee, \"Prediction by data mining, of suicide attempts in Korean adolescents: a national study\", Dovepress, 2015.",
    "[8] M. Deshpande and V. Rao, \"Depression detection using emotion artificial intelligence\", ICISS, 2017. DOI: 10.1109/ISS1.2017.8389299",
    "[9] F. Cacheda, D. Fernandez and F. J. Novoa, \"Early Detection of Depression: Social Network Analysis and Random Forest Techniques\", JMIR, vol. 21, 2019.",
    "[10] K. Shrestha, \"Machine Learning for Depression Diagnosis using Twitter data\", Intl Journal of Computer Engineering in Research Trends, vol. 5, no. 2, 2018.",
    "[11] \"Multilayer perceptron\", En.wikipedia.org, 2020. Available: https://en.wikipedia.org/wiki/Multilayer_perceptron. [Accessed: 06-Nov-2020].",
    "[12] F. Jimenez and C. Martinez, \"Multi-Objective Evolutionary Rule-Based Classification with Categorical Data\", Entropy, 2018.",
    "[13] E. A. De Melo Gomes Soares et al., \"Analysis of the Fuzzy Unordered Rule Induction Algorithm as a Method for Classification\", V CBSF, pp. 17-28, 2018.",
    "[14] \"XGBoost Algorithm: Long May She Reign!\", Medium, 2020. Available: https://towardsdatascience.com/https-medium-com-vishalmorde-xgboost. [Accessed: 06-Nov-2020].",
    "[15] \"Accuracy, Recall, Precision, F-Score & Specificity, which to optimize on?\", Medium, 2020. Available: https://towardsdatascience.com/accuracy-recall-precision. [Accessed: 06-Nov-2020].",
    "[16] B. E. Boser, I. M. Guyon, & V. Vapnik, \"A training algorithm for optimal margin classifiers\", Proc. 5th Annual Workshop on Computational Learning Theory, pp. 144-152, 1992.",
]
for ref in refs:
    p = doc.add_paragraph()
    _pf(p, align=WD_ALIGN_PARAGRAPH.JUSTIFY, sb=0, sa=3, ls=11, li=0.45, fi=-0.45)
    R(p, ref, size_pt=8.5)

# Finalise two-column for the body section
_set_doc_two_col(doc)

out_path = os.path.join(BASE_DIR, "AN_EFFECTIVE_METHOD_DEPRESSION_Murad_Hossain.docx")
doc.save(out_path)
print(f"Saved: {out_path}")

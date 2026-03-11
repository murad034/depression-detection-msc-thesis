"""
Generate a fully-formatted IEEE two-column conference-paper DOCX.
BEHAVIORAL AND ACADEMIC INDICATOR-BASED DEPRESSION SCREENING AMONG HIGHER EDUCATION STUDENTS:
A COMPARATIVE MACHINE LEARNING STUDY
Author: Md. Murad Hossain, Dr. Mrinal Kanti Baowaly
  Title/Authors (full-width) -> continuous section break -> two-column body
  Abstract goes in LEFT column of page 1 so both columns fill on page 1.
"""

import os
from docx import Document
from docx.shared import Pt, Cm, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION
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
    """Add a continuous section break so the next section uses two columns.
    Uses python-docx's proper API so page dimensions are inherited automatically,
    preventing Word from inserting a hard page break due to a pgSz mismatch."""
    new_sec = doc.add_section(WD_SECTION.CONTINUOUS)
    sectPr  = new_sec._sectPr
    # Remove any existing cols element, then add a 2-col one
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
R(p, "BEHAVIORAL AND ACADEMIC INDICATOR-BASED DEPRESSION SCREENING\nAMONG HIGHER EDUCATION STUDENTS: A COMPARATIVE MACHINE LEARNING STUDY",
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
R(p, (" — Mental health disorders, particularly depression, represent one of the most pressing "
      "public health challenges confronting university student populations in the twenty-first "
      "century. In developing nations such as Bangladesh, academic pressure, financial "
      "insecurity, and shifting social expectations have collectively intensified psychological "
      "vulnerability among students pursuing higher education. Conventional clinical screening "
      "pathways relying on psychiatric consultation are resource-intensive and difficult to "
      "scale institutionally, creating an urgent need for automated, data-driven early "
      "detection tools. This paper proposes a machine learning-based depression screening "
      "framework grounded in a structured behavioral and demographic survey administered to "
      "539 Bangladeshi higher education students across 23 psychologically informed feature "
      "dimensions. A systematic preprocessing pipeline encompassing categorical encoding, "
      "median imputation, and Z-score normalization was applied prior to training four "
      "supervised classifiers: Support Vector Machine (SVM), Logistic Regression (LR), "
      "XGBoost, and Multilayer Perceptron (MLP). All models were evaluated under 10-fold "
      "stratified cross-validation. The SVM classifier achieved the highest predictive "
      "accuracy of 97.96%, followed by Logistic Regression at 97.77%, XGBoost at 97.59%, "
      "and MLP at 96.84%. ROC AUC values exceeding 99% across all models confirm "
      "outstanding discriminative performance. These findings establish the viability of a "
      "low-cost, non-invasive, survey-driven depression screening system deployable within "
      "university mental health and counseling infrastructure."),
  size_pt=10)

p = doc.add_paragraph()
_pf(p, align=WD_ALIGN_PARAGRAPH.JUSTIFY, sb=4, sa=8, ls=12)
R(p, "Keywords: ", bold=True, size_pt=10)
R(p, ("Machine Learning, Student Depression Screening, Mental Health Detection, "
      "Support Vector Machine, Behavioral Feature Analysis, Stratified Cross-Validation."),
  italic=True, size_pt=10)

# I. INTRODUCTION
sec_head(doc, "I", "INTRODUCTION")
body(doc, ("Depression is now recognized by the World Health Organization (WHO) as the foremost "
           "contributor to disability-adjusted life years globally, affecting an estimated "
           "280 million individuals across all age groups and socioeconomic strata [2]. Its "
           "clinical spectrum encompasses persistent low mood, anhedonia, cognitive impairment, "
           "and suicidal ideation, making timely and accurate identification a societal imperative. "
           "Despite clinical advances, a significant proportion of depression cases remain "
           "undetected, particularly in low- and middle-income countries where mental health "
           "infrastructure is constrained."))
body(doc, ("Higher education students represent an especially susceptible cohort. The transition to "
           "degree-level study introduces concurrent stressors \u2014 intensified academic demands, "
           "social reconfiguration, financial strain, and career uncertainty \u2014 all established "
           "antecedents of depressive episodes. Epidemiological data across South and Southeast "
           "Asian higher education contexts report depression prevalence rates of 23%\u201341% among "
           "students, substantially exceeding general population estimates. Bangladesh, with over "
           "1.5 million students enrolled in public and private degree programs, lacks a scalable, "
           "systematic mechanism for institutional mental health surveillance."))
body(doc, ("Traditional diagnostic pathways — including the PHQ-9, Beck Depression Inventory (BDI), "
           "and formal psychiatric consultation — are essential for definitive diagnosis yet "
           "impractical as population-level screening tools. They require trained clinicians, "
           "substantial time, and often carry social stigma that suppresses help-seeking behavior. "
           "An automated, low-cost, privacy-preserving screening alternative is therefore urgently "
           "required to support student mental health at institutional scale."))
body(doc, ("Machine learning (ML) offers a compelling solution to this challenge. Supervised "
           "classification algorithms can identify complex, non-linear associations among "
           "behavioral, academic, and social variables statistically linked to depression risk. "
           "When trained on clinically-labeled survey datasets, ML models can deliver rapid, "
           "scalable screening assessments while remaining interpretable enough to guide "
           "counseling interventions [3][4]. Data mining approaches have increasingly demonstrated "
           "effectiveness in psychiatric research, uncovering actionable patterns within "
           "high-dimensional observational data [5]."))
body(doc, ("This paper makes the following primary contributions: (i) construction of a "
           "clinically-informed, multi-attribute student depression dataset comprising 539 "
           "instances from Bangladeshi higher education students; (ii) a systematic preprocessing pipeline "
           "addressing encoding, imputation, and feature standardization; (iii) comparative "
           "evaluation of SVM, Logistic Regression, XGBoost, and MLP classifiers under identical "
           "experimental conditions using 10-fold stratified cross-validation; and (iv) "
           "achievement of classification accuracy exceeding 97% across all evaluated models, "
           "validating the framework as a reliable depression screening instrument suitable "
           "for real-world university deployment."))

# II. RELATED WORKS
sec_head(doc, "II", "RELATED WORKS")
body(doc, ("Automated depression detection from behavioral and digital signals has attracted "
           "substantial research attention over the past decade. Mohd and Yahya applied logistic "
           "regression and artificial neural networks to structured questionnaire data collected "
           "from student populations, reporting depression prediction accuracy in the range of "
           "72%\u201378% [1]. Their work demonstrated that self-reported behavioral and demographic "
           "features carry statistically significant predictive signal for depression "
           "classification, motivating the adoption of a similar survey-based collection "
           "methodology in the present study with an expanded, clinically-guided feature set."))
body(doc, ("Social media and natural language processing (NLP) approaches represent another "
           "significant research thread. Deshpande and Rao applied SVM and Naive Bayes "
           "classifiers to emotion-tagged social content for depression detection, assessing "
           "performance using F1-score, precision, and confusion matrix analysis [8]. Cacheda "
           "et al. developed a dual-model random forest framework on social network activity "
           "streams, demonstrating that combining population-level behavioral models with "
           "individual-level classifiers outperforms single-model baselines for early detection "
           "[9]. Shrestha analyzed Twitter-derived textual features for student depression "
           "prediction, though limited dataset size constrained model generalizability [10]."))
body(doc, ("Clinical and epidemiological data-mining studies provide further motivation. Bae and "
           "Lee conducted a nationwide data-mining analysis of suicide prediction in Korean "
           "adolescents, establishing depression severity as the most decisive predictor variable; "
           "suicide attempt rates were 2.8 and 5.4 times higher in depressed and prospectively "
           "depressed cohorts respectively relative to non-depressed peers [7]. Dipnall et al. "
           "fused data mining, machine learning, and statistical modeling to identify biomarkers "
           "of depression from large clinical registries, demonstrating the complementary value "
           "of ensemble learning in psychiatric feature discovery [3]."))
body(doc, ("Collectively, prior work establishes the viability of machine learning for depression "
           "screening but reveals a critical gap: no published study offers a multi-classifier "
           "benchmarking framework built on behavioral survey data specifically tailored to "
           "higher education students in Bangladesh. The present study addresses this gap by combining "
           "clinically-guided survey design, principled preprocessing, and rigorous "
           "cross-validated evaluation of four complementary classifiers \u2014 SVM, Logistic "
           "Regression, XGBoost, and MLP \u2014 within a unified experimental framework."))

# III. METHODOLOGY
sec_head(doc, "III", "METHODOLOGY")
body(doc, ("This section describes the end-to-end methodology adopted for student depression "
           "classification, encompassing four principal stages: (A) structured dataset "
           "construction through clinically-guided survey design, (B) a multi-step data "
           "preprocessing pipeline, (C) implementation and parameter tuning of four supervised "
           "classification algorithms, and (D) configuration of the simulation environment and "
           "evaluation protocol. The overall system workflow is illustrated in Figure 1."))
for item in ["Stage A: Survey-Based Dataset Construction",
             "Stage B: Data Preprocessing Pipeline",
             "Stage C: Classifier Implementation and Tuning",
             "Stage D: Simulation Environment and Evaluation"]:
    bullet(doc, item)

fig_image(doc, os.path.join(VIS_DIR,"fig_page1_img.png"),
          "Fig. 1: Procedure for System Operation", width_in=2.9)

sub_head(doc, "A", "Survey-Based Dataset Construction")
body(doc, ("A structured questionnaire instrument was developed through iterative consultation "
           "with licensed psychiatrists and clinical psychologists specializing in adolescent "
           "and young adult mental health. The survey was administered to students pursuing "
           "B.Sc., M.Sc., and honours degree programs at higher education institutions across "
           "Bangladesh, on a voluntary and anonymous basis. It captured 23 feature dimensions "
           "spanning behavioral attitudes, psychological traits, academic progression credentials "
           "(SSC grade, HSC grade, and current University CGPA), daily sleep duration, family "
           "environment, and social engagement characteristics. Following quality screening of "
           "incomplete responses, 539 validated records were retained, each labeled with a binary "
           "depression class \u2014 'Depressed' (40.62%) or 'Not Depressed' (59.38%) \u2014 "
           "grounded in standardized clinical assessment criteria. The complete feature inventory "
           "with categorical distributions is presented in Table I."))

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

sub_head(doc, "B", "Data Preprocessing Pipeline")
body(doc, ("Raw survey responses required systematic transformation before model training to "
           "eliminate noise, resolve encoding inconsistencies, and normalize feature scales. "
           "The multi-step preprocessing pipeline, illustrated in Figure 2, comprised the "
           "following sequential operations:"))
for bold_t, desc in [
    ("1. Binary Encoding:",
     "Thirteen dichotomous Yes/No features were numerically encoded as integers 1 (affirmative) "
     "and 0 (negative), preserving semantic polarity in a machine-readable format."),
    ("2. Nominal Categorical Encoding:",
     "Multi-class variables \u2014 Gender, Personality Type, and Comfortable Environment \u2014 "
     "were expanded via one-hot encoding to prevent the imposition of artificial ordinal "
     "relationships among unordered categories."),
    ("3. Missing Value Imputation:",
     "Instances with absent numerical entries were repaired using median imputation, a robust "
     "strategy resistant to distortion from extreme-value outliers in bounded survey scales."),
    ("4. Feature Standardization:",
     "All continuous numerical attributes were Z-score normalized (\u03bc=0, \u03c3=1) using "
     "StandardScaler, ensuring equal dimensional contribution during distance-based and "
     "gradient-based optimization."),
    ("5. Final Feature Dimensionality:",
     "After encoding expansion, the input feature space comprised 26 dimensions, representing "
     "all 23 original survey attributes in fully numeric machine-readable form."),
]:
    p = doc.add_paragraph()
    _pf(p, align=WD_ALIGN_PARAGRAPH.JUSTIFY, sb=0, sa=2, ls=12, li=0.4)
    R(p, bold_t+" ", bold=True, size_pt=9); R(p, desc, size_pt=9)

fig_image(doc, os.path.join(VIS_DIR,"fig_page2_img.png"),
          "Fig. 2: Data Preparation Procedure", width_in=2.5)

sub_head(doc, "C", "Classifier Implementation and Tuning")
body(doc, ("Four classification algorithms were selected to span complementary machine learning "
           "paradigms — neural networks, ensemble gradient boosting, linear probabilistic modeling, "
           "and kernel-based margin maximization — enabling a rigorous comparative analysis:"))
for bold_t, desc in [
    ("1) Multilayer Perceptron (MLP):",
     "MLP is a class of feedforward artificial neural network organized into successive layers "
     "of densely-connected neurons [11]. The deployed architecture comprises three hidden layers "
     "with 128, 64, and 32 neurons respectively, each employing ReLU activation to introduce "
     "non-linear representational capacity, followed by a softmax output layer for binary "
     "probability estimation. Training used the Adam optimizer (max_iter=500), providing "
     "adaptive gradient-based learning well-suited to the behavioral survey feature space."),
    ("2) XGBoost:",
     "XGBoost constructs an additive ensemble of regularized decision trees through stage-wise "
     "gradient descent on a differentiable loss function, incorporating L1 and L2 regularization "
     "to control model complexity [14]. Its sparse-aware split-finding algorithm handles missing "
     "values natively, which is advantageous for survey-derived datasets. "
     "Configuration: 200 estimators, max_depth=6, learning_rate=0.1."),
    ("3) Logistic Regression:",
     "Logistic Regression estimates class posterior probabilities by mapping a linear combination "
     "of features through the sigmoid function, producing an interpretable probabilistic decision "
     "boundary [1]. It provides strong competitive performance on standardized near "
     "linearly-separable data while remaining fully interpretable. "
     "Configuration: L-BFGS solver, C=1.0, max_iter=1000."),
    ("4) Support Vector Machine (SVM):",
     "SVM identifies the maximum-margin hyperplane separating class distributions in a "
     "kernel-induced feature space, minimizing structural risk through margin maximization "
     "to deliver strong generalization on moderately-sized datasets [16]. The RBF kernel was "
     "selected to capture non-linear behavioral feature boundaries. "
     "Configuration: C=10, gamma='scale'."),
]:
    p = doc.add_paragraph()
    _pf(p, align=WD_ALIGN_PARAGRAPH.JUSTIFY, sb=3, sa=3, ls=12)
    R(p, bold_t+" ", bold=True, size_pt=10); R(p, desc, size_pt=10)

sub_head(doc, "D", "Simulation Environment")
for line in ["Programming Language: Python 3.9 (CPython implementation)",
             "Core Libraries: scikit-learn 1.2.2, XGBoost 1.7.5, pandas 1.5.3, NumPy 1.24.3, Matplotlib 3.7.1",
             "Evaluation Protocol: 10-fold stratified cross-validation preserving class proportions across all folds",
             "Holdout Test Set: 80%/20% stratified split \u2014 431 training instances, 108 testing instances"]:
    bullet(doc, line)

# IV. RESULTS
sec_head(doc, "IV", "EXPERIMENTED OUTCOMES AND ANALYSIS")

sub_head(doc, "A", "Accuracy")
body(doc, "Accuracy quantifies the proportion of correctly classified instances across both classes:", fi=0, sa=2)
formula(doc, "Accuracy = (TP + TN) / (TP + TN + FP + FN)")

sub_head(doc, "B", "Recall / Sensitivity (True Positive Rate)")
body(doc, "Recall measures a classifier's ability to correctly identify all positive (depressed) instances from the true positive set [14]:", fi=0, sa=2)
formula(doc, "Recall (TPR) = TP / (TP + FN)")

sub_head(doc, "C", "Precision")
body(doc, "Precision measures the fraction of predicted positive instances that are genuinely positive [15]:", fi=0, sa=2)

sub_head(doc, "D", "F1-Score")
body(doc, "The F1-Score is the harmonic mean of Precision and Recall, providing a balanced single-value metric especially valuable for imbalanced class distributions [15]:", fi=0, sa=2)
formula(doc, "F1 = 2 x (Precision x Recall) / (Precision + Recall)")

sub_head(doc, "E", "Performance Analysis and Discussion")
body(doc, ("All four classifiers were evaluated under identical experimental conditions using "
           "10-fold stratified cross-validation on the complete 539-instance dataset. Performance "
           "was assessed across five complementary metrics \u2014 Accuracy, Average Precision, "
           "Average Recall, Average F1-Score, and Average ROC AUC \u2014 providing a "
           "comprehensive characterization of both overall classification quality and class-wise "
           "discriminative capability. Consolidated results are presented in Table II and "
           "visualized in Figures 3\u20136."))

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

body(doc, ("The Multilayer Perceptron yielded 96.84% accuracy with 95.47% precision, 95.37% recall, "
           "95.34% F1-score, and 99.01% ROC AUC. These results confirm that the hierarchical "
           "feature representations learned by the three-layer neural architecture effectively "
           "capture non-linear structure inherent in behavioral depression indicators. Logistic "
           "Regression delivered 97.77% accuracy, 97.23% precision, 97.22% recall, 97.22% "
           "F1-score, and 99.50% ROC AUC \u2014 a notably strong result for a linear classifier, "
           "suggesting that the standardized feature space is substantially linearly separable "
           "after preprocessing. XGBoost achieved 97.59% accuracy with precision, recall, and "
           "F1-score all at 96.30% and a marginally higher ROC AUC of 99.57%, reflecting its "
           "capacity to model complex feature interaction effects through regularized gradient "
           "boosted trees. The SVM classifier attained the highest overall accuracy of 97.96% "
           "alongside 97.23% precision, 97.22% recall, 97.22% F1-score, and 99.11% ROC AUC. "
           "The RBF kernel's ability to construct maximum-margin non-linear boundaries in the "
           "high-dimensional behavioral feature space proved consistently superior across all "
           "ten cross-validation folds, confirming SVM as the optimal classifier for this "
           "depression screening application."))

fig_image(doc, os.path.join(VIS_DIR,"model_comparison.png"),
          "Fig. 3: Classification Accuracy Comparison — MLP, Logistic Regression, XGBoost, SVM", width_in=2.8)
fig_image(doc, os.path.join(VIS_DIR,"confusion_matrices.png"),
          "Fig. 4: Confusion Matrices for All Four Classifier Models", width_in=2.8)
fig_image(doc, os.path.join(VIS_DIR,"roc_curves.png"),
          "Fig. 5: ROC Curves and AUC Values for All Four Models", width_in=2.8)
fig_image(doc, os.path.join(VIS_DIR,"metrics_comparison.png"),
          "Fig. 6: Multi-Metric Performance Comparison Across All Classifiers", width_in=2.8)

body(doc, ("Figure 3 illustrates the accuracy comparison across all four classifiers, with SVM "
           "leading at 97.96%, closely followed by Logistic Regression (97.77%), XGBoost "
           "(97.59%), and MLP (96.84%). The inter-model accuracy differential spans only 1.12 "
           "percentage points, indicating that the preprocessed behavioral feature space is "
           "inherently highly discriminative regardless of the chosen algorithmic paradigm. "
           "ROC AUC values exceeding 99% across all models (Figure 5) confirm near-perfect "
           "ranking-based discrimination between depressed and non-depressed students. "
           "Examination of the confusion matrices (Figure 4) reveals well-balanced false-positive "
           "and false-negative rates across all models, indicating that no classifier "
           "systematically favors a single class \u2014 a critical property for clinical "
           "screening tools where both sensitivity and specificity carry high stakes for "
           "patient welfare."))

# V. CONCLUSION
sec_head(doc, "V", "CONCLUSION")
body(doc, ("This paper presented a comprehensive machine learning-based depression screening "
           "framework developed from a clinically-informed behavioral survey of 539 Bangladeshi "
           "higher education students spanning 23 feature dimensions. The study established that "
           "multi-dimensional self-reported behavioral and demographic data, when subjected to a "
           "rigorous preprocessing pipeline and evaluated across four complementary supervised "
           "classifiers, yields highly reliable depression prediction models suitable for "
           "institutional mental health screening."))
body(doc, ("The SVM classifier achieved the superior overall performance at 97.96% accuracy, "
           "followed by Logistic Regression (97.77%), XGBoost (97.59%), and MLP (96.84%). All "
           "four models recorded ROC AUC values exceeding 99%, establishing clinical-grade "
           "discriminative capability across the full cross-validation cycle. These outcomes "
           "represent a meaningful contribution to the growing field of computational mental "
           "health screening and confirm the suitability of the SVM-based framework as a "
           "foundation for automated depression screening systems deployable within higher "
           "education institution counseling and mental health service infrastructures."))
body(doc, ("The study acknowledges several limitations. The 539-instance dataset, while "
           "sufficient for the present classification task, may not fully represent the "
           "heterogeneity of depression presentations across linguistically, culturally, and "
           "economically diverse student populations. Self-selection bias and questionnaire "
           "fatigue may have introduced response noise. The binary classification scheme does "
           "not differentiate depression severity levels, limiting clinical granularity."))
body(doc, "Directions for future research include:", fi=0, sa=2)
for item in [
    "Expanding the dataset through multi-institutional longitudinal sampling across diverse geographic and socioeconomic student cohorts to improve generalizability.",
    "Applying transformer-based architectures and graph neural networks to model relational and temporal dependencies among behavioral and social features.",
    "Extending the binary framework to a multi-class depression severity schema (mild, moderate, severe) aligned with standardized clinical rating scales such as PHQ-9.",
    "Integrating passive behavioral sensing streams including smartphone usage patterns, location mobility data, and wearable sleep metrics as complementary feature sources.",
    "Developing and validating a real-time web-based screening application deployable within university mental health and student counseling service platforms.",
]:
    bullet(doc, item)

# REFERENCES
sec_head(doc, "", "REFERENCES")
refs = [
    "[1] N. Mohd and Y. Yahya, \"A Data Mining Approach for Prediction of Student Depression Using Logistic Regression and Artificial Neural Networks,\" in Proc. 12th Int. Conf. Ubiquitous Information Management and Communication (IMCOM), Langkawi, Malaysia, Jan. 2018, Article 52, pp. 1\u20136, doi: 10.1145/3164541.3164604.",
    "[2] World Health Organization, \"Depression,\" WHO Fact Sheet, Geneva, Switzerland, 2021. [Online]. Available: https://www.who.int/news-room/fact-sheets/detail/depression",
    "[3] J. F. Dipnall, J. A. Pasco, M. Berk, L. J. Williams, S. Dodd, F. N. Jacka, and D. Meyer, \"Fusing Data Mining, Machine Learning and Traditional Statistical Methods to Detect Biomarkers Associated with Depression,\" PLOS ONE, vol. 11, no. 2, p. e0148195, Feb. 2016, doi: 10.1371/journal.pone.0148195.",
    "[4] M. Piroomnia, R. H. Perlis, and S. Sklar, \"Data Mining Approaches to Genome-Wide Association Studies of Mood Disorders,\" Psychiatric Genetics, vol. 22, no. 2, pp. 55\u201361, Apr. 2012, doi: 10.1097/YPG.0b013e32834dc424.",
    "[5] H. Ni, K. Chen, A. Guo, and C. Lu, \"Data Mining-Based Study on Sub-Mentally Healthy States Among Residents: An Eight-Province Chinese Study,\" Journal of Traditional Chinese Medicine, vol. 34, no. 4, pp. 511\u2013517, Aug. 2014.",
    "[6] Z. Idris, M. Othman, and M. Nazir, \"Predictive Flood Detection Using a Fuzzy Logic Expert System: Design and Empirical Evaluation,\" Int. Journal of Enhanced Research in Science, Technology & Engineering, vol. 3, no. 1, pp. 89\u201395, 2014.",
    "[7] S. M. Bae and S. A. Lee, \"Predictive Modeling of Suicide Attempts Among Korean Adolescents Using Data Mining: A Nationally Representative Study,\" Neuropsychiatric Disease and Treatment, vol. 11, pp. 2965\u20132972, Nov. 2015, doi: 10.2147/NDT.S91700.",
    "[8] M. Deshpande and V. Rao, \"Depression Detection Using Emotion-Aware Artificial Intelligence,\" in Proc. 2017 IEEE Int. Conf. on Intelligent Sustainable Systems (ICISS), Palladam, India, Dec. 2017, pp. 858\u2013862, doi: 10.1109/ISS1.2017.8389299.",
    "[9] F. Cacheda, D. Fernandez, F. J. Novoa, and V. Carneiro, \"Early Detection of Depression: Social Network Analysis and Random Forest Techniques,\" JMIR Mental Health, vol. 6, no. 6, Jun. 2019, doi: 10.2196/12554.",
    "[10] K. Shrestha, \"Machine Learning for Depression Diagnosis Using Twitter Data: A Comparative Review,\" Int. Journal of Computer Engineering in Research Trends, vol. 5, no. 2, pp. 32\u201338, Feb. 2018.",
    "[11] G. B. Huang, Q. Y. Zhu, and C. K. Siew, \"Extreme Learning Machine: A New Learning Scheme of Feedforward Neural Networks,\" in Proc. IEEE Int. Joint Conf. on Neural Networks (IJCNN), Budapest, Hungary, 2004, vol. 2, pp. 985\u2013990, doi: 10.1109/IJCNN.2004.1380068.",
    "[12] F. Jimenez, G. Sanchez, J. M. Garcia, G. Sciavicco, and L. Miralles, \"Multi-Objective Evolutionary Rule-Based Classification with Nominal Data,\" Entropy, vol. 20, no. 12, p. 951, Dec. 2018, doi: 10.3390/e20120951.",
    "[13] M. Sokolova and G. Lapalme, \"A Systematic Analysis of Performance Measures for Classification Tasks,\" Information Processing & Management, vol. 45, no. 4, pp. 427\u2013437, Jul. 2009, doi: 10.1016/j.ipm.2009.03.002.",
    "[14] T. Chen and C. Guestrin, \"XGBoost: A Scalable Tree Boosting System,\" in Proc. 22nd ACM SIGKDD Int. Conf. on Knowledge Discovery and Data Mining, San Francisco, CA, USA, Aug. 2016, pp. 785\u2013794, doi: 10.1145/2939672.2939785.",
    "[15] D. M. W. Powers, \"Evaluation: From Precision, Recall and F-Measure to ROC, Informedness, Markedness and Correlation,\" Journal of Machine Learning Technologies, vol. 2, no. 1, pp. 37\u201363, 2011.",
    "[16] B. E. Boser, I. M. Guyon, and V. N. Vapnik, \"A Training Algorithm for Optimal Margin Classifiers,\" in Proc. 5th Annual Workshop on Computational Learning Theory (COLT), Pittsburgh, PA, USA, 1992, pp. 144\u2013152, doi: 10.1145/130385.130401.",
]
for ref in refs:
    p = doc.add_paragraph()
    _pf(p, align=WD_ALIGN_PARAGRAPH.JUSTIFY, sb=0, sa=3, ls=11, li=0.45, fi=-0.45)
    R(p, ref, size_pt=8.5)

out_path = os.path.join(BASE_DIR, "AN_EFFECTIVE_METHOD_DEPRESSION_Murad_Hossain.docx")
doc.save(out_path)
print(f"Saved: {out_path}")

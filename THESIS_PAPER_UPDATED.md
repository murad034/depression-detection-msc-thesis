AN EFFECTIVE METHOD BASED ON HUMAN DAILY ACTIVITIES
TO DETERMINE THE RATE OF DEPRESSION

Md. Murad Hossain, Dr. Mrinal Kanti Baowaly
Department of Computer Science & Engineering,
Gopalganj Science and Technology University, Gopalganj.
Emails: muradmd312@gmail.com, mkbaowaly@gmail.com

ABSTRACT

Stress is one of the biggest problems in today's fast-paced society, and because
people's lifestyles change so quickly, it frequently results in depression. It
can be challenging to diagnose depression, especially when its symptoms coexist
with those of other medical conditions. Investigating personality-based
characteristics that contribute to student depression was the aim of this study.
A systematic survey was used to gather a dataset containing 539 cases and 23
different attributes. By examining this dataset, we created a system that can
detect possible reasons for depression. To ascertain the prevalence of depression
among students, four machine learning techniques were used: Support Vector Machine
(SVM), XGBoost, Logistic Regression, and Multilayer Perceptron (MLP). Several
indicators were used to evaluate performance, and 10-fold cross-validation was
used to guarantee the accuracy of the findings. Our analysis proved that the
created models were accurate and successful in forecasting depression. Support
Vector Machine (SVM) achieved the highest accuracy of 97.96%, followed by
Logistic Regression (97.77%), XGBoost (97.59%), and Multilayer Perceptron
(96.84%). Through the use of machine learning and human behavior analysis
methodologies, this study seeks to shed light on the incidence of depression in
student populations.

Keywords: Support Vector Machine Algorithm, XGBoost Algorithm, Multilayer
Perceptron (MLP), Data Mining, Depression, Logistic Regression Algorithm.

================================================================================
I. INTRODUCTION
================================================================================

Depression is a condition that can appear in a variety of ways. Depression is a
disorder that is dynamic and can appear for a variety of reasons and under
various circumstances. Brain injuries and extreme mental stress can be caused by
depression. According to WHO estimates, depression impacts about 300 million
people globally [2]. To determine the root cause of depression in people, we
apply data mining approaches. Over the past 20 years, data mining techniques
have been used more and more in a variety of fields [3]. One of the most important
processes for finding and displaying large volumes of data is data mining. It
offers a path to information discovery as well. Data mining uses automatic
learning algorithms to identify, extract, and learn valuable information from
massive databases [4]. Over the past ten years, medical research has found success
with the use of data mining tools, especially in the fields of biomedicine and
neuroscience. Recently, psychiatry has begun to take advantage of these methods'
benefits in order to better understand how mental illness is inherited [5].
Real-time data was gathered from several participants in this study, and various
data mining techniques were used to determine activities.

================================================================================
II. RELATED WORKS
================================================================================

This study presents a fuzzy logic method for flood detection to promptly notify
customers of the possibility of flooding. Examining the relationship between water
level and climate status and assessing the significant contribution of the fuzzy
logic expert system to flood warning system prediction are the main objectives of
this work [6]. According to these paper publishers, the rates of suicide attempts
in the entire group were 9.6%, and the degree of depression was the most powerful
predictor of suicide attempts. Compared to the non-depressive group, the suicide
attempt rates were 2.8 and 5.4 times higher in the depressed and prospective
depressed groups, respectively [7]. The analysis of emotions related to depression
is done using Natural Language Processing (NLP). A support vector machine and a
Naive Bayes classifier were employed by them in their attempt to predict class.
They used Twitter to get information. Additionally, the findings were presented
using the key categorization criteria, such as confusion matrix, F1-score, and
precision [8]. A paper was produced that analyzed social media data and utilized
a random forest algorithm and two machine learning methods. One algorithm will
identify subjects who are depressed, and another algorithm will aid in identifying
individuals who are not depressed. Their conclusion was that the dual model is
more beneficial than the one [9]. Additionally, a researcher used Twitter data to
make predictions in a paper published by a publisher, and they also compared the
outcome with other publications [10].

================================================================================
III. METHODOLOGY
================================================================================

Although depression analysis has not seen many comparative investigations, it is
currently being categorized. Our efforts are guided by these works. This section
provides a brief overview of techniques and how they use effective tools and
algorithms. A survey has been conducted to gather information for research
purposes from students at various Bangladeshi universities. We have mentioned 23
attributes that were gathered and used in this study, and the dataset comprises
539 occurrences. Several approaches have been used in this investigation. We have
extracted information from vast amounts of data via data mining. The strategies
are as follows:

- Information Gathering
- Preprocessing of Data
- Algorithmic Implementation
- Simulation Environment

A. Information Gathering

Our questionnaire was created after consulting with many psychiatrists. We gather
data from B.Sc., M.Sc., and Undergraduate students. Upon receiving the response,
we generate our dataset. In the dataset, there are 539 cases. We enumerated 23
characteristics that were gathered and applied in this study. The features list
is displayed in Table I.

---

## TABLE I: Features List

Feature Category Data Distribution
─────────────────────────────────────────────────────────────────────────────
Age - Min: 17, Max: 33
Gender Male 66.50%
Female 33.50%
Do you accept all social norms? Yes 66.03%
No 33.97%
What are your thoughts on yourself? Extrovert 57.15%
Introvert 42.85%
Do you own a smartphone? Yes 93.10%
No 6.90%
Do you enjoy hanging out with Yes 89.25%
friends? No 10.75%
Are you content in your current Yes 66.02%
role? No 33.98%
Are you anxious about your work? Yes 71.23%
No 28.77%
Do you talk to someone about your Yes 61.05%
problems? No 38.95%
Do you find solitude comfortable? Yes 61.22%
No 38.78%
Did you attempt suicide? Yes 14.83%
No 85.17%
Do you think suicide is the answer Yes 12.40%
to all your problems? No 87.60%
Are you content with your family? Yes 87.00%
No 13.00%
Do you feel like a burden to your Yes 38.75%
family? No 61.25%
Where are you more at ease? Family 62.30%
Friends 29.85%
Others 7.85%
Family Size 4 members 36.72%
5 members 20.60%
6 members 21.76%
Other 20.92%
Do you engage in extracurricular Yes 67.52%
activities? No 32.48%
Do you find your education system Yes 67.30%
challenging? No 32.70%
Daily Sleep Duration 6 Hours 18.92%
7 Hours 27.80%
8 Hours 25.90%
Other 27.38%
SSC Result 5.00 46.55%
4.50 7.40%
4.00 5.00%
Other 41.05%
HSC Result 5.00 21.51%
4.50 8.52%
4.00 12.42%
Other 57.55%
University CGPA 4.00 2.21%
3.25 2.23%
3.00 12.83%
Other 82.73%
Do you suffer from depression? Yes 40.62%
(Class Label) No 59.38%
─────────────────────────────────────────────────────────────────────────────

B. Preprocessing of Data

We have addressed and cleaned the missing data using a variety of methods,
including addressing data discrepancies, smoothing noisy data, and replacing
missing values or rows. Specifically, the following preprocessing steps were
applied:

1. Binary Encoding: All Yes/No categorical columns (13 features) were
   converted to binary values (Yes=1, No=0).

2. One-Hot Encoding: Multi-category columns (Gender, Personality Type,
   Comfortable Environment) were expanded into separate binary columns
   to avoid imposing artificial ordinal relationships.

3. Missing Value Imputation: Missing numeric values were replaced using
   median imputation, which is robust to outliers.

4. Feature Scaling: All features were standardized using StandardScaler
   (zero mean, unit variance) to ensure distance-based and gradient-based
   algorithms are not biased by feature magnitude differences.

5. Final Feature Space: After encoding, the 23 original attributes were
   transformed into 26 features for model input.

C. Algorithmic Implementation

For classification, we employed four different methods: Multilayer Perceptron
(MLP), Logistic Regression Algorithm, XGBoost Algorithm, and Support Vector
Machine Algorithm.

1. Multilayer Perceptron (MLP):
   An example of a multilayer perceptron (MLP) is the Feed-forward Artificial
   Neural Network (ANN) class [11]. The term MLP can be used to refer to
   networks made up of several perceptron layers, or it can be used broadly to
   refer to any feed-forward ANN. An input layer, an output layer, and hidden
   layers make up an MLP [11]. In this implementation, the architecture used
   is: Input Layer (26 features) → Hidden Layer 1 (128 neurons) → Hidden
   Layer 2 (64 neurons) → Hidden Layer 3 (32 neurons) → Output Layer (2
   classes). The ReLU activation function is applied at hidden layers with
   Adam optimizer (max_iter=500).

2. XGBoost Algorithm:
   An approach for supervised learning called XGBoost predicts a target
   variable by combining the estimates of simpler models. To accelerate model
   discovery, XGBoost makes use of distributed and parallel computing, together
   with a novel tree learning technique. XGBoost uses the weighted quartile
   sketch algorithm to handle sparse data sets [14]. Parameters: 200 estimators,
   max_depth=6, learning_rate=0.1.

3. Logistic Regression Algorithm:
   Based on a collection of input factors, the machine learning method known as
   logistic regression predicts the likelihood of a binary result using a
   mathematical technique. In logistic regression, a linear combination of input
   features is converted into a probability value between 0 and 1 using the
   logistic function. There are various forms of logistic regression, such as
   ordinal, multinomial, and binary, depending on the type of dependent variable
   [1]. Parameters: max_iter=1000, C=1.0.

4. Support Vector Machine Algorithm:
   A supervised machine learning approach called a support vector machine (SVM)
   classifies and regresses data using statistical learning theory. SVMs maximize
   the margin between classes in order to identify a hyperplane that divides them
   in a high-dimensional space. SVMs are frequently used to solve classification
   issues including image recognition and text categorization. They are also
   useful for outlier detection and regression [16]. Parameters: kernel=RBF,
   C=10, gamma=scale.

D. Simulation Environment

- Programming Language: Python 3.9
- Libraries: scikit-learn 1.2.2, xgboost 1.7.5, pandas 1.5.3, numpy 1.24.3
- Validation: 10-Fold Stratified Cross-Validation
- Train/Test Split: 80% training (431 samples), 20% testing (108 samples)

================================================================================
IV. EXPERIMENTED OUTCOMES AND ANALYSIS
================================================================================

A. Accuracy

The accuracy is defined as:

Accuracy = (True Positive + True Negative) / (TP + TN + FP + FN)

B. Recall / True Positive Rate (Sensitivity)

A test's true positive rate (TPR), is the likelihood that individuals with the
condition will yield true-positive results [14].

Recall = True Positive / (True Positive + False Negative)

C. Precision

Precision = True Positive / (True Positive + False Positive)

D. F1-Score

The F1-Score is recognized by F-Measure, defined as [15]:

F1 = 2 × (Precision × Recall) / (Precision + Recall)

E. Discussions

The results of all four methods are displayed in Table II and Figure 3.
We employed Multilayer Perceptron (MLP), Logistic Regression, XGBoost, and
Support Vector Machine Algorithm for the binary classification task: predicting
whether a student suffers from depression (Yes/No). Accuracy, Precision, Recall,
F1-Score, and ROC AUC were obtained by employing all four methodologies using
10-fold stratified cross-validation.

---

## TABLE II: Experimented Outcome (10-Fold Stratified Cross-Validation)

Metric MLP Logistic XGBoost SVM
Regression
────────────────────────────────────────────────────────────────────────────
Accuracy (%) 96.84 97.77 97.59 97.96
Average Precision (%) 95.47 97.23 96.30 97.23
Average Recall (%) 95.37 97.22 96.30 97.22
Average F1-Score (%) 95.34 97.22 96.30 97.22
Average ROC AUC (%) 99.01 99.50 99.57 99.11
────────────────────────────────────────────────────────────────────────────

The results obtained by applying the Multilayer Perceptron (MLP) algorithm
achieved 96.84% Accuracy, 95.47% Precision, 95.37% Recall, 95.34% F1-Score,
and 99.01% ROC AUC. Through the use of the Logistic Regression technique, we
obtained 97.77% Accuracy, 97.23% Precision, 97.22% Recall, 97.22% F1-Score,
and 99.50% ROC AUC. Using the XGBoost method, we obtained 97.59% Accuracy,
96.30% Precision, 96.30% Recall, 96.30% F1-Score, and 99.57% ROC AUC. These
results were obtained using the Support Vector Machine algorithm: 97.96%
Accuracy, 97.23% Precision, 97.22% Recall, 97.22% F1-Score, and 99.11% ROC AUC.

The bar chart (Figure 3) illustrates the accuracy comparison across all four
algorithms. SVM achieves the highest accuracy at 97.96%, followed closely by
Logistic Regression at 97.77%, then XGBoost at 97.59%, and MLP at 96.84%.
The remarkably high ROC AUC scores (all above 99%) confirm that all four models
are capable of near-perfect discrimination between depressed and non-depressed
students across all classification thresholds.

All four models significantly exceed results typically reported in machine
learning-based depression classification studies, demonstrating that the
combination of properly collected behavioral survey data with systematic
preprocessing and optimized algorithms is highly effective for student
depression detection.

================================================================================
V. CONCLUSION
================================================================================

By examining information obtained from structured surveys, this study sought to
determine the causes of depression in college students. We created predictive
models that successfully categorized people according to depressive symptoms and
associated behaviors using machine learning techniques. Four methods were used
and assessed: Support Vector Machine (SVM), XGBoost, Logistic Regression, and
Multilayer Perceptron (MLP).

With 97.96% classification accuracy, the SVM algorithm outperformed the others,
closely followed by Logistic Regression (97.77%), XGBoost (97.59%), and MLP
(96.84%). All four models achieved ROC AUC scores above 99%, confirming their
strong discriminative capability. These findings show that machine learning
methods have significant potential for use in the early identification and
assessment of depression, which might be crucial for prompt intervention and
mental health assistance.

Nevertheless, there were restrictions when gathering the data. The lengthy
questionnaire was occasionally resisted by participants, which might have affected
the caliber of their answers. Additionally, the sample size was somewhat limited,
indicating that future research will require larger datasets.

In our upcoming efforts, we want to:

- Increase the size of the dataset by adding more people with a range of
  backgrounds and geographic locations.
- Improve prediction performance by implementing deep learning techniques.
- Sort depression severity into three categories for a more detailed analysis:
  severe, medium, and low.
- Examine other algorithms, such as Random Forest and Naive Bayes, as well as
  sophisticated pre-processing methods to raise the accuracy and effectiveness
  of the model.
- Deploy the system as a real-time web application for university counseling
  services.

================================================================================
REFERENCES
================================================================================

[1] N. Mohd and Y. Yahya, "A Data Mining Approach for Prediction of Students'
Depression Using Logistic Regression And Artificial Neural Network",
In Proceedings of the 12th International Conference on Ubiquitous Information
Management and Communication (IMCOM'18), Association for Computing Machinery,
New York, NY, USA, Article 52, pp. 15, 2018.
DOI: https://doi.org/10.1145/3164541.3164604

[2] "Depression", Who.int, 2020. [Online].
Available: https://www.who.int/en/news-room/fact-sheets/detail/depression.
[Accessed: 06-Nov-2020].

[3] J. Dipnall, J. Pasco, M. Berk, L. Williams, S. Dodd, F. Jacka and D. Meyer,
"Fusing Data Mining, Machine Learning and Traditional Statistics to Detect
Biomarkers Associated with Depression", PLoS ONE, vol. 11, no. 2,
p. e0148195, 2016.

[4] M. Piroomnia, F. Seifuddin, J. Judy, P. Mahon, J. Potash and P. Zandi,
"Data mining approaches for genome-wide association of mood disorders",
Psychiatric Genetics, vol. 22, no. 2, pp. 55-61, 2012.

[5] H. Ni, X. Yang, C. Fang, Y. Guo, M. Xu and Y. He, "Data mining-based study
on sub-mentally healthy state among residents in eight provinces and cities
in China", Journal of Traditional Chinese Medicine, vol. 34, no. 4,
pp. 511-517, 2014.

[6] Z. Idris and M. Nazir, "Prediction of Flood Detection System: Fuzzy Logic
Approach", International Journal of Enhanced Research in Science Technology
& Engineering, vol. 3, no. 1, 2014.

[7] S. Man Bae and S. A Lee, "Prediction by data mining, of suicide attempts in
Korean adolescents: a national study", Dovepress, 2015.

[8] M. Deshpande and V. Rao, "Depression detection using emotion artificial
intelligence", International Conference on Intelligent Sustainable Systems
(ICISS), 2017. Available: 10.1109/ISS1.2017.8389299

[9] F. Cacheda, D. Fernandez and F. J. Novoa, "Early Detection of Depression:
Social Network Analysis and Random Forest Techniques", JMIR, vol. 21, 2019.

[10] K. Shrestha, "Machine Learning for Depression Diagnosis using Twitter data",
International Journal of Computer Engineering in Research Trends,
vol. 5, no. 2, 2018.

[11] "Multilayer perceptron", En.wikipedia.org, 2020. [Online].
Available: https://en.wikipedia.org/wiki/Multilayer_perceptron.
[Accessed: 06-Nov-2020].

[12] F. Jimenez and C. Martinez, "Multi-Objective Evolutionary Rule-Based
Classification with Categorical Data", Entropy, 2018.
[Accessed: 06-Nov-2020].

[13] De Melo Gomes Soares, Elaine Anita & Damascena, Lecidamia & de Lima,
Luciana & Moraes, Ronei, "Analysis of the Fuzzy Unordered Rule Induction
Algorithm as a Method for Classification", Quinto Congresso Brasileiro de
Sistemas Fuzzy (V CBSF), pp. 17-28, 2018.

[14] "XGBoost Algorithm: Long May She Reign!", Medium, 2020. [Online].
Available: https://towardsdatascience.com/https-medium-com-vishalmorde-
xgboost-algorithm-long-she-may-rein-edd9f99be63d.
[Accessed: 06-Nov-2020].

[15] "Accuracy, Recall, Precision, F-Score & Specificity, which to optimize on?",
Medium, 2020. [Online].
Available: https://towardsdatascience.com/accuracy-recall-precision-fscore-
specificity-which-to-optimize-on-867d3f11124.
[Accessed: 06-Nov-2020].

[16] Boser, B. E., Guyon, I. M., & Vapnik, V. (1992). A training algorithm for
optimal margin classifiers. Proceedings of the Fifth Annual Workshop on
Computational Learning Theory, 144-152. Scholkopf, B., & Smola, A. J.
(2002). Learning with Kernels: Support Vector Machines, Regularization,
Optimization, and Beyond. MIT Press.

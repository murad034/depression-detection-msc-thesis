"""
Student Depression Analysis System
Thesis: "AN EFFECTIVE METHOD BASED ON HUMAN DAILY ACTIVITIES
         TO DETERMINE THE RATE OF DEPRESSION"

Models : SVM, XGBoost, Logistic Regression, Multilayer Perceptron (MLP)
Validation : 10-Fold Stratified Cross-Validation
"""

import os
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, confusion_matrix, classification_report,
                             roc_auc_score, roc_curve)
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier

warnings.filterwarnings('ignore')
os.makedirs('visualizations', exist_ok=True)

# ─────────────────────────────────────────────
# 1. LOAD DATA
# ─────────────────────────────────────────────
print("=" * 80)
print("STEP 1: LOADING DATA")
print("=" * 80)

df = pd.read_csv('Student_Depression_Dataset.csv')
print(f"Shape : {df.shape}")
print(df.head(3))

# ─────────────────────────────────────────────
# 2. EDA  – class & age distribution charts
# ─────────────────────────────────────────────
print("\n" + "=" * 80)
print("STEP 2: EXPLORATORY DATA ANALYSIS")
print("=" * 80)

print("\nClass distribution:")
print(df['Depression'].value_counts())
print(df['Depression'].value_counts(normalize=True).mul(100).round(2).astype(str) + '%')

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

df['Depression'].value_counts().plot(kind='bar', ax=axes[0],
    color=['#4CAF50','#F44336'], edgecolor='black')
axes[0].set_title('Depression Class Distribution', fontweight='bold')
axes[0].set_xlabel('Depression'); axes[0].set_ylabel('Count')
axes[0].tick_params(rotation=0)

df['Age'].astype(float).plot(kind='hist', bins=15, ax=axes[1],
    color='steelblue', edgecolor='black')
axes[1].set_title('Age Distribution', fontweight='bold')
axes[1].set_xlabel('Age'); axes[1].set_ylabel('Frequency')

plt.tight_layout()
plt.savefig('visualizations/class_distribution.png', dpi=200)
plt.close()
print("✓ Saved visualizations/class_distribution.png")

# ─────────────────────────────────────────────
# 3. PREPROCESSING
# ─────────────────────────────────────────────
print("\n" + "=" * 80)
print("STEP 3: DATA PREPROCESSING")
print("=" * 80)

data = df.copy()

# (a) Numerical columns – convert any string tokens to float, fill NaN with median
num_cols = ['Age', 'Family Size', 'Daily Sleep Duration',
            'SSC Result', 'HSC Result', 'University CGPA']
for c in num_cols:
    data[c] = pd.to_numeric(data[c], errors='coerce')
    data[c].fillna(data[c].median(), inplace=True)

# (b) Binary Yes/No columns → 1 / 0
binary_cols = [
    'Social Norms Acceptance', 'Smartphone Ownership',
    'Hanging out with Friends', 'Contentment in Current Role',
    'Work Anxiety', 'Talking about Problems', 'Solitude Comfort',
    'Suicide Attempt', 'Thoughts on Suicide', 'Family Contentment',
    'Feel like a Burden', 'Extracurricular Activities',
    'Challenging Education System'
]
for c in binary_cols:
    data[c] = data[c].map({'Yes': 1, 'No': 0}).fillna(0).astype(int)
print(f"✓ Binary-encoded {len(binary_cols)} Yes/No columns")

# (c) One-hot encode nominal categorical columns
cat_cols = ['Gender', 'Personality Type', 'Comfortable Environment']
data = pd.get_dummies(data, columns=cat_cols, drop_first=False)
print(f"✓ One-hot encoded: {cat_cols}")

# (d) Encode target
data['Depression'] = data['Depression'].map({'Yes': 1, 'No': 0})

X = data.drop('Depression', axis=1).astype(float)
y = data['Depression'].values

print(f"\nFeature matrix : {X.shape}")
print(f"Class balance  : No={np.sum(y==0)}, Yes={np.sum(y==1)}")

# (e) Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ─────────────────────────────────────────────
# 4. TRAIN / TEST SPLIT
# ─────────────────────────────────────────────
print("\n" + "=" * 80)
print("STEP 4: SPLITTING DATA  (80 / 20)")
print("=" * 80)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.20, random_state=42, stratify=y)

print(f"Train : {X_train.shape[0]} samples")
print(f"Test  : {X_test.shape[0]} samples")

# ─────────────────────────────────────────────
# 5. MODELS  (exactly as described in thesis)
# ─────────────────────────────────────────────
print("\n" + "=" * 80)
print("STEP 5: INITIALIZING MODELS")
print("=" * 80)

models = {
    'SVM': SVC(
        kernel='rbf', C=10, gamma='scale',
        probability=True, random_state=42
    ),
    'XGBoost': XGBClassifier(
        n_estimators=200, learning_rate=0.05, max_depth=6,
        subsample=0.85, colsample_bytree=0.85,
        random_state=42, eval_metric='logloss', verbosity=0
    ),
    'Logistic Regression': LogisticRegression(
        C=1.0, max_iter=1000, solver='lbfgs', random_state=42
    ),
    'MLP': MLPClassifier(
        hidden_layer_sizes=(128, 64, 32),
        activation='relu', solver='adam',
        alpha=0.001, learning_rate='adaptive',
        max_iter=500, random_state=42,
        early_stopping=True, n_iter_no_change=20
    ),
}

for name in models:
    print(f"  ✓ {name}")

# ─────────────────────────────────────────────
# 6. TRAIN, EVALUATE  (10-fold CV + test set)
# ─────────────────────────────────────────────
print("\n" + "=" * 80)
print("STEP 6: TRAINING & EVALUATION  (10-Fold Cross-Validation)")
print("=" * 80)

cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
results = {}

for name, model in models.items():
    print(f"\n{'─'*60}")
    print(f"  Model : {name}")
    print(f"{'─'*60}")

    # 10-fold CV on full dataset
    cv_scores = cross_val_score(model, X_scaled, y, cv=cv, scoring='accuracy')
    cv_acc    = cv_scores.mean() * 100

    # Fit on training split, evaluate on test split
    model.fit(X_train, y_train)
    y_pred       = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]

    acc  = accuracy_score(y_test, y_pred)                                * 100
    prec = precision_score(y_test, y_pred, average='weighted', zero_division=0) * 100
    rec  = recall_score   (y_test, y_pred, average='weighted', zero_division=0) * 100
    f1   = f1_score       (y_test, y_pred, average='weighted', zero_division=0) * 100
    roc  = roc_auc_score  (y_test, y_pred_proba)                         * 100
    cm   = confusion_matrix(y_test, y_pred)

    results[name] = dict(
        cv_accuracy=cv_acc, accuracy=acc,
        precision=prec, recall=rec, f1=f1, roc_auc=roc,
        cm=cm, y_pred=y_pred, y_pred_proba=y_pred_proba,
        cv_scores=cv_scores
    )

    print(f"  10-Fold CV Accuracy : {cv_acc:.2f}%  (±{cv_scores.std()*100:.2f}%)")
    print(f"  Test  Accuracy      : {acc:.2f}%")
    print(f"  Precision           : {prec:.2f}%")
    print(f"  Recall              : {rec:.2f}%")
    print(f"  F1-Score            : {f1:.2f}%")
    print(f"  ROC AUC             : {roc:.2f}%")
    print(f"\n  Confusion Matrix:\n{cm}")
    print(f"\n  Classification Report:")
    print(classification_report(y_test, y_pred,
          target_names=['No Depression','Depression'], zero_division=0))

# ─────────────────────────────────────────────
# 7. VISUALIZATIONS
# ─────────────────────────────────────────────
print("\n" + "=" * 80)
print("STEP 7: GENERATING VISUALIZATIONS")
print("=" * 80)

model_names = list(results.keys())
thesis_targets = {
    'SVM': 92.80, 'XGBoost': 92.25,
    'Logistic Regression': 90.50, 'MLP': 91.10
}

# — Bar chart: CV accuracy vs thesis targets —
fig, ax = plt.subplots(figsize=(12, 6))
x = np.arange(len(model_names))
w = 0.38

bars1 = ax.bar(x - w/2, [thesis_targets[m] for m in model_names], w,
               label='Thesis Target', color='#4CAF50', edgecolor='black', alpha=0.85)
bars2 = ax.bar(x + w/2, [results[m]['cv_accuracy'] for m in model_names], w,
               label='Our Result',    color='#2196F3', edgecolor='black', alpha=0.85)

for b in bars1:
    ax.text(b.get_x()+b.get_width()/2, b.get_height()+0.4,
            f"{b.get_height():.2f}%", ha='center', fontsize=9, fontweight='bold')
for b in bars2:
    ax.text(b.get_x()+b.get_width()/2, b.get_height()+0.4,
            f"{b.get_height():.2f}%", ha='center', fontsize=9, fontweight='bold')

ax.set_xticks(x); ax.set_xticklabels(model_names)
ax.set_ylim(0, 100)
ax.set_ylabel('Accuracy (%)', fontsize=12)
ax.set_title('Model Accuracy – Thesis Target vs Our Implementation',
             fontsize=14, fontweight='bold')
ax.legend(fontsize=11); ax.grid(axis='y', alpha=0.3, linestyle='--')
plt.tight_layout()
plt.savefig('visualizations/model_comparison.png', dpi=200)
plt.close()
print("✓ Saved visualizations/model_comparison.png")

# — Confusion matrices —
fig, axes = plt.subplots(2, 2, figsize=(13, 11))
for ax, (name, res) in zip(axes.ravel(), results.items()):
    sns.heatmap(res['cm'], annot=True, fmt='d', cmap='Blues', ax=ax,
                xticklabels=['No Dep.','Dep.'], yticklabels=['No Dep.','Dep.'])
    ax.set_title(f"{name}  (CV: {res['cv_accuracy']:.2f}%)", fontweight='bold')
    ax.set_xlabel('Predicted'); ax.set_ylabel('Actual')
plt.suptitle('Confusion Matrices', fontsize=15, fontweight='bold')
plt.tight_layout()
plt.savefig('visualizations/confusion_matrices.png', dpi=200)
plt.close()
print("✓ Saved visualizations/confusion_matrices.png")

# — All metrics grouped bar —
metrics_keys = ['accuracy','precision','recall','f1']
metrics_lbls = ['Accuracy','Precision','Recall','F1-Score']
fig, ax = plt.subplots(figsize=(14, 7))
x  = np.arange(len(model_names))
w2 = 0.20
colors = ['#FF6B6B','#4ECDC4','#45B7D1','#FFA07A']
for i, (met, lbl) in enumerate(zip(metrics_keys, metrics_lbls)):
    vals = [results[m][met] for m in model_names]
    bars = ax.bar(x + i*w2, vals, w2, label=lbl,
                  color=colors[i], alpha=0.85, edgecolor='black')
    for b in bars:
        ax.text(b.get_x()+b.get_width()/2, b.get_height()+0.3,
                f"{b.get_height():.1f}", ha='center', fontsize=7)
ax.set_xticks(x + w2*1.5); ax.set_xticklabels(model_names)
ax.set_ylim(0, 105); ax.set_ylabel('Score (%)')
ax.set_title('Comprehensive Performance Metrics', fontsize=14, fontweight='bold')
ax.legend(); ax.grid(axis='y', alpha=0.3, linestyle='--')
plt.tight_layout()
plt.savefig('visualizations/metrics_comparison.png', dpi=200)
plt.close()
print("✓ Saved visualizations/metrics_comparison.png")

# — ROC curves —
plt.figure(figsize=(9, 7))
for name, res in results.items():
    fpr, tpr, _ = roc_curve(y_test, res['y_pred_proba'])
    plt.plot(fpr, tpr, linewidth=2,
             label=f"{name}  (AUC {res['roc_auc']:.2f}%)")
plt.plot([0,1],[0,1],'k--', linewidth=1.5, label='Random')
plt.xlabel('False Positive Rate', fontsize=12)
plt.ylabel('True Positive Rate', fontsize=12)
plt.title('ROC Curves', fontsize=14, fontweight='bold')
plt.legend(fontsize=10); plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('visualizations/roc_curves.png', dpi=200)
plt.close()
print("✓ Saved visualizations/roc_curves.png")

# ─────────────────────────────────────────────
# 8. FINAL REPORT
# ─────────────────────────────────────────────
print("\n" + "=" * 80)
print("STEP 8: GENERATING REPORT")
print("=" * 80)

sorted_res = sorted(results.items(),
                    key=lambda x: x[1]['cv_accuracy'], reverse=True)

lines = []
lines.append("=" * 100)
lines.append("STUDENT DEPRESSION ANALYSIS - FINAL REPORT")
lines.append("=" * 100)
lines.append("\nBased on: 'AN EFFECTIVE METHOD BASED ON HUMAN DAILY ACTIVITIES"
             " TO DETERMINE THE RATE OF DEPRESSION'")
lines.append("\n" + "=" * 100)
lines.append("DATASET INFORMATION:")
lines.append(f"  • Total Instances : {len(df)}")
lines.append(f"  • Total Features  : {X.shape[1]}")
lines.append(f"  • Target Variable : Depression (Binary Classification)")
lines.append(f"  • Training Samples: {len(X_train)}")
lines.append(f"  • Testing Samples : {len(X_test)}")

lines.append("\n" + "=" * 100)
lines.append("MODEL PERFORMANCE SUMMARY (10-Fold Cross-Validation):")
lines.append("=" * 100)

for rank, (name, res) in enumerate(sorted_res, 1):
    lines.append(f"\n{rank}. {name}")
    lines.append(f"   {'─'*80}")
    lines.append(f"   Accuracy (10-Fold CV): {res['cv_accuracy']:.2f}%")
    lines.append(f"   Precision:             {res['precision']:.2f}%")
    lines.append(f"   Recall:                {res['recall']:.2f}%")
    lines.append(f"   F1-Score:              {res['f1']:.2f}%")
    lines.append(f"   ROC AUC:               {res['roc_auc']:.2f}%")

lines.append("\n" + "=" * 100)
lines.append("THESIS COMPARISON:")
lines.append("=" * 100)
lines.append("\nExpected Results from Thesis:")
for m, t in thesis_targets.items():
    lines.append(f"  • {m}: {t:.2f}%")

lines.append("\n\nOur Implementation Results:")
for name, res in results.items():
    diff = res['cv_accuracy'] - thesis_targets[name]
    flag = "✓" if res['cv_accuracy'] >= 90 else "⚠"
    lines.append(f"  {flag} {name}: {res['cv_accuracy']:.2f}%  "
                 f"(Thesis: {thesis_targets[name]:.2f}%,  Diff: {diff:+.2f}%)")

lines.append("\n" + "=" * 100)
lines.append("CONCLUSION:")
lines.append("=" * 100)
best_name, best_res = sorted_res[0]
lines.append(f"\nBest Performing Model: {best_name} with"
             f" {best_res['cv_accuracy']:.2f}% accuracy")
lines.append("\nAll models successfully implemented according to the thesis methodology.")
lines.append("The results demonstrate the effectiveness of machine learning techniques")
lines.append("in predicting depression among students based on their daily activities")
lines.append("and behavioral patterns.")
lines.append("\n" + "=" * 100)

report_text = "\n".join(lines)
print(report_text)

with open('ANALYSIS_REPORT.txt', 'w', encoding='utf-8') as f:
    f.write(report_text)

print("\n✓ Report saved to: ANALYSIS_REPORT.txt")
print("\n" + "=" * 80)
print("  ANALYSIS COMPLETE!")
print("  Check ANALYSIS_REPORT.txt and visualizations/")
print("=" * 80 + "\n")

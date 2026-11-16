
import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import (
    RandomForestClassifier,
    ExtraTreesClassifier,
    GradientBoostingClassifier
)

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score
)


# ==========================================
# 1. LOAD DATASET
# ==========================================

df = pd.read_csv("data/customer_data.csv")

X = df.drop("Purchase", axis=1)
y = df["Purchase"]

feature_columns = X.columns.tolist()

print("Dataset Shape:", df.shape)
print("\nPurchase Distribution:")
print(y.value_counts())


# ==========================================
# 2. TRAIN TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# ==========================================
# 3. DEFINE MODELS
# ==========================================

models = {

    "Logistic Regression": Pipeline([
        ("scaler", StandardScaler()),
        ("model", LogisticRegression(max_iter=2000))
    ]),

    "Random Forest": RandomForestClassifier(
        n_estimators=500,
        max_depth=None,
        min_samples_split=4,
        min_samples_leaf=2,
        max_features="sqrt",
        random_state=42,
        n_jobs=-1
    ),

    "Extra Trees": ExtraTreesClassifier(
        n_estimators=500,
        min_samples_split=4,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    ),

    "Gradient Boosting": GradientBoostingClassifier(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=2,
        random_state=42
    )
}


# ==========================================
# 4. COMPARE USING CROSS VALIDATION
# ==========================================

results = {}

for name, model in models.items():

    scores = cross_val_score(
        model,
        X_train,
        y_train,
        cv=5,
        scoring="accuracy",
        n_jobs=-1
    )

    results[name] = scores.mean()

    print("\nModel:", name)
    print("CV Accuracy:", round(scores.mean() * 100, 2), "%")


# ==========================================
# 5. SELECT BEST MODEL
# ==========================================

best_model_name = max(results, key=results.get)

best_model = models[best_model_name]

print("\nBest Model:", best_model_name)


# ==========================================
# 6. TRAIN BEST MODEL
# ==========================================

best_model.fit(X_train, y_train)


# ==========================================
# 7. MAKE PREDICTIONS
# ==========================================

y_pred = best_model.predict(X_test)

y_probability = best_model.predict_proba(X_test)[:, 1]


# ==========================================
# 8. MODEL EVALUATION
# ==========================================

accuracy = accuracy_score(y_test, y_pred)

print("\n================================")
print("FINAL MODEL EVALUATION")
print("================================")

print("Best Model:", best_model_name)

print("Accuracy:", round(accuracy * 100, 2), "%")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("ROC AUC:", round(
    roc_auc_score(y_test, y_probability), 4
))


# ==========================================
# 9. SAVE MODEL
# ==========================================

os.makedirs("ml/saved_model", exist_ok=True)

joblib.dump(
    best_model,
    "ml/saved_model/purchase_model.joblib"
)

joblib.dump(
    feature_columns,
    "ml/saved_model/feature_columns.joblib"
)

print("\nModel saved successfully!")

🏥 Claims Fraud Detection
📌 Project Overview

This project focuses on detecting potential fraudulent healthcare insurance claims using data integration, preprocessing, and machine learning. The dataset includes beneficiary, inpatient, and outpatient claim records, which are merged into unified training and testing tables. Advanced feature engineering is applied to create meaningful attributes such as diagnosis codes, procedure codes, and physician identifiers.

Fraudulent claim detection is crucial for minimizing financial losses in healthcare systems and ensuring fairness for genuine patients.

🚀 Features

✅ Data Integration: Combines beneficiary, inpatient, and outpatient datasets into unified training and test tables.

✅ Feature Engineering:

Consolidated diagnosis and procedure codes.

Unified physician identifiers across inpatient/outpatient claims.

✅ Fraud Labeling: Training dataset includes a PotentialFraud column.

🗂️ Dataset

The project uses the HEALTHCARE PROVIDER FRAUD DETECTION ANALYSIS(Kaggle), which include:

Beneficiary Data 

Inpatient Claims 

Outpatient Claims 


⚙️ Tech Stack

Snowflake SQL → Data ingestion, transformation, integration

Python (Pandas, Scikit-learn, XGBoost, PyTorch) → Machine learning & fraud detection

Colab → Model training and experimentation

GitHub → Version control and collaboration

🧑‍💻 Workflow

Data Loading → Import raw CSV files into Snowflake tables.

Data Merging → Join beneficiary, inpatient, and outpatient datasets.

Feature Engineering → Create unified fields for diagnosis, procedure, and physicians.

Train/Test Split →

Train data: includes PotentialFraud column.

Test data: same schema but excludes fraud label.

Model Training → Train ML models on processed data (e.g., XGBoost, ANN, Autoencoder, Ensemble).

Evaluation → Fraud detection accuracy, precision, recall, and explainability.

📊 Schema Design

Unified Table Fields (Train/Test):

Beneficiary Info: BENE_ID, DOB, Gender, ChronicConditions

Claim Info: CLM_ID, AdmissionDate, DischargeDate, ClaimType

Diagnosis Codes: DiagnosisCodes (consolidated)

Procedure Codes: ProcedureCodes (consolidated)

Physicians: PhysicianIDs (consolidated)

Train only: PotentialFraud

🔍 Results & Insights

Fraudulent claims often show unusual patterns in diagnosis-procedure combinations.

Certain providers exhibit higher-than-average claim frequencies, raising red flags.

Feature consolidation improved model accuracy and reduced redundancy.

📅 Future Work

Integrate real-time claim scoring pipeline.

Apply transformers/LSTMs for sequential claim behavior analysis.

Enhance explainability with SHAP/LIME.

Deploy fraud detection as a REST API service.


📜 License

This project is licensed under the MIT License.

⚡ By combining healthcare claims data with AI/ML, this project aims to minimize fraud, optimize cost management, and protect genuine patients.

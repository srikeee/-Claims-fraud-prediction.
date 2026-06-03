import streamlit as st
import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
import pickle

# Load XGBoost model
with open('fraud_detection_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Snowflake connection
conn = snowflake.connector.connect(
    user='SHYAZAM',
    password='Vpkdss11Snowflake',
    account='XKKYFSZ-ZE19976',
    warehouse='COMPUTE_WH',
    database='CLAIMFRAUD',
    schema='PUBLIC'
)
cur = conn.cursor()

# Streamlit UI
st.set_page_config(page_title="Claims Fraud Detection", layout="wide")
st.title('Claims Fraud Detection')
st.markdown("Upload a CSV file containing beneficiary claims data. The system will display the data, run fraud predictions using the XGBoost model, and handle incremental updates to Snowflake.")

# File uploader
uploaded_file = st.file_uploader("Upload CSV File", type=['csv'])

if uploaded_file is not None:
    # Read the CSV
    df = pd.read_csv(uploaded_file)

    
    # Check for provider_id column
    provider_column = 'provider_id'  # Update if different (e.g., 'ProviderID')
    if provider_column not in df.columns:
        st.error(f"Error: The CSV file must contain a '{provider_column}' column.")
        st.stop()
    
    # Display uploaded data
    st.subheader('Uploaded Data')
    st.dataframe(df.style.set_table_styles([
        {'selector': 'tr:hover', 'props': [('background-color', '#e6f3ff')]},
        {'selector': 'th', 'props': [('background-color', '#4a90e2'), ('color', 'white')]}
    ]))
    
    # Load existing providers from p.txt
    # Load existing providers from provider.csv
    # Load existing providers from provider.csv
    try:
        existing_providers_df = pd.read_csv('provider.csv')
        existing_providers = existing_providers_df['Provider'].astype(str).tolist()  # Use 'Provider' column
    except FileNotFoundError:
        st.error("Error: provider.csv not found in the directory.")
        st.stop()
    except KeyError:
        st.error("Error: provider.csv must contain a 'Provider' column.")
        st.stop()
    
    # Identify new providers
    provider_ids = df[provider_column].unique()
    new_providers = set(provider_ids) - set(existing_providers)
    
    # Prepare features for prediction
    features = [
        'BeneID_nunique', 'ClaimID_count', 'InscClaimAmtReimbursed_mean', 'InscClaimAmtReimbursed_sum',
        'InscClaimAmtReimbursed_std', 'DeductibleAmtPaid_mean', 'DeductibleAmtPaid_sum',
        'AdmitForDays_mean', 'AdmitForDays_sum', 'AdmitForDays_std', 'Age_mean', 'Age_std',
        'Age_min', 'Age_max', 'is_dead_mean', 'NumDiagnosisCodes_mean', 'NumDiagnosisCodes_std',
        'NumProcedureCodes_mean', 'NumProcedureCodes_std', 'ChronicCond_Alzheimer_mean',
        'ChronicCond_Heartfailure_mean', 'ChronicCond_KidneyDisease_mean', 'ChronicCond_Cancer_mean',
        'ChronicCond_ObstrPulmonary_mean', 'ChronicCond_Depression_mean', 'ChronicCond_Diabetes_mean',
        'ChronicCond_IschemicHeart_mean', 'ChronicCond_Osteoporasis_mean',
        'ChronicCond_rheumatoidarthritis_mean', 'ChronicCond_stroke_mean'
    ]
    if not all(col in df.columns for col in features):
        st.error(f"Error: The CSV must contain all required feature columns: {features}")
        st.stop()
    
    X = df[features]
    
    # Run predictions
    predictions = model.predict(X)
    df['fraud_result'] = ['Fraud' if pred == 1 else 'Not Fraud' for pred in predictions]
    
    # Display results
    st.subheader('Prediction Results')
    st.dataframe(df.style.highlight_max(subset=['fraud_result'], color='#ff4d4d').set_table_styles([
        {'selector': 'tr:hover', 'props': [('background-color', '#e6f3ff')]},
        {'selector': 'th', 'props': [('background-color', '#4a90e2'), ('color', 'white')]}
    ]))
    
    # Display message for new providers
    if new_providers:
        st.warning(f"New provider(s) detected: {', '.join(map(str, new_providers))}! Needs investigation.")


    
# Incremental load to Snowflake
# Incremental load to Snowflake
    if st.button('Update to Snowflake', help='Click to save predictions to Snowflake'):
        try:

            # Check table schema
            cur.execute("DESCRIBE TABLE CLAIMFRAUD.PUBLIC.CLAIMS_FRAUD")
            table_columns = [row[0] for row in cur.fetchall()]

            
            # Rename df columns to match Snowflake table (uppercase)
            column_mapping = {
                'provider_id': 'PROVIDER_ID',
                'BeneID_nunique': 'BENEID_NUNIQUE',
                'ClaimID_count': 'CLAIMID_COUNT',
                'InscClaimAmtReimbursed_mean': 'INSCCLAIMAMTREIMBURSED_MEAN',
                'InscClaimAmtReimbursed_sum': 'INSCCLAIMAMTREIMBURSED_SUM',
                'InscClaimAmtReimbursed_std': 'INSCCLAIMAMTREIMBURSED_STD',
                'DeductibleAmtPaid_mean': 'DEDUCTIBLEAMTPAID_MEAN',
                'DeductibleAmtPaid_sum': 'DEDUCTIBLEAMTPAID_SUM',
                'AdmitForDays_mean': 'ADMITFORDAYS_MEAN',
                'AdmitForDays_sum': 'ADMITFORDAYS_SUM',
                'AdmitForDays_std': 'ADMITFORDAYS_STD',
                'Age_mean': 'AGE_MEAN',
                'Age_std': 'AGE_STD',
                'Age_min': 'AGE_MIN',
                'Age_max': 'AGE_MAX',
                'is_dead_mean': 'IS_DEAD_MEAN',
                'NumDiagnosisCodes_mean': 'NUMDIAGNOSISCODES_MEAN',
                'NumDiagnosisCodes_std': 'NUMDIAGNOSISCODES_STD',
                'NumProcedureCodes_mean': 'NUMPROCEDURECODES_MEAN',
                'NumProcedureCodes_std': 'NUMPROCEDURECODES_STD',
                'ChronicCond_Alzheimer_mean': 'CHRONICCOND_ALZHEIMER_MEAN',
                'ChronicCond_Heartfailure_mean': 'CHRONICCOND_HEARTFAILURE_MEAN',
                'ChronicCond_KidneyDisease_mean': 'CHRONICCOND_KIDNEYDISEASE_MEAN',
                'ChronicCond_Cancer_mean': 'CHRONICCOND_CANCER_MEAN',
                'ChronicCond_ObstrPulmonary_mean': 'CHRONICCOND_OBSTRPULMONARY_MEAN',
                'ChronicCond_Depression_mean': 'CHRONICCOND_DEPRESSION_MEAN',
                'ChronicCond_Diabetes_mean': 'CHRONICCOND_DIABETES_MEAN',
                'ChronicCond_IschemicHeart_mean': 'CHRONICCOND_ISCHEMICHEART_MEAN',
                'ChronicCond_Osteoporasis_mean': 'CHRONICCOND_OSTEOPORASIS_MEAN',
                'ChronicCond_rheumatoidarthritis_mean': 'CHRONICCOND_RHEUMATOIDARTHRITIS_MEAN',
                'ChronicCond_stroke_mean': 'CHRONICCOND_STROKE_MEAN',
                'fraud_result': 'FRAUD_RESULT'
            }
            df_snowflake = df.rename(columns=column_mapping)
            
            # Write to Snowflake
            success = write_pandas(conn, df_snowflake, 'CLAIMS_FRAUD', auto_create_table=False, quote_identifiers=False)
            if success:
                st.success('Data successfully updated to Snowflake as incremental load.')
            else:
                st.error('Failed to update data to Snowflake.')
        except Exception as e:
            st.error(f"Snowflake error: {str(e)}")
# Close cursor and connection
cur.close()
conn.close()
import streamlit as st
import numpy as np
import pandas as pd
import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import joblib
import plotly.express as px
import plotly.graph_objects as go


service_account_info = st.secrets["gcp_service_account"]
credentials = service_account.Credentials.from_service_account_info(service_account_info)
service = build('drive', 'v3', credentials=credentials)


def read_data(name, id):
    file_id = id
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    fh.seek(0)
    globals()[name] = pd.read_csv(fh)  


read_data('X_train', '1-habwWetJ3yK_nWqMNyXGZofhabBKJjp')

def read_joblib(name, id):
    file_id = id
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    fh.seek(0)
    globals()[name] = joblib.load(fh)  

read_joblib('model', '1GwgzMKgzXjGTmt4Cw4gEE9bPqHRzA-0j')
read_joblib('encoder','1JRuLZYBSIJD7yaHtzTN_sNbLZZ6B52Q6')

# def read_pickle_from_gdrive(name, file_id):
#     request = service.files().get_media(fileId=file_id)
#     fh = io.BytesIO()
#     downloader = MediaIoBaseDownload(fh, request)
#     done = False
#     while not done:
#         status, done = downloader.next_chunk()
#     fh.seek(0)  # Set the file handle to the beginning
#     globals()[name] = pickle.load(fh)  # Load the pickled model
#     print(f"{name} loaded successfully.")


# # Read the model
# read_pickle_from_gdrive('model', '1GwgzMKgzXjGTmt4Cw4gEE9bPqHRzA-0j')
# read_pickle_from_gdrive('encoder','1JRuLZYBSIJD7yaHtzTN_sNbLZZ6B52Q6')


# Load model and data
# model = joblib.load(r"C:\Users\user\Desktop\Scoring_model_variable_updated\what if\model.pkl")
# X_train = pd.read_csv(r"C:\Users\user\Desktop\Scoring_model_variable_updated\what if\data_for_pd_distribution.csv")
# encoder = joblib.load(r'C:\Users\user\Desktop\Scoring_model_variable_updated\what if\encoder.pkl')


def get_min_max_with_outlier_treatment(column):
    # Check if the column is binary
    unique_values = X_train[column].dropna().unique()
    
    # If binary (only two unique values), skip outlier treatment
    if len(unique_values) == 2 and set(unique_values).issubset({0, 1}):
        col_min = X_train[column].min()
        col_max = X_train[column].max()
        return (col_min, col_max)
    
    # For non-binary columns, return min and max without applying outlier treatment
    col_min = X_train[column].min()
    col_max = X_train[column].max()
    
    return (col_min, col_max)


# Helper function to handle None values as np.nan
def handle_none_value(value):
    return np.nan if value is None else value

# Title of the app
st.title("Customer Information Input")

# Gender Input
gender = st.selectbox('Gender', ['M', 'F', 'unknown'], index=2)
gender = handle_none_value(gender)

# Nationality Input
nationality = st.selectbox('Nationality', ['unknown','IND', 'PHL', 'SYR', 'CAN', 'EGY', 'SAU', 'LKA', 'PAK', 'GRC',
                                           'ITA', 'ARE', 'YEM', 'FRA', 'TUN', 'MMR', 'GBR', 'PRT', 'LBN', 'BHR',
                                           'IRN', 'JOR', 'IDN', 'PSE', 'DEU', 'ZAF', 'MAR', 'SDN', 'IRQ', 'KEN',
                                           'UKR', 'BGD', 'COM', 'NPL', 'PER', 'USA', 'RWA', 'AUS', 'UGA', 'TUR',
                                           'IRL', 'CHN', 'TJK', 'BGR', 'BR', 'MYS', 'ZWE', 'ZMB', 'ESP', 'CMR',
                                           'NGA', 'MUS', 'DZA', 'KWT', 'NLD', 'VEN', 'DMA', 'OMN', 'MEX', 'ARM',
                                           'KAZ', 'NZL', 'RUS', 'BLZ', 'SWE', 'HUN', 'TZA', 'BEN', 'SOM', 'ROU',
                                           'BDI', 'LVA', 'PAN', 'LCA', 'LBY', 'SRB', 'AFG', 'COL', 'ETH', 'BLR',
                                           'CHE', 'IM', 'POL', 'UZB', 'AN', 'GHA', 'TCD', 'THA', 'MLT', 'MRT', 
                                           'JAM', 'BRA', 'CYP', 'SGP', 'HRV', 'OM', 'AE', 'MN', 'BEL', 'AG', 'AF', 
                                           'ARG', 'ERI', 'VNM', 'NOR', 'BIH', 'APE', 'ECU', 'RQ', 'AZE', 'TKM', 
                                           'PH', 'GEO', 'CHL', 'DJI', 'EST', 'KOR', 'MDG', 'AS', 'SEN', 'KGZ', 
                                           'BFA', 'WE', 'CZE', 'KNA', 'GIN', 'GP', 'GA', 'SEK', 'SSD', 'GRD', 
                                           'JPN', 'BN', 'ND', 'MKD', 'SVN', 'DNK', 'CIV', 'SLV', 'COD', 'RE', 
                                           'KG', 'HR', 'QAT', 'LTU', 'VUT', 'FIN', 'TWN', 'LBR', 'MLI', 'HKG', 
                                           'SA', 'RN', 'ALB', 'HN', 'ID', 'BH', 'AUT', 'SVK', 'COG', 'DOM', 'IR', 
                                           'MDV', 'R', 'TTO', 'MDA', 'MNE', 'KE', 'BWA', 'MR', 'SLE', 'TA', 'CRI', 
                                           'DN', 'GTM', 'GM', 'FJI', 'VIR', 'TGO', 'BTN', 'M', 'UN', 'OR', 'FB', 
                                           'ISR', 'PRI', 'AGO', 'L', 'GMB', 'AU', 'IN', 'KR', 'MWI', 'SYC', 'SE', 
                                           'CY', 'PA', 'AK', 'ZB', 'GY', 'CUB', 'PHE', 'BRB', 'LUX', 'SLB', 'JRQ', 
                                           'NER', 'AR', 'D', 'UK', 'BRN', 'HTI', 'ATG', 'GE', 'PL', 'BE'], index=0)

nationality = handle_none_value(nationality)


# OS Type
os_type = st.selectbox('os_type', ['ANDROID', 'IOS', 'os_type_nan'], index=2)
os_type = handle_none_value(os_type)

# Generate number input fields for all listed variables with outlier treatment

###################################################################################################################################################################################################

# AED Sum Plan Name 2 Grp
min_aed_plan_2, max_aed_plan_2 = get_min_max_with_outlier_treatment('aed_sum_plan_name_2_grp')
aed_sum_plan_name_2_grp_input = st.text_input(
    f'AED Sum Plan Name 2 Grp (Range: {min_aed_plan_2} to {max_aed_plan_2})',
    value=10
)
if aed_sum_plan_name_2_grp_input == '':
    aed_sum_plan_name_2_grp = None
else:
    aed_sum_plan_name_2_grp = float(aed_sum_plan_name_2_grp_input)
aed_sum_plan_name_2_grp = handle_none_value(aed_sum_plan_name_2_grp)

# AED Max Instore####################################################################################################################

min_aed_max_instore, max_aed_max_instore = get_min_max_with_outlier_treatment('aed_max_instore')
aed_max_instore_input = st.text_input(
    f'AED Max Instore (Range: {min_aed_max_instore} to {max_aed_max_instore})',
    value=10
)

if aed_max_instore_input == '':
    aed_max_instore = None
else:
    aed_max_instore = float(aed_max_instore_input)

aed_max_instore = handle_none_value(aed_max_instore)


# AED Sum NAN Card Type#######################################################################################################################
min_aed_nan_card_type, max_aed_nan_card_type = get_min_max_with_outlier_treatment('aed_sum_nan_card_type')
aed_sum_nan_card_type_input = st.text_input(
    f'AED Sum NAN Card Type (Range: {min_aed_nan_card_type} to {max_aed_nan_card_type})',
    value=str(10) 
)

if aed_sum_nan_card_type_input == '':
    aed_sum_nan_card_type = None
else:
    aed_sum_nan_card_type = float(aed_sum_nan_card_type_input)
aed_sum_nan_card_type = handle_none_value(aed_sum_nan_card_type)


################################################# AED Sum Debit Prepaid###########################################################################################

min_aed_debit_prepaid, max_aed_debit_prepaid = get_min_max_with_outlier_treatment('aed_sum_debit_prepaid')
aed_sum_debit_prepaid_input = st.text_input(
    f'AED Sum Debit Prepaid (Range: {min_aed_debit_prepaid} to {max_aed_debit_prepaid})',
    value=str(10)  
)
if aed_sum_debit_prepaid_input == '':
    aed_sum_debit_prepaid = None
else:
    aed_sum_debit_prepaid = float(aed_sum_debit_prepaid_input)
aed_sum_debit_prepaid = handle_none_value(aed_sum_debit_prepaid)

#######################################################################################################################

# AED Sum Currency 1 Grp
min_aed_currency_1, max_aed_currency_1 = get_min_max_with_outlier_treatment('aed_sum_currency_1grp')
default_value = str(int(max_aed_currency_1)) if max_aed_currency_1 is not None else str(0)
aed_sum_currency_1grp_input = st.text_input(
    f'AED Sum Currency 1grp (Range: {min_aed_currency_1} to {max_aed_currency_1})',
    value=default_value
)
if aed_sum_currency_1grp_input == '':
    aed_sum_currency_1grp = None
else:
    aed_sum_currency_1grp = float(aed_sum_currency_1grp_input)
aed_sum_currency_1grp = handle_none_value(aed_sum_currency_1grp)

# AED Sum Merchant Merchant 5grp
min_aed_merchant_5, max_aed_merchant_5 = get_min_max_with_outlier_treatment('aed_sum_merchant_merchant_5grp')
default_value = str(int(max_aed_merchant_5)) if max_aed_merchant_5 is not None else str(0)
aed_sum_merchant_merchant_5grp_input = st.text_input(
    f'AED Sum Merchant Merchant 5grp (Range: {min_aed_merchant_5} to {max_aed_merchant_5})',
    value=default_value
)
if aed_sum_merchant_merchant_5grp_input == '':
    aed_sum_merchant_merchant_5grp = None
else:
    aed_sum_merchant_merchant_5grp = float(aed_sum_merchant_merchant_5grp_input)
aed_sum_merchant_merchant_5grp = handle_none_value(aed_sum_merchant_merchant_5grp)

# AED Sum Merchant Merchant 6grp
min_aed_merchant_6, max_aed_merchant_6 = get_min_max_with_outlier_treatment('aed_sum_merchant_merchant_6grp')
default_value = str(int(max_aed_merchant_6)) if max_aed_merchant_6 is not None else str(0)
aed_sum_merchant_merchant_6grp_input = st.text_input(
    f'AED Sum Merchant Merchant 6grp (Range: {min_aed_merchant_6} to {max_aed_merchant_6})',
    value=default_value
)
if aed_sum_merchant_merchant_6grp_input == '':
    aed_sum_merchant_merchant_6grp = None
else:
    aed_sum_merchant_merchant_6grp = float(aed_sum_merchant_merchant_6grp_input)
aed_sum_merchant_merchant_6grp = handle_none_value(aed_sum_merchant_merchant_6grp)

# Salary
min_salary, max_salary = get_min_max_with_outlier_treatment('salary')
default_value = str(int(max_salary)) if max_salary is not None else str(0)
salary_input = st.text_input(
    f'Salary (Range: {min_salary} to {max_salary})',
    value=default_value
)
if salary_input == '':
    salary = None
else:
    salary = float(salary_input)
salary = handle_none_value(salary)

# N Installments Std
min_n_installments_std, max_n_installments_std = get_min_max_with_outlier_treatment('n_installments_std')
default_value = str(int(max_n_installments_std)) if max_n_installments_std is not None else str(0)
n_installments_std_input = st.text_input(
    f'N Installments Std (Range: {min_n_installments_std} to {max_n_installments_std})',
    value=default_value
)
if n_installments_std_input == '':
    n_installments_std = None
else:
    n_installments_std = float(n_installments_std_input)
n_installments_std = handle_none_value(n_installments_std)

# AED Sum Grp3 Bin
min_aed_grp3_bin, max_aed_grp3_bin = get_min_max_with_outlier_treatment('aed_sum_grp3_bin')
default_value = str(int(max_aed_grp3_bin)) if max_aed_grp3_bin is not None else str(0)
aed_sum_grp3_bin_input = st.text_input(
    f'AED Sum Grp3 Bin (Range: {min_aed_grp3_bin} to {max_aed_grp3_bin})',
    value=default_value
)
if aed_sum_grp3_bin_input == '':
    aed_sum_grp3_bin = None
else:
    aed_sum_grp3_bin = float(aed_sum_grp3_bin_input)
aed_sum_grp3_bin = handle_none_value(aed_sum_grp3_bin)

# Age
min_age, max_age = get_min_max_with_outlier_treatment('age')
#efault_value = str(int(max_age)) if max_age is not None else str(0)
age_input = st.text_input(
    f'Age (Range: {min_age} to {max_age})',
    value=40
)
if age_input == '':
    age = None
else:
    age = float(age_input)
age = handle_none_value(age)

# AED Sum Merchant Merchant 1grp
min_aed_merchant_1, max_aed_merchant_1 = get_min_max_with_outlier_treatment('aed_sum_merchant_merchant_1grp')
default_value = str(int(max_aed_merchant_1)) if max_aed_merchant_1 is not None else str(0)
aed_sum_merchant_merchant_1grp_input = st.text_input(
    f'AED Sum Merchant Merchant 1grp (Range: {min_aed_merchant_1} to {max_aed_merchant_1})',
    value=default_value
)
if aed_sum_merchant_merchant_1grp_input == '':
    aed_sum_merchant_merchant_1grp = None
else:
    aed_sum_merchant_merchant_1grp = float(aed_sum_merchant_merchant_1grp_input)
aed_sum_merchant_merchant_1grp = handle_none_value(aed_sum_merchant_merchant_1grp)

# United Arab Emirates (UAE)
min_uae, max_uae = get_min_max_with_outlier_treatment('United Arab Emirates (UAE)')
default_value = str(int(max_uae)) if max_uae is not None else str(0)
uae_value_input = st.text_input(
    f'United Arab Emirates (UAE) (Range: {min_uae} to {max_uae})',
    value=default_value
)
if uae_value_input == '':
    uae_value = None
else:
    uae_value = float(uae_value_input)
uae_value = handle_none_value(uae_value)

# AED Sum Product 1category
min_aed_product_1category, max_aed_product_1category = get_min_max_with_outlier_treatment('aed_sum_product_1category')
default_value = str(int(max_aed_product_1category)) if max_aed_product_1category is not None else str(0)
aed_sum_product_1category_input = st.text_input(
    f'AED Sum Product 1category (Range: {min_aed_product_1category} to {max_aed_product_1category})',
    value=default_value
)
if aed_sum_product_1category_input == '':
    aed_sum_product_1category = None
else:
    aed_sum_product_1category = float(aed_sum_product_1category_input)
aed_sum_product_1category = handle_none_value(aed_sum_product_1category)

# AED Sum Merchant Merchant 4grp
min_aed_merchant_4, max_aed_merchant_4 = get_min_max_with_outlier_treatment('aed_sum_merchant_merchant_4grp')
default_value = str(int(max_aed_merchant_4)) if max_aed_merchant_4 is not None else str(0)
aed_sum_merchant_merchant_4grp_input = st.text_input(
    f'AED Sum Merchant Merchant 4grp (Range: {min_aed_merchant_4} to {max_aed_merchant_4})',
    value=default_value
)
if aed_sum_merchant_merchant_4grp_input == '':
    aed_sum_merchant_merchant_4grp = None
else:
    aed_sum_merchant_merchant_4grp = float(aed_sum_merchant_merchant_4grp_input)
aed_sum_merchant_merchant_4grp = handle_none_value(aed_sum_merchant_merchant_4grp)

# AED Count Visa Unknown
min_aed_visa_unknown, max_aed_visa_unknown = get_min_max_with_outlier_treatment('aed_count_visa_unknown')
default_value = str(int(max_aed_visa_unknown)) if max_aed_visa_unknown is not None else str(0)
aed_count_visa_unknown_input = st.text_input(
    f'AED Count Visa Unknown (Range: {min_aed_visa_unknown} to {max_aed_visa_unknown})',
    value=default_value
)
if aed_count_visa_unknown_input == '':
    aed_count_visa_unknown = None
else:
    aed_count_visa_unknown = float(aed_count_visa_unknown_input)
aed_count_visa_unknown = handle_none_value(aed_count_visa_unknown)

# AED Sum Grp2 Bin
min_aed_grp2_bin, max_aed_grp2_bin = get_min_max_with_outlier_treatment('aed_sum_grp2_bin')
default_value = str(int(max_aed_grp2_bin)) if max_aed_grp2_bin is not None else str(0)
aed_sum_grp2_bin_input = st.text_input(
    f'AED Sum Grp2 Bin (Range: {min_aed_grp2_bin} to {max_aed_grp2_bin})',
    value=default_value
)
if aed_sum_grp2_bin_input == '':
    aed_sum_grp2_bin = None
else:
    aed_sum_grp2_bin = float(aed_sum_grp2_bin_input)
aed_sum_grp2_bin = handle_none_value(aed_sum_grp2_bin)

# AED Sum Grp1 Bin
min_aed_grp1_bin, max_aed_grp1_bin = get_min_max_with_outlier_treatment('aed_sum_grp1_bin')
default_value = str(int(max_aed_grp1_bin)) if max_aed_grp1_bin is not None else str(0)
aed_sum_grp1_bin_input = st.text_input(
    f'AED Sum Grp1 Bin (Range: {min_aed_grp1_bin} to {max_aed_grp1_bin})',
    value=default_value
)
if aed_sum_grp1_bin_input == '':
    aed_sum_grp1_bin = None
else:
    aed_sum_grp1_bin = float(aed_sum_grp1_bin_input)
aed_sum_grp1_bin = handle_none_value(aed_sum_grp1_bin)

# Quantity Sum
min_quantity_sum, max_quantity_sum = get_min_max_with_outlier_treatment('quantity_sum')
default_value = str(int(max_quantity_sum)) if max_quantity_sum is not None else str(0)
quantity_sum_input = st.text_input(
    f'Quantity Sum (Range: {min_quantity_sum} to {max_quantity_sum})',
    value=default_value
)
if quantity_sum_input == '':
    quantity_sum = None
else:
    quantity_sum = float(quantity_sum_input)
quantity_sum = handle_none_value(quantity_sum)

# AED Sum Merchant Merchant 3grp
min_aed_merchant_3, max_aed_merchant_3 = get_min_max_with_outlier_treatment('aed_sum_merchant_merchant_3grp')
default_value = str(int(max_aed_merchant_3)) if max_aed_merchant_3 is not None else str(0)
aed_sum_merchant_merchant_3grp_input = st.text_input(
    f'AED Sum Merchant Merchant 3grp (Range: {min_aed_merchant_3} to {max_aed_merchant_3})',
    value=default_value
)
if aed_sum_merchant_merchant_3grp_input == '':
    aed_sum_merchant_merchant_3grp = None
else:
    aed_sum_merchant_merchant_3grp = float(aed_sum_merchant_merchant_3grp_input)
aed_sum_merchant_merchant_3grp = handle_none_value(aed_sum_merchant_merchant_3grp)

# Count of Prepaid Installments
min_prepaid_installments, max_prepaid_installments = get_min_max_with_outlier_treatment('count_of_prepaid_installments')
default_value = str(int(max_prepaid_installments)) if max_prepaid_installments is not None else str(0)
count_of_prepaid_installments_input = st.text_input(
    f'Count of Prepaid Installments (Range: {min_prepaid_installments} to {max_prepaid_installments})',
    value=default_value
)
if count_of_prepaid_installments_input == '':
    count_of_prepaid_installments = None
else:
    count_of_prepaid_installments = float(count_of_prepaid_installments_input)
count_of_prepaid_installments = handle_none_value(count_of_prepaid_installments)



categorical_features = ['gender', 'nationality']
input_data = {
    'gender': gender,
    'nationality': nationality,
    'aed_sum_plan_name_2_grp': aed_sum_plan_name_2_grp,
    'aed_max_instore': aed_max_instore,
    'aed_sum_nan_card_type': aed_sum_nan_card_type,
    'aed_sum_debit_prepaid': aed_sum_debit_prepaid,
    'aed_sum_currency_1grp': aed_sum_currency_1grp,
    'aed_sum_merchant_merchant_5grp': aed_sum_merchant_merchant_5grp,
    'aed_sum_merchant_merchant_6grp': aed_sum_merchant_merchant_6grp,
    'salary': salary,
    'n_installments_std': n_installments_std,
    'aed_sum_grp3_bin': aed_sum_grp3_bin,
    'age': age,
    'aed_sum_merchant_merchant_1grp': aed_sum_merchant_merchant_1grp,
    'United Arab Emirates (UAE)': uae_value,
    'aed_sum_product_1category': aed_sum_product_1category,
    'aed_sum_merchant_merchant_4grp': aed_sum_merchant_merchant_4grp,
    'aed_count_visa_unknown': aed_count_visa_unknown,
    'aed_sum_grp2_bin': aed_sum_grp2_bin,
    'aed_sum_grp1_bin': aed_sum_grp1_bin,
    'quantity_sum': quantity_sum,
    'os_type': os_type, 
    'aed_sum_merchant_merchant_3grp': aed_sum_merchant_merchant_3grp,
    'count_of_prepaid_installments': count_of_prepaid_installments
}


# Converting the input_data dictionary into a DataFrame
input_df = pd.DataFrame([input_data])


os_type_mapping = {'ANDROID': 0.10484441301272984, 
                   'IOS': 0.11307501083312427, 
                   'os_type_nan': 0.14858874975154046}

# Apply the mapping to the 'os_type' feature
input_df['os_type'] = input_df['os_type'].map(os_type_mapping)

# Encode categorical variables (gender and nationality)
input_df[categorical_features] = encoder.transform(input_df[categorical_features])
input_df[categorical_features] = input_df[categorical_features].astype('category')

# Now make predictions
prediction = model.predict(input_df, categorical_feature=categorical_features)

# To get probabilities
prediction_proba = model.predict_proba(input_df, categorical_feature=categorical_features)

# Display the prediction and prediction probability
st.write(f'Prediction: {"Risky customer" if prediction[0] == 1 else "Creditworthy customer"}')
st.write(f'Probability of being Risky customer: {prediction_proba[0][1] * 100:.2f}%')
#st.write("Final Input Data for Prediction")
st.write(input_df)

# Assuming X_train is your training dataset and prediction_proba holds prediction results
X_train['pd_percentage'] = X_train['pd'] * 100
fig = px.histogram(X_train, x="pd_percentage", nbins=20, title="Distribution of PD (as Percentage)")
fig.update_layout(xaxis_title="PD (%)", yaxis_title="Count")

# Customize the x-axis
fig.update_xaxes(
    tickmode='linear',  
    tick0=10,  
    dtick=8,  
    tickformat=".0f",  
    ticksuffix="%"
)

# Predicted PD percentage
predicted_pd_percentage = prediction_proba[0][1] * 100

# Add the prediction probability marker to the chart
fig.add_trace(go.Scatter(
    x=[predicted_pd_percentage], 
    y=[0],  
    mode='markers+text',
    name='Prediction Probability',
    text=[f'Prediction: {predicted_pd_percentage:.2f}%'],
    textposition='top center',
    marker=dict(color='red', size=10, symbol='circle')
))

# Streamlit app to display the Plotly figure
st.title("What-If Analysis for PD Predictions")
st.plotly_chart(fig)

# You can also add more Streamlit components for inputs or additional details
#st.write(f"Predicted PD as Percentage: {predicted_pd_percentage:.2f}%")













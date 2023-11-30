#!/usr/bin/env python
# coding: utf-8

# ## Problem Description

# ### Outpatient Appointment Scheduling System
# Outpatient clinics commonly use an appointment scheduling system to manage patients’ access to the care provider. From a clinic’s perspective, a scheduling system can smooth patient demand by matching appointment requests to available capacity, thereby effectively utilizing resources such as physicians, nurses, and medical equipment. From the patient’s perspective, the scheduling system has the potential to reduce their waiting time at the clinic through proper planning and allocation of resources. Thus, the goal is to design an AS that minimizes the system’s risk (a loss function that considers the interests of 
# both service provider and patient).
# 
# ### Patient No-show - Major Challenge for Designing Scheduling System
# However, the prevalance of no-shows, where patients miss a scheduled appointment without providing prior notice to the healthcare provider, poses a significant challenge for effective scheduling. No-show contributes to underutilized resources, reduced patient access, and lower revenue. For example, each unused time slot results in a clinic losing \\$200 in revenue, and the US healthcare system is estimated to lose **\\$150 billion** due to no-shows every year.
# 
# ### Common Practice to Tackle No-Shows
# Clinics divide their daily operating hours into smaller equal time periods called **slots**. The scheduling system is built by assigning patients to these slots. To handle no-shows, most hospitals tend to double-book (providing 2 patients with the same appointment slot) by scheduling more than their capacity. They consider all patients to have the same no-show probability (i.e., homogeneous) and overbook by a flat overbooking percentage which often equals to the average no-show rate of the clinic. For example, if the clinic has capacity to serve 10 patients everyday and experiences an average no-show rate of 30%, then the clinic schedules 13 patients to compensate for anticipated no-shows. The 3 additional patients may be double-booked from the beginning of the clinic session or can also be randomly double-booked throughout the clinic session. Nevertheless, such an approach **might not be effective**. This is because prior research has shown that the patient no-show behaviour is not homogenous and depends on an individual patient. 
# 
# ### Lab Objective
# Predicting the likelihood of a patient's show or no-show status can help schedulers to effectively allocate available capacity. For instance, if a patient is very likely to miss an appointment, then it would be more appropriate to double-book that patient to slot that has another patient who is likely to arrive for the appointment. This could achieve better balance of the clinic access, patient waiting time and doctor idle time. To this end, the tasks (key research questions) for this lab are as follows:
# 
# 1. Can machine learning algorithms be used to accurately predict patient's no-show risk using historical data available in the clinic's electronic medical records (EMR)?
# 2. Which features/variables are important in predicting patient no-shows?

# ## Data Description

# This dataset consists of information of about 20,000 medical appointments. The dataset consists of 13 columns:
# 
# **Independent Variables/Features**
# 1. **Age:** Age of each patient (in years).
# 
# 2. **Gender:** Gender of the patient (M or F)
# 
# 3. **DOW:** The day of the week on which the appointment is scheduled (Monday, Tuesday,..., Sunday).
# 
# 4. **LeadTime:** Number of days between the appointment request date and actual appointment date.
# 
# 5. **SMS_received:** It indicates whether the patient received SMS or not (0 = No, 1 = Yes).
# 
# 6. **Scholarship:** Indicates whether the patient is enrolled in government welfare program or not (0 = No, 1 = Yes).
# 
# 7. **Smoking_Status:** Indicates whether the patient smokes or not (0 = No, 1 = Yes).
# 
# 8. **Hypertension:** It indicates whether the patient suffers from Hipertension or not (0 = No, 1 = Yes).
# 
# 9. **Diabetes:** It indicates whether the patient suffers from Diabetes or not (0 = No, 1 = Yes).
# 
# 10. **Alcoholism:** It indicates whether the patient suffers from Alcoholism or not (0 = No, 1 = Yes).
# 
# 11. **Tuberculosis:** Indicates whether the patient suffers from Tuberculosis or not (0 = No, 1 = Yes).
# 
# 12. **Disability:** Total number of disabilities experienced by the individual (Integer). 
# 
# 
# **Outcome Variable**
# 
# **Status:** Indicates whether the patient showed up for the appointment or not (Show-up or No-Show).

# ## Machine Learning Model Development

# ### **Step 0:** Load the required libraries

# In[1]:


#Import pandas for reading the dataset
import pandas as pd

#Import sklearn for machine learning algorithms
import sklearn

# Import train_test_split function
from sklearn.model_selection import train_test_split

# Import Decision Tree Classifier
from sklearn.tree import DecisionTreeClassifier

# Import RF Classifier
from sklearn.ensemble import RandomForestClassifier

#Import scikit-learn metrics module for accuracy calculation
from sklearn import metrics

#Import classification report module for calculating precsion, f1, etc.
from sklearn.metrics import classification_report

#Import confusion_matrix module to generate the confusion matrix
from sklearn.metrics import confusion_matrix


# ### **Step 1:** Load Data

# In[3]:


NoShowData = pd.read_excel(r"data/No-show_Data.xlsx")

NoShowData.sample(5)


# ### **Step 2:** Data Pre-processing

# **Check for Missing Values in Each Column**

# In[4]:


NoShowData.isnull().sum()


# **Note:** If the value against a column name is 0 then that column does not contain any missing value. Otherwise, the number of missing values for that column is displayed. In this case, we do not have any missing values.

# **Check data types and convert it accordingly**
# 
# Each variable can be categorized as continuous or discrete depending on the values it can contain. For instance, the variable "Gender" is a categorical since it can either be "M" or "F". On the other hand, the variable "Age" is a continuous variable since it is not restricted to predefined categories. 

# In[5]:


#Check the column types identified by Python
NoShowData.dtypes


# Note that "category" refers to a categorical data type in Python and "int64" refers to continuous variables. Python has  identified the variable "Gender" and "DOW as objects as these columns have text instead of numbers. All the other variables are classified as continuous. 
# 
# In particular, the variables "SMS_received", "Scholarship", "Smoking_Status", "Hypertension", "Diabetes", "Alcoholism", "Tuberculosis" are **incorrectly classified** as continuous. Therefore, we must first fix these variables to categorical.

# In[6]:


#Convert the variable "Gender" to category
NoShowData['Gender'] = NoShowData['Gender'].astype('category')

#Convert the variable "DOW" to category
NoShowData['DOW'] = NoShowData['DOW'].astype('category')

#Convert the variable "SMS_received" to category
NoShowData['SMS_received'] = NoShowData['SMS_received'].astype('category')

#Convert the variable "Scholarship" to category
NoShowData['Scholarship'] = NoShowData['Scholarship'].astype('category')

#Convert the variable "Smoking_Status" to category
NoShowData['Smoking_Status'] = NoShowData['Smoking_Status'].astype('category')

#Convert the variable "Hypertension" to category
NoShowData['Hypertension'] = NoShowData['Hypertension'].astype('category')

#Convert the variable "Diabetes" to category
NoShowData['Diabetes'] = NoShowData['Diabetes'].astype('category')

#Convert the variable "Alcoholism" to category
NoShowData['Alcoholism'] = NoShowData['Alcoholism'].astype('category')

#Convert the variable "Tuberculosis" to category
NoShowData['Tuberculosis'] = NoShowData['Tuberculosis'].astype('category')


#Check the column types after manual conversion
NoShowData.dtypes


# **One-Hot Encoding Categorical Variables**

# The categorical variables must be coded before being fed into the machine learning model for training. One hot encoding creates new (binary) columns, indicating the presence of each possible value from the original data. Let's work through an example.

# ![Encoding.PNG](attachment:Encoding.PNG)

# One hot encoding is the most widespread approach, and it works very well unless your categorical variable takes on a large number of values (i.e. you generally won't it for variables taking more than 15 different values.)
# 
# Every time we one-hot encode variables, we face multicollinearity issue, a statistical concept where several independent variables in a model are correlated. If the variables are correlated, it will become difficult for the model to tell how strongly a particular variable affects the outcome. This is especially problematic for regression models. One way to overcome this issue is by dropping one of the generated columns. For example, we can drop either Gender_F or Gender_M without potentially losing any information. In this case, we are setting the paramter "drop_first = True", indicating that the first encoded column must be dropped.

# In[7]:


#Dummy code the columns
NoShowData = pd.get_dummies(NoShowData,
columns=["Gender","DOW","SMS_received", "Scholarship", "Smoking_Status", "Hypertension", "Diabetes", "Alcoholism", "Tuberculosis", "Status"],
prefix=["Gender","DOW","SMS_received", "Scholarship", "Smoking_Status", "Hypertension", "Diabetes", "Alcoholism", "Tuberculosis", "Status"], 
                             drop_first = True)


# In[8]:


#Preview coded data
NoShowData.sample(5)


# In[9]:


#Function to preprocess

def Preprocess(NoShowData):
    #Convert the variable "Gender" to category
    NoShowData['Gender'] = NoShowData['Gender'].astype('category')

    #Convert the variable "DOW" to category
    NoShowData['DOW'] = NoShowData['DOW'].astype('category')

    #Convert the variable "SMS_received" to category
    NoShowData['SMS_received'] = NoShowData['SMS_received'].astype('category')

    #Convert the variable "Scholarship" to category
    NoShowData['Scholarship'] = NoShowData['Scholarship'].astype('category')

    #Convert the variable "Smoking_Status" to category
    NoShowData['Smoking_Status'] = NoShowData['Smoking_Status'].astype('category')

    #Convert the variable "Hypertension" to category
    NoShowData['Hypertension'] = NoShowData['Hypertension'].astype('category')

    #Convert the variable "Diabetes" to category
    NoShowData['Diabetes'] = NoShowData['Diabetes'].astype('category')

    #Convert the variable "Alcoholism" to category
    NoShowData['Alcoholism'] = NoShowData['Alcoholism'].astype('category')

    #Convert the variable "Tuberculosis" to category
    NoShowData['Tuberculosis'] = NoShowData['Tuberculosis'].astype('category')
    
    #Dummy code the columns
    NoShowData = pd.get_dummies(NoShowData,
    columns=["Gender","DOW","SMS_received", "Scholarship", "Smoking_Status", "Hypertension", "Diabetes", "Alcoholism", "Tuberculosis"],
    prefix=["Gender","DOW","SMS_received", "Scholarship", "Smoking_Status", "Hypertension", "Diabetes", "Alcoholism", "Tuberculosis"], 
                                 drop_first = True)

    return(NoShowData)


# ### Step 3: Feature Selection

# In[10]:


#selects every column except the last one as independent variable
NoShow_Predictors = pd.DataFrame(NoShowData.iloc[:,:-1])

#Selects the last column as outcome
NoShow_Outcome = pd.DataFrame(NoShowData.iloc[:,-1])


# ### Step 4: Split Data into Training and Testing

# In[11]:


#Split dataset into 75% training set and 25% test set
X_Train_NoShow, X_Test_NoShow, y_Train_NoShow, y_Test_NoShow = train_test_split(NoShow_Predictors, NoShow_Outcome, test_size=0.25, 
                                                                     random_state=8810)


# ### Step 5: Building Predictive Model

# #### Decision Tree Classififer Training

# In[12]:


#Train Decision Tree Classifier object
DT_class_Noshow = DecisionTreeClassifier()

DT_class_Noshow = DT_class_Noshow.fit(X_Train_NoShow, y_Train_NoShow)


# #### Predict Examples in Test Dataset using Trained Decision Tree Classifier 

# In[13]:


y_pred_DT_class = DT_class_Noshow.predict(X_Test_NoShow)


# #### Evaluate Decision Tree Performance

# In[14]:


fpr, tpr, thresholds = metrics.roc_curve(y_Test_NoShow, y_pred_DT_class, pos_label=1)
auc_dt = metrics.auc(fpr, tpr)
auc_dt


# #### Random Forest Classififer Training

# In[15]:


#Train RF Classifier object
RF_class_Noshow = RandomForestClassifier()

RF_class_Noshow = RF_class_Noshow.fit(X_Train_NoShow, y_Train_NoShow.values.ravel())


# #### Predict Examples in Test Dataset using Trained Random Forest Classifier

# In[16]:


y_pred_RF_class = RF_class_Noshow.predict(X_Test_NoShow)


# In[17]:


X_Test_NoShow


# #### Evaluate Random Forest Performance

# In[18]:


fpr, tpr, thresholds = metrics.roc_curve(y_Test_NoShow, y_pred_RF_class, pos_label=1)
auc_rf = metrics.auc(fpr, tpr)
auc_rf


# ### Step 6: Select Best Classifier

# In[19]:


if auc_rf > auc_dt:
    best_classifier = RF_class_Noshow
else:
    best_classifier = DT_class_Noshow


# In[20]:


best_classifier.predict(X_Test_NoShow)


# ### Step 7: Predict New Examples

# In[22]:


#Import new examples
NoShowData_NewExamples = pd.read_excel(r"data/No-show_Data_Testing.xlsx")


NoShowData_NewExamples = Preprocess(NoShowData_NewExamples)


NoShowData_NewExamples.sample(5)


# In[23]:


#Predict Outcome
best_classifier.predict(NoShowData_NewExamples)


# In[ ]:





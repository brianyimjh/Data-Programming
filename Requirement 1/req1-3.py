#!/usr/bin/env python
# coding: utf-8

# # Q3a

# In[1]:


import pandas as pd

# Activity log
activity_log_df = pd.read_csv('accessPerDay.csv')
activity_log_df


# In[2]:


# Submission log
submission_log_df = pd.read_csv('submissionLog.csv')
submission_log_df


# In[3]:


students_activity_df = activity_log_df.groupby(['Name', 'Group'])['Duration'].sum().reset_index()
students_activity_df


# In[4]:


submission_log_df.info()


# In[5]:


students_activity_df.info()


# In[6]:


merged_df = students_activity_df.merge(submission_log_df, how='outer', on=['Name', 'Group'])
merged_df


# In[7]:


merged_df.info()


# In[8]:


sorted_merged_df = merged_df.sort_values('Duration', ascending=False).reset_index(drop=True)
sorted_merged_df


# In[9]:


top50_percent_df = sorted_merged_df.head(len(sorted_merged_df)//2)

top50_percent_df


# In[10]:


# If NaN, means no submission
submitted_count = top50_percent_df['Sub Count'].notna().sum()
# Total number of students in the top 50%
total_students = top50_percent_df['Name'].count()

top50_percent_submission_rate = round((submitted_count/total_students) * 100, 2)
print(top50_percent_submission_rate)


# In[11]:


# +1 since 89/2 is uneven hence, round up to include the odd numbered student
bottom50_percent_df = sorted_merged_df.tail(len(sorted_merged_df)//2 + 1) 

bottom50_percent_df


# In[12]:


# If NaN, means no submission
submitted_count = bottom50_percent_df['Sub Count'].notna().sum()
# Total number of students in the bottom 50%
total_students = bottom50_percent_df['Name'].count()

bottom50_percent_submission_rate = round((submitted_count/total_students) * 100, 2)
print(bottom50_percent_submission_rate)


# In[13]:


print(f"Submission rate of top 50% active students: {top50_percent_submission_rate}%")
print(f"Submission rate of bottom 50% active students: {bottom50_percent_submission_rate}%")


# # Q3b
# 
# The information shows a higher submission rate for the top 50% of students who are more active and spend a longer duration in the learning platform than the bottom 50% of students. Hence, the company can achieve a higher submission rate by incorporating activities in the learning platform to better help students be more active and spend a longer time in the platform throughout their learning process.

# # Q3c

# In[14]:


submission_log_df


# In[15]:


submission_log_df.info()

# Sub Time is not in datetime format


# In[16]:


student_submission_date_df = submission_log_df[['Name', 'Group', 'Sub Time']]
student_submission_date_df


# In[17]:


student_submission_date_df['Date'] = student_submission_date_df['Sub Time'].str[:11]
student_submission_date_df


# In[18]:


student_submission_date_df = student_submission_date_df.drop('Sub Time', axis=1)
student_submission_date_df


# In[19]:


from datetime import datetime

student_submission_date_df['Date'] = pd.to_datetime(student_submission_date_df['Date'], format='%b-%d-%Y')
student_submission_date_df


# In[20]:


student_submission_date_df.info()

# Date is now in datetime format


# In[21]:


activity_log_df


# In[22]:


activity_log_df.info()

# Date is not in datetime format


# In[23]:


format_date_activity_df = activity_log_df.copy()
format_date_activity_df['Date'] = pd.to_datetime(activity_log_df['Date'], format='%Y-%m-%d')
format_date_activity_df


# In[24]:


format_date_activity_df.info()

# Date is now in datetime format


# In[25]:


# Only merge students with the lastest submission dates
merged_df = format_date_activity_df.merge(student_submission_date_df, how='inner', on=['Name', 'Group', 'Date'])
merged_df


# # Q3d

# In[26]:


activity_log_df


# In[27]:


access_more_than_10_students_df = activity_log_df.copy()

# Count number of times students access the platform
access_more_than_10_students_df = access_more_than_10_students_df.groupby(['Group', 'Name'])['Duration']                                    .count().reset_index()
access_more_than_10_students_df


# In[28]:


# Rename column
access_more_than_10_students_df = access_more_than_10_students_df.rename(columns={'Duration': 'Count'})
access_more_than_10_students_df


# In[29]:


# Filter students who accessed the platform at least 10 times
access_more_than_10_students_df = access_more_than_10_students_df.query('Count >= 10')
access_more_than_10_students_df


# In[30]:


# Count number of students for each group
access_more_than_10_students_df = access_more_than_10_students_df.groupby(['Group']).count()['Count']
access_more_than_10_students_df


# # Q3e

# In[31]:


activity_log_df


# In[32]:


submission_log_df


# In[33]:


# Total submissions for each group
total_submit_df = submission_log_df.groupby(['Group'])['Name'].count().reset_index()
total_submit_df


# In[34]:


# Rename column
total_submit_df = total_submit_df.rename(columns={'Name': 'Total Sub Count'})
total_submit_df


# In[35]:


# Eliminate all repeated students records
total_students_df = activity_log_df.groupby(['Group', 'Name'])['Duration'].sum().reset_index()
total_students_df


# In[36]:


# Total students for each group
total_students_df = total_students_df.groupby(['Group'])['Name'].count().reset_index()
total_students_df


# In[37]:


# Rename column
total_students_df = total_students_df.rename(columns={'Name': 'Total Students Count'})
total_students_df


# In[38]:


merged_df = total_submit_df.merge(total_students_df, how='outer', on=['Group'])
merged_df


# In[39]:


merged_df.fillna(0, inplace=True)
merged_df


# In[40]:


merged_df['Sub Rate'] = (merged_df['Total Sub Count'] / merged_df['Total Students Count']) * 100
merged_df


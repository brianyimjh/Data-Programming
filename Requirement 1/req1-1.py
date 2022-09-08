#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

# Activity log
activity_log_df = pd.read_csv('accessPerDay.csv')
activity_log_df


# In[2]:


activity_log_df.info()

# Data has no NaN values


# # Q1a

# In[3]:


# Group students and sum their activity time
total_activity_time_df = activity_log_df.groupby(['Name'])['Duration'].sum().reset_index()
total_activity_time_df


# In[4]:


total_activity_time_df.info()


# In[5]:


total_activity_time_df.to_csv('total_activity_time.csv')


# # Q1b(i)

# In[6]:


activity_log_df


# In[7]:


# Mean of groups in descending order
group_df = activity_log_df.groupby(['Group'])['Duration'].mean().sort_values(ascending=False).reset_index()
group_df


# # Q1b(ii)

# In[8]:


activity_log_df


# In[9]:


students_df = activity_log_df.groupby(['Name'])['Duration'].sum()                                .sort_values(ascending=False).reset_index()
students_df


# In[10]:


top3_most_active_df = students_df.head(3)
top3_most_active_df


# In[11]:


top3_least_active_df = students_df.tail(3)
top3_least_active_df


# # Q1c

# In[12]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import seaborn as sns

figure, ax = plt.subplots()

ax = sns.barplot(x=top3_most_active_df['Name'], y=top3_most_active_df['Duration'])

ax.set_title("Top 3 Most Active Students")
figure.tight_layout()


# # Q1d

# In[13]:


# Get names of top 3 most active students
merged_top3_most_df = top3_most_active_df.copy()
merged_top3_most_df.drop(columns=['Duration'], inplace=True)
merged_top3_most_df


# In[14]:


# Merge for date and duration
merged_top3_most_df = merged_top3_most_df.merge(activity_log_df, how='left', on=['Name'])
merged_top3_most_df


# In[15]:


merged_top3_most_df.drop(columns=['Group'], inplace=True)
merged_top3_most_df


# In[16]:


# Get names of top 3 least active students
merged_top3_least_df = top3_least_active_df.copy()
merged_top3_least_df.drop(columns=['Duration'], inplace=True)
merged_top3_least_df


# In[17]:


# Merge for date and duration
merged_top3_least_df = merged_top3_least_df.merge(activity_log_df, how='left', on=['Name'])
merged_top3_least_df


# In[18]:


merged_top3_least_df.drop(columns=['Group'], inplace=True)
merged_top3_least_df


# In[19]:


# Merge both df to plot
merged_df = merged_top3_most_df.append(merged_top3_least_df).reset_index(drop=True)
merged_df


# In[20]:


# Sort Date
merged_df = merged_df.sort_values(['Date']).reset_index(drop=True)
merged_df


# In[21]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(rc={'figure.figsize':(11.7,8.27)})

figure, ax = plt.subplots()

ax = sns.lineplot(x='Date', y='Duration', data=merged_df, hue='Name')
ax.set_xticklabels(merged_df['Date'], rotation=50)

ax.set_title('Activity Time Of Top 3 Most and Top 3 Least Students')
figure.tight_layout()


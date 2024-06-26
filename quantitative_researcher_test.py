# -*- coding: utf-8 -*-
"""Quantitative Researcher test.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1sLep0fmPOz2_ypejTf045kfH4VyUufkU
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from functools import reduce
from datetime import datetime

"""Loading and checking the files

"""

df_events=pd.read_csv('events.csv')
df_events.head()

df_applicants=pd.read_csv('applicants.csv')
df_applicants.head()

df_sessions=pd.read_csv('sessions.csv')
df_sessions.head()

"""Consolidation of the files into one complete file according to session_id



"""

dfs = [df_events, df_applicants, df_sessions]
merged_df = reduce(lambda left, right: pd.merge(left, right, on='session_id', how='outer'), dfs)

merged_df.to_excel('merged_output.xlsx', index=False)

"""An examination of what we received




"""

df_all = pd.read_excel('merged_output.xlsx')
df_all.head()

"""Deleting duplicate values"""

df_all.drop_duplicates(inplace=True)
df_all.head()

"""Setting a "clean" date without times"""

df_all['event_datetime'] = pd.to_datetime(df_all['event_datetime'], errors='coerce')
df_all['event_date'] = df_all['event_datetime'].dt.date

"""Creating a separation between the change date on March 15, 2259"""

filter_date = pd.to_datetime('2259-03-15').date()
before_date = df_all[df_all['event_date'] < filter_date]
after_date = df_all[df_all['event_date'] >= filter_date]

"""Check data before the date"""

before_date.head()

"""Checking data after the date"""

after_date.head()

"""Converting the variables from text form to number:

start gets the value 1

end gets the value 2
"""

before_date.loc[before_date['event_type'] == 'end_of_underwriting', 'event_type'] = 1
before_date.loc[before_date['event_type'] == 'Ally submitted test results', 'event_type'] = 2

after_date.loc[after_date['event_type'] == 'end_of_underwriting', 'event_type'] = 1
after_date.loc[after_date['event_type'] == 'Ally submitted test results', 'event_type'] = 2

"""Checking the data after the conversion"""

before_date_filtered = before_date[before_date['event_type'].isin([1, 2])]
after_date_filtered = after_date[after_date['event_type'].isin([1, 2])]

print(before_date_filtered)

"""Comparing times: start vs finish"""

before_date_filtered['event_datetime'] = pd.to_datetime(before_date_filtered['event_datetime'])

results = pd.DataFrame(columns=['session_id', 'start_time', 'end_time', 'duration'])

session_ids = before_date_filtered['session_id'].unique()

for session_id in session_ids:
    session_data = before_date_filtered[before_date_filtered['session_id'] == session_id]

    start_events = session_data[session_data['event_type'] == 1]
    end_events = session_data[session_data['event_type'] == 2]

    if not start_events.empty and not end_events.empty:
        start_time = start_events['event_datetime'].iloc[0]
        end_time = end_events['event_datetime'].iloc[0]

        duration = end_time - start_time

        session_result = pd.DataFrame({
            'session_id': [session_id],
            'start_time': [start_time],
            'end_time': [end_time],
            'duration': [duration]
        })

        results = pd.concat([results, session_result], ignore_index=True)

print(results)

"""Descriptive statistics"""

results.describe()

"""Creating a graph"""

mean_duration = results['duration'].mean()

print("Average Duration:", mean_duration)

plt.figure(figsize=(10, 6))
sns.histplot(results['duration'].dt.total_seconds() / 60, kde=True, bins=20)
plt.title('Distribution of Activity Durations')
plt.xlabel('Duration (minutes)')
plt.ylabel('Frequency')
plt.show()

"""We will perform the same analyzes for the data set after the change"""

after_date_filtered['event_datetime'] = pd.to_datetime(after_date_filtered['event_datetime'])

results_after = pd.DataFrame(columns=['session_id', 'start_time', 'end_time', 'duration'])

session_ids = after_date_filtered['session_id'].unique()

for session_id in session_ids:
    session_data = after_date_filtered[after_date_filtered['session_id'] == session_id]

    start_events = session_data[session_data['event_type'] == 1]
    end_events = session_data[session_data['event_type'] == 2]

    if not start_events.empty and not end_events.empty:
        start_time = start_events['event_datetime'].iloc[0]
        end_time = end_events['event_datetime'].iloc[0]

        duration = end_time - start_time

        session_result = pd.DataFrame({
            'session_id': [session_id],
            'start_time': [start_time],
            'end_time': [end_time],
            'duration': [duration]
        })

        results_after = pd.concat([results_after, session_result], ignore_index=True)

print(results_after)

results_after.describe()

"""Examining the maximum and abnormal result"""

max_result = results_after[results_after['duration'] == results_after['duration'].max()]

print("Max Duration Result:")
print(max_result)

print("Outlier Result:")
print(results_after.iloc[56].head())

"""Deleting the abnormal result"""

max_index = results_after['duration'].idxmax()

results_after.drop(index=max_index, inplace=True)

"""Re-examination of the data"""

results_after.describe()

mean_duration_after = results_after['duration'].mean()

print("Average Duration:", mean_duration_after)

plt.figure(figsize=(10, 6))
sns.histplot(results_after['duration'].dt.total_seconds() / 60, kde=True, bins=20)
plt.title('Distribution of Activity Durations')
plt.xlabel('Duration (minutes)')
plt.ylabel('Frequency')
plt.show()

results_after

"""Creating a graph comparing the data before and after the change.
Added an average line to highlight the change
"""

mean_duration_minutes = mean_duration.total_seconds() / 60
mean_duration_after_minutes = mean_duration_after.total_seconds() / 60

plt.figure(figsize=(10, 6))

sns.histplot(results['duration'].dt.total_seconds() / 60, kde=True, bins=20, color='blue', label='Before')
sns.histplot(results_after['duration'].dt.total_seconds() / 60, kde=True, bins=20, color='darkred', label='After')

plt.axvline(x=mean_duration_minutes, color='blue', linestyle='--', label='Mean Before')
plt.axvline(x=mean_duration_after_minutes, color='darkred', linestyle='--', label='Mean After')

plt.title('Distribution of Activity Durations Before and After')
plt.xlabel('Duration (minutes)')
plt.ylabel('Frequency')
plt.legend()
plt.show()
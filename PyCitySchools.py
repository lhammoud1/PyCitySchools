#!/usr/bin/env python
# coding: utf-8

# In[26]:


# Dependencies and Setup
import pandas as pd

# File to Load (Remember to Change These)
school_data_to_load = "schools_complete.csv"
student_data_to_load = "students_complete.csv"

# Read School and Student Data File and store into Pandas DataFrames
school_data = pd.read_csv(school_data_to_load)
student_data = pd.read_csv(student_data_to_load)

# Combine the data into a single dataset.  
school_data_complete = pd.merge(student_data, school_data, how="left", on=["school_name", "school_name"])
school_data_complete.head()


# In[27]:


# Calculate the total number of schools

unique_school_name=school_data_complete['school_name'].unique()


total_school_number=len(unique_school_name)

total_school_number


# In[28]:


# Calculate the total number of students
total_students_number=school_data_complete['student_name'].count()
total_students_number


# In[30]:


# Calculate the total budget
total_budget = school_data['Budget'].sum()
total_budget


# In[31]:


# Calculate the average math score.
average_math_score = school_data_complete["math_score"].mean()
average_math_score


# In[32]:


# Calculate the average reading score
average_reading_score = school_data_complete["reading_score"].mean()
average_reading_score


# In[33]:


#Calculate the percentage of students with a passing math score (70 or greater)

students_passing_math = school_data_complete.loc[school_data_complete["math_score"] >= 70]
number_students_passing_math = students_passing_math["Student ID"].count()

percent_passing_math = (number_students_passing_math / total_students_number) * 100

percent_passing_math


# In[34]:


# Calculate the percentage of students with a passing reading score (70 or greater)
students_passing_reading = school_data_complete.loc[school_data_complete["reading_score"] >= 70]
number_students_passing_reading = students_passing_reading["Student ID"].count()

percent_passing_reading = (number_students_passing_reading / total_students_number) * 100
percent_passing_reading


# In[35]:


# Calculate the percentage of students who passed math and reading (% Overall Passing)

Overall_passing = school_data_complete[(school_data_complete['math_score'] >= 70) & (school_data_complete['reading_score'] >= 70)]['Student ID'].count()/total_students_number*100
Overall_passing


# In[38]:


# Create a dataframe to hold the above results
district_summary = pd.DataFrame({
    "Total Schools": total_school_number,
    "Total Students": f"{total_students_number:,}",
    "Total Budget": f"${total_budget:,.2f}",
    "Average Math Score": f"{average_math_score:.6f}",
    "Average Reading Score": f"{average_reading_score:.5f}",
    "% Passing Math": f"{percent_passing_math:.6f}",
    "% Passing Reading": f"{percent_passing_reading:.6f}",
    "% Overall Passing": f"{Overall_passing: .6f}"
}, index=[0])

district_summary


# In[39]:


# Group by school name
school_name = school_data_complete.set_index('school_name').groupby(['school_name'])


# In[40]:


# school types by school name
school_type = school_data.set_index('school_name')['type']


# In[41]:


#  Calculate total students
total_student = school_name['Student ID'].count()


# In[43]:


# Total school budget
total_school_budget = school_data.set_index('school_name')['Budget']


# In[44]:


# per student budget
budget_per_student = (school_data.set_index('school_name')['Budget']/school_data.set_index('school_name')['size'])


# In[45]:


# Average Math Score

average_math_score = school_name['math_score'].mean()


# In[46]:


# Average Reading Score
average_reading_score = school_name['reading_score'].mean()


# In[47]:


# % Passing Math

pass_math_percent = school_data_complete[school_data_complete['math_score'] >= 70].groupby('school_name')['Student ID'].count()/total_student*100


# In[48]:


# % Passing Reading

pass_read_percent = school_data_complete[school_data_complete['reading_score'] >= 70].groupby('school_name')['Student ID'].count()/total_student*100


# In[49]:


# % Overall Passing (The percentage of students that passed math and reading.

overall_pass = school_data_complete[(school_data_complete['reading_score'] >= 70) & (school_data_complete['math_score'] >= 70)].groupby('school_name')['Student ID'].count()/total_student*100


# In[50]:


school_summary = pd.DataFrame({
    "School Type": school_type,
    "Total Students": total_student,
    "Per Student Budget": budget_per_student,
    "Total School Budget": total_school_budget,
    "Average Math Score": average_math_score,
    "Average Reading Score": average_reading_score,
    '% Passing Math': pass_math_percent,
    '% Passing Reading': pass_read_percent,
    "% Overall Passing": overall_pass
})


#munging
school_summary = school_summary[['School Type', 
                          'Total Students', 
                          'Total School Budget', 
                          'Per Student Budget', 
                          'Average Math Score', 
                          'Average Reading Score',
                          '% Passing Math',
                          '% Passing Reading',
                          '% Overall Passing']]


#formatting
school_summary.style.format({'Total Students': '{:}',
                          "Total School Budget": "${:,.2f}",
                          "Per Student Budget": "${:.2f}",
                          'Average Math Score': "{:6f}", 
                          'Average Reading Score': "{:6f}", 
                          "% Passing Math": "{:6f}", 
                          "% Passing Reading": "{:6f}"})


# In[51]:


# Sort and display the top five schools by passing rate 
top_perform = school_summary.sort_values("% Overall Passing", ascending = False)
top_perform.head().style.format({'Total Students': '{:}',
                           "Total School Budget": "${:,.2f}", 
                           "Per Student Budget": "${:.2f}", 
                           "% Passing Math": "{:6f}", 
                           "% Passing Reading": "{:6f}", 
                           "% Overall Passing": "{:6f}"})


# In[52]:


# Sort and display the bottom five schools by passing rate 
bottom_perform = top_perform.tail()
bottom_perform = bottom_perform.sort_values('% Overall Passing')
bottom_perform.style.format({'Total Students': '{: }', 
                       "Total School Budget": "${:,.2f}", 
                       "Per Student Budget": "${:.2f}", 
                       "% Passing Math": "{:6f}", 
                       "% Passing Reading": "{:6f}", 
                       "% Overall Passing": "{:6f}"})


# In[53]:


#creates grade level average math scores for each school 
ninth_math = student_data.loc[student_data['grade'] == '9th'].groupby('school_name')["math_score"].mean()
tenth_math = student_data.loc[student_data['grade'] == '10th'].groupby('school_name')["math_score"].mean()
eleventh_math = student_data.loc[student_data['grade'] == '11th'].groupby('school_name')["math_score"].mean()
twelfth_math = student_data.loc[student_data['grade'] == '12th'].groupby('school_name')["math_score"].mean()

math_scores = pd.DataFrame({
        "9th": ninth_math,
        "10th": tenth_math,
        "11th": eleventh_math,
        "12th": twelfth_math
})
math_scores = math_scores[['9th', '10th', '11th', '12th']]
math_scores.index.name = "School Name"

#show and format
math_scores.style.format({'9th': '{:.6f}', 
                          "10th": '{:.6f}', 
                          "11th": "{:.6f}", 
                          "12th": "{:.6f}"})


# In[54]:


#creates grade level average reading scores for each school
ninth_reading = student_data.loc[student_data['grade'] == '9th'].groupby('school_name')["reading_score"].mean()
tenth_reading = student_data.loc[student_data['grade'] == '10th'].groupby('school_name')["reading_score"].mean()
eleventh_reading = student_data.loc[student_data['grade'] == '11th'].groupby('school_name')["reading_score"].mean()
twelfth_reading = student_data.loc[student_data['grade'] == '12th'].groupby('school_name')["reading_score"].mean()

#merges the reading score averages by school and grade together
reading_scores = pd.DataFrame({
        "9th": ninth_reading,
        "10th": tenth_reading,
        "11th": eleventh_reading,
        "12th": twelfth_reading
})
reading_scores = reading_scores[['9th', '10th', '11th', '12th']]
reading_scores.index.name = "School Name"

#format
reading_scores.style.format({'9th': '{:.6f}', 
                             "10th": '{:.6f}', 
                             "11th": "{:.6f}", 
                             "12th": "{:.6f}"})


# In[56]:


# create spending bins


bins = [0, 584, 629, 644, 675]
group_name = ["<$584", "$585-629", "$630-644", "$645-675"]

school_data_complete['spending_bins'] = pd.cut(school_data_complete['Budget']/school_data_complete['size'], bins, labels = group_name)

#group by spending
by_spending = school_data_complete.groupby('spending_bins')


avg_math = by_spending['math_score'].mean()

avg_read = by_spending['reading_score'].mean()
pass_math = school_data_complete[school_data_complete['math_score'] >= 70].groupby('spending_bins')['Student ID'].count()/by_spending['Student ID'].count()*100
pass_read = school_data_complete[school_data_complete['reading_score'] >= 70].groupby('spending_bins')['Student ID'].count()/by_spending['Student ID'].count()*100
overall = school_data_complete[(school_data_complete['reading_score'] >= 70) & (school_data_complete['math_score'] >= 70)].groupby('spending_bins')['Student ID'].count()/by_spending['Student ID'].count()*100
    
# df build            
scores_by_spend = pd.DataFrame({
    "Average Math Score": avg_math,
    "Average Reading Score": avg_read,
    "% Passing Math": pass_math,
    "% Passing Reading": pass_read,
    "% Overall Passing": overall
            
})
            
#reorder columns
scores_by_spend = scores_by_spend[[
    "Average Math Score",
    "Average Reading Score",
    "% Passing Math",
    "% Passing Reading",
    "% Overall Passing"
]]

scores_by_spend.index.name = "Per Student Budget"


#formating
scores_by_spend.style.format({'Average Math Score': '{:.2f}', 
                              'Average Reading Score': '{:.2f}', 
                              '% Passing Math': '{:.2f}', 
                              '% Passing Reading':'{:.2f}', 
                              '% Overall Passing': '{:.2f}'})


# In[57]:


# create size bins
bins = [0, 1000, 1999,5000]
group_name = ["Small (<1000)", "Medium (1000-2000)" , "Large (2000-5000)"]
school_data_complete['size_bins'] = pd.cut(school_data_complete['size'], bins, labels = group_name)

#group by spending
by_size = school_data_complete.groupby('size_bins')

#calculations 
average_math_score = by_size['math_score'].mean()
average_reading_score = by_size['math_score'].mean()
pass_math_percent = school_data_complete[school_data_complete['math_score'] >= 70].groupby('size_bins')['Student ID'].count()/by_size['Student ID'].count()*100
pass_read_percent = school_data_complete[school_data_complete['reading_score'] >= 70].groupby('size_bins')['Student ID'].count()/by_size['Student ID'].count()*100
overall = school_data_complete[(school_data_complete['reading_score'] >= 70) & (school_data_complete['math_score'] >= 70)].groupby('size_bins')['Student ID'].count()/by_size['Student ID'].count()*100

            
# df build            
scores_by_size = pd.DataFrame({
    "Average Math Score": average_math_score,
    "Average Reading Score": average_reading_score,
    '% Passing Math': pass_math_percent,
    '% Passing Reading': pass_read_percent,
    '% Overall Passing': overall
            
})
            
#reorder columns
scores_by_size = scores_by_size[[
    "Average Math Score",
    "Average Reading Score",
    '% Passing Math',
    '% Passing Reading',
    '% Overall Passing'
]]

scores_by_size.index.name = "Total Students"
scores_by_size = scores_by_size.reindex(group_name)

#formating
scores_by_size.style.format({'Average Math Score': '{:.6f}', 
                              'Average Reading Score': '{:.6f}', 
                              '% Passing Math': '{:.6f}', 
                              '% Passing Reading':'{:.6f}', 
                              '% Overall Passing': '{:.6f}'})


# In[58]:


# group by type of school
schoo_type = school_data_complete.groupby("type")

#calculations 
average_math_score = schoo_type['math_score'].mean()
average_reading_score = schoo_type['math_score'].mean()
pass_math_percent = school_data_complete[school_data_complete['math_score'] >= 70].groupby('type')['Student ID'].count()/schoo_type['Student ID'].count()*100
pass_read_percent = school_data_complete[school_data_complete['reading_score'] >= 70].groupby('type')['Student ID'].count()/schoo_type['Student ID'].count()*100
overall = school_data_complete[(school_data_complete['reading_score'] >= 70) & (school_data_complete['math_score'] >= 70)].groupby('type')['Student ID'].count()/schoo_type['Student ID'].count()*100

# df build            
scores_schoo_type = pd.DataFrame({
    "Average Math Score": average_math_score,
    "Average Reading Score": average_reading_score,
    '% Passing Math': pass_math_percent,
    '% Passing Reading': pass_read_percent,
    "% Overall Passing": overall})
    
#reorder columns
scores_schoo_type = scores_schoo_type[[
    "Average Math Score",
    "Average Reading Score",
    '% Passing Math',
    '% Passing Reading',
    "% Overall Passing"
]]
scores_schoo_type.index.name = "Type of School"


#formating
scores_schoo_type.style.format({'Average Math Score': '{:.6f}', 
                              'Average Reading Score': '{:.6f}', 
                              '% Passing Math': '{:.6f}', 
                              '% Passing Reading':'{:.6f}', 
                              '% Overall Passing': '{:.6f}'})


# In[ ]:





# %%
import pandas as pd
import matplotlib.pyplot as plt

# Read the data: number of births each year
# The csv format is: <Year>, <Born>. For example: 2019, 100
def read_born_csv():
    df = pd.read_csv('./born.csv')
    df.columns = df.columns.str.strip()
    return df


# Extend the birth data to a given year
# For the future years that has no data, then set it to 95% of the previous year
# The drop will stop when the birth number reaches 5 million.
# For exmaple
# - if the latest data is 2022, 956
# 2023, 908 (956 * 0.95)
# 2024, 862 (908 * 0.95)
# 2025, 819 (862 * 0.95)
def extend_born_data(df, till_year):
    latest_year = df['Year'].max()
    latest_born = df.loc[df['Year'] == latest_year, 'Born'].values[0]
    for year in range(latest_year + 1, till_year + 1):
        latest_born = latest_born * 0.95
        if latest_born < 500:
            latest_born = 500
        # use concat to append a row to a dataframe
        df = pd.concat([df, pd.DataFrame([[year, latest_born]], columns=df.columns)])
        # df = df.append({'Year': year, 'Born': latest_born}, ignore_index=True)
    return df


# Calculate the average age of the population for a given year
# Given the number of people born each year, the current year, and the death age
# Do not modify the dataframe
def average_age(df, current_year, death_age):
    df['Age'] = current_year - df['Year']
    total_age = df['Born'] * df['Age'] * (df['Age'] < death_age) * (df['Age'] >= 0)
    total = df['Born'] * (df['Age'] < death_age) * (df['Age'] >= 0)
    return total_age.sum() / total.sum()


# Make a new dataframe to store the average age for each year
# The csv format is: <Year>, <AverageAge>
# For example: 2019, 20.5
def create_average_age_df(df, till_year, death_age):
    age_df = pd.DataFrame(columns=['Year', 'AverageAge'])
    for year in range(2023, till_year):
        ag = average_age(df, year, death_age)
        age_df = pd.concat([age_df, pd.DataFrame([[year, ag]], columns=age_df.columns)])
    return age_df


# Calculate the number of people between age a and b, not including b
# Given the number of people born each year, the current year, and the death age
# Do not modify the dataframe
def num_between_age_a_and_b(df, a, b, current_year, death_age):
    df['Age'] = current_year - df['Year']
    x = df['Born'] * (df['Age'] >= a) * (df['Age'] < b) * (df['Age'] < death_age)
    return x.sum()


# Make a new dataframe to store the number of total, worker, children, and old people for each year
# The csv format is: <Year>, <Total>, <Worker>, <Children>, <Old>
# For example: 2019, 100, 50, 20, 30
def create_group_df(df, till_year, worker_age, retire_age, death_age):
    group_df = pd.DataFrame(columns=['Year', 'Total', 'Worker', 'Children', 'Old'])
    for year in range(2023, till_year):
        total = num_between_age_a_and_b(df, 0, death_age - 1, year, death_age)
        old = num_between_age_a_and_b(df, retire_age, death_age - 1, year, death_age)
        worker = num_between_age_a_and_b(df, worker_age, retire_age, year, death_age)
        children = num_between_age_a_and_b(df, 0, worker_age, year, death_age)
        group_df = pd.concat([group_df, pd.DataFrame([[year, total, worker, children, old]], columns=group_df.columns)])
    return group_df


# constants
worker_age = 20
retire_age = 50
death_age = 79
till_year = 2100

# Set the font to Chinese
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']

# Prepare the data
df = read_born_csv()
df = extend_born_data(df, till_year)

average_age_df = create_average_age_df(df, till_year, death_age)
average_age_df = average_age_df[average_age_df['Year'] % 5 == 0]
# plot the average age for each year
plt.title(u'中国人口平均年龄')
plt.xlabel('年份')
plt.ylabel('岁')
plt.plot(average_age_df['Year'], average_age_df['AverageAge'], marker='o', label=u'平均年龄', color='red')
plt.legend()
plt.show()


group_df = create_group_df(df, till_year, worker_age, retire_age, death_age)
# plot the ratio of worker, children, and old people for each 5 years
# show line chart for each group
# show the value for the marker
group_df['WorkerRate'] = group_df['Worker'] / group_df['Total']
group_df['ChildrenRate'] = group_df['Children'] / group_df['Total']
group_df['OldRate'] = group_df['Old'] / group_df['Total']
group_df = group_df[group_df['Year'] % 5 == 0]

# Plot the line chart for average age for each year
plt.title(u'中国人口平均年龄')
plt.xlabel('年份')
plt.ylabel('岁')


plt.title(u'中国人口数量预测')
plt.xlabel('年份')
plt.ylabel('万人')
plt.plot(group_df['Year'], group_df['Worker'], marker='o', label=u'劳动人口', color='blue')
plt.plot(group_df['Year'], group_df['Children'], marker='o', label=u'儿童青少年', color='green')
plt.plot(group_df['Year'], group_df['Old'], marker='o', label=u'老年人', color='orange')
plt.legend()
plt.show()


# Plot the line chart for each group
plt.title(u'中国人口结构比例')
plt.xlabel('年份')
plt.ylabel('占比')
plt.ylim(0, 1)
# Blue line for worker
plt.plot(group_df['Year'], group_df['WorkerRate'], marker='o', label='劳动人口', color='blue')
# Green line for children
plt.plot(group_df['Year'], group_df['ChildrenRate'], marker='o', label='少年儿童', color='green')
# Orange line for old
plt.plot(group_df['Year'], group_df['OldRate'], marker='o', label='老年人口', color='orange')

# Add labels to the marker
# for i, row in group_df.iterrows():
#     # show percentage
#     plt.annotate(round(row['Worker'] * 100, 2), (row['Year'], row['Worker']), textcoords="offset points", xytext=(0,10), ha='center')
#     plt.annotate(round(row['Children'] * 100, 2), (row['Year'], row['Children']), textcoords="offset points", xytext=(0,10), ha='center')
#     plt.annotate(round(row['Old'] * 100, 2), (row['Year'], row['Old']), textcoords="offset points", xytext=(0,10), ha='center')

plt.legend()
plt.show()

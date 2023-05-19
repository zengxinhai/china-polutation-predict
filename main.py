# utf-8 encoding

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


# Add a column to the dataframe to indicate the age of the people given the current year
def add_age(df, current_year):
    df['Age'] = current_year - df['Year']
    return df


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
def create_group_df(df, till_year, death_age):
    group_df = pd.DataFrame(columns=['Year', 'Total', 'Worker', 'Children', 'Old'])
    for year in range(2023, till_year):
        total = num_between_age_a_and_b(df, 0, 78, year, death_age)
        old = num_between_age_a_and_b(df, 60, 78, year, death_age)
        worker = num_between_age_a_and_b(df, 20, 60, year, death_age)
        children = num_between_age_a_and_b(df, 0, 20, year, death_age)
        group_df = pd.concat([group_df, pd.DataFrame([[year, total, worker, children, old]], columns=group_df.columns)])
    return group_df


df = read_born_csv()
df = extend_born_data(df, 2200)
df = add_age(df, 2023)
group_df = create_group_df(df, 2100, 79)
# plot the ratio of worker, children, and old people for each 5 years
# show line chart for each group
# show the value for the marker
group_df['WorkerRate'] = group_df['Worker'] / group_df['Total']
group_df['ChildrenRate'] = group_df['Children'] / group_df['Total']
group_df['OldRate'] = group_df['Old'] / group_df['Total']
group_df = group_df[group_df['Year'] % 5 == 0]

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
# plt.title(u'中国人口数量预测')
# plt.xlabel('年份')
# plt.ylabel('万人')
# plt.plot(group_df['Year'], group_df['Worker'], marker='o', label=u'劳动人口', color='blue')
# plt.plot(group_df['Year'], group_df['Children'], marker='o', label=u'儿童青少年', color='green')
# plt.plot(group_df['Year'], group_df['Old'], marker='o', label=u'老年人', color='orange')
# plt.legend()
# plt.show()


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

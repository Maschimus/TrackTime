import pandas as pd
import matplotlib.pyplot as plt
from classes.time_separation import TimeSeparation
import numpy as np
class Analytics:
    def __init__(self, df):
        self.df = df

    def calculate_work_hours(self):
        """Calculates the total work hours from the data.
            Exclude Feierabend and Pause entries.
        """
        return self.df[(self.df["Name"] != "Feierabend") & (self.df["Name"] != "Pause")]['TimeDiff'].dt.total_seconds().sum() / 3600

    def calculate_activity_hours(self):
        """Calculates the total hours spent on each activity."""
        return self.df.groupby('Name')['TimeDiff'].sum() / pd.Timedelta('1 hour')
    
    def caluclate_activity_hours_without_Feierabend(self):
        """Calculates the total hours spent on each activity without Feierabend."""
        return self.df[self.df["Name"] != "Feierabend"].groupby('Name')['TimeDiff'].sum() / pd.Timedelta('1 hour')
    
    def work_vs_activity(self):
        """Calculates the time spent on work compared to the time spent on each activity."""
        in_work=self.df[(self.df["Name"] != "Feierabend")]['TimeDiff'].dt.total_seconds().sum() / 3600
        not_work=self.df[(self.df["Name"] == "Feierabend")]['TimeDiff'].dt.total_seconds().sum() / 3600
        return in_work/(not_work+in_work)
    
    def work_vs_activity_with_pendel(self):
        """Calculates the time spent on work compared to the time spent on each activity and subtracts 5 hours work way"""
        in_work=self.df[(self.df["Name"] != "Feierabend")]['TimeDiff'].dt.total_seconds().sum() / 3600
        not_work=self.df[(self.df["Name"] == "Feierabend")]['TimeDiff'].dt.total_seconds().sum() / 3600
        return (in_work+5)/(not_work+in_work)
    
    def work_vs_freetime(self):
        """Calculates the time spent on work compared to the time spent on each activity and subtracts 5 hours work way subtracts 7*8 hours for sleep and 2*1.5 hours for eating
            Only works for full weeks
        """
        in_work=self.df[(self.df["Name"] != "Feierabend")]['TimeDiff'].dt.total_seconds().sum() / 3600
        not_work=self.df[(self.df["Name"] == "Feierabend")]['TimeDiff'].dt.total_seconds().sum() / 3600
        return (in_work+5)/(not_work+in_work-59)
    
    def night_shifts(self):
        '''Working after 23:00 is considered as night shift.'''
        return self.df[(self.df["Name"] != "Feierabend") & (self.df["TimeStamp"].dt.hour > 23)]['TimeDiff'].dt.total_seconds().sum() / 3600
    


    ''' Daily metrics'''

    def break_time_per_day(self):
        """Calculates the break time per day."""
        days= TimeSeparation(self.df).split_by_day()
        break_time=np.zeros(len(days))
        for i,day in enumerate(days):
            break_time[i]=day[day["Name"] == "Break"]['TimeDiff'].sum() / pd.Timedelta('1 minutes')
        return break_time
    
    def starting_time(self):
        """Calculates the starting time of the day."""
        days = TimeSeparation(self.df).split_by_day()
        starting_time = []
        for day in days:
            min_time = day['TimeStamp'].min().time()
            formatted_time = min_time.strftime('%H:%M:%S')
            starting_time.append(formatted_time)
        return starting_time
    
    def activities_per_day(self):
        """Calculates the number of activities per day."""
        days = TimeSeparation(self.df).split_by_day()
        activities = []
        for day in days:
            activities.append(len(day)-1 )  # Subtract 2 to exclude the Feierabend
        return activities
    
    def activities_with_more_than_2_hours_per_day(self):
        """Calculates the number of activities per day where each activity is more than 2 hours."""
        days = TimeSeparation(self.df).split_by_day()
        activities = np.zeros(len(days))-1  # Subtract 1 to exclude the Feierabend
        for i, day in enumerate(days):
            for _, row in day.iterrows():
                if row['TimeDiff'] > pd.Timedelta('2 hours'):
                    activities[i] += 1
        return activities

    ''' Plots'''



    def plot_of_activities(self):
        """Plots the percentage of total hours spent on each activity as a pie chart."""
        activity_hours = self.caluclate_activity_hours_without_Feierabend()
        if activity_hours is not None:
            total_hours = activity_hours.sum()
            activity_percentage = (activity_hours / total_hours * 100).round().astype(int)
            plt.figure(figsize=(8, 8))
            plt.pie(activity_percentage, labels=activity_percentage.index, autopct='%1.1f%%', startangle=140)
            plt.ylabel('Percentage of Total Hours')
            plt.title('Percentage of Total Hours Spent on Each Activity')
            #plt.show()
        else:
            print("No data to plot.")


    def plot_bar_of_activities(self):
        """
        This function takes the DataFrame with columns 'TimeStamp', 'Name', and 'TimeDiff',
        and creates a calendar-like stacked bar chart to show the daily distribution of activities.
        """
        df = self.df.copy()

        # Add an 'Hour' and 'Date' column to the DataFrame
        df['Hour'] = df['TimeStamp'].dt.hour
        df['Date'] = df['TimeStamp'].dt.date

        # Initialize a DataFrame to store the start and end times of activities for each day
        daily_activities = []

        # Loop through each date and calculate the start and end times for each activity
        for date in df['Date'].unique():
            day_df = df[df['Date'] == date].copy()
            day_df['StartHour'] = day_df['TimeStamp'].dt.hour + day_df['TimeStamp'].dt.minute / 60
            day_df['EndHour'] = day_df['StartHour'] + day_df['TimeDiff'].dt.total_seconds() / 3600
            daily_activities.append(day_df)

        # Plotting
        fig, ax = plt.subplots(figsize=(12, 8))

        colors = plt.cm.tab20(np.linspace(0, 1, len(df['Name'].unique())))
        color_map = {name: colors[i] for i, name in enumerate(df['Name'].unique())}
        color_map['Feierabend'] = 'white'
        color_map['Pause'] = 'black'

        # To track which labels have been added to the legend
        legend_labels_added = set()

        for i, day_df in enumerate(daily_activities):
            bottom = np.zeros(24)
            for name in day_df['Name'].unique():
                activity_df = day_df[day_df['Name'] == name]
                for idx, row in activity_df.iterrows():
                    start = row['StartHour']
                    duration = row['EndHour'] - row['StartHour']
                    if name not in legend_labels_added:
                        ax.bar(i, duration, bottom=start, color=color_map[name], edgecolor='grey', alpha=0.5 if name not in ['Feierabend', 'Pause'] else 1.0, label=name)
                        legend_labels_added.add(name)
                    else:
                        ax.bar(i, duration, bottom=start, color=color_map[name], edgecolor='grey', alpha=0.5 if name not in ['Feierabend', 'Pause'] else 1.0)

        ax.set_xlabel('Date')
        ax.set_ylabel('Hours')
        ax.set_title('Daily Distribution of Activities')
        ax.set_ylim(0, 24)
        ax.set_xticks(np.arange(len(df['Date'].unique())))
        ax.set_xticklabels([str(date) for date in df['Date'].unique()], rotation=45)
        ax.set_yticks(np.arange(0, 25, 1))
        ax.set_yticklabels([str(hour) for hour in range(25)])
        ax.invert_yaxis()  # Invert y-axis to have 0 at the top and 24 at the bottom
        ax.legend(loc='upper right', bbox_to_anchor=(1.15, 1))

        #plt.show()
import pandas as pd
from datetime import datetime, timedelta
from io import StringIO

class TimeSeparation:
    """
    TimeSeparation is a class to handle separating data by time periods.
    
    Attributes:
        data (pd.DataFrame): The data to process.
    """

    def __init__(self, data):
        """
        Initializes the TimeSeparation with data.

        Args:
            data (pd.DataFrame): The data to process.
        """
        self.data = data

    def separate_last_week(self):
        """Separates the data from the last week."""
        current_time = datetime.now()
        last_monday = current_time - timedelta(days=current_time.weekday())
        last_week_data = self.data[self.data['TimeStamp'] >= last_monday]
        return last_week_data
    
    def separate_last_month(self):
        """Separates the data from the last month."""
        current_time = datetime.now()
        first_day_of_current_month = current_time.replace(day=1)
        last_month = first_day_of_current_month - timedelta(days=1)
        first_day_of_last_month = last_month.replace(day=1)
        last_month_data = self.data[self.data['TimeStamp'] >= first_day_of_last_month]
        return last_month_data
    
    def separate_last_year(self):
        """Separates the data from the last year."""
        current_time = datetime.now()
        first_day_of_current_year = current_time.replace(month=1, day=1)
        last_year = first_day_of_current_year - timedelta(days=1)
        first_day_of_last_year = last_year.replace(month=1, day=1)
        last_year_data = self.data[self.data['TimeStamp'] >= first_day_of_last_year]
        return last_year_data
    
 
    def split_by_day(self):
        """Splits the data into days."""
        return [day_df for _, day_df in self.data.groupby(self.data['TimeStamp'].dt.date)]
    
    def split_by_week(self):
        """Splits the data into weeks."""
        return [week_df for _, week_df in self.data.groupby(self.data['TimeStamp'].dt.week)]
    
    def split_by_month(self):
        """Splits the data into months."""
        return [month_df for _, month_df in self.data.groupby(self.data['TimeStamp'].dt.month)]
    
    def split_by_year(self):
        """Splits the data into years."""
        return [year_df for _, year_df in self.data.groupby(self.data['TimeStamp'].dt.year)]
    
    

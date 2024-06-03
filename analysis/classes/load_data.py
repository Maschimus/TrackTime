import pandas as pd
import os

class LoadData:

 
    def __init__(self, filename):
        self.filename = filename
  
        self.df = None

    def load_csv(self):
        # Check if the file exists
        if os.path.isfile(self.filename):
            print(f"File found: {self.filename}")
            try:
                # Reading the CSV file
                self.df = pd.read_csv(self.filename, parse_dates=['TimeStamp'])
                print("File read successfully.")
   
                # process data and return
                self.process_data()
                return self.df
                
            except Exception as e:
                print(f"An error occurred while reading the file: {e}")
                return False
        else:
            print(f"File not found: {self.filename}")
            return False

    def process_data(self):
        if self.df is not None:
            try:
                # Sort the DataFrame by 'TimeStamp'
                self.df = self.df.sort_values(by='TimeStamp')
                print("DataFrame sorted by 'TimeStamp'.")

                # Calculate time differences between each entry and the next entry
                self.df['TimeDiff'] = self.df['TimeStamp'].shift(-1) - self.df['TimeStamp']
                print("Time differences calculated.")

                # Reorder columns to have ID, Name, TimeStamp, TimeDiff, Description
                self.df = self.df[['ID', 'Name', 'TimeStamp', 'TimeDiff', 'Description']]
                print("Columns reordered.")
                return True
            except Exception as e:
                print(f"An error occurred while processing the data: {e}")
                return False
        else:
            print("DataFrame is not loaded.")
            return False


if __name__ == "__main__":
    data_loader = LoadData('data/activities2.csv')
    if data_loader.load_csv():
        if data_loader.process_data():
            data_loader.display_data()

import pandas as pd  # Import pandas at the beginning of the script
from classes.load_data import LoadData  # Import the LoadData class from classes/load_data.py
from classes.time_separation import TimeSeparation  # Import the TimeSeparation class from classes/time_separation.py
from classes.analytics import Analytics  # Import the Analytics class from classes/analytics.py
from classes.report import Report  # Import the Report class from classes/report.py
import os
import datetime

if __name__ == "__main__":
    # Correct path to the CSV file relative to the location of main.py
    filename = os.path.join(os.path.dirname(__file__), "data", "activities2.csv")
    
    # Create the reports directory if it doesn't exist
    reports_dir = os.path.join(os.path.dirname(__file__), "reports")
    os.makedirs(reports_dir, exist_ok=True)
    
    # Create a unique report filename based on the current date and time
    report_filename = f"sample_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    reportpath = os.path.join(reports_dir, report_filename)
    
    df = LoadData(filename=filename).load_csv()

    # Only work with last week's data
    last_week_data = TimeSeparation(df).separate_last_week()
    lastWeeksData = Analytics(last_week_data)
    analytics = Analytics(last_week_data)

    print(analytics.caluclate_activity_hours_without_Feierabend( ))
    
    report = Report(datetime.datetime.now(), "Weekly Report")
    report.generate_pdf(reportpath, analytics)
    print(f"Report generated at: {reportpath}")

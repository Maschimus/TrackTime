from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from datetime import datetime
import os
import matplotlib.pyplot as plt
import numpy as np



class Report:
    def __init__(self, report_date, report_type, report_id=1):
        self.report_id = report_id
        self.report_date = report_date.strftime("%Y-%m-%d %H:%M:%S")
        self.report_type = report_type

    def generate_pdf(self, filename, analytics):
        """Generates a PDF with a title and logo, including analyses and plots."""
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter

        # Path to the logo image
        logo_path = os.path.join(os.path.dirname(__file__), "..\\images", "logo.png")

        # Draw the logo at the top of the page
        c.drawImage(logo_path, 72, height - 100, width=100, preserveAspectRatio=True, mask='auto')

        # Title
        title = f"Report: {self.report_type}"
        c.setFont("Helvetica-Bold", 20)
        c.drawString(72, height - 150, title)

        # Date
        report_date = f"Date: {self.report_date}"
        c.setFont("Helvetica", 12)
        c.drawString(72, height - 180, report_date)

        # Report ID
        report_id = f"Report ID: {self.report_id}"
        c.setFont("Helvetica", 12)
        c.drawString(72, height - 200, report_id)

        # Add text analysis results
        self.add_text_analysis(c, analytics, height - 230)

        # Add array text analysis results
        self.add_array_text_analysis(c, analytics, height - 430)

        # Add plots
        self.add_plots(c, analytics, height - 630)
        c.save()

    def add_text_analysis(self, c, analytics, start_height):
        """Adds text analysis results to the PDF."""
        results = [
            ("Total work hours (excluding Feierabend and Pause):", np.round(analytics.calculate_work_hours(), 1)),
            ("Work vs Activity Ratio:", np.round(analytics.work_vs_activity(), 2)),
            ("Work vs Activity with Pendel:", np.round(analytics.work_vs_activity_with_pendel(), 2)),
            ("Work vs Freetime:", np.round(analytics.work_vs_freetime(), 2)),
            ("Night Shifts (hours):", analytics.night_shifts()),
            ("Activities with more than 2 hours per day:", analytics.activities_with_more_than_2_hours_per_day()),
            ("Number of activities per day:", analytics.activities_per_day()),
            ("Starting time of each day:", analytics.starting_time()),
            ("Break time per day (minutes):", np.round(analytics.break_time_per_day(),2)),
        ]
        width, height = letter
        c.setFont("Helvetica", 12)
        text = c.beginText(72, start_height)
        for desc, result in results:
            text.textLine(f"{desc} {result}")
            start_height -= 15
            if start_height < 72:  # Check for new page
                c.drawText(text)
                c.showPage()
                text = c.beginText(72, height - 72)
        c.drawText(text)

    def add_array_text_analysis(self, c, analytics, start_height):
        """Adds array text analysis results to the PDF."""
        activity_hours = analytics.caluclate_activity_hours_without_Feierabend()
        array_results = [
            ("Hours spent on each activity without Feierabend:", activity_hours)
        ]
        width, height = letter
        c.setFont("Helvetica", 12)
        text = c.beginText(72, start_height)
        for desc, result in array_results:
            text.textLine(f"{desc}")
            start_height -= 15
            for activity, hours in result.items():
                text.textLine(f"    {activity}: {np.round(hours, 2)} hours")
                start_height -= 15
                if start_height < 72:
                    c.drawText(text)
                    c.showPage()
                    text = c.beginText(72, height - 72)
        c.drawText(text)


    def add_plots(self, c, analytics, start_height):
        """Generates and adds plots to the PDF."""
        width, height = letter
        plot_functions = [
            analytics.plot_of_activities,
            analytics.plot_bar_of_activities
        ]

        for plot_func in plot_functions:
            # Generate the plot and save as image
            plot_filename = f"plot_{plot_func.__name__}.png"
            plot_func()
            plt.savefig(plot_filename)
            plt.close()

            # Add the plot to the PDF
            c.showPage()  # Start a new page for each plot
            plot_image = ImageReader(plot_filename)
            c.drawImage(plot_image, 72, height - 700, width=width - 144, preserveAspectRatio=True, mask='auto')

            # Remove the temporary plot image
            os.remove(plot_filename)

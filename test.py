import csv
from datetime import datetime,timedelta



def analyze_employee_data(filename):
    """Analyzes employee data from a CSV file and identifies those who meet certain criteria.

    Args:
        filename (str): The path to the CSV file.

    Raises:
        ValueError: If the file is not a valid CSV file.
    """

    try:
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)  # Skipping of the header row

            # Creating a dictionary to store employee data
            employees = {}
            for row in reader:
                try:
                    #Taking only required data i.e., positon_id,employee_name,time_in,time_out,hours
                    position_id = row[0]
                    employee_name = row[7]
                    time_in = datetime.strptime(row[2], '%m/%d/%Y %I:%M %p')
                    time_out = datetime.strptime(row[3], '%m/%d/%Y %I:%M %p')
                    hours = row[4]

                    if position_id not in employees:
                        employees[position_id] = {
                            'name': employee_name,
                            'shifts': []
                        }
                    employees[position_id]['shifts'].append({
                        'time_in': time_in,
                        'time_out': time_out,
                        'hours': hours
                    })
                except ValueError:
                    print(f"Invalid data format in row: {row}") #edge case - printing invalid data
                    continue  # Skipping to the next row

            # Analyze employee data
            for position_id, data in employees.items():
                # a) Worked for 7 consecutive days
                consecutive_days = 1
                previous_date = None
                for shift in data['shifts']:
                    shift_date = shift['time_in'].date()
                    if previous_date and shift_date - previous_date != timedelta(days=1):  # Using timedelta to calculate coonsecutive days
                        consecutive_days = 1
                    else:
                        consecutive_days += 1
                    previous_date = shift_date
                    if consecutive_days == 7:
                        print(f"Employee {data['name']} (Position ID: {position_id}) has worked for 7 consecutive days.") #Print name and position of employee

                # b) Less than 10 hours between shifts but greater than 1 hour
                for i in range(1, len(data['shifts'])):
                    time_between_shifts = (data['shifts'][i]['time_in'] - data['shifts'][i-1]['time_out']).total_seconds() / 3600
                    if 1 < time_between_shifts < 10:
                        print(f"Employee {data['name']} (Position ID: {position_id}) has less than 10 hours between shifts on {data['shifts'][i]['time_in'].date()}.") #Print name and position of employee

                # c) Worked for more than 14 hours in a single shift
                for shift in data['shifts']:
                    hours_worked = float(shift['hours'].split(':')[0]) + float(shift['hours'].split(':')[1]) / 60
                    if hours_worked > 14:
                        print(f"Employee {data['name']} (Position ID: {position_id}) has worked for more than 14 hours in a single shift on {shift['time_in'].date()}.") #Print name and position of employee
#Handling file errors
    except FileNotFoundError:
        print(f"Error: File not found: {filename}")
    except csv.Error as e:
        print(f"Error: Invalid CSV file: {e}")

filename = "D:\Downloads\Assignment_Timecard.xlsx - Sheet1.csv"  #importing file present in downloads folder
analyze_employee_data(filename)

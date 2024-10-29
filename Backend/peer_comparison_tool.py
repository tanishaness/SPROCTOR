import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Define a Student class to initialize student data and track changes over time
class Student:
    def __init__(self, name, study_hours, participation_rate, assignment_completion):
        self.name = name
        self.study_hours = [study_hours]
        self.participation_rate = [participation_rate]
        self.assignment_completion = [assignment_completion]

    # Method to update metrics for longitudinal tracking
    def update_metrics(self, study_hours, participation_rate, assignment_completion):
        self.study_hours.append(study_hours)
        self.participation_rate.append(participation_rate)
        self.assignment_completion.append(assignment_completion)

    # Calculate average metrics for the student across all timepoints
    def average_metrics(self):
        return {
            "average_study_hours": np.mean(self.study_hours),
            "average_participation_rate": np.mean(self.participation_rate),
            "average_assignment_completion": np.mean(self.assignment_completion)
        }

# Calculate overall averages for the latest metrics among all students
def calculate_averages(students):
    study_hours = np.array([s.study_hours[-1] for s in students])
    participation_rates = np.array([s.participation_rate[-1] for s in students])
    assignment_completions = np.array([s.assignment_completion[-1] for s in students])
    
    return {
        "average_study_hours": np.mean(study_hours),
        "average_participation_rate": np.mean(participation_rates),
        "average_assignment_completion": np.mean(assignment_completions)
    }

# Identify outliers based on a customizable threshold (default is 1.5)
def identify_outliers(students, averages, threshold=1.5):
    outliers = []
    for student in students:
        # Detect outliers in each metric based on standard deviation
        if (abs(student.study_hours[-1] - averages["average_study_hours"]) > threshold * np.std([s.study_hours[-1] for s in students])):
            outliers.append((student.name, 'Study Hours'))
        if (abs(student.participation_rate[-1] - averages["average_participation_rate"]) > threshold * np.std([s.participation_rate[-1] for s in students])):
            outliers.append((student.name, 'Participation Rate'))
        if (abs(student.assignment_completion[-1] - averages["average_assignment_completion"]) > threshold * np.std([s.assignment_completion[-1] for s in students])):
            outliers.append((student.name, 'Assignment Completion'))

    return outliers

# Calculate Peer Comparison Index (PCI) as the average of individual average metrics
def calculate_peer_comparsion_index(students):
    scores = []
    for student in students:
        avg_metrics = student.average_metrics()
        score = (avg_metrics["average_study_hours"] + avg_metrics["average_participation_rate"] + avg_metrics["average_assignment_completion"]) / 3
        scores.append((student.name, score))
    return scores 

# Visualize student metrics with averages and outliers highlighted
def visualize_results(students, averages, outliers):
    behaviors = ['Study Hours', 'Participation Rate', 'Assignment Completion']
    
    # Set up figure for the bar chart
    plt.figure(figsize=(12, 6))
    bar_width = 0.2  # Width for each student's bars
    x_indices = np.arange(len(behaviors))  # X positions for bars
    avg_colors = ['red', 'blue', 'green']  # Colors for average lines
    
    # Create bar chart for each student's latest metrics
    for i, student in enumerate(students):
        plt.bar(x_indices + (i * bar_width), 
                [student.study_hours[-1], student.participation_rate[-1], student.assignment_completion[-1]], 
                width=bar_width, label=student.name)

    # Add lines for average values in each metric category
    for i, (avg, color) in enumerate(zip(
        [averages['average_study_hours'], averages['average_participation_rate'], averages['average_assignment_completion']],
        avg_colors)):
        plt.axhline(y=avg, color=color, linestyle='--', label=f'Average {behaviors[i]}')

    plt.title('Student Behaviors and Averages')
    plt.xlabel('Behaviors')
    plt.ylabel('Values')
    plt.xticks(x_indices + bar_width * (len(students) - 1) / 2, behaviors)
    plt.legend()
    plt.tight_layout()
    plt.show()

# Generate a report in CSV format containing average metrics and outlier status
def generate_report(students, averages, outliers):
    report_data = {
        "Name": [],
        "Average Study Hours": [],
        "Average Participation Rate": [],
        "Average Assignment Completion": [],
        "Outlier Status": []
    }
    
    for student in students:
        avg_metrics = student.average_metrics()
        report_data["Name"].append(student.name)
        report_data["Average Study Hours"].append(avg_metrics["average_study_hours"])
        report_data["Average Participation Rate"].append(avg_metrics["average_participation_rate"])
        report_data["Average Assignment Completion"].append(avg_metrics["average_assignment_completion"])
        report_data["Outlier Status"].append("Outlier" if any(name == student.name for name, _ in outliers) else "Normal")
    
    df = pd.DataFrame(report_data)
    df.to_csv('student_report.csv', index=False)
    print("\nReport generated: student_report.csv")

# Helper function to handle user input with a default value option
def get_float_input(prompt, default_value):
    while True:
        try:
            value = input(prompt)
            if value.strip() == "":
                return default_value
            return float(value)
        except ValueError:
            print("Invalid input. Please enter a valid number.")

# Main function to initialize student data, calculate metrics, identify outliers, and generate reports
def main():
    students = []
    
    # Collect user input for each student
    while True:
        name = input("Enter student name (or 'done' to finish): ")
        if name.lower() == 'done':
            break
            
        study_hours = get_float_input("Enter study hours (default is 0): ", 0)
        participation_rate = get_float_input("Enter participation rate (0-1, default is 0): ", 0)
        assignment_completion = get_float_input("Enter assignment completion (0-1, default is 0): ", 0)
        
        students.append(Student(name, study_hours, participation_rate, assignment_completion))

    if students:
        averages = calculate_averages(students)
        outliers = identify_outliers(students, averages)

        print("\nAverages:")
        for key, value in averages.items():
            print(f"{key}: {value:.2f}")

        print("\nOutliers:")
        for name, behavior in outliers:
            print(f"{name} is an outlier in {behavior}")
            
        peer_comparsion_scores = calculate_peer_comparsion_index(students)
        print("\nPeer Comparison Index (PCI):")
        for name, score in peer_comparsion_scores:
            print(f"{name}: {score:.2f}")
            
        generate_report(students, averages, outliers)
        visualize_results(students, averages, outliers)
    else:
        print("No student data entered.")

# Run the main function
if __name__ == "__main__":
    main()

import numpy as np
import matplotlib.pyplot as plt
import random

class Student:
    def __init__(self, name, study_hours, participation_rate, assignment_completion):
        self.name = name
        self.study_hours = study_hours
        self.participation_rate = participation_rate
        self.assignment_completion = assignment_completion

def calculate_averages(students):
    study_hours = np.array([s.study_hours for s in students])
    participation_rates = np.array([s.participation_rate for s in students])
    assignment_completions = np.array([s.assignment_completion for s in students])
    
    return {
        "average_study_hours": np.mean(study_hours),
        "average_participation_rate": np.mean(participation_rates),
        "average_assignment_completion": np.mean(assignment_completions)
    }

def identify_outliers(students, averages):
    outliers = []
    threshold = 1.5
    
    for student in students:
        if (abs(student.study_hours - averages["average_study_hours"]) > threshold * np.std([s.study_hours for s in students])):
            outliers.append((student.name, 'Study Hours'))
        if (abs(student.participation_rate - averages["average_participation_rate"]) > threshold * np.std([s.participation_rate for s in students])):
            outliers.append((student.name, 'Participation Rate'))
        if (abs(student.assignment_completion - averages["average_assignment_completion"]) > threshold * np.std([s.assignment_completion for s in students])):
            outliers.append((student.name, 'Assignment Completion'))

    return outliers

def visualize_results(students, averages, outliers):
    behaviors = ['Study Hours', 'Participation Rate', 'Assignment Completion']
    
    # Create a figure
    plt.figure(figsize=(12, 6))
    
    # Set the width of each bar
    bar_width = 0.2
    
    # X positions for each behavior
    x_indices = np.arange(len(behaviors))
    
    # Define colors for average lines
    avg_colors = ['red', 'blue', 'green']
    
    # Create bars for each student
    for i, student in enumerate(students):
        plt.bar(x_indices + (i * bar_width), 
                [student.study_hours, student.participation_rate, student.assignment_completion], 
                width=bar_width, label=student.name)

    # Add dotted lines for averages with different colors
    for i, (avg, color) in enumerate(zip(
        [averages['average_study_hours'], averages['average_participation_rate'], averages['average_assignment_completion']],
        avg_colors)):
        plt.axhline(y=avg, color=color, linestyle='--', label=f'Average {behaviors[i]}')

    # Set the labels, title, and ticks
    plt.title('Student Behaviors and Averages')
    plt.xlabel('Behaviors')
    plt.ylabel('Values')
    plt.xticks(x_indices + bar_width * (len(students) - 1) / 2, behaviors)
    plt.legend()
    
    # Show the plot
    plt.tight_layout()
    plt.show()

def main():
    students = []
    
    # User input for student data
    while True:
        name = input("Enter student name (or 'done' to finish): ")
        if name.lower() == 'done':
            break
        study_hours = float(input("Enter study hours: "))
        participation_rate = float(input("Enter participation rate (0-1): "))
        assignment_completion = float(input("Enter assignment completion (0-1): "))
        students.append(Student(name, study_hours, participation_rate, assignment_completion))

    averages = calculate_averages(students)
    outliers = identify_outliers(students, averages)

    print("\nAverages:")
    for key, value in averages.items():
        print(f"{key}: {value:.2f}")
    
    print("\nOutliers:")
    for name, behavior in outliers:
        print(f"{name} is an outlier in {behavior}")

    # Visualize results
    visualize_results(students, averages, outliers)

if __name__ == "__main__":
    main()

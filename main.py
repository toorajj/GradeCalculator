###########################################################
# Program's Name: main.py
# Purpose: Report Generator
# Modify Date: 5/23/2024
# Created By: Tooraj Jabbarnia

# Algorithm:
# Read csv date file using pandas and data frame,
# Display a menu for:
# 1. Data Summary,
# 2. Sample Data,
# 4. Display Initial DataFrame,
# 5. Generate a clean report,
# 6. Output "Exam Average" Line Plot,
# 7. Output "Grades" Bar Graph,
# 8. Output "Grades" Pie Chart
# X. or 'x' to Exit

import pandas as pd
import math
import matplotlib.pyplot as plt 

# read the csv file and assign to df 
df = pd.read_csv('student-scores.csv')

# to include all columns in data summary
pd.set_option('display.max_columns', None)
# to include all columns in initial DataFrame
pd.set_option('display.width', None)

# Defult values for choices
choices = ['1', '2', '3', '4', '5', '6', '7', '8', 'x', 'X']
# to start the while loop
choice = '1'

# to input enter key
def enterKey():
    input("\nPress the [Enter] key to continue")

# menu print
def menu():
    print('===== Menu =====\n1. Data Summary\n2. Sample Data\n3. Display Initial DataFrame\n4. Generate raw report\n5. Generate a clean report\n6. Output "Exam Average" Line Plot\n7. Output "Grades" Bar Graph, \n8. Output "Grades" Pie Chart\nX. Exit')

# takes DataFrame and index, returns lowest number
def dropTest(df, i):
        dropExam = min(df.T1[i], df.T2[i], df.T3[i],df.T4[i])
        return(dropExam)

# takes a number, compares value to dictionary and assigns a letter grade (key) and returns a string, if not a number recieved returns 'F'
def getGrade(scoreSum):
    grades = {90: 'A', 80: 'B', 70: 'C', 60: 'D', 0: 'F'}
    for score, gradeMsg in grades.items():
        if (scoreSum/4) >= score:
            return(gradeMsg)
        elif math.isnan(scoreSum):
            return('F')
    
# runs as long as 1-5 is chosen, exits with 'x'
while choice in choices:
    menu()    
    choice = input('Please enter your choice(1, 2, 3, 4, 5, 6, 7, 8 or X): ')
    if choice == '1':
        print('\nData summary:\n')
        print(df.info())
        enterKey()
    
    elif choice == '2':
        print('\nSample record:')
        print(df.sample())
        enterKey()
        
    elif choice == '3':
        print('\nInitial DataFrame')
        print(df)
        enterKey()
    
    elif choice == '4':
        
        print()
        print('Name\t\t\t\tT1\tT2\tT3\tT4\tFinal\tTotal\t   SID\t   Grade\n')
        
        # to print T1 to T4, use dropTest function to deduct lowest score, print total score for the row and get grade from getGrade function and generate grand score total excluding dropped score 
        # and add a 'Total' & 'Grade' column with calculated values for each row to df_sorted
        df_sorted = df.sort_values('Name').reset_index()
        total = []
        grade = []
        grandTotal = 0
        for i in range (len(df_sorted)):
            final = float(df_sorted.Final[i].split()[0])
            print(f'{df_sorted.Name[i]:.<31}{df_sorted.T1[i]:<8}{df_sorted.T2[i]:<8}{df_sorted.T3[i]:<8}{df_sorted.T4[i]:<9}{final:<8.1f}', end = '')
            totalScore = df_sorted.T1[i] + df_sorted.T2[i] + df_sorted.T3[i] + df_sorted.T4[i] + final - dropTest(df_sorted, i)
            total.append(totalScore)
            print(f'{totalScore:<8}{df_sorted.SID[i]:.<10}{getGrade(totalScore):.>4}')
            grandTotal = totalScore + grandTotal
            grade.append(getGrade(totalScore))
        df_sorted['Total'] = total
        df_sorted['Grade'] = grade
            
        print(f'  Number of students: {len(df_sorted)}      =====   =====   =====   =====    =====   ======   ==============')
        print(f'\t\t\tMin{df_sorted.T1.min():.>8}{df_sorted.T2.min():8}{df_sorted.T3.min():8}{df_sorted.T4.min():8}\t{float(df_sorted.Final.min().split()[0])} {df_sorted.Total.min():8}\t{df_sorted.Grade.max():.>14}')
        print(f'\t\t\tMax{df_sorted.T1.max():.>8}{df_sorted.T2.max():8}{df_sorted.T3.max():8}{df_sorted.T4.max():8}\t{float(df_sorted.Final.max().split()[0])} {df_sorted.Total.max():8}\t{df_sorted.Grade.min():.>14}')
        
        # to separate digits from string and average
        finalTotal = 0
        for x in range(len(df_sorted)):
            finalTotal = float(df_sorted['Final'][x].split()[0]) + finalTotal
        finalAvg = finalTotal / (len(df_sorted))
        
        print(f'\t\t\tAvg{df_sorted.T1.mean():.>8.1f}{df_sorted.T2.mean():8.1f}{df_sorted.T3.mean():8.1f}{df_sorted.T4.mean():8.1f}\t{finalAvg:.1f}{grandTotal/len(df_sorted):8}\t{getGrade(grandTotal/(len(df_sorted))):.>14}')
        
        enterKey()
        
    elif choice == '5':
        
        df_clean = df.dropna(subset = ['SID']).fillna(0).sort_values('Name').reset_index(drop=True)
        for i in range (0, 95):
            print('-', end = '')
        
        print('\nName\t\t\t\t    T1\t   T2\t  T3\t T4   Final  Total    SID \t Grade\n')
        total = []
        grade = []
        finalSum = 0
        
        for i in range(len(df_clean)):
            final = float(df_clean.Final[i].split()[0])
            finalTotal = df_clean.T1[i] + df_clean.T2[i] + df_clean.T3[i] + df_clean.T4[i] + final - dropTest(df_clean, i) 
            print(f'{df_clean.Name[i]:.<34}{df_clean.T1[i]:>5}{df_clean.T2[i]:>7}{df_clean.T3[i]:>7}{df_clean.T4[i]:>7}{final:>7.1f}{finalTotal:>7}{df_clean.SID[i]:>10}{getGrade(finalTotal):.>8}')
            total.append(finalTotal)
            grade.append(getGrade(finalTotal))
            finalSum = float(df_clean['Final'][i].split()[0]) + finalSum
            
        print('\t\t\t\t  =====  =====  =====  =====  =====  =====  ================')
        df_clean['Total'] = total
        df_clean['Grade'] = grade
        print(f'  Number of students: {len(df_clean)}    Min{df_clean.T1.min():.>8}{df_clean.T2.min():>7}{df_clean.T3.min():>7}{df_clean.T4.min():>7}{df_clean.Final.min().split()[0]:>7}{df_clean.Total.min():>7}  {df_clean.Grade.max():.>16}')
        print(f'\t\t\t    Max{df_clean.T1.max():.>8}{df_clean.T2.max():>7}{df_clean.T3.max():>7}{df_clean.T4.max():>7}{df_clean.Final.max().split()[0]:>7}{df_clean.Total.max():>7}  {df_clean.Grade.min():.>16}')
        print(f'\t\t\t    Avg{df_clean.T1.mean():.>8.1f}{df_clean.T2.mean():>7.1f}{df_clean.T3.mean():>7.1f}{df_clean.T4.mean():>7.1f}{finalSum/len(df_clean):>7.1f}{df_clean.Total.mean():>7.1f}  {getGrade(df_clean.Total.sum()/len(df_clean)):.>16}')
        enterKey()
        
    
    elif choice == '6':
        
        df_clean = df.dropna(subset = ['SID']).fillna(0).sort_values('Name').reset_index(drop=True)

        
        plt.plot(df_clean.index, df_clean.T1, color = 'r', linestyle= '-', marker = '.', label = 'T1')
        plt.plot(df_clean.index, df_clean.T2, color = 'b', linestyle= '--', marker = '.', label = 'T2')
        plt.plot(df_clean.index, df_clean.T3, color = 'y', linestyle= '-.', marker = '.', label = 'T3')
        plt.plot(df_clean.index, df_clean.T4, color = 'g', linestyle= ':', marker = '.', label = 'T4')

        plt.legend()
        plt.title('Line plot with the four exams and the final average scores')
        plt.xlabel('Students')
        plt.ylabel('Scores')
        plt.tight_layout()
        plt.grid()
        plt.savefig('LinePlot.png')
        enterKey()
    
    elif choice == '7':
    
        df_clean = df.dropna(subset = ['SID']).fillna(0).sort_values('Name').reset_index(drop=True)

        grade = []
        for i in range(len(df_clean)):
            final = float(df_clean.Final[i].split()[0])
            finalTotal = df_clean.T1[i] + df_clean.T2[i] + df_clean.T3[i] + df_clean.T4[i] + final - dropTest(df_clean, i) 
            grade.append(getGrade(finalTotal))
        df_clean['Grade'] = grade
    
        # Creates a dictionary and adds a count based on grades 
        gradeCount = df_clean['Grade'].value_counts().to_dict()
    
        # Plot
        plt.bar('A', gradeCount['A'], width = 0.8, label = "A")
        plt.bar('B', gradeCount['B'], width = 0.8, label = "B")
        plt.bar('C', gradeCount['C'], width = 0.8, label = "C")
        plt.bar('D', gradeCount['D'], width = 0.8, label = "D")
        plt.bar('F', gradeCount['F'], width = 0.8, label = "F")
        
        plt.legend()
        plt.title("Number of A, B, C, D and F's")
        plt.xlabel('Grades')
        plt.ylabel('Count')
        plt.tight_layout()
        plt.savefig('BarGraph.png')

        enterKey()
    
    elif choice == '8':
        
        df_clean = df.dropna(subset = ['SID']).fillna(0).sort_values('Name').reset_index(drop=True)

        grade = []
        for i in range(len(df_clean)):
            final = float(df_clean.Final[i].split()[0])
            finalTotal = df_clean.T1[i] + df_clean.T2[i] + df_clean.T3[i] + df_clean.T4[i] + final - dropTest(df_clean, i) 
            grade.append(getGrade(finalTotal))
        df_clean['Grade'] = grade
    
        # Creates a dictionary and adds a count based on grades 
        gradeCount = df_clean['Grade'].value_counts().to_dict()
        
        # Formatting
        slice_colors = ['r', 'y', 'g', 'b', 'w']
        slice_popout = [0.1, 0, 0, 0, 0]
        plt.style.use('fivethirtyeight')

        group = ['A', 'B', 'C', 'D', 'F']
        dist = [gradeCount['A'], gradeCount['B'], gradeCount['C'], gradeCount['D'], gradeCount['F']]

        plt.pie(dist, labels = group, colors = slice_colors, explode = slice_popout, wedgeprops = {'edgecolor' : 'black'})
        plt.title("Number of A, B, C, D and F's")
        plt.savefig('PieGraph.png')

        enterKey()

    elif choice.lower() == 'x':
        break
        

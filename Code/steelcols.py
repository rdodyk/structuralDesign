# Program to design steel beams as per CSA S16
import math
from memberclasses import Column

#Functions

shapes = []
with open('../Assets/aisc-shapes-database-v15.csv', 'r') as steelCSV:
    for row in steelCSV:
        shapes.append(row.strip().split(','))
        # Metric shape names @ column 82
        # Check excel file for referencing columns

# Get basic properties of design column
def colProperties ():
    # Get length of column
    while True:
        try:
            l = float(input("Length of your column: "))
            break
        except ValueError:
            print ("Please enter a valid length")

    # Get column loads
    while True:
        try:
            P = float(input("Factored axial force on column: "))
            Mx = float(input("Factered moment about strong axis: "))
            My = float(input("Factored moment about weak axis: "))
            break
        except ValueError:
            print ("That is not a valid input, please try again")

    # Get column k value
    while True:
        try:
            k = float(input("Column k value: "))
            break
        except ValueError:
            print ("k. Take this seriously")

    

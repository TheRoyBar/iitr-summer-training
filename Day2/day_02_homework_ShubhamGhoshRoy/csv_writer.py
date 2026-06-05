#13. **CSV Result Writer**  
#Store three student records in a CSV file using Python's csv module.
import csv

student1 = {
    'name' : 'A',
    'marks' : 98
    }

student2 = {
    'name' : 'B',
    'marks' : 78
    }

student3 = {
    'name' : 'C',
    'marks' : 48
    }

with open('university_records.csv', 'w', newline='') as csvfile:
    fieldnames = ['name', 'marks']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(student1)
    writer.writerows(student2)
    writer.writerows(student3)
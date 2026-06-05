# Create a simple **Student Profile Analyzer** 
# that gives suggestions based on attendance, Python score, project count, 
# and feedback text. This is a rule-based version of a future AI advisor.

a = int(input("Enter your attendance percentage:"))
python_score = int(input("Enter your python score:"))
project_count = int(input("Enter your project count:"))
feedback = input("Enter your feedback from the options: web, data, charts, communication, leader, reports, detail, django, ")

if a < 70:
    print("Attendance is too low. Focus on classes before career placement!")

if python_score >= 85 and "data" in feedback:
    print("Data Scientist (Strong Python skills + interest in data)")

if python_score >= 90 and project_count >= 3:
    print("Machine Learning Engineer (High score + great project portfolio)")

if 70 <= python_score < 90 and project_count >= 2:
    print("Software Engineer (Solid coding foundation and practical building skills)")

if 60 <= python_score < 85 and "charts" in feedback or "reports" in feedback:
    print("Data Analyst (Good Python basics with a knack for reporting)")

if 60 <= python_score < 80 and "detail" in feedback:
    print(" QA Automation Engineer (Detail-oriented, uses Python for testing)")

if "web" in feedback or "django" in feedback:
    print("Web Developer (Interest in building web applications)")

if "communication" in feedback or "leader" in feedback:
    print("Technical Product Manager (Great interpersonal skills + tech background)")

else:
    print("General Python Developer (Keep learning to find your niche!)")
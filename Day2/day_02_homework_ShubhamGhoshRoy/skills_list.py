#**Skill List Manager**  
#Create a list of skills. Add a new skill, remove a skill, and print total skills.

skills = ['Running', 'Swimming', 'Cooking']
new_skill = input("Enter your new skill:")
skills.append(new_skill)

remove_skill = input("Enter forgotten skill:")
skills.remove(remove_skill)

print(skills)
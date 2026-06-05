#10. **Feedback Cleaner**  
#  Take student feedback and clean it using strip(), lower(), and replace().

feedback = input("Enter your feedback:")

feedback = feedback.strip()
feedback = feedback.lower()
feedback = feedback.replace('i', 'I')

print(feedback)
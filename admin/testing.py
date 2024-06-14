from datetime import datetime

# Get the current date and time
now = datetime.now()

# Format the date as 'Month Day, Year'
formatted_date = now.strftime("%B %d, %Y")

# Get the current hour
current_hour = now.hour

# Generate greeting message based on the current time
if current_hour < 12:
    greeting = "Good Morning!"
elif 12 <= current_hour < 18:
    greeting = "Good Afternoon!"
else:
    greeting = "Good Evening!"

# Print the formatted date and greeting message
print(f"Current date: {formatted_date}")
print(greeting)
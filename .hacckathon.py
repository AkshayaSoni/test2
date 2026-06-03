import time 
from datetime import datetime, timedelta
name = input("your name please:  ").strip().capitalize()
user_test_name = input("Give the name of the test/quiz: " ).strip().capitalize()

while True:
    try:
        number_chapter = int(input("how many numbers of the chapter you have to study "))
        break
    except ValueError:
        print("Please enter a whole number of chapters.")

while True:
    try:
        how_manydays = int(input("how many days left for the test/quiz "))
        break
    except ValueError:
        print("Please enter a whole number of days.")

while True:
    try:
        hours_per_day = float(input("how many hours you can study per day "))
        break
    except ValueError:
        print("Please enter a valid number of hours per day.")

while True:
    try:
        starting_time = int(input("What time do you want to start studying? (enter hour in 12-hour format, e.g., 6 for 6pm) "))
        if 1 <= starting_time <= 12:
            break
        print("Please enter an hour between 1 and 12.")
    except ValueError:
        print("Please enter a valid hour in 12-hour format.")

while True:
    starting_period = input("Is that AM or PM? (enter am or pm) ").strip().lower()
    if starting_period in ("am", "pm"):
        break
    print("Please enter am or pm.")

if starting_period == "am":
    if starting_time == 12:
        starting_time = 0
else:
    if starting_time != 12:
        starting_time += 12

while True:
    try:
        time_method = int(input("Choose time method : 24:00 or 12:00 (enter 24 or 12) "))
        if time_method in (12, 24):
            break
        print("Please enter 12 or 24.")
    except ValueError:
        print("Please enter 12 or 24.")

if time_method == 12:
    print("You have chosen 12-hour time format. Study sessions will be scheduled accordingly.")
else:
    print("You have chosen 24-hour time format. Study sessions will be scheduled accordingly.")

if how_manydays <= 0:
    how_manydays = 1
    print("Days must be at least 1. Using 1 day.")
if number_chapter < 0:
    number_chapter = 0
    print("Number of chapters cannot be negative. Using 0 chapters.")
if hours_per_day < 0:
    hours_per_day = 0
    print("Hours per day cannot be negative. Using 0 hours per day.")
if starting_time < 0 or starting_time > 23:
    starting_time = 18
    print("Invalid starting time. Defaulting to 18:00.")

chapters_per_day = max(1, number_chapter // how_manydays)
total_study_minutes = (hours_per_day * 60) # turns hours into minutes
minutes_per_chapter = max(1, total_study_minutes // chapters_per_day)
print("Option 1 (One-liner study Tracker: Set reminders for any subject days or weeks in advance so you never miss a test. Option 2 (Step-by-Step)")
print("Welcome to Study Tracker!")
print("Choose any subject.")
print("Set how many days or weeks ahead you want a reminder of.")
print("Relax—we'll handle the rest")
print("Welcome to the study guide for " + user_test_name)

# helper for 12/24 hour output formatting

def format_time(dt):
    if time_method == 12:
        return dt.strftime("%I:%M %p").lstrip("0").replace(" 0", " ")
    return dt.strftime("%H:%M")

# build a study schedule table with time on the y axis
chapter_distribution = [number_chapter // how_manydays + (1 if i < number_chapter % how_manydays else 0) for i in range(how_manydays)]
current_chapter = 1

print("\nStudy schedule table:")
for day_index in range(how_manydays):
    day_date = (datetime.now().date() + timedelta(days=day_index)).isoformat()
    print(f"\nDay {day_index + 1} ({day_date}):")
    day_start = datetime.now().replace(hour=starting_time, minute=0, second=0, microsecond=0) + timedelta(days=day_index)
    chapter_count = chapter_distribution[day_index]
    if chapter_count == 0:
        rest_label = f"{format_time(day_start)} - {format_time(day_start)}"
        print(f"  {rest_label}  Rest day")
        continue
    study_hours_per_chapter = hours_per_day / chapter_count

    for session_index in range(chapter_count):
        session_start = day_start + timedelta(hours=session_index * study_hours_per_chapter)
        session_end = session_start + timedelta(hours=study_hours_per_chapter)
        time_label = f"{format_time(session_start)} - {format_time(session_end)}"
        print(f"  {time_label}  Chapter {current_chapter}")
        current_chapter += 1
    

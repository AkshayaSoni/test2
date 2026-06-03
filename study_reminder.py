#!/usr/bin/env python3
import argparse
import json
import subprocess
import time
from datetime import datetime, timedelta


def build_plan(test_name, chapters, days, hours_per_day, start_hour=18):
    chapters = int(chapters)
    days = int(days)
    hours_per_day = float(hours_per_day)

    # distribute chapters across days (as evenly as possible)
    base = chapters // days
    rem = chapters % days
    plan = []
    chapter_num = 1
    hours_per_chapter = (hours_per_day * days) / chapters if chapters > 0 else 0

    for d in range(days):
        today_chapters = base + (1 if d < rem else 0)
        day_items = []
        start = datetime.now().replace(hour=int(start_hour), minute=0, second=0, microsecond=0) + timedelta(days=d)
        current = start
        for i in range(today_chapters):
            duration_hours = hours_per_chapter
            item = {
                "chapter": chapter_num,
                "start": current.isoformat(),
                "duration_hours": round(duration_hours, 2)
            }
            day_items.append(item)
            # advance time
            current = current + timedelta(hours=duration_hours)
            chapter_num += 1

        plan.append({
            "day_index": d + 1,
            "date": start.date().isoformat(),
            "items": day_items
        })

    return {
        "test_name": test_name,
        "chapters": chapters,
        "days": days,
        "hours_per_day": hours_per_day,
        "hours_per_chapter": round(hours_per_chapter, 3),
        "plan": plan,
    }


def print_plan(plan):
    print(f"Study plan for: {plan['test_name']}")
    print(f"Chapters: {plan['chapters']} over {plan['days']} days ({plan['hours_per_day']} hrs/day)")
    print(f"Estimated hours per chapter: {plan['hours_per_chapter']}")
    print()
    for day in plan['plan']:
        print(f"Day {day['day_index']} — {day['date']}")
        if not day['items']:
            print("  Rest day")
        for it in day['items']:
            start = datetime.fromisoformat(it['start'])
            end = start + timedelta(hours=it['duration_hours'])
            print(f"  Chapter {it['chapter']}: {start.strftime('%Y-%m-%d %H:%M')} — {end.strftime('%H:%M')} ({it['duration_hours']} hrs)")
        print()


def save_plan(plan, path='study_plan.json'):
    with open(path, 'w') as f:
        json.dump(plan, f, indent=2)
    print(f"Saved plan to {path}")


def send_notification(title, body):
    try:
        subprocess.run(['notify-send', title, body])
    except FileNotFoundError:
        print(f"Notification: {title} - {body}")


def run_reminders(plan):
    # flatten items with datetime
    events = []
    for day in plan['plan']:
        for it in day['items']:
            start = datetime.fromisoformat(it['start'])
            events.append((start, it))

    events.sort(key=lambda x: x[0])
    print(f"Running reminders for {len(events)} sessions. Press Ctrl+C to stop.")
    try:
        for start, it in events:
            now = datetime.now()
            if start <= now:
                # if it's in the past, notify immediately
                send_notification(f"Study now: {plan['test_name']}", f"Chapter {it['chapter']} — {it['duration_hours']} hrs")
                continue
            wait = (start - now).total_seconds()
            # sleep until event
            time.sleep(wait)
            send_notification(f"Study Reminder: {plan['test_name']}", f"Time to study Chapter {it['chapter']} ({it['duration_hours']} hrs)")
    except KeyboardInterrupt:
        print("Stopped reminders by user.")


def main():
    parser = argparse.ArgumentParser(description='Study reminder and timetable generator')
    parser.add_argument('--test', required=False, help='Test/Quiz name')
    parser.add_argument('--chapters', required=False, type=int, help='Number of chapters')
    parser.add_argument('--days', required=False, type=int, help='Days left')
    parser.add_argument('--hours', required=False, type=float, help='Hours per day')
    parser.add_argument('--start-hour', required=False, type=int, default=18, help='Preferred start hour (0-23)')
    parser.add_argument('--save', action='store_true', help='Save plan to study_plan.json')
    parser.add_argument('--run-reminders', action='store_true', help='Run reminders now (requires notify-send)')

    args = parser.parse_args()

    if not (args.test and args.chapters and args.days and args.hours):
        # interactive
        test = args.test or input('Test/Quiz name: ').strip()
        chapters = args.chapters or int(input('Number of chapters: ').strip())
        days = args.days or int(input('Days left: ').strip())
        hours = args.hours or float(input('Hours per day: ').strip())
    else:
        test = args.test
        chapters = args.chapters
        days = args.days
        hours = args.hours

    plan = build_plan(test, chapters, days, hours, start_hour=args.start_hour)
    print_plan(plan)
    if args.save:
        save_plan(plan)
    if args.run_reminders:
        run_reminders(plan)


if __name__ == '__main__':
    main()

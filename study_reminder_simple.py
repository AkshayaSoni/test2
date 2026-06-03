#!/usr/bin/env python3
from datetime import datetime, timedelta
import json


def build_simple_plan(test_name, chapters, days, hours_per_day):
    chapters = int(chapters)
    days = int(days)
    hours_per_day = float(hours_per_day)

    base = chapters // days if days > 0 else 0
    rem = chapters % days if days > 0 else 0
    plan = []
    chap = 1
    hours_per_chapter = (hours_per_day * days) / chapters if chapters > 0 else 0

    for d in range(days):
        count = base + (1 if d < rem else 0)
        date = (datetime.now().date() + timedelta(days=d)).isoformat()
        day_entry = {"day": d + 1, "date": date, "sessions": []}
        for i in range(count):
            day_entry["sessions"].append({"chapter": chap, "hours": round(hours_per_chapter, 2)})
            chap += 1
        plan.append(day_entry)

    return {
        "test_name": test_name,
        "chapters": chapters,
        "days": days,
        "hours_per_day": hours_per_day,
        "plan": plan,
    }


def print_simple_plan(plan):
    print(f"Study plan for: {plan['test_name']}")
    print(f"Total chapters: {plan['chapters']} — {plan['days']} days — {plan['hours_per_day']} hrs/day")
    print()
    for day in plan['plan']:
        print(f"Day {day['day']} ({day['date']}):")
        if not day['sessions']:
            print("  Rest day")
        for s in day['sessions']:
            print(f"  Chapter {s['chapter']} — {s['hours']} hrs")
        print()


def main():
    # simple interactive inputs
    test = input('Test/Quiz name: ').strip()
    chapters = int(input('Number of chapters: ').strip())
    days = int(input('Days left: ').strip())
    hours = float(input('Hours per day: ').strip())

    plan = build_simple_plan(test, chapters, days, hours)
    print_simple_plan(plan)

    # also print JSON for backend consumption
    print('\nJSON output:')
    print(json.dumps(plan, indent=2))


if __name__ == '__main__':
    main()

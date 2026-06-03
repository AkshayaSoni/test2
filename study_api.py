from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)


def build_plan(test_name, chapters, days, hours_per_day, start_hour=18):
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
        sessions = []
        for i in range(count):
            sessions.append({"chapter": chap, "hours": round(hours_per_chapter, 2), "date": date, "start_hour": start_hour})
            chap += 1
        plan.append({"day": d + 1, "date": date, "sessions": sessions})

    return {
        "test_name": test_name,
        "chapters": chapters,
        "days": days,
        "hours_per_day": hours_per_day,
        "plan": plan,
    }


@app.route('/now', methods=['GET'])
def now():
    return jsonify({"now": datetime.now().isoformat()})


@app.route('/plan', methods=['POST'])
def plan():
    data = request.get_json() or {}
    test = data.get('test')
    chapters = data.get('chapters')
    days = data.get('days')
    hours = data.get('hours')
    start_hour = data.get('start_hour', 18)

    if not all([test, chapters, days, hours]):
        return jsonify({"error": "missing fields: required fields are test, chapters, days, hours"}), 400

    try:
        plan = build_plan(test, chapters, days, hours, start_hour=start_hour)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    return jsonify(plan)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

document.querySelector('form').addEventListener('submit', function(e) {
    e.preventDefault();

    // Ask for permission the second they hit Generate
    if ("Notification" in window) {
        Notification.requestPermission();
    }

    // Grab all inputs from the HTML form
    const name = document.querySelector('input[name="name"]').value;
    const testName = document.querySelector('input[name="user_test_name"]').value;
    const totalChapters = parseInt(document.querySelector('input[name="number_chapter"]').value) || 0;
    const daysLeft = parseInt(document.querySelector('input[name="how_manydays"]').value) || 1;
    const hoursPerDay = parseFloat(document.querySelector('input[name="hours_per_day"]').value) || 0;
    const timeMethod = document.querySelector('select[name="time_method"]').value;

    // --- 🚨 PYTHON AM/PM LOGIC TRANSLATED TO JS 🚨 ---
    let rawStartingHour = parseInt(document.querySelector('input[name="starting_time"]').value) || 6;
    const startingPeriod = document.querySelector('select[name="starting_period"]').value;
    
    let startingHour = rawStartingHour;
    if (startingPeriod === "am") {
        if (startingHour === 12) {
            startingHour = 0; // Midnight
        }
    } else {
        if (startingHour !== 12) {
            startingHour += 12; // Convert PM to 24-hour clock for the math
        }
    }
    // --------------------------------------------------

    const safeDaysLeft = daysLeft <= 0 ? 1 : daysLeft;
    const baseChaptersPerDay = Math.floor(totalChapters / safeDaysLeft);
    const extraChapters = totalChapters % safeDaysLeft;
    
    let currentChapter = 1;
    let scheduledAlarmsCount = 0;

    let tableHTML = `
        <h2 style="text-align: center; margin-top: 40px; color: #a855f7; font-size: 1.5rem; font-weight: 700;">
            🗓️ Schedule for ${testName} (${name})
        </h2>
        <table style="width: 100%; border-collapse: collapse; margin-top: 20px; background: rgba(15, 23, 42, 0.6); border-radius: 16px; overflow: hidden; border: 1px solid rgba(255, 255, 255, 0.1);">
            <thead>
                <tr style="background: linear-gradient(90deg, #6366f1, #a855f7); color: white;">
                    <th style="padding: 16px; text-align: left; font-size: 0.9rem; text-transform: uppercase;">Timeline</th>
                    <th style="padding: 16px; text-align: left; font-size: 0.9rem; text-transform: uppercase;">Study Window</th>
                    <th style="padding: 16px; text-align: left; font-size: 0.9rem; text-transform: uppercase;">Target</th>
                </tr>
            </thead>
            <tbody>
    `;

    for (let dayIndex = 0; dayIndex < safeDaysLeft; dayIndex++) {
        let chaptersToday = baseChaptersPerDay + (dayIndex < extraChapters ? 1 : 0);
        
        let currentDate = new Date();
        currentDate.setDate(currentDate.getDate() + dayIndex);
        let dateString = currentDate.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });

        tableHTML += `<tr style="border-bottom: 1px solid rgba(255, 255, 255, 0.05);"><td style="padding: 16px; font-weight: 700; color: #94a3b8;">Day ${dayIndex + 1} <span style="font-weight: 400; font-size: 0.85rem; display: block; color: #64748b;">(${dateString})</span></td>`;

        if (chaptersToday === 0) {
            tableHTML += `<td style="padding: 16px; color: #64748b;">-- : --</td><td style="padding: 16px; color: #64748b; font-style: italic;">Rest Day 😴</td></tr>`;
            continue;
        }

        let studyHoursPerChapter = hoursPerDay / chaptersToday;
        let timeSlotsHTML = "";
        let chapterTargetsHTML = "";

        for (let sessionIndex = 0; sessionIndex < chaptersToday; sessionIndex++) {
            let startTime = new Date();
            startTime.setDate(startTime.getDate() + dayIndex);
            startTime.setHours(startingHour, 0, 0, 0);
            startTime.setMinutes(startTime.getMinutes() + (sessionIndex * studyHoursPerChapter * 60));
            
            let endTime = new Date(startTime.getTime());
            endTime.setMinutes(endTime.getMinutes() + (studyHoursPerChapter * 60));

            let clockFormat = timeMethod === "12" 
                ? { hour: 'numeric', minute: '2-digit', hour12: true }
                : { hour: '2-digit', minute: '2-digit', hour12: false };

            let startStr = startTime.toLocaleTimeString('en-US', clockFormat);
            let endStr = endTime.toLocaleTimeString('en-US', clockFormat);

            let timeUntilStudy = startTime.getTime() - Date.now();

            if (timeUntilStudy > 0) {
                scheduledAlarmsCount++;
                
                setTimeout(() => {
                    if (Notification.permission === "granted") {
                        new Notification("🔥 Time to Lock In!", {
                            body: `${name} okay and lock in study time is going to be ${startStr} to ${endStr} okay for your test - ${testName}`,
                            icon: "https://cdnjs.cloudflare.com/ajax/libs/twemoji/14.0.2/72x72/1f4da.png"
                        });
                    }
                }, timeUntilStudy);
            }

            timeSlotsHTML += `<div style="margin-bottom: 8px; color: #6366f1; font-weight: 600;">${startStr} - ${endStr}</div>`;
            chapterTargetsHTML += `<div style="margin-bottom: 8px; color: #f8fafc;">Chapter ${currentChapter}</div>`;
            
            currentChapter++;
        }

        tableHTML += `<td style="padding: 16px; vertical-align: top;">${timeSlotsHTML}</td><td style="padding: 16px; vertical-align: top;">${chapterTargetsHTML}</td></tr>`;
    }

    tableHTML += `</tbody></table>`;

    document.getElementById('timetable-output').innerHTML = tableHTML;
    
    if (Notification.permission === "granted" && scheduledAlarmsCount > 0) {
        new Notification(`✅ ${name}, lock in for your test: ${testName}!`, {
            body: `Your schedule is calculated! ${scheduledAlarmsCount} alarms have been queued up for your study sessions. Leave this tab open!`
        });
    }
});
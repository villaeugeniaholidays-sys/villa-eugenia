#!/usr/bin/env python3
"""Fetch the private Airbnb iCal feed and write data/availability.json.

The iCal URL is read from the AIRBNB_ICAL_URL environment variable
(set as a GitHub Actions secret so it never appears in the repository).
Airbnb's export contains one VEVENT per reserved/blocked period; every
date covered by an event is marked as booked. DTEND is exclusive
(check-out day), matching how a calendar should display availability.
"""
import json
import os
import re
import sys
import urllib.request
from datetime import date, datetime, timedelta

url = os.environ.get("AIRBNB_ICAL_URL", "").strip()
if not url:
    print("AIRBNB_ICAL_URL secret is not set — skipping sync.")
    sys.exit(0)

req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (calendar-sync)"})
ics = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")

# Unfold folded iCal lines (RFC 5545)
ics = ics.replace("\r\n", "\n").replace("\n ", "").replace("\n\t", "")

booked = set()
for block in re.findall(r"BEGIN:VEVENT(.*?)END:VEVENT", ics, re.S):
    m_start = re.search(r"DTSTART(?:;VALUE=DATE)?[^:]*:(\d{8})", block)
    m_end = re.search(r"DTEND(?:;VALUE=DATE)?[^:]*:(\d{8})", block)
    if not (m_start and m_end):
        continue
    d = datetime.strptime(m_start.group(1), "%Y%m%d").date()
    end = datetime.strptime(m_end.group(1), "%Y%m%d").date()  # exclusive
    while d < end:
        booked.add(d.isoformat())
        d += timedelta(days=1)

# Keep the file small: only today onwards, max 18 months ahead
today = date.today()
horizon = today + timedelta(days=550)
booked = sorted(d for d in booked if today.isoformat() <= d <= horizon.isoformat())

out = {"updated": datetime.utcnow().isoformat(timespec="seconds") + "Z", "booked": booked}
os.makedirs("data", exist_ok=True)
with open("data/availability.json", "w") as f:
    json.dump(out, f, indent=2)
print(f"Wrote {len(booked)} booked dates.")

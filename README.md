# Villa Eugenia — Website

A bilingual (EN/IT) single-page website for the beachside villa in Santa Margherita di Pula, Sardinia.

## What's inside

| Path | Purpose |
|---|---|
| `index.html` | The whole website (design, gallery, calendar, form, EN/IT) |
| `photos/` | 27 optimized photos (from the professional shoot) |
| `data/availability.json` | Booked dates shown on the calendar (auto-updated) |
| `data/reviews.json` | Optional review quotes — paste real Airbnb reviews here |
| `scripts/sync_ical.py` | Converts the Airbnb iCal feed into `availability.json` |
| `.github/workflows/sync-calendar.yml` | Runs the sync every 6 hours on GitHub |

## Deploy on GitHub Pages (free) — one-time setup

1. Create a free account at github.com (if you don't have one).
2. Create a new **public** repository, e.g. `villa-la-perla`.
3. Upload the entire contents of this folder to the repository
   (drag & drop works: "uploading an existing file" link on the repo page —
   make sure the hidden `.github` folder is included; using `git push` is safer).
4. Repo → **Settings → Pages** → Source: `Deploy from a branch` → Branch: `main`, folder `/ (root)` → Save.
5. After ~2 minutes the site is live at `https://<your-username>.github.io/villa-la-perla/`.

### Connect the Airbnb availability sync

1. Airbnb → Listings → your listing → **Calendar → Availability → Connect to another website → Copy the export link** (a URL ending in `.ics`).
2. GitHub repo → **Settings → Secrets and variables → Actions → New repository secret**
   - Name: `AIRBNB_ICAL_URL`
   - Value: the copied `.ics` link
3. Repo → **Actions** tab → "Sync Airbnb availability" → **Run workflow** (first run; afterwards it runs every 6 hours automatically).

> Keep the iCal link secret — anyone who has it can read your booking dates.

### Enquiry form

The form posts to FormSubmit (free) and delivers to **villaeugeniaholidays@gmail.com**.
The **first** submission triggers a confirmation email from formsubmit.co —
click the activation link in it once, and all future enquiries arrive normally.

### Custom domain (optional, later)

Buy a domain (e.g. `villalaperlasardinia.com`), then in the repo:
Settings → Pages → Custom domain, and point the domain's DNS
(CNAME → `<your-username>.github.io`) at GitHub. HTTPS is automatic.

## Editing content

- Text lives in `index.html` — English inline, Italian in the `I18N.it` dictionary in the `<script>` at the bottom.
- To add/remove photos: put the file in `photos/` and edit the `PHOTOS` list in the script.
- To show review quotes: edit `data/reviews.json`, e.g.

```json
{
  "reviews": [
    {"name": "Anna", "date": "July 2026", "text": "Wonderful villa, steps from the beach!"}
  ]
}
```

## Registration

Italian national registration code (CIN) `IT092050C2000S2986` is displayed in the footer, as required for short-term rental advertising.

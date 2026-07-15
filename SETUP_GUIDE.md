# Project Borderlands Dashboard — Setup Guide & Fellowship Checklist Mapping

## What's in this folder

| File | What it is |
|---|---|
| `raw_coalition_contacts.csv` | Real, messy source data pulled from the Project Borderlands proposal (inconsistent "Local?" values, blank fields, free-text tags). |
| `clean_merge_data.py` | Python script that cleans that raw data and merges it with a second structured data source (founding members, partner orgs, Learning Lab concepts, locations, goals). |
| `borderlands_data.json` | The output of the script — one clean dataset the dashboard reads. |
| `index.html` | The dashboard itself — a single self-contained web page. |
| `SETUP_GUIDE.md` | This file. |

## How to run it locally

1. Open a terminal in this folder.
2. (Optional — only if you change the CSV) Regenerate the dataset:
   ```
   python3 clean_merge_data.py
   ```
3. Start a local server (browsers block `fetch()` of local JSON files opened directly from disk):
   ```
   python3 -m http.server 8000
   ```
4. Open `http://localhost:8000` in your browser.

## How to deploy it as a real, live website

Any static host works since it's plain HTML/JS with no build step:

- **GitHub Pages** (free): push this folder to a GitHub repo, enable Pages in repo settings, pointing at the root. You'll get a URL like `https://yourname.github.io/project-borderlands-dashboard`.
- **Netlify / Vercel** (free): drag-and-drop the folder in their dashboard, or connect the GitHub repo.

Once deployed, that URL *is* your "simple website or web page" deliverable — you can link it directly in the application.

## Connecting the Google Form → Sheet → Dashboard workflow (~5 minutes)

This is the "workflow that connects two tools" piece — a real form that populates a sheet, which the dashboard reads live. It also powers the **Physical Space** tab's "Vote on a date/time & commit to a role" card, where viewers pick which dates work and sign up for a role (setup, food, photography, translation, outreach, cleanup) for an upcoming Learning Lab.

1. Create a **Google Form** titled something like "Project Borderlands — Learning Lab Interest," with fields like Name, Email, Which Learning Lab this is for, date/time options (checkboxes), and Role you can help with (setup / food / photography / translation / outreach / cleanup).
2. In the Form's **Responses** tab, click the Sheets icon to create a linked **Google Sheet**.
3. In that Sheet: **File → Share → Publish to web**. Choose the response sheet/tab, format **CSV**, click **Publish**. Copy the URL it gives you.
4. Open `index.html`, find these lines near the top of the `<script>` block:
   ```js
   const SHEET_CSV_URL = "";
   const LEARNING_LAB_FORM_URL = "";
   ```
   Paste your published CSV URL into `SHEET_CSV_URL`. For `LEARNING_LAB_FORM_URL`, take your Google Form's normal share link (ends in `/viewform`) and change it to end in `/viewform?embedded=true` — that embeds the actual fillable form on the page.
5. Reload the dashboard:
   - **Physical Space → "Vote on a date/time & commit to a role"** now shows the live, embedded form itself.
   - **Physical Space → "Learning Lab sign-up interest"** now shows a live count pulled straight from form submissions.

## Connecting real social + email links

On the **Digital Space** tab, the "Connect with us" card is config-driven. Near the top of the `<script>` block:
```js
const SOCIAL_LINKS = {
  TikTok: "",
  Instagram: "",
  Facebook: "",
  YouTube: "",
  Email: "mailto:gabiperez1115@gmail.com",
};
```
Fill in each platform URL once real accounts exist. Until then, each shows as "(not connected)" rather than a broken/fake link. Email is already live.

## Using the Claude chat assistant

Go to the **Ask Borderlands AI** tab, paste an Anthropic API key (from console.anthropic.com), and ask it something like *"Draft a 90-minute outline for the Intergenerational Cooking Circle Learning Lab."* It calls the real Claude API directly from the browser — the key stays in page memory only for that session and is never saved or transmitted anywhere else. For a production version, that call would go through a small backend instead of straight from the browser, to avoid exposing the key at all — noted in the on-page disclaimer too.

## How this maps to the fellowship application checkboxes

| Checkbox | Where it lives |
|---|---|
| **A script that cleans, merges, or analyzes data** | `clean_merge_data.py` — cleans the messy raw coalition contact data (normalizes "Yes?" / "Maybe - PNW?" / "No - Montana" into structured status + region fields, extracts hashtags, categorizes discovery channels) and merges it with a second structured data source (founders, orgs, Learning Lab concepts) into `borderlands_data.json`. |
| **A dashboard or data visualization** | `index.html` — hand-built, dependency-free HTML/CSS bar charts across all three spaces (discovery channels, skills/roles, locality breakdown), plus stat cards, a sample content-performance table, and a map. (No charting library — this removes an external CDN as a point of failure.) |
| **A simple website or web page** | `index.html` itself, deployable as a live URL via GitHub Pages/Netlify (see above). |
| **A workflow that connects two tools** | Google Form → Google Sheet → dashboard fetch, described above. Once `SHEET_CSV_URL` is set, form submissions show up live on the Physical Space tab with no manual step in between. |
| **Something that uses an API** | Two real API integrations: Open-Meteo (live weather for Learning Lab planning, no key required) and the Anthropic Claude API (chat assistant). |
| **A chatbot or tool that uses Claude / another LLM** | The "Ask Borderlands AI" tab — a real, working call to the Claude Messages API scoped with a system prompt specific to the project. |
| **Something else** | The interactive Leaflet map of Learning Lab and partner locations across the Salish Sea, tying the "Physical Space" concept to an actual geographic visualization. |

## A note on the data

The **partner orgs, founding members, Learning Lab concepts, and goals** are real, taken directly from the Project Borderlands proposal document. The **7 sample coalition contacts** shown in the Coalition Space table are intentionally **placeholder entries named after native Pacific Northwest flora and fauna** (Cedar Raven, Chinook Rising, Osprey Wing, Huckleberry Moon, Sword Fern Walker, Salal Bloom, Madrona Grove) — they exist only to demonstrate how the cleaning/merging script works on realistically messy input, not to represent real people. The dashboard states the coalition's actual current size (40 members) separately from that sample table, and the app is explicit in-page (banners on the Digital and Coalition tabs) that these are placeholder/demo entries. The "sample content performance" numbers on the Digital tab are filler too, clearly labeled as such. Worth saying plainly if asked in an interview: this is a working mockup with placeholder data standing in for real numbers, not a claim that the program already has this data.

<h1>Project Borderlands — Community Dashboard</h1>
<p><strong>A demo project built for my Claude Corps Fellowship application.</strong></p>
<p>
Hi — I'm Gabi Perez. This repo is a working mockup of a community dashboard for
<a href="#what-project-borderlands-is">Project Borderlands</a>, a social impact
initiative I founded. I'm sharing it with the Anthropic team as part of my
fellowship application.
</p>
<hr>
<h2 id="what-project-borderlands-is">What Project Borderlands is</h2>
<p>
Project Borderlands is a digital storytelling and community media initiative I
founded, working alongside Indigenous and non-Indigenous collaborators in the
Salish Sea region of Washington. It moves through three connected spaces:
</p>
<ul>
  <li><strong>Physical</strong> — Learning Labs, where communities gather in person</li>
  <li><strong>Digital</strong> — short-form storytelling shared online</li>
  <li><strong>Coalition</strong> — the network of people who keep the work alive between gatherings</li>
</ul>
<p>
The full proposal — the thinking, the research, the people involved — is
attached separately as a PDF alongside my application.
</p>
<h2>What this dashboard is</h2>
<p>
When I first sketched out Project Borderlands, I drew the three spaces as a
cycle: what happens on the land feeds the stories that go online, and what
grows online should be able to pull people back into the room. That diagram
is in the original proposal. This dashboard is the first real attempt at
actually building that — a working page where you can see all three spaces
at once, instead of just describing how they're supposed to connect.
</p>
<p>
It's a demo, not a finished product. Some of what's in it is real, pulled
straight from the proposal: the founding coalition, the local partner
organizations, the Learning Lab concepts, the project's goals. Some of it is
placeholder data, clearly labeled as such in the app itself — a sample set
of coalition contacts named after native Pacific Northwest flora and fauna
(Cedar Raven, Salal Bloom, and so on) standing in for a future real roster,
and a few made-up content performance numbers standing in for analytics
that don't exist yet because nothing has launched. I built it this way on
purpose: I wanted to show what the tool would look like and how it would
work, without pretending the program is further along than it is.
</p>
<h2>The honest part</h2>
<p>
This is quite literally what I had in mind when I first started working on
Project Borderlands — a way to hold the physical, digital, and coalition
work in one place instead of scattered across a proposal doc, a Google
Drive, and my own head. I didn't have the technical background to build it
back then. Working through this with Claude is what closed that gap: I went
from a diagram on a page to something you can actually click through, in
about as long as it would've taken me to just describe the idea to someone
else. If I'd had this kind of tool when I was first drafting the project, I
think it would have moved a lot faster and a lot further. That's a real
part of why I'm applying — I want to keep having that kind of leverage, and
I want to help build it for other people doing this kind of work too.
</p>
<h2>Quick start</h2>
<pre><code># clone the repo, then from inside it:
python3 clean_merge_data.py       # (optional) regenerate borderlands_data.json
python3 -m http.server 8000       # serve the folder locally
</code></pre>
<p>Then open <code>http://localhost:8000</code> in your browser.</p>
<p>
For deploying it as a live URL (GitHub Pages, Netlify) and connecting the
Google Form/Sheet and Claude chat pieces, see
<a href="./SETUP_GUIDE.md"><code>SETUP_GUIDE.md</code></a>.
</p>
<h2>What's in this repo</h2>
<table>
  <thead>
    <tr>
      <th>File</th>
      <th>What it is</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><a href="./index.html"><code>index.html</code></a></td>
      <td>The dashboard itself — Physical, Digital, and Coalition space views, a live weather feed, and a Claude-powered chat assistant.</td>
    </tr>
    <tr>
      <td><a href="./clean_merge_data.py"><code>clean_merge_data.py</code></a></td>
      <td>The script that cleans a messy raw contact list and merges it with the project's structured program data into one dataset.</td>
    </tr>
    <tr>
      <td><a href="./raw_coalition_contacts.csv"><code>raw_coalition_contacts.csv</code></a></td>
      <td>The raw, intentionally messy input to that script.</td>
    </tr>
    <tr>
      <td><a href="./borderlands_data.json"><code>borderlands_data.json</code></a></td>
      <td>The script's output — what the dashboard actually reads.</td>
    </tr>
    <tr>
      <td><a href="./SETUP_GUIDE.md"><code>SETUP_GUIDE.md</code></a></td>
      <td>How to run it, deploy it, and connect the live Google Form/Sheet and Claude chat pieces. Also maps each part of this project to the fellowship's technical checklist.</td>
    </tr>
  </tbody>
</table>
<hr>
<p>Thanks for taking the time to look at this.</p>
<p>— Gabi</p>

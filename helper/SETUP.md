# Set up the museum's lookup helper (free, about 10 minutes)

Metron (comics) and BoardGameGeek (board games) block web pages from talking to them directly.
This helper runs on Cloudflare's free plan, adds your API tokens, and passes results back to the museum.
Your Metron and BGG tokens are stored as Cloudflare secrets, not on your phone.

1. **Create a free Cloudflare account** at https://dash.cloudflare.com/sign-up (skip adding a website).
2. In the dashboard, go to **Workers & Pages → Create → Create Worker** (start from "Hello World").
   Name it `museum-helper` and click **Deploy**.
3. Click **Edit code**, delete everything in `worker.js`, paste the contents of
   [`worker.js`](worker.js) from this folder, then click **Deploy**.
4. Go back to the worker → **Settings → Variables and Secrets** and add:
   | Name | Type | Value |
   |---|---|---|
   | `METRON_TOKEN` | Secret | your Metron API token (Metron account page → generate API token) |
   | `BGG_TOKEN` | Secret | your BoardGameGeek token (skip until BGG approves you) |
   | `ALLOWED_ORIGIN` | Text | `https://erictheblair.github.io` (add your own domain later, comma separated) |
   Click **Deploy** / **Save** after adding them.
5. Copy the worker's address (looks like `https://museum-helper.yourname.workers.dev`).
6. In the museum: **⚙︎ Settings → Lookups → Lookup helper**, paste the address, tap **Test**, then **Save lookup settings**.

The helper only answers requests coming from your museum's address. Cloudflare's free plan allows
100,000 requests a day, far more than a collection needs.

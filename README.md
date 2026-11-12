# The Collection: a private museum for your collections

A small web app (no server, no database). The app files hold none of your data.
Your catalog (`catalog.json`) and every photo and COA scan live in your own Dropbox,
in `Dropbox/Apps/<your app name>/`. Sign in with Dropbox on each device.

## Put it online (free, about 5 minutes)
Pick one:
- **GitHub Pages:** create an empty repository, upload these files, then Settings → Pages →
  "Deploy from a branch" → `main` / root. Your address will be `https://<you>.github.io/<repo>/`.
- **Netlify Drop:** sign in at app.netlify.com/drop and drag this folder onto the page.
- **Cloudflare Pages:** Workers & Pages → Create → Pages → Upload assets → drop this folder.

## Connect Dropbox (one time)
1. dropbox.com/developers/apps/create → Scoped access → App folder → name it (e.g. "Eric Museum").
2. Permissions tab: tick `files.content.write` and `files.content.read`, then Submit.
3. Settings tab → Redirect URIs: add your site's exact address (e.g. `https://you.github.io/museum/`).
   The app's Settings page shows the exact address to paste.
4. Open the site → ⚙︎ Settings → paste the App key → Connect Dropbox. Repeat the sign-in on your phone.
5. On your phone: Share → Add to Home Screen.

You can also try it without Dropbox: it saves on that device only until you connect.

## Privacy
- Private mode (Settings) hides prices, values, serial numbers and cert numbers,
  so you can hand someone your phone.
- The app can only see its own folder in your Dropbox, nothing else.
- Back up anytime from Settings (CSV spreadsheet or JSON). Photos are already in Dropbox.

## Barcode scanning & lookups
Tap **▦ Scan** to scan a UPC/EAN/ISBN with your phone camera (or type the number).
Lookups use free public sources: Open Library (books), MusicBrainz + Cover Art Archive (records),
Wikidata (movie/laserdisc director, year, runtime, cast), and UPCitemdb (general products, limited free daily lookups).
Optional: add a free Discogs token in Settings for better record and laserdisc matches.
For older items without barcodes, type the title and press **🔎 Look up**.
Use **More details** on any piece for your own label/value pairs (edition number, variant, signed by…).
Barcode scanning uses ZXing (Apache-2.0), bundled in `vendor/`.

## Gallery mode
Open any collection and choose Gallery mode to walk a hall of framed pieces. Pick a room
(50s diner, aquarium, cabin, castle, Christmas, greenhouse, haunted mansion, library, modern,
museum, neon arcade, starship), press ▶ Tour to let it play, or ⛶ (or F) for full screen on a computer.
Room artwork lives in `rooms/`.

## Quick edit
On a computer, hover over a piece in a collection and click ✎ to edit its details without leaving the page.

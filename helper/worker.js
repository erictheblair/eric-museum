// Museum lookup helper — a tiny Cloudflare Worker.
// Metron and BoardGameGeek don't allow web pages to call them directly, so the museum
// asks this helper, which adds your login/token (stored as Cloudflare secrets) and passes
// the answer back. It only answers requests coming from your museum's address.

export default {
  async fetch(request, env) {
    const allowed = (env.ALLOWED_ORIGIN || "https://erictheblair.github.io")
      .split(",").map(s => s.trim().replace(/\/+$/, ""));
    const origin = request.headers.get("Origin") || "";
    const cors = {
      "Access-Control-Allow-Origin": allowed.includes(origin) ? origin : allowed[0],
      "Access-Control-Allow-Methods": "GET, OPTIONS",
      "Access-Control-Allow-Headers": "*",
      "Vary": "Origin",
    };
    if (request.method === "OPTIONS") return new Response(null, { headers: cors });
    if (request.method !== "GET") return new Response("Method not allowed", { status: 405, headers: cors });
    if (!allowed.includes(origin)) return new Response("Forbidden", { status: 403, headers: cors });

    const url = new URL(request.url);
    const headers = { "User-Agent": "MuseumLookupHelper/1.0" };
    let target;
    if (url.pathname.startsWith("/metron/")) {
      if (!env.METRON_USER || !env.METRON_PASS) return new Response("Metron login not set", { status: 401, headers: cors });
      target = "https://metron.cloud/api/" + url.pathname.slice("/metron/".length) + url.search;
      headers.Authorization = "Basic " + btoa(env.METRON_USER + ":" + env.METRON_PASS);
      headers.Accept = "application/json";
    } else if (url.pathname.startsWith("/bgg/")) {
      if (!env.BGG_TOKEN) return new Response("BGG token not set", { status: 401, headers: cors });
      target = "https://boardgamegeek.com/xmlapi2/" + url.pathname.slice("/bgg/".length) + url.search;
      headers.Authorization = "Bearer " + env.BGG_TOKEN;
    } else {
      return new Response("Museum lookup helper is running.", { status: 200, headers: cors });
    }

    const upstream = await fetch(target, { headers, cf: { cacheTtl: 3600, cacheEverything: true } });
    const out = new Response(upstream.body, { status: upstream.status, headers: cors });
    out.headers.set("Content-Type", upstream.headers.get("Content-Type") || "application/octet-stream");
    return out;
  },
};

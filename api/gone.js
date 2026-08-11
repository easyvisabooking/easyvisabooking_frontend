// Returns 410 Gone for permanently retired URLs.
//
// Why a function: this is an otherwise fully static deployment, and vercel.json
// can express 3xx redirects and rewrites but not a 410 status. Google treats 410
// as a permanent removal signal and retires the URL faster than a repeatedly
// re-queued 404.
//
// Wired up via the "rewrites" entries in vercel.json. To revert to plain 404s,
// delete this file and those rewrite entries.

module.exports = function handler(req, res) {
  res.statusCode = 410;
  res.setHeader('Content-Type', 'text/html; charset=utf-8');
  res.setHeader('Cache-Control', 'public, max-age=0, s-maxage=86400');
  res.setHeader('X-Robots-Tag', 'noindex');
  res.end(
    '<!doctype html><html lang="en"><head><meta charset="utf-8">' +
      '<meta name="viewport" content="width=device-width, initial-scale=1">' +
      '<meta name="robots" content="noindex">' +
      '<title>Page Removed | Easy Visa Booking</title></head>' +
      '<body style="font-family:system-ui,sans-serif;max-width:36rem;margin:15vh auto;padding:0 1.5rem">' +
      '<h1>This page has been removed</h1>' +
      '<p>We no longer offer US visa appointment assistance for this location, ' +
      'and this page will not be coming back.</p>' +
      '<p><a href="/services/">See the locations we do serve</a> or ' +
      '<a href="/contact/">contact us</a>.</p>' +
      '</body></html>'
  );
};

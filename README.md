# kc_archive
TO-DO's:
* Clean up the terrible-looking frontend, especially on the landing page
* Do-not-archive feature (which turns out is not "ghostposting") ✔ Done. Went with option two using [b][/b]
   * Option one: check the subject field; if it equals to some value, replace message with "[not archived]"
   * Option two: check the last n characters of the message field; if it equals to some value, replace message with "[not archived]"
* Add a live link to kohlchan in thread.html; if expired, don't
* Add a live link to uploads on kohlchan; if expired, keep the assburger.jpg (requires database rework)
* Add a response-watching service, preferably through persistent cookies: if user receives a response, notify them through some medium
* Add a page that lists n amount of the newest threads archived, with a part of their respective OP posts next to them. Example:
    * thread 123456: [countryball] [date] "[post body text stripped of html]"
    * thread 123457: [countryball] [date] "[post body text stripped of html]"
    * etc

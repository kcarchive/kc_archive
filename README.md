# kc_archive
TO-DO's:
* Clean up the terrible-looking frontend, especially on the landing page ✔ Done. Thank you BR Bernd :3
    * Some other things I'd like to do on the front end:
        * Learn some jQuery wizardry and add countryball images in the "countries" option menu
        * Use a single field for date fields (I would prefer not to bother the back-end with this, if possible)
        * Figure out a better way to display search results
        * Somehow make every page mobile-friendly
        * Figure out the best way to prevent double form submission from client's side
* Do-not-archive feature (which turns out is not "ghostposting") ✔ Done. Went with option two using [b][/b]
   * Option one: check the subject field; if it equals to some value, replace message with "[not archived]"
   * Option two: check the last n characters of the message field; if it equals to some value, replace message with "[not archived]"
* Add a live link to kohlchan in thread.html ✔ Done.
* Add a live link to uploads on kohlchan; if expired, keep the assburger.jpg (requires database rework)
* Add a response-watching service, preferably through persistent cookies: if user receives a response, notify them through some medium
* Add a page that lists n amount of the newest threads archived, with a part of their respective OP posts next to them. Example: ✔ Done.
    * thread 123456: [countryball] [date] "[post body text stripped of html]"
    * thread 123457: [countryball] [date] "[post body text stripped of html]"
    * etc
* Implement an image-archiving service that saves only sized-down thumbnails of said images
* Show replies next to the cursor when mouseovering anchors, like on kc
* Create a separate page for statiscics such as:
    * Posts per hour by countryball
    * Amount of posts that contain certain keywords given by the user graphed with time, country and frequency
    * Total archived posts, total archived threads, etc
* Write a mysql function to strip post bodies of html tags (currently, if you search /int/ every post with >>#### comes up)

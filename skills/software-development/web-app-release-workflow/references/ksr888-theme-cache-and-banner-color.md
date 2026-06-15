# KSR888 theme cache, luxury CSS, and banner color notes

Session takeaway:
- KSR888 desktop/mobile theme changes can be masked by browser/CDN cache even when the container is rebuilt successfully.
- To force a visible UI delta, update the stylesheet href with a new query string and, when needed, switch to a new CSS filename (for example `*.luxury.css`) so the browser cannot reuse a stale asset path.
- For banner/carousel color fixes, avoid global image filters that apply to all `img`, `video`, or `svg` elements. Add a more specific override for `.banner img`, `.banner-carousel img`, `.banner-carousel .item img`, and `.banner-carousel .carousel-inner img` so banners stay fully colored.
- When checking whether the live page actually picked up the new theme, probe the exact public CSS URL and the rendered HTML, then verify the stylesheet link in the HTML contains the newest version tag.
- If the live page still looks unchanged after deploy, create a new cache-busted CSS filename and update the HTML reference instead of only changing the query string.

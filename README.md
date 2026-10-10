BW ATM Finder — 3D interactive globe
This version replaces the Leaflet 2D map with a rotatable 3D Earth globe using Globe.gl.
Repository structure
Keep the existing ATM data file and use this structure:
index.html
README.md
data/botswana_atms.json
The page expects the JSON file at ./data/botswana_atms.json. Each record should include fields such as atm_name, bank, town, address, landmark, latitude, longitude, services, and verification_status.
Publish with GitHub Pages
Upload/replace index.html in your repository.
Keep your existing data/botswana_atms.json in a folder named data.
Commit changes to the main branch.
If GitHub Pages is already enabled, wait for deployment and refresh the published site.
Important
Globe.gl, Three.js dependencies and Earth textures load from public CDNs; an internet connection is required.
Only records with valid latitude and longitude appear as globe pins.
The directory is not automatically verified by this interface. Use verification_status: "verified" only when the ATM has actually been checked against a trustworthy source.
ATM coordinates, bank names, address strings and service claims should be checked before public use.
Device location requires browser permission and a secure context such as GitHub Pages HTTPS.

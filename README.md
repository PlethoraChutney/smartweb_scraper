# SmartWeb Scraper
Make sure you have beautifulsoup4 installed.

You should be able to download SmartWeb files from OHSU campus
even without a login. While you're saving them, the format isn't
too important, all you need is some kind of unique identifier
at the front of the file. Then run the script and it should just work.

`python scraper.py {prefix} {directory}`

It'll output `{prefix}_names_deps.csv`

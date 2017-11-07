# meetup_scraping

Scraper to scrape contact information for a segment of companies from bundes-telefonbuch.de. Developed as part of a PyData meetup in Munich

## Instructions
1. pip install -r requirements.txt
2. Running the spider in yellowpages/yellowpages

 scrapy crawl telefonbuch -a sector=<your_desired_sector_in_german> -a city=<city> -o <output_file>
 
 Example: scrapy crawl telefonbuch -a sector="Auto" -a city="Muenchen" -o "Auto_Muenchen.csv"

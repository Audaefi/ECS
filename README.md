# ECS (E-Commerce Scraper)

## Project Details

Project Name: ECS

Project Period: 2022-09 ~ Present (Continuing development & operation)

Project Description: Scrapy, Playwright-based Domestic & Overseas Marketplace Scraper

Tag : `Python` `Scrapy` `Playwright` `EC2` `S3`

## Description
Python Scrapy spider that scrapes product data from various marketplaces.

These scrapers extract the following fields from product pages:

- Product URL
- Image URL
- Product Name
- Price
- Seller / Manufacturer Name
Etc.


## Usage

<img width="1217" alt="Screenshot 2022-11-27 at 9 03 30 PM" src="https://user-images.githubusercontent.com/24248797/204138676-63635c3a-48cc-4b71-89b1-8bf116ee80e6.png">

```
- Specify a Marketplace to collect (ESSENTIAL / multiple arguments are possible)

  -t | —target `Marketplace_1` `Marketplace_2` ..
  

- Specify the number of page collections for the specified Marketplace (ESSENTIAL)

  -p | —page `Marketplace_1_pages` `Marketplace_2_pages` ..
  

- Specify a search keyword (ESSENTIAL / multiple arguments are possible)

  -k | —keyword `Keyword_1` `Keyword_2` ..
  

- Enable proxy (default = 'n')

  -x | —proxy `'y' or 'n'`


- Only data including the keyword in the product name can be collected (multiple arguments are possible)

  -i | —include `Include Keyword_1` `Include Keyword_2` ..


- Drop all data including the keyword in the product name (multiple arguments are possible)

  -e | —exclude `Exclude Keyword_1` `Exclude Keyword_2` ..


- The data of all products sold by the 'seller' can be dropped (multiple arguments are possible)

  -a | —auth `Authorised Seller_1` `Authorised Seller_2` ..


- Collect only data on products sold by the 'seller' (multiple arguments are possible)

  -u | —unth `Unauthorised Seller_1` `Unauthorised Seller_2` ..
```

### Example (Basic)
```
python3 main.py -t ssg -p 1 -k macbook
python3 main.py --target ssg --page 1 --keyword macbook
python3 main.py --target ssg gmarket auction --page 1 4 2 --keyword macbook
```

### Example (Advanced)
```
python3 main.py --target ssg gmarket auction --page 1 4 2 --keyword macbook --include air
python3 main.py -k iphone -t amazon gmarket aliexpress -p 1 2 2 -e pro -p y
python3 main.py --target aliexpress alibaba --page 2 2 --keyword pokemon --exclude hoodie -proxy y -auth Shop0014392 
```


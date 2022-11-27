# ECS (E-Commerce Scraper)

## Project Details

Project Name: ECS

Project Period: 2022-09 ~ Present (continuous development & operation)

Project Description: Scrapy, Playwright-based Domestic/Overseas Marketplace Scraper

Tag : `Python` `Scrapy` `Playwright` `EC2` `S3`


## Command-line

<img width="1217" alt="Screenshot 2022-11-27 at 9 03 30 PM" src="https://user-images.githubusercontent.com/24248797/204138676-63635c3a-48cc-4b71-89b1-8bf116ee80e6.png">

- Specify a Marketplace to Collect (essential command / can specify multiple)

  -t | —target `Marketplace_1` `Marketplace_2` ..

- Specify the collection page amount for the specified Marketplaces (essential command / multiple arguments are possible)

  -p | —page `Marketplace_1_pages` `Marketplace_2_pages` ..

- Specifying search keywords (essential command / multiple arguments are possible)

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

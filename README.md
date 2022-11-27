# ECS (E-Commerce Scraper)

## Project Details
`Python` `Scrapy` `Playwright` `EC2` `S3`
Project Name: ECS

Project period: 2022-09 ~ Present (continuous development & operation)

Project Description: Scrapy, Playwright-based Domestic/Overseas Marketplace Scraper


## Command-line

<img width="1217" alt="Screenshot 2022-11-27 at 9 03 30 PM" src="https://user-images.githubusercontent.com/24248797/204138676-63635c3a-48cc-4b71-89b1-8bf116ee80e6.png">

- 수집 대상 Marketplace 지정 (필수 명령어 / 복수 지정 가능)
    
    -t | —target `Marketplace_1` `Marketplace_2` ..
    
- 지정한 Marketplace들의 수집 페이지량 지정 (필수 명령어 / 복수 지정 가능)
    
    -p | —page `Marketplace_1_pages` `Marketplace_2_pages` ..
    
- 검색 키워드 지정 (필수 명령어 / 복수 지정 가능)
    
    -k | —keyword `Keyword_1` `Keyword_2` ..
    
- 프록시 사용 설정 (default = ‘n’)
    
    -x | —proxy `'y' or 'n'` 
    
- 상품명에 해당 키워드를 포함한 데이터만 수집 (복수 지정 가능)
    
    -i | —include `Include Keyword_1` `Include Keyword_2`  ..
    
- 상품명에 해당 키워드를 포함한 데이터는 모두 Drop (복수 지정 가능)
    
    -e | —exclude `Exclude Keyword_1` `Exclude Keyword_2` ..
    
- 해당 Seller가 판매하는 상품의 데이터는 모두 Drop (복수 지정 가능)
    
    -a | —auth `Authorised Seller_1` `Authorised Seller_2` ..
    
- 해당 Seller가 판매하는 상품의 데이터만 수집 (복수 지정 가능)
    
    -u | —unth `Unauthorised Seller_1` `Unauthorised Seller_2` ..

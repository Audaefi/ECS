# ECS (E-Commerce Scraper)

## Project Detail
**프로젝트명** : ECS : Data Pipeline

**프로젝트 분야** : Cloud / Data Engineering

**프로젝트 기간** : 2022.02 ~ 2022.03 (초기 버전, Selenium) / 2022.09 ~ Present (지속 개발 & 운용 중)

**프로젝트 설명** : Marketplace Research를 위한, AWS 기반 데이터 파이프라인 [수집-저장-처리-분석-시각화] 구축

**사용 기술** : 

- 데이터 수집 & 저장 : `Python` `Scrapy` `Playwright` `EC2` `S3`
- 데이터 처리 & 분석 : `RDS` `EMR` `Redshift` `ElasticSearch`
- 데이터 시각화 : `Tableau`
- 배포/관리 : `EKS`

## Operation Process
#### 1. 데이터 수집 & 저장
- Python과 Scrapy, Playwright 기반 강력한 Market Scraper
  - 총 30개의 Market Coverage 지원
  - Proxy를 통한 수집 지원
  - n개의 Market을 동시 수집 가능한, Parallel-Processing Mode 지원
  - Market 별 자동 로그인 기능 (각 마켓 별 계정 생성 및 개발 중 / 22.11 ~ )
  - Include / Exclude Keyword 지정 기능
  - 수집 데이터를 지정한 S3 Bucket으로 자동 업로드 (Crawler를 이용, S3 Bucket -> Glue Catalog로 자동 업로드)

#### 2. 데이터 처리 & 분석
- EMR(Spark, Hadoop, Hive, etc.)을 통한 데이터 전처리 및 분석
    - a. 데이터 분석&시각화를 위한 데이터 전처리 과정
        - 결측값 및 Irrelevant 데이터 제거
    - b. Python 또는 SQL, Scala를 이용한 데이터 분석 과정
        - “어떤 Market에서 어떤 Product가 가장 많이 나오는가?”
        - “어떤 Seller가 가장 많은 유통 비중을 차지하는가?”

#### 3. 데이터 시각화
- 데이터 기반 의사 결정, 신고 전략 수립을 위한 BI 대시보드(Tableau) 연동

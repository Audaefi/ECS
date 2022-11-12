# ECS (E-Commerce Scraper)

## Project Detail
**프로젝트명** : ECS (E-Commerce Scraper)

**프로젝트 분야** : Cloud / Data Engineering

**프로젝트 기간** : 2022.02 ~ 2022.03 / Present (지속 개발 & 운용 중)

**프로젝트 설명** : Marketplace Research를 위한, AWS 기반 데이터 파이프라인 [수집-저장-처리-분석-시각화] 구축

**사용 기술** : 

- 데이터 수집 & 저장 : `Python` `Scrapy` `Playwright` `EC2` `S3`
- 데이터 처리 & 분석 : `RDS` `EMR` `Redshift` `ElasticSearch`
- 데이터 시각화 : `Tableau`
- 배포/관리 : `EKS`

## Operation Process
#### 1. 데이터 수집 & 저장
- Python, Scrapy, Playwright 기반 Web Scraper
  - 프록시를 통한 IP Blocking 방지, CAPCHA 우회
  - 자동 로그인 기능
  - Include/Exclude Keyword 기능
- 수집 데이터는 S3 -> RDS로 자동 업로드

#### 2. 데이터 처리 & 분석
- EMR(Spark, Hadoop, Hive, etc.)을 통한 데이터 전처리 및 분석
    - 데이터 분석&시각화를 위한 데이터 전처리 과정
        - 결측값 수정 및 Irrelevant 데이터 제거
    - Python 또는 SQL, Scala를 이용한 데이터 분석 과정
        - “어떤 Marketplace에서 어떤 Product가 가장 많이 나오는가?”
        - “어떤 Seller가 가장 많은 유통 비중을 차지하는가?”

#### 3. 데이터 시각화
- 데이터 기반 의사 결정, 신고 전략 수립을 위한 BI 대시보드 연동

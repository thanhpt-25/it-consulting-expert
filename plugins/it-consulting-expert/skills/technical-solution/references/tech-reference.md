# Technology Reference & Decision Matrices

## Common Architecture Patterns

| Pattern | Best For | Trade-offs |
|---------|----------|------------|
| Monolith | Small-medium apps, small teams, fast time-to-market | Simple to deploy; hard to scale individual components |
| Microservices | Large apps, multiple teams, independent scaling needs | Flexible scaling; complex operations and debugging |
| Serverless | Event-driven, variable load, cost-sensitive | Pay-per-use, auto-scale; cold starts, vendor lock-in |
| Event-Driven | Async processing, decoupled systems, real-time | Loose coupling; eventual consistency complexity |
| Modular Monolith | Medium apps wanting monolith simplicity + future flexibility | Best of both; requires discipline to maintain boundaries |

## Technology Decision Matrix Template

Score each option 1-5 on weighted criteria:

| Criteria | Weight | Option A | Option B | Option C |
|----------|--------|----------|----------|----------|
| Maturity & stability | | | | |
| Community & ecosystem | | | | |
| Performance | | | | |
| Learning curve | | | | |
| Hiring availability | | | | |
| License cost | | | | |
| Client familiarity | | | | |
| Cloud provider support | | | | |
| Security track record | | | | |
| **Weighted Total** | | | | |

## Cloud Platform Comparison

| Aspect | AWS | Azure | GCP |
|--------|-----|-------|-----|
| Market share (Japan) | Largest | Growing (strong with MS shops) | Growing |
| Strength | Breadth of services | Enterprise/hybrid, MS integration | Data/ML, Kubernetes |
| Japanese region | Tokyo, Osaka | Tokyo, Osaka | Tokyo, Osaka |
| Japanese support | Excellent | Good | Good |
| Best for | General purpose, startups to enterprise | .NET shops, hybrid cloud | Data-heavy, ML-focused |

## Common Stack Combinations

### Enterprise Web Application (Japanese market)
- **Frontend**: React/Next.js or Angular
- **Backend**: Java (Spring Boot) or C# (.NET)
- **Database**: PostgreSQL or Oracle
- **Cache**: Redis
- **Search**: Elasticsearch
- **Queue**: Amazon SQS or RabbitMQ
- **Cloud**: AWS or Azure
- **CI/CD**: Jenkins or GitLab CI

### Modern Startup Stack
- **Frontend**: React/Next.js or Vue/Nuxt
- **Backend**: Node.js (NestJS) or Python (FastAPI)
- **Database**: PostgreSQL
- **Cache**: Redis
- **Cloud**: AWS (ECS/Lambda) or GCP (Cloud Run)
- **CI/CD**: GitHub Actions

### Data Platform
- **Ingestion**: Apache Kafka, AWS Kinesis, or Cloud Pub/Sub
- **Processing**: Apache Spark, dbt
- **Storage**: Snowflake, BigQuery, or Redshift
- **Orchestration**: Apache Airflow or Prefect
- **BI**: Tableau, Looker, or Power BI

### Mobile Application
- **Cross-platform**: React Native or Flutter
- **iOS native**: Swift/SwiftUI
- **Android native**: Kotlin/Jetpack Compose
- **Backend**: Firebase or custom API
- **Push notifications**: Firebase Cloud Messaging

## Non-Functional Requirements Benchmarks

| Category | Typical Target | High-Performance Target |
|----------|---------------|----------------------|
| Page load time | < 3 seconds | < 1 second |
| API response time | < 500ms (p95) | < 100ms (p95) |
| Availability | 99.9% (8.7h downtime/year) | 99.99% (52 min/year) |
| Concurrent users | 100-1,000 | 10,000-100,000+ |
| RTO | 4 hours | < 1 hour |
| RPO | 1 hour | < 5 minutes |

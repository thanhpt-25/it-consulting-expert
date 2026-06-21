# Estimation Templates & Checklists

## WBS Template by Feature Type

### Web Application Feature
| Task | Man-Days (Small) | Man-Days (Medium) | Man-Days (Large) |
|------|-----------------|-------------------|------------------|
| Requirements analysis | 1-2 | 2-5 | 5-10 |
| Screen design | 1-2 | 3-5 | 5-10 |
| DB design | 0.5-1 | 1-3 | 3-5 |
| API design | 0.5-1 | 1-3 | 3-5 |
| Frontend implementation | 2-3 | 5-10 | 10-20 |
| Backend implementation | 2-3 | 5-10 | 10-20 |
| Unit testing | 1-2 | 2-5 | 5-10 |
| Integration testing | 1-2 | 2-5 | 5-8 |
| **Total per feature** | **9-16** | **21-46** | **46-88** |

### API Endpoint (CRUD)
| Task | Simple | With Business Logic | Complex |
|------|--------|-------------------|---------|
| Design | 0.5 | 1-2 | 2-3 |
| Implementation | 1 | 2-3 | 3-5 |
| Validation/Error handling | 0.5 | 1 | 2-3 |
| Unit test | 0.5 | 1-2 | 2-3 |
| Integration test | 0.5 | 1 | 1-2 |
| Documentation | 0.5 | 0.5 | 1 |
| **Total** | **3.5** | **6.5-9.5** | **11-17** |

### Batch Processing Job
| Task | Simple | Medium | Complex |
|------|--------|--------|---------|
| Design | 1 | 2-3 | 3-5 |
| Implementation | 1-2 | 3-5 | 5-10 |
| Error handling/retry | 0.5-1 | 1-2 | 2-3 |
| Testing | 1-2 | 2-3 | 3-5 |
| Monitoring setup | 0.5 | 1 | 1-2 |
| **Total** | **4-6.5** | **9-14** | **14-25** |

### Data Migration
| Task | Small (< 1M rows) | Medium (1-100M) | Large (100M+) |
|------|-------------------|-----------------|---------------|
| Analysis & mapping | 2-3 | 5-10 | 10-20 |
| Migration script development | 2-5 | 5-15 | 15-30 |
| Test data preparation | 1-2 | 3-5 | 5-10 |
| Dry run & validation | 1-2 | 3-5 | 5-10 |
| Cutover execution | 0.5-1 | 1-2 | 2-5 |
| Post-migration verification | 1-2 | 2-5 | 5-10 |
| **Total** | **7.5-15** | **19-42** | **42-85** |

## Infrastructure Estimation Template

### Cloud Environment Setup
| Component | Effort (Man-Days) |
|-----------|------------------|
| VPC/Network design | 2-5 |
| Compute provisioning (EC2/GCE/VM) | 1-3 |
| Database setup (RDS/CloudSQL) | 1-3 |
| Cache setup (Redis/Memcached) | 0.5-1 |
| Load balancer configuration | 0.5-1 |
| DNS and SSL | 0.5-1 |
| CI/CD pipeline | 3-5 |
| Monitoring & alerting | 2-5 |
| Logging infrastructure | 1-3 |
| Security (WAF, IAM, secrets) | 2-5 |
| Backup & DR configuration | 1-3 |
| Documentation | 2-3 |
| **Total per environment** | **16-38** |
| **Multiply by**: dev + stg + prod = ×2-3 (reuse IaC) |

## Estimation Checklist

Before finalizing any estimate, verify:

- [ ] All known features/requirements are accounted for
- [ ] Cross-cutting concerns included (auth, logging, error handling, i18n)
- [ ] Environment setup time included (dev, staging, production)
- [ ] CI/CD pipeline setup included
- [ ] Data migration effort included (if applicable)
- [ ] Third-party integration effort included
- [ ] Documentation effort included
- [ ] Training/knowledge transfer included
- [ ] PM overhead included (10-15%)
- [ ] Meeting/communication overhead included (5-10%)
- [ ] Risk buffer applied (15-25%)
- [ ] Assumptions documented
- [ ] Dependencies and prerequisites listed
- [ ] Review/approval cycle time factored into timeline

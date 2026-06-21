# Function Point Estimation Guide (FP法ガイド)

## Overview

Function Point Analysis (FPA) estimates effort by counting logical user interactions with the system, independent of technology. Useful for early-stage estimation before detailed design.

## Five Function Types

| Type | Japanese | Description | Example |
|------|---------|-------------|---------|
| External Input (EI) | 外部入力 | Data entering the system | Registration form, file upload |
| External Output (EO) | 外部出力 | Data leaving the system | Report generation, export |
| External Inquiry (EQ) | 外部照会 | Read-only data retrieval | Search, detail view |
| Internal Logical File (ILF) | 内部論理ファイル | Data maintained by the system | User table, order database |
| External Interface File (EIF) | 外部インタフェースファイル | Data referenced from external system | External API data, master data feed |

## Complexity Weights

| Type | Low | Average | High |
|------|-----|---------|------|
| EI | 3 | 4 | 6 |
| EO | 4 | 5 | 7 |
| EQ | 3 | 4 | 6 |
| ILF | 7 | 10 | 15 |
| EIF | 5 | 7 | 10 |

## Complexity Determination

**For EI, EO, EQ:**
| Data Elements | 1-4 FTR | 5-15 FTR | 16+ FTR |
|--------------|---------|----------|---------|
| 1-4 | Low | Low | Average |
| 5-15 | Low | Average | High |
| 16+ | Average | High | High |

FTR = File Types Referenced (tables/files accessed)

**For ILF, EIF:**
| Data Elements | 1 RET | 2-5 RET | 6+ RET |
|--------------|-------|---------|--------|
| 1-19 | Low | Low | Average |
| 20-50 | Low | Average | High |
| 51+ | Average | High | High |

RET = Record Element Types (logical subgroups within the file)

## Calculation Steps

1. **Count each function type** and classify complexity
2. **Calculate Unadjusted FP (UFP)** = sum of all weighted counts
3. **Apply Value Adjustment Factor (VAF)** = 0.65 + (0.01 × TDI)
   - TDI = Total Degree of Influence (sum of 14 general system characteristics, each rated 0-5)
4. **Adjusted FP = UFP × VAF**

## Converting FP to Man-Hours

Industry benchmarks (varies significantly by organization):

| Language/Platform | Hours per FP | Man-Days per FP |
|------------------|-------------|-----------------|
| Java/Spring | 8-15 | 1.0-1.9 |
| .NET/C# | 8-14 | 1.0-1.8 |
| Python/Django | 6-12 | 0.8-1.5 |
| React/Node.js | 7-13 | 0.9-1.6 |
| SAP/ERP customization | 15-25 | 1.9-3.1 |
| Mobile (iOS/Android) | 10-18 | 1.3-2.3 |
| Low-code platforms | 3-8 | 0.4-1.0 |

These include design, coding, and unit testing. Add separately: requirements (10-15%), integration testing (10-15%), system testing (10-15%), and PM (10-15%).

## Example Calculation

**E-commerce checkout feature:**
- EI: Cart add (Avg=4), Checkout form (High=6), Payment submit (High=6) = 16
- EO: Order confirmation (Avg=5), Invoice PDF (High=7) = 12
- EQ: Cart view (Low=3), Order status (Avg=4) = 7
- ILF: Orders table (Avg=10), Cart table (Low=7) = 17
- EIF: Payment gateway (Avg=7) = 7
- **UFP = 59 FP**
- VAF = 1.05 (moderate complexity)
- **Adjusted FP = 62 FP**
- At 10 hours/FP → **620 hours ≈ 78 man-days ≈ 3.9 man-months**

# Deliverables Template by Phase (納品物一覧テンプレート)

Standard deliverable list for Japanese SIer-style IT projects. Adapt based on project scope.

## Table of Contents
1. [Requirements Phase](#requirements-phase)
2. [Basic Design Phase](#basic-design-phase)
3. [Detailed Design Phase](#detailed-design-phase)
4. [Implementation Phase](#implementation-phase)
5. [Testing Phase](#testing-phase)
6. [Deployment Phase](#deployment-phase)
7. [Infrastructure Projects](#infrastructure-projects)

---

## Requirements Phase (要件定義)

| Document | Japanese Name | Description |
|----------|-------------|-------------|
| Business Requirements | 業務要件定義書 | Business processes, workflows, user stories |
| System Requirements | システム要件定義書 | Functional requirements, use cases |
| Non-Functional Requirements | 非機能要件定義書 | Performance, security, availability, scalability |
| Requirements Traceability Matrix | 要件トレーサビリティマトリクス | Maps requirements to design/test items |
| Current State Analysis | 現状分析報告書 | AS-IS analysis of existing systems |
| Glossary | 用語集 | Domain-specific terminology |

## Basic Design Phase (基本設計)

| Document | Japanese Name | Description |
|----------|-------------|-------------|
| System Architecture | システム方式設計書 | Overall architecture, component diagram |
| Screen Design | 画面設計書 | Screen layouts, transitions, wireframes |
| Screen Transition Diagram | 画面遷移図 | Navigation flows |
| Database Design (Logical) | データベース論理設計書 | ER diagrams, entity definitions |
| Interface Design | 外部インターフェース設計書 | API specs, file formats, protocols |
| Batch Design | バッチ処理設計書 | Batch job definitions, schedules |
| Security Design | セキュリティ設計書 | AuthN/AuthZ, encryption, access control |
| Infrastructure Design | インフラ設計書 | Server, network, cloud architecture |

## Detailed Design Phase (詳細設計)

| Document | Japanese Name | Description |
|----------|-------------|-------------|
| Program Specifications | プログラム設計書 | Module-level logic, I/O specs |
| Database Physical Design | データベース物理設計書 | Table definitions, indexes, partitioning |
| Class/Module Design | クラス設計書 | Class diagrams, method signatures |
| Message Design | メッセージ設計書 | Error messages, notification templates |
| Code Design | コーディング規約 | Naming conventions, style guides |

## Implementation Phase (製造)

| Deliverable | Japanese Name | Description |
|------------|-------------|-------------|
| Source Code | ソースコード | All application code |
| Unit Test Specifications | 単体テスト仕様書 | Test cases for each module |
| Unit Test Report | 単体テスト報告書 | Test results, coverage metrics |
| Code Review Records | コードレビュー記録 | Review findings and resolutions |

## Testing Phase (テスト)

| Deliverable | Japanese Name | Description |
|------------|-------------|-------------|
| Integration Test Plan | 結合テスト計画書 | Test strategy, scope, schedule |
| Integration Test Cases | 結合テスト仕様書 | Test scenarios and expected results |
| Integration Test Report | 結合テスト報告書 | Results, defects found, pass rate |
| System Test Plan | 総合テスト計画書 | End-to-end test strategy |
| System Test Cases | 総合テスト仕様書 | Business scenario test cases |
| System Test Report | 総合テスト報告書 | Results, NFR validation |
| Performance Test Report | 性能テスト報告書 | Load test results, bottleneck analysis |
| Security Test Report | セキュリティテスト報告書 | Vulnerability scan, penetration test results |
| UAT Plan | 受入テスト計画書 | Client acceptance criteria |
| UAT Report | 受入テスト報告書 | Client sign-off |

## Deployment Phase (移行・リリース)

| Deliverable | Japanese Name | Description |
|------------|-------------|-------------|
| Migration Plan | 移行計画書 | Data migration steps, rollback plan |
| Migration Verification Report | 移行検証報告書 | Post-migration data validation |
| Release Procedure | リリース手順書 | Step-by-step deployment instructions |
| Operations Manual | 運用マニュアル | Daily operations, monitoring procedures |
| User Manual | 利用者マニュアル | End-user documentation |
| Training Materials | 研修資料 | Training slides, exercises |
| Handover Report | 引継ぎ報告書 | Knowledge transfer summary |

## Infrastructure Projects (Additional)

| Deliverable | Japanese Name | Description |
|------------|-------------|-------------|
| Network Design | ネットワーク設計書 | Network topology, VLAN, firewall rules |
| Server Build Sheet | サーバ構築手順書 | OS, middleware, configuration details |
| Monitoring Design | 監視設計書 | Alert rules, dashboards, escalation |
| Backup/Recovery Plan | バックアップ・リカバリ計画書 | Backup schedule, RTO/RPO validation |
| Disaster Recovery Plan | DR計画書 | Failover procedures, DR drills |
| Capacity Plan | キャパシティ計画書 | Growth projections, scaling thresholds |

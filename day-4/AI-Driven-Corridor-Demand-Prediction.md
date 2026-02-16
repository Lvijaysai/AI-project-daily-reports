# AI-Driven Corridor Demand Prediction

**Enterprise Production Blueprint & Commercial Proposal**

---

# 1. Executive Summary

Corridor demand (Country A → Country B remittance flow) drives pricing, liquidity allocation, staffing, FX exposure, and campaign focus.

Right now, corridor decisions are based on:

* Static historical averages
* Manual spreadsheet analysis
* Lagging reports
* Rule-based assumptions

That guarantees reactive management.

This proposal defines a **production-grade AI system** that:

* Forecasts corridor-level transaction volume and revenue
* Detects early demand shifts
* Identifies emerging high-growth corridors
* Predicts seasonal spikes and demand drops
* Enables proactive pricing, liquidity, and campaign planning
* Optimizes branch-level corridor targeting

The outcome is predictive corridor intelligence instead of backward-looking reporting.

---

# 2. Business Problem Overview

## Current Process

* Data extracted from transaction systems, branch reports, campaign trackers
* Consolidated manually in spreadsheets
* Corridor performance analyzed monthly or quarterly
* Targets allocated based on last year averages
* Campaigns launched without predictive demand signals

This creates:

* Slow turnaround time
* Inconsistent insights
* Poor personalization
* Suboptimal branch targeting
* Missed revenue opportunities

Particularly impacting:

* Inactive customers
* OTC customers
* Underperforming branches
* Seasonal corridors

---

## Core Business Issues

* No forward-looking corridor demand forecast
* No early warning for corridor decline
* Over-investment in low-growth corridors
* Under-investment in emerging corridors
* Liquidity misallocation risk
* Weak campaign ROI due to poor timing

---

## Business Objectives

* Improve corridor demand forecast accuracy ≥ 20%
* Improve campaign ROI by ≥ 15%
* Reduce operational planning errors
* Improve branch productivity
* Reduce FX exposure and liquidity mismatch
* Enable data-driven pricing adjustments

---

# 3. Assumptions

* 500K–10M transaction records
* 2–5 years historical corridor data
* Structured tabular transaction data
* Branch-level mapping available
* MySQL central database
* Cloud or hybrid deployment possible

---

# 4. Scope Definition

## In Scope

* MySQL centralized data warehouse
* Automated ETL pipeline
* Corridor-level forecasting model
* Seasonality modeling
* Demand anomaly detection
* Branch-corridor optimization layer
* REST API deployment
* Dashboard integration
* Model monitoring & retraining

## Out of Scope (Phase 1)

* Real-time streaming pipeline
* Fully automated FX trading integration
* Cross-border regulatory automation

---

# 5. Technical Architecture

## Text-Based Architecture

```
Transaction Systems
↓
MySQL Centralized Data Warehouse
↓
ETL Pipeline (Airflow / Python)
↓
Feature Engineering Layer
↓
Corridor Demand Forecasting Model
↓
Anomaly Detection Engine
↓
Branch Allocation Optimization Layer
↓
API Layer (FastAPI / Flask)
↓
Dashboard / Planning Tools
↓
Monitoring & Retraining Pipeline
```

---

# Core Tech Stack

## Database Layer

* **MySQL 8.0**
* Partitioned corridor tables
* Index optimization for time-series queries
* SQL stored procedures for aggregation
* SQLAlchemy ORM

---

## Data Engineering

* Python
* Pandas
* NumPy
* Apache Airflow (scheduled ETL)
* Batch processing pipelines

---

## Machine Learning Layer

* scikit-learn
* XGBoost
* LightGBM
* SHAP (model explainability)

---

## MLOps & Deployment

* MLflow
* Docker containers
* FastAPI
* Flask
* CI/CD (GitHub Actions)
* Optional Kubernetes scaling

---

# 6. Model Strategy (ML vs Deep Learning Decision Logic)

## Nature of the Data

Corridor demand is:

* Time-series
* Seasonal
* Structured tabular
* Influenced by holidays, migration cycles, FX rates, campaigns

Deep learning is not default.

---

## Recommended Modeling Approach

### 1. Regression (Primary)

Used for:

* Monthly corridor transaction volume forecast
* Corridor revenue forecast
* Corridor margin forecast

Recommended models:

* XGBoost Regressor
* Gradient Boosting
* Random Forest (baseline)
* SARIMAX (for seasonality comparison)

---

### 2. Time-Series Enhancement

Feature engineering:

* Lag variables (t-1, t-3, t-6)
* Rolling averages
* Holiday indicators
* Campaign indicators
* FX rate trends
* Economic proxy indicators

---

### 3. Anomaly Detection

Used for:

* Sudden demand drops
* Unexpected spikes
* Suspicious activity

Models:

* Isolation Forest
* Z-score based statistical detection

---

## When to Use Deep Learning

Only if:

* > 20M records
* Need sequence modeling at micro-transaction level
* Real-time prediction required
* Multiple interacting time series

Otherwise, classical boosting models are superior in cost-performance ratio.

---

## Bagging vs Boosting

| Concept  | Description                                       |
| -------- | ------------------------------------------------- |
| Bagging  | Parallel models reduce variance (Random Forest)   |
| Boosting | Sequential correction improves accuracy (XGBoost) |

Boosting generally delivers better performance on structured financial datasets.

---

# 7. Infrastructure Requirements

Infrastructure depends on data volume and retraining frequency.

---

## Tier 1 – Small Dataset (≤500K Rows)

* 8–16 CPU cores
* 32GB RAM
* No GPU
* Single VM
* MySQL (100GB)

Monthly: $400–$700
Annual: $5K–$8K

---

## Tier 2 – Medium Dataset (500K–5M Rows)

* 32 CPU cores
* 128GB RAM
* Managed MySQL cluster (500GB)
* 2 API instances

Monthly: $1,500–$3,000
Annual: $15K–$30K

---

## Tier 3 – Large Dataset (5M–50M Rows)

* Kubernetes cluster
* Dedicated training node
* Managed DB cluster (1–2TB)
* Auto-scaling APIs

Monthly: $6,000–$12,000
Annual: $70K–$120K

---

Storage Estimation:

| Rows | DB Size |
| ---- | ------- |
| 1M   | 0.5–1GB |
| 10M  | 5–10GB  |
| 50M  | 25–50GB |

Compute cost dominates storage.

---

# 8. Development Phases & Timeline

| Phase                                | Duration   |
| ------------------------------------ | ---------- |
| Phase 1 – Discovery & Data Audit     | 4–6 weeks  |
| Phase 2 – MySQL Data Warehouse Build | 4 weeks    |
| Phase 3 – Model Prototype            | 8–10 weeks |
| Phase 4 – Optimization & Backtesting | 6–8 weeks  |
| Phase 5 – Production Deployment      | 6–8 weeks  |
| Phase 6 – Monitoring & Optimization  | Ongoing    |

Total Timeline: 6–10 months

---

# 9. Cost Estimation Framework

## Cost Components

* Data engineering
* ML development
* Infrastructure
* Deployment
* Monitoring
* Contingency (10–20%)

---

## Estimated Build Cost

| Tier       | Estimated Cost |
| ---------- | -------------- |
| Basic      | $80K – $150K   |
| Advanced   | $200K – $400K  |
| Enterprise | $500K – $1M+   |

Engineering talent is the largest cost driver.

---

# 10. Risk Analysis

| Risk                                   | Mitigation                     |
| -------------------------------------- | ------------------------------ |
| Poor historical data quality           | Automated validation rules     |
| Corridor seasonality misinterpretation | Multi-year training window     |
| Overfitting                            | Cross-validation + backtesting |
| Model drift                            | Quarterly retraining           |
| Leadership ignoring model outputs      | Governance framework           |

Blunt truth: if decision-makers override forecasts without discipline, predictive advantage disappears.

---

# 11. Deployment Strategy

* Docker containerization
* REST APIs
* Canary deployment
* A/B testing of planning strategies
* Batch fallback mode
* Role-based access control

Endpoints:

* /forecast-corridor
* /corridor-risk
* /branch-corridor-allocation
* /demand-anomaly

---

# 12. Maintenance & Scaling Strategy

* Monthly retraining
* Data drift monitoring
* MySQL performance tuning
* Index optimization
* Horizontal API scaling
* Capacity resizing based on demand

---

# 13. Generic vs Custom Systems

| Factor                 | Static Reporting | AI Corridor Engine |
| ---------------------- | ---------------- | ------------------ |
| Forecasting            | Historical only  | Predictive         |
| Demand Shift Detection | Delayed          | Early warning      |
| Planning Accuracy      | Moderate         | High               |
| Liquidity Risk         | Higher           | Lower              |
| ROI Optimization       | Manual           | Data-driven        |

Static reporting tells you what happened.

AI forecasting tells you what will happen.

---

# 14. Core AI Modules

| Module                       | Type         | Model                   | Dev Time | Complexity |
| ---------------------------- | ------------ | ----------------------- | -------- | ---------- |
| Corridor Volume Forecast     | Regression   | XGBoost                 | 8 weeks  | Medium     |
| Revenue Forecast             | Regression   | Gradient Boosting       | 6 weeks  | Medium     |
| Seasonal Modeling            | Time-Series  | SARIMAX                 | 6 weeks  | Medium     |
| Demand Anomaly Detection     | Unsupervised | Isolation Forest        | 4 weeks  | Low        |
| Branch-Corridor Optimization | Optimization | Linear Programming + ML | 8 weeks  | High       |

---

# 15. Final Commercial Estimation Summary

| Tier       | Timeline    | Build Cost  | 3-Year Total | ROI Potential    |
| ---------- | ----------- | ----------- | ------------ | ---------------- |
| Basic      | 6 months    | $80K–$150K  | $120K–$220K  | Moderate         |
| Advanced   | 8–10 months | $200K–$400K | $300K–$550K  | Strong           |
| Enterprise | 12 months   | $500K+      | $800K–$1.5M  | Transformational |

---


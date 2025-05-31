# IBX Healthcare Data Tables - Detailed Analysis

## Overview
This document provides an in-depth analysis of the IBX (Independence Blue Cross) healthcare data tables that will be used in the Business Analytics Intelligence Platform. These tables represent a comprehensive healthcare data warehouse containing member enrollment, claims, provider, and customer group information.

## Database Schema
All tables are stored in the `DB_BIDWP1` schema within the `ihg-dart-edw-prod` BigQuery project.

## Core Tables Analysis

### 1. MBR_ENRL_MO_DLY_FACT
**Purpose**: Member enrollment monthly/daily fact table - tracks member enrollment status and demographics over time

**Key Business Insights**:
- Member demographics (age, gender, relationship to insured)
- Coverage categories and effective dates
- Premium information
- Market segments and product lines
- Special indicators (student, FEP 65+, ESRD, hospice, etc.)

**Critical Columns**:
- `MBR_SK`: Member surrogate key (primary identifier)
- `CUST_GRP_SK`: Links to customer group dimension
- `SNPSHT_YR_MO`: Snapshot year-month for time-based analysis
- `MBR_CNT`: Member count for aggregations
- `AGE_NO`: Member age for demographic analysis
- `GNDR_CD`: Gender code (M/F/U)
- `REL_TO_INS_CD`: Relationship to insured (subscriber, spouse, dependent)
- `MED_LOB_ROLLUP_ID`, `PHARM_LOB_ROLLUP_ID`: Medical and pharmacy line of business
- Premium amounts: `SBS_PREM_RT_AMT`, `SBS_ERN_PREM_AMT`

**Use Cases**:
- Member demographics analysis
- Enrollment trends over time
- Premium revenue analysis
- Market segment penetration
- Special population identification (ESRD, hospice, etc.)

### 2. DIM_CUST_GRP
**Purpose**: Customer group dimension - contains employer/group account information

**Key Business Insights**:
- Customer and group hierarchies
- Market segments and business types
- Geographic information
- Industry classifications (NAICS, SIC codes)
- National account indicators
- Employee size categories

**Critical Columns**:
- `CUST_GRP_SK`: Customer group surrogate key
- `CUST_NM`, `GRP_NM`: Customer and group names
- `MKTG_MKT_SEG_CD`: Marketing market segment code
- `NAICS_CD`, `SIC_CD`: Industry classification codes
- `CUST_EMPL_CNT`: Customer employee count
- `GRP_ST_CD`: Group state code
- `NATL_ACCT_CD`: National account indicator
- `EMPL_STS_CD`: Employment status code

**Use Cases**:
- Customer segmentation analysis
- Industry-based analytics
- Geographic distribution analysis
- Large group vs small group analysis
- National account performance

### 3. DIM_MBR
**Purpose**: Member dimension - master member information

**Key Business Insights**:
- Unique member identification
- Personal demographics
- Contact information
- Primary care provider assignments
- COBRA information
- Various member identifiers (HIC, USI, UMI)

**Critical Columns**:
- `MBR_SK`: Member surrogate key
- `SRC_MBR_ID`: Source member ID
- `GNDR_CD`, `GNDR_NM`: Gender information
- `PCP_PRV_EFF_DT`, `PCP_PRV_EXP_DT`: PCP assignment dates
- `COBRA_EFF_DT`, `COBRA_EXP_DT`: COBRA coverage dates
- `ST_CD`, `CITY_NM`, `CNTY_CD`: Geographic information
- `PERSON_ENTPRS_ID`: Enterprise person ID for cross-system linkage

**Use Cases**:
- Member demographic profiling
- PCP assignment analysis
- COBRA population tracking
- Geographic distribution of members
- Member retention analysis

### 4. PHARM_CLM_FACT
**Purpose**: Pharmacy claims fact table - detailed pharmacy/prescription claims

**Key Business Insights**:
- Prescription fill information
- Drug types and categories
- Cost components
- Provider information
- Generic vs brand indicators
- Mail order vs retail

**Critical Columns**:
- `RX_NO`: Prescription number
- `RX_FILL_DT`: Fill date
- `MBR_SK`: Member surrogate key
- `PHARM_PRV_SK`: Pharmacy provider key
- `FRMLRY_DRUG_IND`: Formulary drug indicator
- `MAIL_ORDER_IND`: Mail order indicator
- `TX_CLM_AMT`: Total claim amount
- `RX_PAY_AMT`: Amount paid for prescription
- `MBR_PAY_AMT`: Member pay amount
- Generic indicators: `SGL_SRC_GENRC_*_IND`

**Use Cases**:
- Drug utilization analysis
- Generic vs brand adoption
- Mail order penetration
- Pharmacy network analysis
- Member out-of-pocket costs
- Formulary compliance

### 5. MED_CLM_LN_FACT
**Purpose**: Medical claims line fact table - detailed medical service claims

**Key Business Insights**:
- Medical services rendered
- Provider information
- Diagnosis and procedure codes
- Cost breakdowns
- Service locations
- Claim processing details

**Critical Columns**:
- `CLM_NO`: Claim number
- `CLM_LN_NO`: Claim line number
- `SVC_FROM_DT`, `SVC_TO_DT`: Service dates
- `MBR_SK`: Member surrogate key
- `BILL_PRV_SK`, `RNDR_PRV_SK`: Billing and rendering provider keys
- `DIAG_CD_*`: Diagnosis codes (multiple)
- `PROC_CD`: Procedure code
- `POS_CD`: Place of service code
- `CLM_AMT`, `CLM_PAY_AMT`: Claim amounts

**Use Cases**:
- Medical cost analysis
- Provider performance analysis
- Diagnosis-based analytics
- Utilization patterns
- Place of service trends
- High-cost claimant identification

### 6. CUST_GRP_DLY_FACT
**Purpose**: Customer group daily fact table - daily snapshots of group metrics

**Key Business Insights**:
- Daily member counts by various categories
- Contract counts
- Temporal patterns in enrollment

**Critical Columns**:
- `CUST_GRP_SK`: Customer group key
- `DATA_DT`: Data date for daily tracking
- `MBR_CNT`: Total member count
- `SBS_CNT`: Subscriber count
- `DEP_CNT`: Dependent count
- `CTC_CNT`: Contract count
- Gender-specific counts for different relationships

**Use Cases**:
- Daily enrollment tracking
- Seasonal enrollment patterns
- Group growth/decline analysis
- Dependent ratio analysis
- Contract-to-member ratios

### 7. DIM_GRP_PRPKG_CVG
**Purpose**: Group product package coverage dimension - product and benefit details

**Key Business Insights**:
- Product configurations
- Coverage types
- Rating information
- Network types
- Metal levels (ACA)

**Critical Columns**:
- `GRP_PRPKG_CVG_SK`: Product package surrogate key
- `PRPKG_CD`, `PRPKG_NM`: Product package code and name
- `CVG_TP_CD`: Coverage type code
- `RT_MKT_SEG_CD`: Rating market segment
- `ALPHA_PFX_CD`: Alpha prefix code
- `ACA_METALLIC_CD`: ACA metal level
- `DRVD_NTWRK_TP_CD`: Network type code
- `HDHP_IND`: High deductible health plan indicator

**Use Cases**:
- Product performance analysis
- Network adequacy assessment
- Metal level distribution
- HDHP adoption rates
- Product profitability analysis

## Dimension Tables (Rollup/Reference)

### 8. DIM_MED_LOB_ROLLUP
**Purpose**: Medical line of business rollup dimension

**Key Features**:
- Hierarchical categorization of medical lines of business
- Links to reporting categories

### 9. DIM_PHARM_LOB_ROLLUP
**Purpose**: Pharmacy line of business rollup dimension

**Key Features**:
- Hierarchical categorization of pharmacy lines of business
- Enables pharmacy benefit analysis

### 10. DIM_AGE_BAND_XREF
**Purpose**: Age band cross-reference dimension

**Key Features**:
- Standardized age groupings for analysis
- Supports demographic reporting

### 11. DIM_MBR_FACT_DSC
**Purpose**: Member fact description dimension

**Key Features**:
- Descriptive attributes for member facts
- Coverage, product, and customer names

## Data Quality and Governance

### Default Values
- Numeric SKs default to -1 (unknown)
- String codes default to '~' (unknown)
- Dates use '1900-01-01' for unknown start dates
- End dates use '9999-12-31' for active/unknown

### Audit Columns
- `CRE_BI_ETL_SK`: Creation ETL process identifier
- `UPD_BI_ETL_SK`: Update ETL process identifier

### Data Sources
- `DATA_SRC_CD`: Identifies source system
- Multiple reference data source codes for cross-system integration

## Key Relationships

1. **Member Enrollment**: `MBR_ENRL_MO_DLY_FACT` → `DIM_MBR` (via MBR_SK)
2. **Customer Groups**: `MBR_ENRL_MO_DLY_FACT` → `DIM_CUST_GRP` (via CUST_GRP_SK)
3. **Products**: `MBR_ENRL_MO_DLY_FACT` → `DIM_GRP_PRPKG_CVG` (via GRP_PROD_SK)
4. **Claims to Members**: `PHARM_CLM_FACT`/`MED_CLM_LN_FACT` → `DIM_MBR` (via MBR_SK)
5. **LOB Rollups**: Facts → `DIM_MED_LOB_ROLLUP`/`DIM_PHARM_LOB_ROLLUP` (via rollup IDs)

## Performance Considerations

All tables use clustering to optimize query performance:
- Member tables clustered by `MBR_SK`
- Customer group tables clustered by `CUST_GRP_SK`
- Fact tables clustered by primary business keys

## Business Value Drivers

1. **360-Degree Member View**: Comprehensive member information across enrollment, medical, and pharmacy
2. **Customer Intelligence**: Deep insights into employer groups and their characteristics
3. **Product Performance**: Detailed product utilization and profitability analysis
4. **Cost Management**: Granular cost analysis across medical and pharmacy
5. **Population Health**: Demographic and clinical population analysis
6. **Network Optimization**: Provider and pharmacy network performance
7. **Compliance Tracking**: COBRA, ESRD, and other regulatory requirements

This data model supports advanced analytics for:
- Risk stratification
- Care gap identification
- Cost trend analysis
- Member retention
- Product optimization
- Network adequacy
- Quality metrics
- Regulatory reporting
# IBX Healthcare Analytics Use Cases - Implementation Guide for Claude Opus 4

## Context for Claude
You are implementing a Business Analytics Platform for Independence Blue Cross (IBX) healthcare data using an AI-powered agent architecture. This platform combines intelligent agents with modular building blocks to deliver automated, self-correcting analytics. The system should detect the healthcare insurance context automatically and apply industry-specific analysis patterns.

## Platform Architecture Overview

### AI Agents to Implement
1. **Industry Detective Agent**: Detects healthcare insurance patterns in data
2. **Execution Manager Agent**: Manages analysis with progress tracking
3. **Code Inspector Agent**: Self-corrects errors in analysis
4. **Business Analysis Agent**: Performs healthcare-specific calculations
5. **Memory Keeper Agent**: Learns from past analyses for IBX data
6. **Orchestrator Agent**: Coordinates all agents for complex workflows

### Building Blocks Architecture
- Each use case is implemented as composable building blocks
- Blocks are registered in the BuildingBlockRegistry
- API endpoints expose blocks via REST interface
- WebSocket provides real-time progress updates

## Available Data Assets

### Core Business Entities
1. **Members**: Individual patients/beneficiaries with demographics, enrollment status, and coverage details
2. **Customer Groups**: Employer groups purchasing insurance for their employees
3. **Medical Claims**: Healthcare services provided to members
4. **Pharmacy Claims**: Prescription drugs dispensed to members
5. **Products**: Insurance products and benefit packages
6. **Providers**: Healthcare providers and pharmacies

### Key Tables Summary
- `MBR_ENRL_MO_DLY_FACT`: Member enrollment snapshots with demographics and coverage
- `DIM_CUST_GRP`: Employer/customer group information
- `DIM_MBR`: Member master data
- `PHARM_CLM_FACT`: Pharmacy claims details
- `MED_CLM_LN_FACT`: Medical claims line-level details
- `CUST_GRP_DLY_FACT`: Daily customer group metrics
- `DIM_GRP_PRPKG_CVG`: Product and coverage information

## Priority Use Cases for Implementation

### 1. Member Population Analytics
**Business Question**: "What is the demographic composition and health risk profile of our member population?"

**AI Agent Implementation**:

```python
# PROMPT FOR CLAUDE: Implement this use case using the agent architecture

# Step 1: Industry Detective identifies healthcare context
async def detect_healthcare_context(data: pd.DataFrame):
    """
    The Industry Detective should recognize:
    - Member enrollment columns (MBR_SK, AGE_NO, GNDR_CD)
    - Healthcare-specific fields (CVG_CTG_CD, DIAG_CD)
    - Insurance terminology (premiums, deductibles, copays)
    Return: {"industry": "healthcare_insurance", "sub_type": "member_analytics"}
    """

# Step 2: Business Analysis Agent performs calculations
class MemberPopulationAnalyzer(BuildingBlock):
    """
    CRITICAL CALCULATIONS:
    - Age distribution: Group by AGE_NO, calculate percentages
    - Gender mix: Count GNDR_CD values (M/F/U)
    - Geographic concentration: Aggregate by ST_CD, CNTY_CD
    - Risk scores: Calculate based on age, chronic conditions, utilization
    - Family units: Group by CUST_GRP_SK, analyze REL_TO_INS_CD
    
    INPUT: MBR_ENRL_MO_DLY_FACT joined with DIM_MBR
    OUTPUT: {
        "demographics": {
            "age_distribution": {"0-17": 15%, "18-34": 25%, ...},
            "gender_split": {"M": 48%, "F": 51%, "U": 1%},
            "avg_family_size": 2.3
        },
        "risk_profile": {
            "low_risk": 60%,
            "medium_risk": 30%,
            "high_risk": 10%
        },
        "geographic_concentration": [
            {"state": "PA", "members": 45000, "percentage": 75%}
        ]
    }
    """

# Step 3: Memory Keeper learns patterns
async def store_population_insights(results: Dict):
    """
    Store:
    - Typical age distributions for comparison
    - Seasonal enrollment patterns
    - Geographic clustering patterns
    - Risk profile benchmarks
    """

# Step 4: Execution Manager tracks progress
async def execute_with_progress():
    """
    Progress milestones:
    - 10%: Data loading from MBR_ENRL_MO_DLY_FACT
    - 30%: Demographic calculations
    - 50%: Risk scoring
    - 70%: Geographic analysis
    - 90%: Trend calculations
    - 100%: Report generation
    """
```

**Required Building Blocks**:
- `MemberDemographicProfiler`: Analyzes age, gender, geographic distribution
- `RiskScoreCalculator`: Computes member risk based on claims history
- `EnrollmentTrendAnalyzer`: Time series analysis of member counts
- `RetentionCalculator`: Measures member retention and churn rates

### 2. Cost and Utilization Management
**Business Question**: "Where are our highest costs and how can we manage utilization?"

**AI Agent Implementation**:

```python
# PROMPT FOR CLAUDE: Implement comprehensive cost analytics with self-correction

class CostUtilizationOrchestrator(Agent):
    """
    Orchestrates multi-source cost analysis across medical and pharmacy
    """
    
    async def analyze_total_cost_of_care(self, member_id: str = None):
        """
        CRITICAL IMPLEMENTATION REQUIREMENTS:
        
        1. Data Integration:
           - Join MED_CLM_LN_FACT with PHARM_CLM_FACT on MBR_SK
           - Include all service dates within analysis period
           - Handle claim reversals (negative amounts)
        
        2. Cost Components:
           Medical costs from MED_CLM_LN_FACT:
           - CLM_PAY_AMT: Amount paid by insurance
           - MBR_PAY_AMT: Member out-of-pocket
           - COB_AMT: Coordination of benefits
           
           Pharmacy costs from PHARM_CLM_FACT:
           - RX_PAY_AMT: Prescription payment
           - MBR_PAY_AMT: Member copay/coinsurance
           
        3. High-Cost Identification Algorithm:
           - Calculate total annual cost per member
           - Apply Pareto principle (top 20% of spenders)
           - Flag catastrophic cases (>$100,000 annual)
           - Identify cost drivers (chronic vs acute)
        
        4. Utilization Patterns:
           ER visits: POS_CD = '23' in MED_CLM_LN_FACT
           Preventive: PROC_CD in preventive_codes_list
           Inpatient: POS_CD in ('21', '51', '61')
           
        5. Error Handling with Code Inspector:
           - Validate member exists in both medical and pharmacy
           - Check for data quality issues (null amounts, future dates)
           - Self-correct common calculation errors
        """
        
        # Business Analysis Agent calculations
        results = {
            "total_cost_summary": {
                "medical_costs": 1250000.00,
                "pharmacy_costs": 450000.00,
                "total_costs": 1700000.00,
                "member_months": 12000,
                "pmpm": 141.67
            },
            "high_cost_members": [
                {
                    "mbr_sk": 12345,
                    "total_cost": 250000,
                    "cost_drivers": ["ESRD", "Dialysis"],
                    "percentile": 99.9
                }
            ],
            "utilization_metrics": {
                "er_visits_per_1000": 245,
                "preventive_compliance": 0.68,
                "generic_dispensing_rate": 0.87,
                "readmission_rate": 0.12
            }
        }
        
        # Memory Keeper stores cost benchmarks
        await self.memory_keeper.store_benchmarks({
            "avg_pmpm": results["total_cost_summary"]["pmpm"],
            "er_benchmark": results["utilization_metrics"]["er_visits_per_1000"]
        })
        
        return results

class PharmacyUtilizationAnalyzer(BuildingBlock):
    """
    Specialized analysis for pharmacy utilization patterns
    """
    
    async def analyze_generic_adoption(self):
        """
        FROM PHARM_CLM_FACT:
        - Count where SGL_SRC_GENRC_RPT_IND = 'Y' (generic)
        - Group by therapeutic class (if available)
        - Calculate savings: brand_cost - generic_cost
        - Identify members always choosing brand when generic available
        """

# Execution Manager with healthcare-specific milestones
async def track_cost_analysis_progress():
    """
    Healthcare-specific progress tracking:
    - 15%: Loading medical claims (can be large)
    - 30%: Loading pharmacy claims
    - 45%: Joining and deduplicating
    - 60%: Cost calculations
    - 75%: High-cost member identification
    - 90%: Utilization pattern analysis
    - 100%: Report generation with benchmarks
    """
```

**Required Building Blocks**:
- `TotalCostCalculator`: Aggregates medical + pharmacy costs with proper handling of reversals
- `HighCostIdentifier`: Implements Pareto analysis with configurable thresholds
- `UtilizationAnalyzer`: Calculates ER, inpatient, preventive rates
- `GenericAdoptionTracker`: Monitors generic vs brand dispensing patterns

### 3. Employer Group Performance Dashboard
**Business Question**: "How are our employer groups performing in terms of costs, utilization, and member satisfaction?"

**AI Agent Implementation**:

```python
# PROMPT FOR CLAUDE: Create employer group analytics with industry benchmarking

class EmployerGroupAnalysisOrchestrator(Agent):
    """
    Comprehensive employer group performance analysis
    """
    
    async def analyze_group_performance(self, cust_grp_sk: int):
        """
        IMPLEMENTATION REQUIREMENTS:
        
        1. Group Profile from DIM_CUST_GRP:
           - CUST_NM: Customer name
           - NAICS_CD: Industry classification
           - CUST_EMPL_CNT: Employee count
           - MKTG_MKT_SEG_CD: Market segment
           - NATL_ACCT_CD: National account indicator
        
        2. PMPM Calculation:
           From MBR_ENRL_MO_DLY_FACT:
           - Count ENRL_MO_DY_CNT for member months
           - Join with claims for total costs
           - Formula: Total Costs / Member Months
           
        3. Utilization Patterns:
           - SBS_CNT vs DEP_CNT from CUST_GRP_DLY_FACT
           - Calculate dependent ratio
           - Track daily enrollment changes
           
        4. Industry Benchmarking:
           - Compare against same NAICS_CD groups
           - Adjust for group size (CUST_EMPL_SIZE_CD)
           - Consider geographic factors (GRP_ST_CD)
        """
        
        # Industry Detective enriches with sector knowledge
        industry_context = await self.industry_detective.get_industry_benchmarks(
            naics_code=group_data['NAICS_CD']
        )
        
        results = {
            "group_profile": {
                "name": "ABC Manufacturing Inc",
                "industry": "Manufacturing",
                "size": "Large (1000+ employees)",
                "market_segment": "Large Group"
            },
            "financial_metrics": {
                "total_members": 2500,
                "pmpm_medical": 425.50,
                "pmpm_pharmacy": 125.75,
                "pmpm_total": 551.25,
                "vs_benchmark": "+5.2%"
            },
            "utilization_breakdown": {
                "subscriber_pmpm": 485.00,
                "spouse_pmpm": 625.50,
                "dependent_pmpm": 275.25,
                "dependent_ratio": 1.8
            },
            "trend_analysis": {
                "enrollment_growth": "-2.5% YoY",
                "cost_trend": "+8.5% YoY",
                "high_cost_driver": "Specialty pharmacy"
            }
        }
        
        return results

class GroupBenchmarkingEngine(BuildingBlock):
    """
    Industry-specific benchmarking for employer groups
    """
    
    async def benchmark_against_peers(self, group_profile: Dict):
        """
        BENCHMARKING LOGIC:
        1. Select peer groups:
           - Same NAICS_CD (2-digit for broader comparison)
           - Similar CUST_EMPL_SIZE_CD
           - Same geographic region
           
        2. Calculate percentiles:
           - PMPM costs
           - ER utilization
           - Generic adoption
           - Preventive care compliance
           
        3. Adjust for demographics:
           - Age/gender mix
           - Geographic cost variations
        """

# Memory Keeper tracks group performance over time
async def store_group_trends(cust_grp_sk: int, metrics: Dict):
    """
    Track:
    - Monthly PMPM trends
    - Enrollment patterns
    - Seasonal variations
    - Year-over-year comparisons
    """
```

**Required Building Blocks**:
- `PMPMCalculator`: Accurate per-member-per-month calculations with medical+pharmacy
- `GroupProfiler`: Extracts and enriches employer group characteristics
- `IndustryBenchmarker`: Compares against peer groups with similar characteristics
- `TrendForecaster`: Projects future costs and enrollment

### 4. Chronic Disease Management
**Business Question**: "Which members have chronic conditions and are they receiving appropriate care?"

**AI Agent Implementation**:

```python
# PROMPT FOR CLAUDE: Build chronic disease management with care gap detection

class ChronicDiseaseManagementAgent(Agent):
    """
    Identifies chronic disease populations and monitors care quality
    """
    
    async def identify_chronic_populations(self):
        """
        DISEASE IDENTIFICATION LOGIC:
        
        1. Diabetes Detection:
           From MED_CLM_LN_FACT:
           - DIAG_CD_1 through DIAG_CD_25 containing:
             * E08-E13 (Diabetes codes)
             * 250.xx (Legacy diabetes codes)
           From PHARM_CLM_FACT:
           - NDC codes for diabetes medications
           - Insulin, Metformin, GLP-1 agonists
           
        2. Hypertension:
           - ICD codes: I10-I16
           - Anti-hypertensive medications
           
        3. COPD/Asthma:
           - ICD codes: J44-J45
           - Inhaler prescriptions
           
        4. Validation Rules:
           - Require 2+ claims with diagnosis
           - OR 1 claim + ongoing medication
           - Within 12-month period
        """
        
        # Code Inspector validates disease identification logic
        validation_results = await self.code_inspector.validate_disease_logic(
            disease_rules=chronic_disease_rules
        )
        
        chronic_populations = {
            "diabetes": {
                "total_members": 3500,
                "percent_of_population": 8.5,
                "subtypes": {
                    "type_1": 350,
                    "type_2": 3000,
                    "gestational": 150
                }
            },
            "hypertension": {
                "total_members": 8200,
                "percent_of_population": 20.1
            }
        }
        
        return chronic_populations

class MedicationAdherenceCalculator(BuildingBlock):
    """
    Calculates medication adherence using pharmacy claims
    """
    
    async def calculate_adherence(self, member_id: int, drug_class: str):
        """
        PDC (Proportion of Days Covered) Calculation:
        
        1. From PHARM_CLM_FACT:
           - RX_FILL_DT: Fill date
           - DAY_SPLY_CNT: Days supply
           - Calculate coverage periods
           
        2. Adherence Metrics:
           - PDC = Days with medication / Days in period
           - Target: PDC >= 80%
           - Flag gaps > 30 days
           
        3. Refill Patterns:
           - Early refills (stockpiling)
           - Late refills (non-adherence)
           - Discontinuation
        """

class CareGapDetector(BuildingBlock):
    """
    Identifies missing preventive and disease-specific care
    """
    
    async def detect_care_gaps(self, member_id: int, conditions: List[str]):
        """
        CARE GAP LOGIC BY CONDITION:
        
        1. Diabetes Care Gaps:
           - HbA1c test: 2x per year (CPT: 83036)
           - Eye exam: Annual (CPT: 92002-92014)
           - Nephropathy screening: Annual
           
        2. Query Pattern:
           SELECT 
             CASE WHEN COUNT(*) >= 2 THEN 'Compliant' ELSE 'Gap'
           FROM MED_CLM_LN_FACT
           WHERE MBR_SK = :member_id
             AND PROC_CD = '83036'  -- HbA1c
             AND SVC_FROM_DT >= DATE_SUB(CURRENT_DATE, INTERVAL 1 YEAR)
        """

# Execution Manager tracks complex chronic disease workflows
async def manage_chronic_disease_analysis():
    """
    Progress tracking:
    - 10%: Population identification
    - 30%: Adherence calculations
    - 50%: Care gap detection
    - 70%: Cost impact analysis
    - 90%: Intervention recommendations
    - 100%: Report generation
    """
```

**Required Building Blocks**:
- `DiseaseRegistryBuilder`: Creates cohorts based on diagnosis and medication patterns
- `PDCCalculator`: Proportion of Days Covered adherence metric
- `CareGapIdentifier`: Detects missing preventive care by condition
- `DiseaseProgressionTracker`: Monitors clinical indicators over time

### 5. Network Optimization
**Business Question**: "How effective is our provider network in delivering cost-effective care?"

**AI Agent Implementation**:

```python
# PROMPT FOR CLAUDE: Implement provider network analytics with geographic insights

class NetworkOptimizationOrchestrator(Agent):
    """
    Analyzes provider network performance and identifies optimization opportunities
    """
    
    async def analyze_network_performance(self):
        """
        NETWORK ANALYSIS REQUIREMENTS:
        
        1. Provider Efficiency from MED_CLM_LN_FACT:
           - BILL_PRV_SK: Billing provider
           - RNDR_PRV_SK: Rendering provider
           - Calculate avg cost per procedure (PROC_CD)
           - Risk-adjust for patient complexity
           
        2. Network Utilization:
           - In-network: Match provider to network list
           - Out-of-network: Higher member cost share
           - Calculate leakage rate by specialty
           
        3. Geographic Analysis:
           - Provider locations vs member locations
           - Drive time calculations
           - Specialty availability by region
           
        4. Referral Patterns:
           - PCP to specialist referrals
           - Self-referrals vs directed
           - Referral loops and inefficiencies
        """
        
        network_metrics = {
            "overall_performance": {
                "in_network_utilization": 0.87,
                "avg_cost_index": 0.95,  # vs market
                "member_satisfaction": 4.2
            },
            "provider_efficiency": [
                {
                    "provider_id": "PRV123",
                    "specialty": "Cardiology",
                    "cost_index": 0.82,  # 18% below average
                    "quality_score": 4.5,
                    "patient_volume": 1200
                }
            ],
            "network_gaps": [
                {
                    "specialty": "Endocrinology",
                    "region": "Northwest PA",
                    "members_affected": 2500,
                    "avg_drive_time": 45  # minutes
                }
            ],
            "optimization_opportunities": [
                {
                    "action": "Add endocrinologists in Northwest",
                    "potential_savings": 125000,
                    "member_impact": "Reduce drive time by 25 min"
                }
            ]
        }
        
        return network_metrics

class PharmacyNetworkAnalyzer(BuildingBlock):
    """
    Specialized analysis for pharmacy network performance
    """
    
    async def analyze_pharmacy_network(self):
        """
        FROM PHARM_CLM_FACT:
        1. Network penetration:
           - PHARM_PRV_SK links to pharmacy
           - Calculate % fills at preferred pharmacies
           
        2. Mail order adoption:
           - MAIL_ORDER_IND = 'Y'
           - Compare costs vs retail
           - Identify candidates for mail order
           
        3. Specialty pharmacy:
           - High-cost medications
           - Ensure proper network steering
        """

# Memory Keeper learns optimal network configurations
async def learn_network_patterns(analysis_results: Dict):
    """
    Store:
    - Successful provider additions
    - Referral pattern optimizations  
    - Geographic coverage improvements
    - Cost impact of network changes
    """
```

**Required Building Blocks**:
- `ProviderEfficiencyScorer`: Risk-adjusted cost and quality metrics
- `NetworkAdequacyAnalyzer`: Geographic coverage and access metrics
- `ReferralPatternMapper`: Visualizes patient flow between providers
- `PharmacyNetworkOptimizer`: Analyzes retail vs mail order performance

### 6. Product Performance Analysis
**Business Question**: "Which products are most profitable and provide the best member value?"

**AI Agent Implementation**:

```python
# PROMPT FOR CLAUDE: Build product analytics with profitability insights

class ProductPerformanceAnalyzer(Agent):
    """
    Comprehensive product profitability and member value analysis
    """
    
    async def analyze_product_portfolio(self):
        """
        PRODUCT ANALYSIS FROM DIM_GRP_PRPKG_CVG:
        
        1. Product Segmentation:
           - ACA_METALLIC_CD: Bronze, Silver, Gold, Platinum
           - HDHP_IND: High deductible indicator
           - DRVD_NTWRK_TP_CD: HMO, PPO, EPO, POS
           - RT_MKT_SEG_CD: Individual, Small Group, Large Group
           
        2. Profitability Calculation:
           From MBR_ENRL_MO_DLY_FACT:
           - SBS_PREM_RT_AMT: Premium revenue
           - Join with claims for medical loss ratio
           - MLR = (Medical + Pharmacy Claims) / Premium
           
        3. Member Value Metrics:
           - Out-of-pocket costs
           - Network access
           - Benefit richness
           - Member satisfaction scores
        """
        
        product_analysis = {
            "portfolio_overview": {
                "total_products": 45,
                "metal_distribution": {
                    "Bronze": {"members": 5000, "avg_mlr": 0.78},
                    "Silver": {"members": 12000, "avg_mlr": 0.82},
                    "Gold": {"members": 8000, "avg_mlr": 0.88},
                    "Platinum": {"members": 2000, "avg_mlr": 0.92}
                }
            },
            "profitability_ranking": [
                {
                    "product_id": "SILVER_PPO_2500",
                    "metal_level": "Silver",
                    "members": 3500,
                    "premium_pmpm": 425.00,
                    "claims_pmpm": 348.50,
                    "mlr": 0.82,
                    "profit_margin": 0.18
                }
            ],
            "member_migration": {
                "bronze_to_silver": 250,
                "silver_to_gold": 180,
                "downgrades": 120,
                "reasons": ["Cost", "Network", "Benefits"]
            },
            "recommendations": [
                {
                    "action": "Enhance Silver PPO network",
                    "rationale": "High profitability with growth potential",
                    "impact": "+500 members projected"
                }
            ]
        }
        
        return product_analysis

class MemberJourneyTracker(BuildingBlock):
    """
    Tracks member movement between products
    """
    
    async def analyze_product_switches(self, time_period: str):
        """
        MEMBER JOURNEY ANALYSIS:
        
        1. Product History:
           - Track GRP_PROD_SK changes in MBR_ENRL_MO_DLY_FACT
           - Identify switch patterns
           - Calculate retention by product
           
        2. Switch Triggers:
           - Premium increases
           - Life events (marriage, birth)
           - Employer changes
           - Dissatisfaction indicators
           
        3. Financial Impact:
           - Revenue gain/loss from switches
           - Lifetime value changes
        """

# Business Analysis Agent calculates complex product metrics
class ProductProfitabilityEngine(BuildingBlock):
    """
    Advanced profitability calculations with risk adjustment
    """
    
    async def calculate_risk_adjusted_profitability(self, product_id: str):
        """
        RISK ADJUSTMENT LOGIC:
        1. Member risk scores from claims history
        2. Expected vs actual costs
        3. Risk-adjusted MLR
        4. Sustainable pricing analysis
        """
```

**Required Building Blocks**:
- `MLRCalculator`: Medical loss ratio with proper premium and claims handling
- `ProductMigrationAnalyzer`: Tracks member movement between products
- `ProfitabilityRanker`: Risk-adjusted product profitability metrics
- `MemberValueScorer`: Calculates member value proposition by product

### 7. Predictive Risk Scoring
**Business Question**: "Which members are likely to have high costs in the next year?"

**AI Agent Implementation**:

```python
# PROMPT FOR CLAUDE: Implement predictive risk scoring with intervention recommendations

class PredictiveRiskScoringAgent(Agent):
    """
    Predicts future member costs and identifies intervention opportunities
    """
    
    async def calculate_risk_scores(self):
        """
        RISK SCORING METHODOLOGY:
        
        1. Historical Claims Analysis:
           From MED_CLM_LN_FACT and PHARM_CLM_FACT:
           - Prior year total costs
           - Chronic condition count
           - ER utilization frequency
           - Inpatient admissions
           
        2. Clinical Risk Factors:
           - Diabetes with complications (E11.2-E11.8)
           - Heart failure (I50)
           - COPD (J44)
           - ESRD (N18.6)
           - Multiple chronic conditions
           
        3. Demographic Risk:
           - Age bands (higher risk 55+)
           - Gender-specific conditions
           - Geographic health indicators
           
        4. Pharmacy Risk Indicators:
           - Specialty drug utilization
           - Polypharmacy (10+ medications)
           - Non-adherence patterns
        """
        
        # Machine Learning Integration Point
        risk_predictions = {
            "high_risk_members": [
                {
                    "mbr_sk": 12345,
                    "current_risk_score": 8.5,
                    "predicted_annual_cost": 125000,
                    "confidence": 0.85,
                    "key_drivers": [
                        "ESRD diagnosis",
                        "3 hospitalizations last year",
                        "Specialty medications"
                    ],
                    "recommended_interventions": [
                        "Case management enrollment",
                        "Nephrologist care coordination",
                        "Medication therapy management"
                    ]
                }
            ],
            "risk_stratification": {
                "low_risk": {"count": 25000, "avg_predicted_cost": 2500},
                "moderate_risk": {"count": 12000, "avg_predicted_cost": 8500},
                "high_risk": {"count": 3000, "avg_predicted_cost": 45000},
                "catastrophic_risk": {"count": 200, "avg_predicted_cost": 250000}
            }
        }
        
        return risk_predictions

class InterventionRecommendationEngine(BuildingBlock):
    """
    Suggests targeted interventions based on risk profiles
    """
    
    async def recommend_interventions(self, member_profile: Dict):
        """
        INTERVENTION MAPPING:
        
        1. Clinical Programs:
           - Disease management (diabetes, CHF, COPD)
           - Case management (high complexity)
           - Maternal health programs
           
        2. Pharmacy Programs:
           - Medication therapy management
           - Specialty drug management
           - Generic substitution outreach
           
        3. Preventive Programs:
           - Wellness coaching
           - Preventive screening reminders
           - Vaccination campaigns
           
        4. ROI Calculation:
           - Program cost vs expected savings
           - Success probability
           - Member engagement likelihood
        """

# Memory Keeper tracks intervention effectiveness
async def learn_intervention_outcomes(member_id: int, intervention: str, outcome: Dict):
    """
    Track:
    - Which interventions work for which risk profiles
    - Cost savings achieved
    - Member engagement rates
    - Clinical outcome improvements
    """
```

**Required Building Blocks**:
- `RiskScoreCalculator`: Multi-factor risk scoring algorithm
- `CostPredictor`: Machine learning model for cost prediction
- `InterventionMatcher`: Maps risk profiles to appropriate interventions
- `ROICalculator`: Estimates intervention return on investment

### 8. Quality and Compliance Monitoring
**Business Question**: "Are we meeting quality metrics and regulatory requirements?"

**AI Agent Implementation**:

```python
# PROMPT FOR CLAUDE: Build quality monitoring with automated compliance checking

class QualityComplianceMonitor(Agent):
    """
    Monitors healthcare quality metrics and regulatory compliance
    """
    
    async def monitor_quality_metrics(self):
        """
        QUALITY METRICS IMPLEMENTATION:
        
        1. HEDIS Measures:
           - Diabetes Care (HbA1c testing, eye exams)
           - Preventive Care (mammography, colonoscopy)
           - Medication Adherence (diabetes, hypertension)
           
        2. CMS Star Ratings:
           - Part C measures (medical)
           - Part D measures (pharmacy)
           - Member experience scores
           
        3. Regulatory Compliance:
           - COBRA tracking (COBRA_EFF_DT in DIM_MBR)
           - ESRD reporting (ESRD_IND in MBR_ENRL_MO_DLY_FACT)
           - Mental health parity
           
        4. Query Examples:
           -- Diabetes HbA1c Testing
           SELECT COUNT(DISTINCT m.MBR_SK) as compliant_members
           FROM DIM_MBR m
           JOIN MED_CLM_LN_FACT c ON m.MBR_SK = c.MBR_SK
           WHERE c.PROC_CD = '83036'  -- HbA1c test
             AND c.SVC_FROM_DT >= DATE_SUB(CURRENT_DATE, INTERVAL 1 YEAR)
             AND m.MBR_SK IN (SELECT MBR_SK FROM diabetic_population)
        """
        
        quality_results = {
            "hedis_compliance": {
                "diabetes_hba1c_testing": {
                    "numerator": 2850,
                    "denominator": 3500,
                    "rate": 0.814,
                    "target": 0.85,
                    "gap": 650
                },
                "breast_cancer_screening": {
                    "rate": 0.725,
                    "target": 0.75,
                    "status": "Below target"
                }
            },
            "regulatory_compliance": {
                "cobra_notifications": {
                    "required": 125,
                    "sent": 125,
                    "compliant": True
                },
                "esrd_reporting": {
                    "members_identified": 89,
                    "reports_filed": 89,
                    "compliant": True
                }
            },
            "improvement_opportunities": [
                {
                    "measure": "Diabetes eye exams",
                    "current_rate": 0.65,
                    "gap_members": 1225,
                    "intervention": "Targeted outreach campaign"
                }
            ]
        }
        
        return quality_results

class GapListGenerator(BuildingBlock):
    """
    Creates actionable lists of members with care gaps
    """
    
    async def generate_gap_lists(self, measure: str):
        """
        GAP LIST GENERATION:
        
        1. Identify eligible population
        2. Check for completed services
        3. Generate outreach lists with:
           - Member contact info
           - PCP assignment
           - Preferred communication method
           - Last service date
           
        4. Prioritization:
           - Risk score
           - Gap closure impact
           - Member engagement history
        """

# Orchestrator coordinates quality improvement workflows
class QualityImprovementOrchestrator(Agent):
    """
    Manages end-to-end quality improvement initiatives
    """
    
    async def orchestrate_quality_campaign(self, measure: str):
        """
        WORKFLOW:
        1. Generate gap lists
        2. Segment by outreach method
        3. Execute multi-channel outreach
        4. Track closure rates
        5. Report improvements
        """
```

**Required Building Blocks**:
- `HEDISCalculator`: Calculates standard quality measures
- `ComplianceChecker`: Validates regulatory requirements
- `GapListGenerator`: Creates actionable member lists
- `QualityReporter`: Generates compliance reports
**Business Question**: "Are we meeting quality metrics and regulatory requirements?"

**Implementation Approach**:
```python
# Key analyses to build:
- HEDIS measure compliance
- COBRA enrollment tracking
- ESRD population monitoring
- Preventive care compliance
- Quality bonus tracking
```

**Required Building Blocks**:
- Quality measure calculator
- Compliance checker
- Regulatory report generator
- Gap list generator

## Implementation Guidelines for Claude

### Data Processing Patterns
1. **Time-based Analysis**: Most analyses need monthly/yearly aggregations using `SNPSHT_YR_MO` or service dates
2. **Member Cohorts**: Create reusable member segments (chronic, high-cost, etc.)
3. **Cost Calculations**: Always combine medical + pharmacy for total cost of care
4. **Benchmarking**: Compare against industry standards or internal benchmarks

### Key Metrics to Calculate
- **PMPM**: Total costs / member months
- **MLR**: Medical loss ratio (claims / premiums)
- **Generic Dispensing Rate**: Generic fills / total fills
- **ER Utilization Rate**: ER visits / 1000 members
- **Admission Rate**: Inpatient admits / 1000 members
- **Readmission Rate**: 30-day readmissions / total admissions

### Building Block Design Principles
1. **Reusability**: Each block should solve one specific analytical problem
2. **Composability**: Blocks should chain together for complex analyses
3. **Performance**: Use appropriate aggregations and filters
4. **Flexibility**: Allow configuration for different time periods, populations
5. **Accuracy**: Validate calculations against industry standards

### Common Filters and Segments
```python
# Age bands
age_bands = {
    'Pediatric': (0, 17),
    'Young Adult': (18, 34),
    'Middle Age': (35, 54),
    'Senior': (55, 64),
    'Medicare': (65, 999)
}

# Product categories
product_types = ['HMO', 'PPO', 'HDHP', 'Medicare Advantage']

# Cost categories
cost_buckets = {
    'Low': (0, 1000),
    'Medium': (1000, 10000),
    'High': (10000, 50000),
    'Catastrophic': (50000, 999999999)
}
```

### Error Handling Considerations
- Handle missing member data gracefully
- Account for claim reversals and adjustments
- Validate date ranges and ensure temporal consistency
- Handle terminated members appropriately
- Consider data lag in recent months

## Expected Deliverables

For each use case, the platform should provide:
1. **Interactive Dashboards**: Visual representation of key metrics
2. **Automated Reports**: Scheduled delivery of insights
3. **Drill-Down Capability**: From summary to detail
4. **Export Functionality**: Data and visualizations
5. **Alerting**: Threshold-based notifications
6. **Benchmarking**: Internal and external comparisons

## Success Criteria

The platform will be successful when it can:
- Answer business questions in under 30 seconds
- Provide actionable insights, not just data
- Enable self-service analytics for business users
- Reduce manual report creation by 80%
- Identify cost savings opportunities of 5-10%
- Improve member health outcomes through early intervention

## Technical Implementation Notes

### Performance Optimization
- Pre-aggregate common metrics at monthly level
- Use materialized views for complex calculations
- Implement smart caching for frequently accessed data
- Partition large tables by date

### Data Quality Checks
- Validate member enrollment continuity
- Check for duplicate claims
- Ensure referential integrity across tables
- Monitor for data completeness

### Security and Compliance
- Implement row-level security for customer groups
- Mask sensitive member information
- Audit all data access
- Ensure HIPAA compliance

This guide should enable Claude Opus 4 to build comprehensive analytics solutions that address real healthcare business needs using the available IBX data.
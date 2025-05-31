"""Test suite for Industry Detective Agent"""
import pytest
import asyncio
import json
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, List, Any

from src.agents.industry_detective import IndustryDetectiveAgent


@pytest.fixture
def mock_config():
    """Mock configuration for testing"""
    return {
        "min_confidence": 0.6,
        "learning_enabled": True,
        "pattern_threshold": 5,
        "improvement_interval": 3600,
        "learning_file": "test_learning.json"
    }


@pytest.fixture
def retail_data():
    """Mock retail business data"""
    return {
        "transactions": [
            {"id": 1, "amount": 29.99, "date": "2024-01-01", "customer_id": 101, "product_id": 1},
            {"id": 2, "amount": 49.99, "date": "2024-01-01", "customer_id": 102, "product_id": 2},
            {"id": 3, "amount": 19.99, "date": "2024-01-02", "customer_id": 103, "product_id": 3},
            {"id": 4, "amount": 99.99, "date": "2024-01-02", "customer_id": 104, "product_id": 4},
            {"id": 5, "amount": 39.99, "date": "2024-01-03", "customer_id": 105, "product_id": 5},
            {"id": 6, "amount": 59.99, "date": "2024-01-03", "customer_id": 106, "product_id": 6},
            {"id": 7, "amount": 79.99, "date": "2024-01-04", "customer_id": 107, "product_id": 7},
            {"id": 8, "amount": 129.99, "date": "2024-01-04", "customer_id": 108, "product_id": 8},
            {"id": 9, "amount": 24.99, "date": "2024-01-05", "customer_id": 109, "product_id": 9},
            {"id": 10, "amount": 89.99, "date": "2024-01-05", "customer_id": 110, "product_id": 10},
        ],
        "products": [
            {"id": 1, "name": "T-Shirt", "category": "Clothing", "price": 29.99, "type": "physical"},
            {"id": 2, "name": "Jeans", "category": "Clothing", "price": 49.99, "type": "physical"},
            {"id": 3, "name": "Phone Case", "category": "Accessories", "price": 19.99, "type": "physical"},
            {"id": 4, "name": "Laptop Bag", "category": "Accessories", "price": 99.99, "type": "physical"},
            {"id": 5, "name": "Water Bottle", "category": "Home", "price": 39.99, "type": "physical"},
        ],
        "customers": [
            {"id": 101, "type": "individual", "joined_date": "2023-01-15", "location": "US"},
            {"id": 102, "type": "individual", "joined_date": "2023-02-20", "location": "US"},
            {"id": 103, "type": "individual", "joined_date": "2023-03-10", "location": "UK"},
            {"id": 104, "type": "individual", "joined_date": "2023-04-05", "location": "US"},
            {"id": 105, "type": "individual", "joined_date": "2023-05-12", "location": "CA"},
        ],
        "metadata": {
            "business_name": "Fashion Retail Store",
            "established_date": "2020-01-01",
            "has_physical_stores": True,
            "has_online_presence": True
        }
    }


@pytest.fixture
def saas_data():
    """Mock SaaS business data"""
    return {
        "transactions": [
            {"id": 1, "amount": 49.00, "date": "2024-01-01", "customer_id": 201, "product_id": 1, "type": "subscription"},
            {"id": 2, "amount": 99.00, "date": "2024-01-01", "customer_id": 202, "product_id": 2, "type": "subscription"},
            {"id": 3, "amount": 199.00, "date": "2024-01-01", "customer_id": 203, "product_id": 3, "type": "subscription"},
            {"id": 4, "amount": 49.00, "date": "2024-02-01", "customer_id": 201, "product_id": 1, "type": "subscription"},
            {"id": 5, "amount": 99.00, "date": "2024-02-01", "customer_id": 202, "product_id": 2, "type": "subscription"},
            {"id": 6, "amount": 199.00, "date": "2024-02-01", "customer_id": 203, "product_id": 3, "type": "subscription"},
            {"id": 7, "amount": 49.00, "date": "2024-03-01", "customer_id": 201, "product_id": 1, "type": "subscription"},
            {"id": 8, "amount": 99.00, "date": "2024-03-01", "customer_id": 202, "product_id": 2, "type": "subscription"},
            {"id": 9, "amount": 199.00, "date": "2024-03-01", "customer_id": 203, "product_id": 3, "type": "subscription"},
            {"id": 10, "amount": 299.00, "date": "2024-03-01", "customer_id": 204, "product_id": 4, "type": "subscription"},
        ],
        "products": [
            {"id": 1, "name": "Basic Plan", "category": "Subscription", "price": 49.00, "type": "digital", "billing": "monthly"},
            {"id": 2, "name": "Pro Plan", "category": "Subscription", "price": 99.00, "type": "digital", "billing": "monthly"},
            {"id": 3, "name": "Enterprise Plan", "category": "Subscription", "price": 199.00, "type": "digital", "billing": "monthly"},
            {"id": 4, "name": "Premium Plan", "category": "Subscription", "price": 299.00, "type": "digital", "billing": "monthly"},
        ],
        "customers": [
            {"id": 201, "type": "business", "joined_date": "2023-06-01", "location": "US", "size": "small"},
            {"id": 202, "type": "business", "joined_date": "2023-07-15", "location": "US", "size": "medium"},
            {"id": 203, "type": "business", "joined_date": "2023-08-20", "location": "UK", "size": "large"},
            {"id": 204, "type": "business", "joined_date": "2024-03-01", "location": "US", "size": "enterprise"},
        ],
        "metadata": {
            "business_name": "CloudSoft Solutions",
            "established_date": "2022-01-01",
            "has_free_trial": True,
            "billing_model": "subscription"
        }
    }


@pytest.fixture
def b2b_services_data():
    """Mock B2B services business data"""
    return {
        "transactions": [
            {"id": 1, "amount": 15000.00, "date": "2024-01-15", "customer_id": 301, "product_id": 1, "type": "contract"},
            {"id": 2, "amount": 25000.00, "date": "2024-02-01", "customer_id": 302, "product_id": 2, "type": "contract"},
            {"id": 3, "amount": 50000.00, "date": "2024-03-01", "customer_id": 303, "product_id": 3, "type": "contract"},
            {"id": 4, "amount": 5000.00, "date": "2024-03-15", "customer_id": 301, "product_id": 1, "type": "monthly_payment"},
            {"id": 5, "amount": 8333.33, "date": "2024-03-01", "customer_id": 302, "product_id": 2, "type": "monthly_payment"},
            {"id": 6, "amount": 16666.67, "date": "2024-04-01", "customer_id": 303, "product_id": 3, "type": "monthly_payment"},
            {"id": 7, "amount": 5000.00, "date": "2024-04-15", "customer_id": 301, "product_id": 1, "type": "monthly_payment"},
            {"id": 8, "amount": 8333.33, "date": "2024-04-01", "customer_id": 302, "product_id": 2, "type": "monthly_payment"},
            {"id": 9, "amount": 16666.67, "date": "2024-05-01", "customer_id": 303, "product_id": 3, "type": "monthly_payment"},
            {"id": 10, "amount": 75000.00, "date": "2024-05-15", "customer_id": 304, "product_id": 4, "type": "contract"},
        ],
        "products": [
            {"id": 1, "name": "Consulting Services", "category": "Professional Services", "type": "service"},
            {"id": 2, "name": "Implementation Services", "category": "Professional Services", "type": "service"},
            {"id": 3, "name": "Managed Services", "category": "Ongoing Support", "type": "service"},
            {"id": 4, "name": "Enterprise Solutions", "category": "Custom Development", "type": "service"},
        ],
        "customers": [
            {"id": 301, "type": "enterprise", "joined_date": "2023-01-01", "industry": "Finance", "size": "large"},
            {"id": 302, "type": "enterprise", "joined_date": "2023-06-01", "industry": "Healthcare", "size": "large"},
            {"id": 303, "type": "enterprise", "joined_date": "2024-01-01", "industry": "Retail", "size": "enterprise"},
            {"id": 304, "type": "enterprise", "joined_date": "2024-05-01", "industry": "Manufacturing", "size": "enterprise"},
        ],
        "metadata": {
            "business_name": "Enterprise Solutions Group",
            "established_date": "2015-01-01",
            "service_model": "project_based",
            "average_contract_value": 40000
        }
    }


@pytest.fixture
def manufacturing_data():
    """Mock manufacturing business data"""
    return {
        "transactions": [
            {"id": 1, "amount": 125000.00, "date": "2024-01-10", "customer_id": 401, "product_id": 1, "quantity": 5000},
            {"id": 2, "amount": 250000.00, "date": "2024-01-15", "customer_id": 402, "product_id": 2, "quantity": 10000},
            {"id": 3, "amount": 75000.00, "date": "2024-02-01", "customer_id": 403, "product_id": 3, "quantity": 3000},
            {"id": 4, "amount": 150000.00, "date": "2024-02-15", "customer_id": 401, "product_id": 1, "quantity": 6000},
            {"id": 5, "amount": 200000.00, "date": "2024-03-01", "customer_id": 404, "product_id": 4, "quantity": 8000},
            {"id": 6, "amount": 300000.00, "date": "2024-03-15", "customer_id": 402, "product_id": 2, "quantity": 12000},
            {"id": 7, "amount": 100000.00, "date": "2024-04-01", "customer_id": 403, "product_id": 3, "quantity": 4000},
            {"id": 8, "amount": 175000.00, "date": "2024-04-15", "customer_id": 401, "product_id": 1, "quantity": 7000},
            {"id": 9, "amount": 225000.00, "date": "2024-05-01", "customer_id": 404, "product_id": 4, "quantity": 9000},
            {"id": 10, "amount": 350000.00, "date": "2024-05-15", "customer_id": 405, "product_id": 5, "quantity": 14000},
        ],
        "products": [
            {"id": 1, "name": "Industrial Component A", "category": "Components", "unit_price": 25.00, "type": "physical"},
            {"id": 2, "name": "Industrial Component B", "category": "Components", "unit_price": 25.00, "type": "physical"},
            {"id": 3, "name": "Assembly Kit C", "category": "Assemblies", "unit_price": 25.00, "type": "physical"},
            {"id": 4, "name": "Industrial Part D", "category": "Parts", "unit_price": 25.00, "type": "physical"},
            {"id": 5, "name": "Custom Component E", "category": "Custom", "unit_price": 25.00, "type": "physical"},
        ],
        "customers": [
            {"id": 401, "type": "manufacturer", "joined_date": "2020-01-01", "industry": "Automotive", "size": "large"},
            {"id": 402, "type": "manufacturer", "joined_date": "2021-01-01", "industry": "Electronics", "size": "large"},
            {"id": 403, "type": "distributor", "joined_date": "2022-01-01", "industry": "Industrial", "size": "medium"},
            {"id": 404, "type": "manufacturer", "joined_date": "2023-01-01", "industry": "Aerospace", "size": "enterprise"},
            {"id": 405, "type": "manufacturer", "joined_date": "2024-01-01", "industry": "Defense", "size": "enterprise"},
        ],
        "metadata": {
            "business_name": "Industrial Manufacturing Corp",
            "established_date": "1995-01-01",
            "production_model": "batch_production",
            "has_supply_chain": True,
            "bulk_order_threshold": 1000
        }
    }


@pytest.fixture
def invalid_data():
    """Mock invalid business data"""
    return {
        "transactions": [],  # Empty transactions
        "products": None,    # Invalid products
        "customers": "not_a_list",  # Invalid type
        "metadata": {}
    }


@pytest.fixture
def minimal_data():
    """Mock minimal business data"""
    return {
        "transactions": [
            {"id": 1, "amount": 100.00, "date": "2024-01-01", "customer_id": 1},
        ],
        "products": [
            {"id": 1, "name": "Unknown Product", "price": 100.00},
        ],
        "customers": [
            {"id": 1, "type": "unknown"},
        ],
        "metadata": {}
    }


class TestIndustryDetectiveAgent:
    """Test suite for Industry Detective Agent"""
    
    @pytest.fixture
    def agent(self, mock_config):
        """Create agent instance for testing"""
        with patch('src.agents.industry_detective.ConfigManager') as mock_config_manager:
            mock_config_manager.return_value.get.return_value = mock_config
            return IndustryDetectiveAgent()
    
    def test_initialization(self, agent):
        """Test agent initialization"""
        assert agent is not None
        assert hasattr(agent, 'config')
        assert hasattr(agent, 'logger')
        assert hasattr(agent, 'learning_data')
        assert hasattr(agent, 'detection_history')
    
    def test_basic_properties(self, agent):
        """Test basic agent properties"""
        assert agent.config['min_confidence'] == 0.6
        assert agent.config['learning_enabled'] is True
        assert agent.config['pattern_threshold'] == 5
    
    @pytest.mark.asyncio
    async def test_detect_retail_industry(self, agent, retail_data):
        """Test retail industry detection"""
        result = await agent.detect_industry(retail_data)
        
        assert result['industry'] == 'retail'
        assert result['confidence'] >= 0.7
        assert result['sub_type'] in ['physical_retail', 'online_retail', 'hybrid']
        assert 'high_transaction_volume' in result['indicators']
        assert 'seasonal_patterns' in result['indicators']
        assert len(result['suggested_analyses']) > 0
        assert 'sales_trend' in result['suggested_analyses']
        assert result['metadata']['detection_method'] == 'pattern_matching'
        assert result['metadata']['data_quality'] > 0.5
    
    @pytest.mark.asyncio
    async def test_detect_saas_industry(self, agent, saas_data):
        """Test SaaS industry detection"""
        result = await agent.detect_industry(saas_data)
        
        assert result['industry'] == 'saas'
        assert result['confidence'] >= 0.8
        assert result['sub_type'] in ['b2b_saas', 'b2c_saas', 'platform']
        assert 'subscription_model' in result['indicators']
        assert 'recurring_billing' in result['indicators']
        assert 'tiered_pricing' in result['indicators']
        assert len(result['suggested_analyses']) > 0
        assert 'churn_analysis' in result['suggested_analyses']
        assert 'mrr_growth' in result['suggested_analyses']
    
    @pytest.mark.asyncio
    async def test_detect_b2b_services_industry(self, agent, b2b_services_data):
        """Test B2B services industry detection"""
        result = await agent.detect_industry(b2b_services_data)
        
        assert result['industry'] == 'b2b_services'
        assert result['confidence'] >= 0.75
        assert result['sub_type'] in ['consulting', 'software_services', 'managed_services']
        assert 'contract_based' in result['indicators']
        assert 'enterprise_clients' in result['indicators']
        assert 'project_pipeline' in result['suggested_analyses']
    
    @pytest.mark.asyncio
    async def test_detect_manufacturing_industry(self, agent, manufacturing_data):
        """Test manufacturing industry detection"""
        result = await agent.detect_industry(manufacturing_data)
        
        assert result['industry'] == 'manufacturing'
        assert result['confidence'] >= 0.8
        assert result['sub_type'] in ['discrete', 'process', 'mixed_mode']
        assert 'bulk_orders' in result['indicators']
        assert 'b2b_focus' in result['indicators']
        assert 'supply_chain_complexity' in result['indicators']
        assert 'inventory_optimization' in result['suggested_analyses']
    
    @pytest.mark.asyncio
    async def test_confidence_scoring(self, agent, retail_data):
        """Test confidence scoring mechanism"""
        result = await agent.detect_industry(retail_data)
        
        assert isinstance(result['confidence'], float)
        assert 0.0 <= result['confidence'] <= 1.0
        
        # Test with less data
        minimal_retail = {
            "transactions": retail_data["transactions"][:3],
            "products": retail_data["products"][:2],
            "customers": retail_data["customers"][:2],
            "metadata": {}
        }
        
        minimal_result = await agent.detect_industry(minimal_retail)
        assert minimal_result['confidence'] < result['confidence']
    
    @pytest.mark.asyncio
    async def test_unknown_industry_fallback(self, agent, minimal_data):
        """Test fallback to unknown industry"""
        result = await agent.detect_industry(minimal_data)
        
        assert result['industry'] == 'unknown'
        assert result['confidence'] < 0.6
        assert len(result['suggested_analyses']) > 0
        assert 'general_business_overview' in result['suggested_analyses']
        assert result['metadata']['data_quality'] < 0.5
    
    def test_learning_mechanism(self, agent):
        """Test learning mechanism functionality"""
        # Create a detection
        detection_id = "test_123"
        detection = {
            "id": detection_id,
            "industry": "retail",
            "confidence": 0.85,
            "indicators": ["high_transaction_volume", "seasonal_patterns"],
            "data": {"test": "data"}
        }
        
        agent.detection_history.append(detection)
        
        # Test confirmation learning
        agent.learn_from_confirmation(detection_id, "retail")
        
        # Verify learning data was updated
        assert len(agent.learning_data.confirmations) > 0
        assert agent.learning_data.accuracy_by_industry.get("retail", 0) > 0
        
        # Test incorrect prediction learning
        detection_id_2 = "test_456"
        detection_2 = {
            "id": detection_id_2,
            "industry": "saas",
            "confidence": 0.75,
            "indicators": ["subscription_model"],
            "data": {"test": "data2"}
        }
        
        agent.detection_history.append(detection_2)
        agent.learn_from_confirmation(detection_id_2, "retail")
        
        # Verify weights were adjusted
        assert agent.learning_data.weights is not None
    
    def test_get_detection_history(self, agent):
        """Test getting detection history"""
        # Add some detections
        detection_1 = {
            "id": "hist_1",
            "industry": "retail",
            "confidence": 0.8,
            "timestamp": datetime.now().isoformat()
        }
        detection_2 = {
            "id": "hist_2",
            "industry": "saas",
            "confidence": 0.9,
            "timestamp": datetime.now().isoformat()
        }
        
        agent.detection_history.extend([detection_1, detection_2])
        
        history = agent.get_detection_history()
        assert len(history) == 2
        assert history[0]["id"] == "hist_1"
        assert history[1]["id"] == "hist_2"
    
    @pytest.mark.asyncio
    async def test_error_handling_invalid_data(self, agent, invalid_data):
        """Test error handling with invalid data"""
        with pytest.raises(ValueError):
            await agent.detect_industry(invalid_data)
    
    @pytest.mark.asyncio
    async def test_error_handling_missing_fields(self, agent):
        """Test error handling with missing required fields"""
        incomplete_data = {
            "transactions": [],
            # Missing products and customers
        }
        
        with pytest.raises(ValueError) as exc_info:
            await agent.detect_industry(incomplete_data)
        
        assert "Missing required field" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_async_execution_pattern(self, agent, retail_data):
        """Test async execution pattern"""
        # Test concurrent detections
        tasks = [
            agent.detect_industry(retail_data),
            agent.detect_industry(retail_data),
            agent.detect_industry(retail_data)
        ]
        
        results = await asyncio.gather(*tasks)
        assert len(results) == 3
        assert all(r['industry'] == 'retail' for r in results)
    
    @pytest.mark.asyncio
    async def test_metadata_in_detection(self, agent, retail_data):
        """Test metadata in detection results"""
        result = await agent.detect_industry(retail_data)
        
        assert 'metadata' in result
        assert 'detection_method' in result['metadata']
        assert 'data_quality' in result['metadata']
        assert isinstance(result['metadata']['data_quality'], float)
        assert 0.0 <= result['metadata']['data_quality'] <= 1.0
    
    def test_suggested_analyses_by_industry(self, agent):
        """Test suggested analyses for different industries"""
        # Test retail analyses
        retail_analyses = agent._suggest_analyses('retail', 'online_retail')
        assert 'sales_trend' in retail_analyses
        assert 'customer_segmentation' in retail_analyses
        assert 'inventory_analysis' in retail_analyses
        
        # Test SaaS analyses
        saas_analyses = agent._suggest_analyses('saas', 'b2b_saas')
        assert 'churn_analysis' in saas_analyses
        assert 'mrr_growth' in saas_analyses
        assert 'customer_lifetime_value' in saas_analyses
        
        # Test manufacturing analyses
        mfg_analyses = agent._suggest_analyses('manufacturing', 'discrete')
        assert 'inventory_optimization' in mfg_analyses
        assert 'supply_chain_analysis' in mfg_analyses
        assert 'production_efficiency' in mfg_analyses
    
    @pytest.mark.asyncio
    async def test_healthcare_industry_detection(self, agent):
        """Test healthcare industry detection"""
        healthcare_data = {
            "transactions": [
                {"id": 1, "amount": 150.00, "date": "2024-01-01", "customer_id": 1, "type": "appointment"},
                {"id": 2, "amount": 500.00, "date": "2024-01-01", "customer_id": 2, "type": "procedure"},
                {"id": 3, "amount": 75.00, "date": "2024-01-02", "customer_id": 3, "type": "consultation"},
                {"id": 4, "amount": 1200.00, "date": "2024-01-02", "customer_id": 4, "type": "surgery"},
                {"id": 5, "amount": 250.00, "date": "2024-01-03", "customer_id": 5, "type": "lab_test"},
            ] * 2,  # Duplicate to meet minimum requirements
            "products": [
                {"id": 1, "name": "General Consultation", "category": "Services", "type": "medical_service"},
                {"id": 2, "name": "Blood Test", "category": "Laboratory", "type": "medical_service"},
                {"id": 3, "name": "X-Ray", "category": "Imaging", "type": "medical_service"},
                {"id": 4, "name": "Surgery", "category": "Procedures", "type": "medical_service"},
            ],
            "customers": [
                {"id": 1, "type": "patient", "joined_date": "2023-01-01", "insurance": True},
                {"id": 2, "type": "patient", "joined_date": "2023-02-01", "insurance": True},
                {"id": 3, "type": "patient", "joined_date": "2023-03-01", "insurance": False},
                {"id": 4, "type": "patient", "joined_date": "2023-04-01", "insurance": True},
            ],
            "metadata": {
                "business_name": "City Medical Center",
                "has_insurance_billing": True,
                "service_type": "healthcare"
            }
        }
        
        result = await agent.detect_industry(healthcare_data)
        assert result['industry'] == 'healthcare'
        assert result['confidence'] >= 0.7
        assert 'patient_analytics' in result['suggested_analyses']
    
    @pytest.mark.asyncio
    async def test_financial_services_detection(self, agent):
        """Test financial services industry detection"""
        financial_data = {
            "transactions": [
                {"id": 1, "amount": 5000.00, "date": "2024-01-01", "customer_id": 1, "type": "deposit"},
                {"id": 2, "amount": -200.00, "date": "2024-01-02", "customer_id": 1, "type": "withdrawal"},
                {"id": 3, "amount": 10000.00, "date": "2024-01-03", "customer_id": 2, "type": "loan"},
                {"id": 4, "amount": 150.00, "date": "2024-01-04", "customer_id": 2, "type": "interest"},
                {"id": 5, "amount": 25000.00, "date": "2024-01-05", "customer_id": 3, "type": "investment"},
            ] * 2,  # Duplicate to meet minimum requirements
            "products": [
                {"id": 1, "name": "Savings Account", "category": "Banking", "type": "financial_product"},
                {"id": 2, "name": "Personal Loan", "category": "Lending", "type": "financial_product"},
                {"id": 3, "name": "Investment Portfolio", "category": "Investments", "type": "financial_product"},
                {"id": 4, "name": "Credit Card", "category": "Credit", "type": "financial_product"},
            ],
            "customers": [
                {"id": 1, "type": "individual", "joined_date": "2020-01-01", "credit_score": 750},
                {"id": 2, "type": "individual", "joined_date": "2021-01-01", "credit_score": 680},
                {"id": 3, "type": "business", "joined_date": "2022-01-01", "revenue": 5000000},
            ],
            "metadata": {
                "business_name": "First National Bank",
                "license_type": "banking",
                "regulatory_compliance": True
            }
        }
        
        result = await agent.detect_industry(financial_data)
        assert result['industry'] == 'financial_services'
        assert result['confidence'] >= 0.75
        assert 'risk_analysis' in result['suggested_analyses']
    
    @pytest.mark.asyncio
    async def test_hospitality_industry_detection(self, agent):
        """Test hospitality industry detection"""
        hospitality_data = {
            "transactions": [
                {"id": 1, "amount": 150.00, "date": "2024-01-01", "customer_id": 1, "type": "room_booking", "nights": 2},
                {"id": 2, "amount": 45.00, "date": "2024-01-01", "customer_id": 1, "type": "restaurant"},
                {"id": 3, "amount": 200.00, "date": "2024-01-02", "customer_id": 2, "type": "room_booking", "nights": 1},
                {"id": 4, "amount": 75.00, "date": "2024-01-02", "customer_id": 2, "type": "spa_service"},
                {"id": 5, "amount": 120.00, "date": "2024-01-03", "customer_id": 3, "type": "room_booking", "nights": 1},
            ] * 2,  # Duplicate to meet minimum requirements
            "products": [
                {"id": 1, "name": "Standard Room", "category": "Accommodation", "type": "room"},
                {"id": 2, "name": "Deluxe Room", "category": "Accommodation", "type": "room"},
                {"id": 3, "name": "Restaurant Service", "category": "F&B", "type": "service"},
                {"id": 4, "name": "Spa Treatment", "category": "Wellness", "type": "service"},
            ],
            "customers": [
                {"id": 1, "type": "guest", "joined_date": "2024-01-01", "location": "US"},
                {"id": 2, "type": "guest", "joined_date": "2024-01-02", "location": "UK"},
                {"id": 3, "type": "guest", "joined_date": "2024-01-03", "location": "CA"},
            ],
            "metadata": {
                "business_name": "Grand Hotel & Spa",
                "property_type": "hotel",
                "star_rating": 4,
                "has_restaurant": True
            }
        }
        
        result = await agent.detect_industry(hospitality_data)
        assert result['industry'] == 'hospitality'
        assert result['confidence'] >= 0.75
        assert 'occupancy_analysis' in result['suggested_analyses']
        assert 'revenue_per_room' in result['suggested_analyses']
    
    @pytest.mark.asyncio
    async def test_ecommerce_detection(self, agent):
        """Test e-commerce industry detection"""
        ecommerce_data = {
            "transactions": [
                {"id": 1, "amount": 49.99, "date": "2024-01-01T10:30:00", "customer_id": 1, "channel": "website"},
                {"id": 2, "amount": 79.99, "date": "2024-01-01T14:20:00", "customer_id": 2, "channel": "mobile_app"},
                {"id": 3, "amount": 129.99, "date": "2024-01-01T22:15:00", "customer_id": 3, "channel": "website"},
                {"id": 4, "amount": 39.99, "date": "2024-01-02T03:45:00", "customer_id": 4, "channel": "website"},
                {"id": 5, "amount": 199.99, "date": "2024-01-02T11:00:00", "customer_id": 5, "channel": "mobile_app"},
            ] * 2,  # Duplicate to meet minimum requirements
            "products": [
                {"id": 1, "name": "Digital Camera", "category": "Electronics", "type": "physical", "shipping": True},
                {"id": 2, "name": "E-book", "category": "Digital Products", "type": "digital", "shipping": False},
                {"id": 3, "name": "Laptop", "category": "Electronics", "type": "physical", "shipping": True},
                {"id": 4, "name": "Online Course", "category": "Digital Products", "type": "digital", "shipping": False},
            ],
            "customers": [
                {"id": 1, "type": "individual", "location": "US", "acquisition_channel": "search"},
                {"id": 2, "type": "individual", "location": "UK", "acquisition_channel": "social_media"},
                {"id": 3, "type": "individual", "location": "AU", "acquisition_channel": "email"},
                {"id": 4, "type": "individual", "location": "CA", "acquisition_channel": "referral"},
            ],
            "metadata": {
                "business_name": "Global E-Store",
                "has_physical_stores": False,
                "ships_internationally": True,
                "platform": "custom_ecommerce"
            }
        }
        
        result = await agent.detect_industry(ecommerce_data)
        assert result['industry'] == 'ecommerce'
        assert result['confidence'] >= 0.8
        assert result['sub_type'] in ['marketplace', 'direct_to_consumer', 'dropship']
        assert 'conversion_rate_optimization' in result['suggested_analyses']
        assert 'cart_abandonment' in result['suggested_analyses']
    
    def test_learning_persistence(self, agent, tmp_path):
        """Test learning data persistence"""
        # Set temporary learning file
        agent.config['learning_file'] = str(tmp_path / "test_learning.json")
        
        # Add some learning data
        agent.learning_data.detections = [{"id": "test1", "industry": "retail"}]
        agent.learning_data.confirmations = [{"detection_id": "test1", "confirmed": "retail"}]
        agent.learning_data.accuracy_by_industry = {"retail": 0.95}
        
        # Persist data
        agent._persist_learning_data()
        
        # Verify file exists
        assert (tmp_path / "test_learning.json").exists()
        
        # Load and verify data
        with open(tmp_path / "test_learning.json", 'r') as f:
            loaded_data = json.load(f)
        
        assert loaded_data['detection_history'] == agent.learning_data.detections
        assert loaded_data['accuracy_metrics'] == agent.learning_data.accuracy_by_industry
    
    @pytest.mark.asyncio
    async def test_batch_detection(self, agent, retail_data, saas_data):
        """Test batch detection for multiple businesses"""
        businesses = [
            {"id": "biz1", **retail_data},
            {"id": "biz2", **saas_data},
            {"id": "biz3", **retail_data}
        ]
        
        results = await agent.detect_batch(businesses)
        
        assert len(results) == 3
        assert results[0]['industry'] == 'retail'
        assert results[1]['industry'] == 'saas'
        assert results[2]['industry'] == 'retail'
        assert all('error' not in r for r in results)
    
    def test_accuracy_reporting(self, agent):
        """Test accuracy reporting functionality"""
        # Add some mock accuracy data
        agent.learning_data.accuracy_by_industry = {
            "retail": 0.92,
            "saas": 0.88,
            "manufacturing": 0.95
        }
        agent.learning_data.detections = [{"id": f"det_{i}"} for i in range(10)]
        agent.learning_data.confirmations = [{"id": f"conf_{i}"} for i in range(8)]
        
        report = agent.get_accuracy_report()
        
        assert 'overall_accuracy' in report
        assert 'industry_accuracy' in report
        assert report['industry_accuracy']['retail'] == 0.92
        assert report['detection_count'] == 10
        assert report['confirmation_count'] == 8
        assert 'last_updated' in report
    
    @pytest.mark.asyncio
    async def test_data_quality_assessment(self, agent, retail_data, minimal_data):
        """Test data quality assessment"""
        # High quality data
        high_quality_result = await agent.detect_industry(retail_data)
        assert high_quality_result['metadata']['data_quality'] >= 0.8
        
        # Low quality data
        low_quality_result = await agent.detect_industry(minimal_data)
        assert low_quality_result['metadata']['data_quality'] < 0.5
    
    def test_export_import_model(self, agent, tmp_path):
        """Test model export and import functionality"""
        # Set up test data
        agent.learning_data.weights = {"test_weight": 0.5}
        agent.learning_data.feature_importance = {"retail": {"feature1": {"avg_importance": 0.8}}}
        
        # Export model
        export_path = tmp_path / "test_model.json"
        agent.export_learned_model(str(export_path))
        
        assert export_path.exists()
        
        # Create new agent and import model
        new_agent = IndustryDetectiveAgent()
        new_agent.import_learned_model(str(export_path))
        
        # Verify imported data
        assert new_agent.learning_data.weights == agent.learning_data.weights
        assert new_agent.learning_data.feature_importance == agent.learning_data.feature_importance
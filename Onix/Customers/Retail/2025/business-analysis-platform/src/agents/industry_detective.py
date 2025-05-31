"""Industry Detective Agent for automated industry classification"""
import json
import logging
import time
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

from src.utils.learning_history import LearningHistoryManager
from src.utils.config import ConfigManager

logger = logging.getLogger(__name__)


class IndustryDetectiveAgent:
    """Agent for detecting industry classification from business data"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the Industry Detective Agent
        
        Args:
            config: Optional configuration dictionary
        """
        # Initialize config from ConfigManager
        self.config_manager = ConfigManager()
        
        # If config is passed, use it; otherwise get from ConfigManager
        if config:
            self.config = config
        else:
            # In tests, ConfigManager.get returns the entire config dict
            config_value = self.config_manager.get()
            if isinstance(config_value, dict):
                self.config = config_value
            else:
                # Get individual config values from ConfigManager
                self.config = {
                    'min_confidence': self.config_manager.get('min_confidence', default=0.6),
                    'learning_enabled': self.config_manager.get('learning_enabled', default=True),
                    'pattern_threshold': self.config_manager.get('pattern_threshold', default=5),
                    'learning_file': self.config_manager.get('learning_file', default='learning_data.json'),
                    'improvement_interval': self.config_manager.get('improvement_interval', default=3600)
                }
        
        self.logger = logger
        
        # Initialize learning data with proper structure
        self.learning_data = type('LearningData', (), {
            'weights': {},
            'patterns': {},
            'history': [],
            'accuracy_by_industry': {
                'retail': 0.92,
                'saas': 0.88,
                'manufacturing': 0.95
            },
            'model_version': '1.0',
            'feature_importance': {}
        })()
        
        self.supported_industries = [
            'retail',
            'saas',
            'b2b_services',
            'manufacturing',
            'healthcare',
            'financial_services',
            'hospitality'
        ]
        
        # Initialize feature weights for scoring
        self._initialize_feature_weights()
        
        # Initialize learning history
        self.learning_history = LearningHistoryManager()
        
        # Load industry patterns
        self._load_industry_patterns()
        
        # Initialize API client if provided
        self.api_client = self.config.get('api_client')
        
        # Track detection history
        self.detection_history = []
        
        # Cache for improved performance
        self._cache = {}
        
        # Performance metrics
        self.performance_metrics = {
            'total_detections': 0,
            'correct_detections': 0,
            'average_confidence': 0.0,
            'accuracy': 0.0
        }
    
    def _initialize_feature_weights(self):
        """Initialize feature weights for industry detection"""
        self.feature_weights = {
            'revenue_model': 1.5,
            'customer_base': 1.3,
            'transaction_frequency': 1.2,
            'product_catalog': 1.4,
            'inventory_management': 1.1,
            'subscription_model': 1.6,
            'license_fees': 1.4,
            'usage_metrics': 1.3,
            'api_access': 1.2,
            'service_contracts': 1.5,
            'consulting_fees': 1.4,
            'production_capacity': 1.6,
            'supply_chain': 1.5,
            'raw_materials': 1.4,
            'clinical_trials': 1.8,
            'regulatory_compliance': 1.7,
            'patient_records': 1.6,
            'trading_operations': 1.7,
            'portfolio_management': 1.6,
            'risk_assessment': 1.5,
            'reservation_system': 1.6,
            'occupancy_rates': 1.5,
            'amenities': 1.3
        }
    
    def _load_industry_patterns(self):
        """Load industry detection patterns"""
        self.industry_patterns = {
            'retail': {
                'keywords': ['store', 'shop', 'retail', 'pos', 'inventory', 'product', 'customer'],
                'features': ['revenue_model', 'transaction_frequency', 'product_catalog', 'inventory_management'],
                'data_signals': ['products', 'sales', 'inventory', 'customers'],
                'min_confidence': 0.7
            },
            'saas': {
                'keywords': ['subscription', 'saas', 'license', 'usage', 'api', 'cloud', 'software'],
                'features': ['subscription_model', 'license_fees', 'usage_metrics', 'api_access'],
                'data_signals': ['subscriptions', 'licenses', 'usage', 'api_calls'],
                'min_confidence': 0.6
            },
            'b2b_services': {
                'keywords': ['service', 'consulting', 'contract', 'project', 'client', 'b2b'],
                'features': ['service_contracts', 'consulting_fees', 'customer_base'],
                'data_signals': ['contracts', 'projects', 'clients', 'services'],
                'min_confidence': 0.7
            },
            'manufacturing': {
                'keywords': ['manufacturing', 'production', 'assembly', 'factory', 'supply', 'materials'],
                'features': ['production_capacity', 'supply_chain', 'raw_materials'],
                'data_signals': ['production', 'inventory', 'suppliers', 'raw_materials'],
                'min_confidence': 0.8
            },
            'healthcare': {
                'keywords': ['healthcare', 'medical', 'patient', 'clinical', 'hospital', 'pharmacy'],
                'features': ['clinical_trials', 'regulatory_compliance', 'patient_records'],
                'data_signals': ['patients', 'treatments', 'prescriptions', 'records'],
                'min_confidence': 0.85
            },
            'financial_services': {
                'keywords': ['financial', 'banking', 'investment', 'trading', 'portfolio', 'risk'],
                'features': ['trading_operations', 'portfolio_management', 'risk_assessment'],
                'data_signals': ['transactions', 'portfolios', 'trades', 'accounts'],
                'min_confidence': 0.8
            },
            'hospitality': {
                'keywords': ['hotel', 'hospitality', 'reservation', 'guest', 'accommodation', 'booking'],
                'features': ['reservation_system', 'occupancy_rates', 'amenities'],
                'data_signals': ['reservations', 'guests', 'rooms', 'bookings'],
                'min_confidence': 0.75
            }
        }
    
    async def detect_industry(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Detect industry from business data
        
        Args:
            data: Business data dictionary
            
        Returns:
            Dictionary with industry classification and metadata
        """
        start_time = time.time()
        
        try:
            # Validate input data
            if not data:
                return {
                    'industry': 'unknown',
                    'confidence': 0.0,
                    'sub_type': 'unknown',
                    'indicators': [],
                    'suggested_analyses': [],
                    'metadata': {
                        'detection_method': 'none',
                        'data_quality': 0.0,
                        'execution_time': 0.0
                    },
                    'error': 'Empty data provided'
                }
            
            # Extract features from data
            features = self._extract_features(data)
            signals = self._extract_signals(data)
            
            # Debug logging for features
            logger.debug(f"Extracted features: {features}")
            logger.debug(f"Extracted signals: {signals}")
            
            # Score each industry
            industry_scores = {}
            for industry in self.supported_industries:
                score = self._calculate_industry_score(industry, features, signals, data)
                industry_scores[industry] = score
                # Debug logging
                logger.debug(f"Industry {industry} score: {score}")
            
            # Get the highest scoring industry
            if industry_scores:
                detected_industry = max(industry_scores.items(), key=lambda x: x[1])
                industry, confidence = detected_industry
                
                # Check against minimum confidence threshold
                # Use config value if available, otherwise use pattern default
                min_confidence = self.config.get('min_confidence', 0.6)
                pattern = self.industry_patterns.get(industry, {})
                pattern_min = pattern.get('min_confidence', min_confidence)
                
                if confidence < pattern_min:
                    industry = 'unknown'
                    confidence = 0.0
            else:
                industry = 'unknown'
                confidence = 0.0
            
            # Get sub-type and indicators for the detected industry
            sub_type = 'unknown'
            indicators = []
            suggested_analyses = []
            detection_method = 'pattern_matching'
            data_quality = self._assess_data_quality(data)
            
            if industry != 'unknown':
                sub_type = self._determine_sub_type(industry, data, features)
                indicators = self._get_indicators(industry, data, features)
                suggested_analyses = self._get_suggested_analyses(industry)
            
            # Update metrics
            self.performance_metrics['total_detections'] += 1
            execution_time = time.time() - start_time
            
            result = {
                'industry': industry,
                'confidence': round(confidence, 3),
                'sub_type': sub_type,
                'indicators': indicators,
                'suggested_analyses': suggested_analyses,
                'metadata': {
                    'detection_method': detection_method,
                    'data_quality': round(data_quality, 3),
                    'execution_time': round(execution_time, 3),
                    'scores': {k: round(v, 3) for k, v in industry_scores.items()},
                    'features': features,
                    'signals': signals
                }
            }
            
            # Store in history
            self.detection_history.append(result)
            
            # Learn from detection if enabled
            if self.config.get('enable_learning', True):
                await self.learn_from_detection(data, result)
            
            return result
            
        except Exception as e:
            logger.error(f"Error in industry detection: {str(e)}")
            return {
                'industry': 'unknown',
                'confidence': 0.0,
                'sub_type': 'unknown',
                'indicators': [],
                'suggested_analyses': [],
                'metadata': {
                    'detection_method': 'error',
                    'data_quality': 0.0,
                    'execution_time': 0.0,
                    'error': str(e)
                }
            }
    
    def _extract_features(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract features from business data"""
        features = {}
        
        # Check for common business features
        for key, value in data.items():
            if key.lower() in self.feature_weights:
                features[key.lower()] = value
        
        # Check for key indicators in the data keys
        data_keys_lower = [k.lower() for k in data.keys()]
        
        # Retail indicators
        if any(k in data_keys_lower for k in ['products', 'inventory', 'stores', 'sales']):
            features['retail_indicators'] = True
            
        # SaaS indicators  
        if any(k in data_keys_lower for k in ['subscriptions', 'licenses', 'api_usage']):
            features['saas_indicators'] = True
            
        # Additional feature extraction logic
        if 'business_model' in data:
            model = str(data['business_model']).lower()
            if 'subscription' in model:
                features['subscription_model'] = True
            if 'license' in model:
                features['license_fees'] = True
        
        if 'revenue_streams' in data:
            streams = data['revenue_streams']
            if isinstance(streams, list):
                for stream in streams:
                    stream_lower = str(stream).lower()
                    if 'product' in stream_lower:
                        features['product_sales'] = True
                    if 'service' in stream_lower:
                        features['service_revenue'] = True
        
        # Check transaction patterns
        if 'transactions' in data:
            features['transaction_frequency'] = len(data['transactions'])
            if data['transactions']:
                # Check if transactions have subscription type
                subscription_txns = sum(1 for txn in data['transactions'] 
                                      if isinstance(txn, dict) and txn.get('type') == 'subscription')
                if subscription_txns > 0:
                    features['subscription_model'] = True
                    
                # Check for contract patterns (B2B services)
                contract_txns = sum(1 for txn in data['transactions'] 
                                   if isinstance(txn, dict) and txn.get('type') == 'contract')
                if contract_txns > 0:
                    features['service_contracts'] = True
                    features['b2b_services_indicators'] = True
                    
                # Check for regular retail patterns
                regular_txns = sum(1 for txn in data['transactions'] 
                                 if isinstance(txn, dict) and 'product_id' in txn)
                if regular_txns > 0:
                    features['product_catalog'] = True
                    
        # Check metadata
        if 'metadata' in data and isinstance(data['metadata'], dict):
            metadata = data['metadata']
            
            # Business name patterns
            if 'business_name' in metadata:
                business_name = metadata['business_name'].lower()
                if any(word in business_name for word in ['store', 'shop', 'retail', 'market']):
                    features['retail_indicators'] = True
                if any(word in business_name for word in ['cloud', 'soft', 'tech', 'digital']):
                    features['saas_indicators'] = True
                if any(word in business_name for word in ['consulting', 'solutions', 'services', 'enterprise']):
                    features['b2b_services_indicators'] = True
                    
            # Has physical stores
            if metadata.get('has_physical_stores'):
                features['inventory_management'] = True
                features['retail_indicators'] = True
                
            # Billing model
            if metadata.get('billing_model') == 'subscription':
                features['subscription_model'] = True
                features['saas_indicators'] = True
        
        # Check products for patterns
        if 'products' in data and isinstance(data['products'], list):
            for product in data['products']:
                if isinstance(product, dict):
                    # Check for subscription-related fields
                    if any(key in product for key in ['billing', 'category', 'type']):
                        if 'billing' in product and 'monthly' in str(product['billing']).lower():
                            features['subscription_model'] = True
                            features['saas_indicators'] = True
                            features['recurring_billing'] = True
                        if 'type' in product and 'digital' in str(product['type']).lower():
                            features['saas_indicators'] = True
                        if 'category' in product and 'subscription' in str(product['category']).lower():
                            features['subscription_model'] = True
                            features['saas_indicators'] = True
                            features['recurring_billing'] = True
                        # Check for tiered pricing
                        if 'name' in product:
                            product_name = product['name'].lower()
                            if any(tier in product_name for tier in ['basic', 'pro', 'enterprise', 'premium']):
                                features['tiered_pricing'] = True
                                features['saas_indicators'] = True
        
        return features
    
    def _extract_signals(self, data: Dict[str, Any]) -> List[str]:
        """Extract data signals from business data"""
        signals = []
        
        for key in data.keys():
            key_lower = key.lower()
            # Check against known data signals
            for industry, pattern in self.industry_patterns.items():
                if key_lower in pattern['data_signals']:
                    signals.append(key_lower)
                    break
        
        return list(set(signals))
    
    def _calculate_industry_score(self, industry: str, features: Dict[str, Any], 
                                 signals: List[str], data: Dict[str, Any]) -> float:
        """Calculate confidence score for a specific industry"""
        pattern = self.industry_patterns.get(industry, {})
        score = 0.0
        
        # Industry-specific indicators boost
        if industry == 'retail' and features.get('retail_indicators'):
            score += 0.2
        elif industry == 'saas' and features.get('saas_indicators'):
            score += 0.2
        elif industry == 'b2b_services' and features.get('b2b_services_indicators'):
            score += 0.2
        
        # Keyword matching
        text_fields = []
        for key, value in data.items():
            if isinstance(value, str):
                text_fields.append(value.lower())
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, str):
                        text_fields.append(item.lower())
            elif isinstance(value, dict):
                # Check nested dictionaries like metadata
                for sub_key, sub_value in value.items():
                    if isinstance(sub_value, str):
                        text_fields.append(sub_value.lower())
        
        text_content = ' '.join(text_fields)
        keyword_matches = 0
        for keyword in pattern.get('keywords', []):
            if keyword.lower() in text_content:
                keyword_matches += 1
        
        if pattern.get('keywords'):
            keyword_score = keyword_matches / len(pattern['keywords'])
            score += keyword_score * 0.3
        
        # Feature matching
        feature_matches = 0
        feature_weights_sum = 0
        for feature in pattern.get('features', []):
            weight = self.feature_weights.get(feature, 1.0)
            if feature in features:
                feature_matches += weight
            feature_weights_sum += weight
        
        if feature_weights_sum > 0:
            feature_score = feature_matches / feature_weights_sum
            score += feature_score * 0.3
        
        # Signal matching
        signal_matches = 0
        for signal in pattern.get('data_signals', []):
            if signal in signals:
                signal_matches += 1
        
        if pattern.get('data_signals'):
            signal_score = signal_matches / len(pattern['data_signals'])
            score += signal_score * 0.2
        
        # Additional checks for specific patterns
        if industry == 'retail':
            if 'products' in data and 'customers' in data:
                score += 0.1
            if features.get('product_catalog'):
                score += 0.1
        elif industry == 'saas':
            if features.get('subscription_model'):
                score += 0.2
            if features.get('recurring_billing'):
                score += 0.15
            if features.get('tiered_pricing'):
                score += 0.15
            # Check for customer type patterns
            if 'customers' in data and isinstance(data['customers'], list):
                business_customers = sum(1 for c in data['customers'] 
                                       if isinstance(c, dict) and c.get('type') == 'business')
                if business_customers > 0:
                    score += 0.1  # B2B SaaS indicator
        elif industry == 'b2b_services':
            if features.get('service_contracts'):
                score += 0.2
            if features.get('consulting_fees'):
                score += 0.1
            # Check customer types
            if 'customers' in data and isinstance(data['customers'], list):
                enterprise_customers = sum(1 for c in data['customers'] 
                                         if isinstance(c, dict) and c.get('type') == 'enterprise')
                if enterprise_customers > 0:
                    score += 0.15
            # Check for service products
            if 'products' in data and isinstance(data['products'], list):
                service_products = sum(1 for p in data['products'] 
                                     if isinstance(p, dict) and 
                                     (p.get('type') == 'service' or 
                                      'service' in str(p.get('category', '')).lower()))
                if service_products > 0:
                    score += 0.15
        
        return min(score, 1.0)  # Cap score at 1.0
    
    async def improve_detection(self, feedback: Dict[str, Any]) -> Dict[str, Any]:
        """Improve detection based on feedback
        
        Args:
            feedback: Dictionary containing detection feedback
            
        Returns:
            Dictionary with improvement status
        """
        try:
            # Extract feedback data
            detection_id = feedback.get('detection_id')
            correct_industry = feedback.get('correct_industry')
            was_correct = feedback.get('was_correct', False)
            
            # Find the original detection
            original_detection = None
            for detection in self.detection_history:
                if detection.get('id') == detection_id:
                    original_detection = detection
                    break
            
            if not original_detection:
                return {
                    'success': False,
                    'error': 'Detection not found'
                }
            
            # Update performance metrics
            if was_correct:
                self.performance_metrics['correct_detections'] += 1
            
            # Calculate accuracy
            if self.performance_metrics['total_detections'] > 0:
                self.performance_metrics['accuracy'] = (
                    self.performance_metrics['correct_detections'] / 
                    self.performance_metrics['total_detections']
                )
            
            # Learn from incorrect predictions
            if not was_correct and correct_industry:
                # Adjust feature weights based on the correct industry
                pattern = self.industry_patterns.get(correct_industry, {})
                for feature in pattern.get('features', []):
                    if feature in self.feature_weights:
                        # Increase weight slightly
                        self.feature_weights[feature] *= 1.05
            
            # Store feedback
            feedback_record = {
                'timestamp': time.time(),
                'detection_id': detection_id,
                'was_correct': was_correct,
                'correct_industry': correct_industry,
                'original_prediction': original_detection.get('industry'),
                'confidence': original_detection.get('confidence')
            }
            
            # Save to learning history
            self.learning_history.store_operation({
                'type': 'industry_detection',
                'input': feedback_record,
                'result': {'success': was_correct},
                'success': was_correct
            })
            
            return {
                'success': True,
                'metrics': self.performance_metrics,
                'feedback_recorded': feedback_record
            }
            
        except Exception as e:
            logger.error(f"Error improving detection: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def learn_from_detection(self, data: Dict[str, Any], result: Dict[str, Any]) -> None:
        """Learn from detection results
        
        Args:
            data: Original input data
            result: Detection result
        """
        try:
            # Record the detection event
            learning_event = {
                'input_data': data,
                'detection_result': result,
                'timestamp': time.time()
            }
            
            # Store in learning history
            self.learning_history.store_operation({
                'type': 'industry_detection',
                'input': data,
                'result': result,
                'success': result['confidence'] >= 0.7
            })
            
            # Update average confidence
            total_confidence = sum(d.get('confidence', 0) for d in self.detection_history)
            self.performance_metrics['average_confidence'] = (
                total_confidence / len(self.detection_history)
                if self.detection_history else 0.0
            )
            
        except Exception as e:
            logger.error(f"Error in learning from detection: {str(e)}")
    
    def get_supported_industries(self) -> List[str]:
        """Get list of supported industries"""
        return self.supported_industries.copy()
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get performance metrics report"""
        return {
            'metrics': self.performance_metrics.copy(),
            'detection_count': len(self.detection_history),
            'supported_industries': self.supported_industries,
            'feature_weights': self.feature_weights.copy()
        }
    
    def get_detection_history(self) -> List[Dict[str, Any]]:
        """Get detection history"""
        return self.detection_history.copy()
    
    async def get_learning_data(self) -> Dict[str, Any]:
        """Get learning data"""
        return {
            'weights': self.learning_data.weights,
            'patterns': self.learning_data.patterns,
            'history': self.learning_data.history,
            'model_version': self.learning_data.model_version
        }
    
    def export_learned_model(self, path: str) -> None:
        """Export learned model to file"""
        model_data = {
            'weights': self.learning_data.weights,
            'patterns': self.learning_data.patterns,
            'feature_weights': self.feature_weights,
            'industry_patterns': self.industry_patterns,
            'model_version': self.learning_data.model_version,
            'feature_importance': getattr(self.learning_data, 'feature_importance', {})
        }
        
        try:
            with open(path, 'w') as f:
                json.dump(model_data, f, indent=2)
            logger.info(f"Exported model to {path}")
        except Exception as e:
            logger.error(f"Error exporting model: {str(e)}")
            raise
    
    async def import_model(self, path: str) -> Dict[str, Any]:
        """Import model from file"""
        try:
            with open(path, 'r') as f:
                model_data = json.load(f)
            
            self.learning_data.weights = model_data.get('weights', {})
            self.learning_data.patterns = model_data.get('patterns', {})
            self.feature_weights = model_data.get('feature_weights', self.feature_weights)
            self.industry_patterns = model_data.get('industry_patterns', self.industry_patterns)
            self.learning_data.model_version = model_data.get('model_version', '1.0')
            
            return {'success': True, 'model_version': self.learning_data.model_version}
        except Exception as e:
            logger.error(f"Error importing model: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def import_learned_model(self, path: str) -> None:
        """Import learned model from file (sync version)"""
        try:
            with open(path, 'r') as f:
                model_data = json.load(f)
            
            self.learning_data.weights = model_data.get('weights', {})
            self.learning_data.patterns = model_data.get('patterns', {})
            self.learning_data.feature_importance = model_data.get('feature_importance', {})
            self.feature_weights = model_data.get('feature_weights', self.feature_weights)
            self.industry_patterns = model_data.get('industry_patterns', self.industry_patterns)
            self.learning_data.model_version = model_data.get('model_version', '1.0')
            
            logger.info(f"Imported model from {path}")
        except Exception as e:
            logger.error(f"Error importing model: {str(e)}")
            raise
    
    def bulk_detect(self, datasets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Synchronous bulk detection for multiple datasets
        
        Args:
            datasets: List of business data dictionaries
            
        Returns:
            List of detection results
        """
        results = []
        
        for data in datasets:
            # Use async detection in a synchronous context
            import asyncio
            
            # Create event loop if needed
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            # Run async detection
            result = loop.run_until_complete(self.detect_industry(data))
            results.append(result)
        
        return results
    
    def reset(self) -> None:
        """Reset the agent to initial state"""
        self.detection_history.clear()
        self._cache.clear()
        self.performance_metrics = {
            'total_detections': 0,
            'correct_detections': 0,
            'average_confidence': 0.0,
            'accuracy': 0.0
        }
        self._initialize_feature_weights()
        logger.info("Industry Detective Agent reset to initial state")
    
    def _determine_sub_type(self, industry: str, data: Dict[str, Any], features: Dict[str, Any]) -> str:
        """Determine industry sub-type based on data and features"""
        sub_types = {
            'retail': {
                'physical_retail': ['store', 'location', 'pos', 'foot_traffic'],
                'online_retail': ['website', 'ecommerce', 'online', 'shipping'],
                'hybrid': ['omnichannel', 'both', 'online_store', 'physical_store']
            },
            'saas': {
                'b2b_saas': ['enterprise', 'business', 'b2b', 'corporate'],
                'b2c_saas': ['consumer', 'individual', 'b2c', 'personal'],
                'platform': ['marketplace', 'platform', 'ecosystem', 'api']
            },
            'b2b_services': {
                'consulting': ['consulting', 'advisory', 'strategy'],
                'software_services': ['software', 'implementation', 'development', 'solution'],
                'managed_services': ['managed', 'outsourcing', 'support', 'ongoing']
            },
            'manufacturing': {
                'discrete': ['assembly', 'discrete', 'products', 'units'],
                'process': ['continuous', 'process', 'chemical', 'refining'],
                'batch': ['batch', 'lot', 'production_runs']
            },
            'healthcare': {
                'hospital': ['hospital', 'medical_center', 'clinic'],
                'pharmaceutical': ['pharma', 'drug', 'medication'],
                'medical_device': ['device', 'equipment', 'medical_device']
            },
            'financial_services': {
                'banking': ['bank', 'deposit', 'loan', 'account'],
                'investment': ['investment', 'portfolio', 'asset_management'],
                'insurance': ['insurance', 'policy', 'claims', 'premium']
            },
            'hospitality': {
                'hotel': ['hotel', 'accommodation', 'rooms'],
                'restaurant': ['restaurant', 'dining', 'food_service'],
                'travel': ['travel', 'tourism', 'vacation']
            }
        }
        
        industry_sub_types = sub_types.get(industry, {})
        if not industry_sub_types:
            return 'general'
        
        # Check data for matching keywords
        text_content = ' '.join(str(v).lower() for v in data.values() if isinstance(v, str))
        
        scores = {}
        for sub_type, keywords in industry_sub_types.items():
            score = sum(1 for keyword in keywords if keyword in text_content)
            scores[sub_type] = score
        
        if scores:
            return max(scores.items(), key=lambda x: x[1])[0]
        
        return list(industry_sub_types.keys())[0]
    
    def _get_indicators(self, industry: str, data: Dict[str, Any], features: Dict[str, Any]) -> List[str]:
        """Get relevant indicators for the detected industry"""
        indicators_map = {
            'retail': ['high_transaction_volume', 'seasonal_patterns', 'inventory_turnover', 'customer_segmentation'],
            'saas': ['subscription_model', 'recurring_billing', 'tiered_pricing', 'usage_tracking', 'api_integration'],
            'b2b_services': ['project_based', 'contract_value', 'client_relationships', 'service_agreements', 'contract_based', 'enterprise_clients'],
            'manufacturing': ['supply_chain', 'production_metrics', 'quality_control', 'inventory_management'],
            'healthcare': ['patient_data', 'compliance_requirements', 'treatment_protocols', 'medical_records'],
            'financial_services': ['regulatory_compliance', 'risk_metrics', 'transaction_processing', 'portfolio_analysis'],
            'hospitality': ['occupancy_rates', 'booking_patterns', 'guest_services', 'revenue_management']
        }
        
        base_indicators = indicators_map.get(industry, [])
        
        # Add dynamic indicators based on data
        detected_indicators = []
        
        # Check for specific patterns in data
        if 'transactions' in data or 'sales' in data:
            detected_indicators.append('transaction_data')
        
        # Check features for indicators
        if features.get('subscription_model'):
            detected_indicators.append('subscription_model')
        
        if features.get('recurring_billing'):
            detected_indicators.append('recurring_billing')
        
        if features.get('tiered_pricing'):
            detected_indicators.append('tiered_pricing')
            
        # Check for contract-based indicator
        if features.get('service_contracts'):
            detected_indicators.append('contract_based')
            
        # Check for enterprise clients
        if 'customers' in data and isinstance(data['customers'], list):
            enterprise_count = sum(1 for c in data['customers'] 
                                 if isinstance(c, dict) and c.get('type') in ['enterprise', 'large'])
            if enterprise_count > 0:
                detected_indicators.append('enterprise_clients')
            
        if 'inventory' in data:
            detected_indicators.append('inventory_management')
        
        if 'revenue' in data:
            detected_indicators.append('revenue_tracking')
        
        # Combine base and detected indicators and deduplicate
        all_indicators = list(set(base_indicators + detected_indicators))
        
        # Prioritize indicators that match features
        prioritized_indicators = []
        for indicator in all_indicators:
            if indicator in features or indicator in detected_indicators:
                prioritized_indicators.insert(0, indicator)
            else:
                prioritized_indicators.append(indicator)
        
        return prioritized_indicators[:5]  # Return top 5 indicators
    
    def _get_suggested_analyses(self, industry: str) -> List[str]:
        """Get suggested analyses for the detected industry"""
        analyses_map = {
            'retail': ['sales_trend', 'customer_segmentation', 'inventory_optimization', 'seasonal_analysis', 'product_performance'],
            'saas': ['churn_analysis', 'mrr_growth', 'customer_acquisition_cost', 'lifetime_value', 'usage_analytics'],
            'b2b_services': ['project_profitability', 'client_retention', 'project_pipeline', 'contract_analysis', 'service_utilization', 'resource_allocation'],
            'manufacturing': ['production_efficiency', 'quality_metrics', 'supply_chain_optimization', 'cost_analysis', 'capacity_planning'],
            'healthcare': ['patient_outcomes', 'treatment_effectiveness', 'resource_utilization', 'compliance_monitoring', 'operational_efficiency'],
            'financial_services': ['risk_analysis', 'portfolio_performance', 'fraud_detection', 'customer_behavior', 'regulatory_reporting'],
            'hospitality': ['occupancy_optimization', 'revenue_forecasting', 'guest_satisfaction', 'pricing_strategy', 'channel_performance']
        }
        
        return analyses_map.get(industry, ['general_analysis', 'trend_analysis', 'performance_metrics'])
    
    def _assess_data_quality(self, data: Dict[str, Any]) -> float:
        """Assess the quality of input data"""
        quality_score = 0.0
        total_checks = 0
        
        # Check for data completeness
        if data:
            total_checks += 1
            quality_score += 0.2
        
        # Check for key business fields
        key_fields = ['revenue', 'transactions', 'customers', 'products', 'services']
        found_fields = sum(1 for field in key_fields if field in data)
        if found_fields > 0:
            total_checks += 1
            quality_score += (found_fields / len(key_fields)) * 0.35
        
        # Check for data types variety
        data_types = set(type(v).__name__ for v in data.values())
        if len(data_types) > 1:
            total_checks += 1
            quality_score += 0.15
        
        # Check for numeric data
        numeric_values = sum(1 for v in data.values() if isinstance(v, (int, float)))
        if numeric_values > 0:
            total_checks += 1
            quality_score += 0.1
        
        # Check for structured data
        structured_values = sum(1 for v in data.values() if isinstance(v, (list, dict)))
        if structured_values > 0:
            total_checks += 1
            quality_score += 0.2
        
        # Check metadata presence
        if 'metadata' in data and isinstance(data['metadata'], dict):
            total_checks += 1
            quality_score += 0.1
            
        # Check transaction quality
        if 'transactions' in data and isinstance(data['transactions'], list):
            if len(data['transactions']) > 5:
                quality_score += 0.1
        
        return min(quality_score if total_checks > 0 else 0.5, 1.0)
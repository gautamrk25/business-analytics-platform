import React, { useState, useEffect } from 'react';
import { 
  Database, Search, Table, ChevronDown, ChevronRight,
  Lightbulb, LineChart, Calendar, Bird, Target, Zap, Code, Sparkles, Check, AlertTriangle, RefreshCw,
  Brain, Box, Play, Focus, GitBranch, Server, Upload, Monitor, 
  Users, Heart, Cpu, CheckCircle, X, TrendingUp, DollarSign, Film,
  Clock, Repeat, MousePointer, CheckSquare, BarChart, Anchor,
  Mail, Smartphone, Globe, Shield, Bot, Book, LayoutDashboard, Ruler, // Add Ruler for Measure icon
  MeasurePage, // Add MeasurePage for Measure navigation
  Settings, // Add Settings for Operate icon
  Library // Add Library for Resources icon
} from 'lucide-react';
import MLLifecycleDashboard from './MLLifecycleDashboard';
import ActivationDashboard from './ActivationDashboard';
import ActivationFlow from './ActivationFlow';
import OperatePage from './OperatePage';
import ResourcesPage from './ResourcesPage';

// At the top of the file, add DOMAIN_DATA constant
const DOMAIN_DATA = {
  "User & Customer Data Domain": {
    categories: {
      "User Profile & Demographics": [
        { name: "BI.PLUTO_DW.USER_DIM", description: "Core user demographic information" },
        { name: "BI.PLUTO_DW.CLIENT_USER_MAPPING", description: "User-client relationship mapping" },
        { name: "BI.PLUTO_DW.USER_ENTITLEMENTS", description: "User permissions and access rights" },
        { name: "ODIN_PRD.SECURE.USER_DIM", description: "Secure user information" },
        { name: "SANDBOX.ANALYSIS_MARKETING.RETENTION_KPI_WINBACK", description: "User retention analysis" }
      ],
      "User Behavior & Engagement": [
        { name: "BI.PLUTO_DW.USER_BEHAVIOR_FACT", description: "User interaction data" },
        { name: "BI.PLUTO_DW.USER_VIDEO_SEGMENT_FACT", description: "Detailed video viewing segments" },
        { name: "SANDBOX.ANALYSIS_MARKETING.BOUNCE_RATE_MONTHLY", description: "User engagement metrics" },
        { name: "ODIN_PRD.RPT.CUSTOMER_ATTRIBUTE_CONTENT_ENGAGEMENT", description: "Content engagement patterns" }
      ],
      "User Preferences": [
        { name: "BI.PLUTO_DW.USER_PREFERENCES", description: "User settings and preferences" },
        { name: "BI.PLUTO_DW.WATCHLIST", description: "User saved content" },
        { name: "BI.PLUTO_DW.CONTENT_RATINGS", description: "User content ratings" }
      ]
    }
  },
  "Content Data Domain": {
    categories: {
      "Content Metadata": [
        { name: "BI.PLUTO_DW.EPISODE_DIM", description: "Episode information" },
        { name: "BI.PLUTO_DW.SERIES_DIM", description: "Series details" },
        { name: "BI.PLUTO_DW.CLIP_DIM", description: "Clip information" },
        { name: "BI.PLUTO_DW.CHANNEL_DIM", description: "Channel details" },
        { name: "ODIN_PRD.DW_ODIN.CMS_SERIES_DIM", description: "Content management system series data" }
      ],
      "Content Performance": [
        { name: "SANDBOX.ANALYSIS_CONTENT.ASSET_LEVEL_VIEWERSHIP", description: "Content viewing metrics" },
        { name: "SANDBOX.ANALYSIS_CONTENT.VOD_PERFORMANCE_TREND", description: "VOD performance analysis" },
        { name: "RPT.CP_DAILY_CATEGORY", description: "Category performance metrics" },
        { name: "RPT.CP_DAILY_CHANNEL", description: "Channel performance metrics" },
        { name: "RPT.CP_DAILY_EPISODE", description: "Episode performance metrics" }
      ],
      "Content Rights & Licensing": [
        { name: "BI.PLUTO_DW.CONTENT_RIGHTS", description: "Content licensing information" },
        { name: "BI.PLUTO_DW.TERRITORY_RIGHTS", description: "Geographic rights data" },
        { name: "BI.PLUTO_DW.LICENSE_WINDOWS", description: "Content availability windows" }
      ]
    }
  },
  "Streaming & Technical Data Domain": {
    categories: {
      "Quality of Service": [
        { name: "BI.RPT.DQI_DETAILED", description: "Detailed quality indicators" },
        { name: "BI.RPT.DQI_SUMMARY", description: "Summary quality metrics" },
        { name: "BI.ETL.CLIENT_QUALITY_STG", description: "Client streaming quality data" },
        { name: "ODIN_PRD.RPT.AD_LOAD_DASHBOARD", description: "Ad delivery performance" }
      ],
      "Platform & Device": [
        { name: "BI.PLUTO_DW.APP_NAME_DIM", description: "Application information" },
        { name: "ODIN_PRD.DW_ODIN.DEVICE_DIM", description: "Device details" },
        { name: "ODIN_PRD.DW_ODIN.BROWSER_DIM", description: "Browser information" },
        { name: "ODIN_PRD.DW_ODIN.SCREEN_DIM", description: "Screen specifications" }
      ],
      "Technical Performance": [
        { name: "BI.PLUTO_DW.ERROR_EVENTS", description: "Streaming error tracking" },
        { name: "BI.PLUTO_DW.BANDWIDTH_METRICS", description: "Network performance data" },
        { name: "BI.PLUTO_DW.CDN_PERFORMANCE", description: "Content delivery metrics" }
      ]
    }
  },
  "Advertising & Monetization Domain": {
    categories: {
      "Ad Performance": [
        { name: "EXT_FEEDS.FREEWHEEL.DAILY_CONTENT_REPORT", description: "Ad content metrics" },
        { name: "HIST.RPT.SSBI_AD_DELIVERY_FUNNEL", description: "Ad delivery analysis" },
        { name: "SANDBOX.ENGINEERING.AD_EXPERIENCE", description: "Ad experience metrics" },
        { name: "BI.FRM.AD_RIGHTS_LOOKUP_US", description: "Ad rights management" }
      ],
      "Revenue & Business Metrics": [
        { name: "BI.FRM.THE_ROKU_CHANNEL_REVENUE_US", description: "Revenue data" },
        { name: "SANDBOX.ANALYSIS_MARKETING.FORECAST_FINANCE_FORECAST", description: "Financial projections" },
        { name: "BI.RPT.KPI_MONTHLY", description: "Key performance indicators" },
        { name: "BI.RPT.KPI_DAILY", description: "Daily business metrics" }
      ],
      "Advertiser Data": [
        { name: "BI.PLUTO_DW.ADVERTISER_DIM", description: "Advertiser information" },
        { name: "BI.PLUTO_DW.CAMPAIGN_PERFORMANCE", description: "Ad campaign metrics" },
        { name: "BI.PLUTO_DW.AD_INVENTORY", description: "Available ad space data" }
      ]
    }
  },
  "Marketing & Analytics Domain": {
    categories: {
      "Campaign Performance": [
        { name: "EXT_FEEDS.STG.KOCHAVA_ATTRIBUTION_EVENT", description: "Marketing attribution" },
        { name: "SANDBOX.ANALYSIS_MARKETING.KOCHAVA_CAMPAIGNS", description: "Campaign analysis" },
        { name: "SANDBOX.ANALYSIS_MARKETING.UTM_MAPPING", description: "UTM tracking data" },
        { name: "EXT_FEEDS.AMPLITUDE.AMPLITUDE_DAILY", description: "User analytics" }
      ],
      "Customer Acquisition": [
        { name: "SANDBOX.ANALYSIS_MARKETING.MAU_FCAST_MTD_DAILY", description: "Monthly active users forecast" },
        { name: "SANDBOX.ANALYSIS_MARKETING.CONTENT_SUPPLY_DASHBOARD", description: "Content supply metrics" },
        { name: "ODIN_PRD.RPT.REFERRAL_DATA_DAILY", description: "Referral tracking" }
      ],
      "Marketing Analytics": [
        { name: "BI.PLUTO_DW.MARKETING_CHANNEL_PERFORMANCE", description: "Channel effectiveness" },
        { name: "BI.PLUTO_DW.CONVERSION_FUNNEL", description: "User conversion data" },
        { name: "BI.PLUTO_DW.ATTRIBUTION_MODELS", description: "Marketing attribution models" }
      ]
    }
  },
  "Geographic & Location Domain": {
    categories: {
      "Geographic Data": [
        { name: "BI.PLUTO_DW.GEO_DIM", description: "Geographic dimension data" },
        { name: "BI.REFERENCE.COUNTRY_CODE_MAPPING", description: "Country code references" },
        { name: "ODIN_PRD.STG.MAXMIND_GEOCITY_IPV4", description: "IP geolocation data" },
        { name: "BI.REFERENCE.GEO_DIM_XREF", description: "Geographic cross-reference data" }
      ],
      "Regional Performance": [
        { name: "BI.PLUTO_DW.REGIONAL_METRICS", description: "Region-specific performance" },
        { name: "BI.PLUTO_DW.MARKET_PENETRATION", description: "Market reach statistics" },
        { name: "BI.PLUTO_DW.TERRITORY_PERFORMANCE", description: "Territory-level metrics" }
      ],
      "Location Intelligence": [
        { name: "BI.PLUTO_DW.VIEWING_PATTERNS_GEO", description: "Geographic viewing trends" },
        { name: "BI.PLUTO_DW.MARKET_SEGMENTS_GEO", description: "Geographic market segments" },
        { name: "BI.PLUTO_DW.LOCATION_BASED_METRICS", description: "Location-based analytics" }
      ]
    }
  }
};

// Add this constant after the DOMAIN_DATA constant
const sourceTables = {
  userProfile: [
    'BI.PLUTO_DW.USER_DIM',
    'BI.PLUTO_DW.GEO_DIM',
    'BI.PLUTO_DW.USER_ENTITLEMENTS'
  ],
  viewingBehavior: [
    'BI.PLUTO_DW.USER_VIDEO_SEGMENT_FACT',
    'BI.PLUTO_DW.EPISODE_DIM'
  ],
  contentPreferences: [
    'BI.PLUTO_DW.USER_VIDEO_SEGMENT_FACT',
    'BI.PLUTO_DW.EPISODE_DIM'
  ],
  deviceUsage: [
    'BI.PLUTO_DW.CLIENT_USER_MAPPING',
    'BI.PLUTO_DW.APP_NAME_DIM',
    'ODIN_PRD.DW_ODIN.DEVICE_DIM'
  ],
  advancedBehavior: [
    'BI.PLUTO_DW.USER_VIDEO_SEGMENT_FACT',
    'BI.PLUTO_DW.EPISODE_DIM'
  ]
};

const targetViews = {
  userProfile: 'user_360_profile',
  viewingBehavior: 'user_viewing_behavior',
  contentPreferences: 'user_content_preferences',
  deviceUsage: 'user_device_profile',
  advancedBehavior: 'user_advanced_behavior_metrics'
};

// Keep the original transformations for eagle plan
const transformations = {
  userProfile: [
    'Join user demographics with geographic data',
    'Include entitlement and subscription status',
    'Create unified user profile view'
  ],
  viewingBehavior: [
    'Calculate viewing recency (days since last watch)',
    'Determine viewing frequency (distinct viewing days)',
    'Compute total watch duration',
    'Generate RFM scores'
  ],
  contentPreferences: [
    'Analyze genre preferences',
    'Calculate content type distribution',
    'Determine top genres per user',
    'Create genre affinity scores'
  ],
  deviceUsage: [
    'Aggregate device usage patterns',
    'Determine primary device types',
    'Track multi-device usage',
    'Monitor app preferences'
  ],
  advancedBehavior: [
    'Calculate viewing time patterns',
    'Analyze binge-watching behavior',
    'Measure content completion rates',
    'Track platform loyalty metrics'
  ]
};

// Add new transformations for activation use cases
const activationTransformations = {
  highValueUsers: [
    'Propensity Scoring Model',
    'Revenue Prediction Algorithm',
    'Premium Content Affinity Analysis',
    'User Engagement Scoring'
  ],
  retentionRisk: [
    'Churn Prediction Model',
    'Engagement Pattern Analysis',
    'Watch Time Trend Detection',
    'Content Drop-off Analysis'
  ],
  contentRecommendations: [
    'Hybrid Graph Neural Net',
    'Content Similarity Analysis',
    'User Preference Learning',
    'Real-time Recommendation Updates'
  ],
  viewerSegmentation: [
    'Behavioral Clustering Algorithm',
    'Demographic Segmentation',
    'Viewing Pattern Classification',
    'Cross-Channel Analysis'
  ]
};

// Add this constant after the transformations object
const flowDescriptions = {
  userProfile: "Combines demographic and geographic data to create comprehensive user profiles for targeted marketing and personalization",
  viewingBehavior: "Analyzes watch patterns and calculates RFM (Recency, Frequency, Monetary) metrics to understand user engagement",
  contentPreferences: "Determines genre and content type preferences to power content recommendations and programming decisions",
  deviceUsage: "Tracks platform and device patterns to optimize streaming experience across different devices",
  advancedBehavior: "Analyzes detailed viewing patterns including binge-watching behavior and content completion rates"
};

// Update the base fields in the segmentationViews constant
const segmentationViews = {
  base: {
    title: 'Core Segments',
    description: 'Foundation segmentation view combining core user attributes',
    fields: {
      'Viewing Time Patterns': {
        'daily_viewing_hours': 'Average daily viewing duration',
        'peak_viewing_time': 'Most active viewing period',
        'viewing_consistency': 'Regularity of viewing schedule',
        'time_slot_preference': 'Preferred viewing time slots'
      },
      'Weekend vs Weekday Preferences': {
        'weekend_ratio': 'Proportion of weekend viewing',
        'weekday_pattern': 'Active weekdays distribution',
        'weekend_binge_ratio': 'Weekend binge-watching tendency',
        'time_availability': 'Typical viewing availability'
      },
      'Binge Watching Behavior': {
        'binge_frequency': 'Frequency of binge sessions',
        'binge_duration': 'Average binge session length',
        'series_completion': 'Series completion rate',
        'content_marathon': 'Long-session viewing patterns'
      },
      'Platform Usage Patterns': {
        'primary_platform': 'Most used viewing platform',
        'device_switching': 'Cross-device viewing behavior',
        'platform_preference': 'Platform usage distribution',
        'viewing_environment': 'Typical viewing setup'
      },
      'Engagement Metrics': {
        'recency_score': 'High/Medium/Low based on last watch',
        'frequency_score': 'High/Medium/Low based on viewing days',
        'total_hours_watched': 'Total viewing duration',
        'movie_hours': 'Hours spent watching movies',
        'series_hours': 'Hours spent watching series'
      },
      'Content Preferences': {
        'top_genres': 'Array of user\'s top genre preferences',
        'device_type': 'Primary device used for streaming'
      },
      'Base Segments': {
        'engagement_segment': 'Super User/Regular User/At Risk',
        'content_preference_segment': 'Movie Preferred/Series Preferred/Mixed Viewer'
      }
    }
  },
  enhanced: {
    title: 'Advanced Segments',
    description: 'Advanced segmentation with behavioral patterns',
    fields: {
      'Time-Based Patterns': {
        'viewing_time_segment': 'Morning/Afternoon/Prime Time/Night Owl',
        'viewing_pattern_segment': 'Weekend Warrior/Weekday Warrior/Balanced',
        'avg_viewing_hour': 'Average hour of day for viewing',
        'weekend_ratio': 'Proportion of weekend viewing'
      },
      'Content Engagement': {
        'engagement_type_segment': 'Binge Watcher/Content Completionist/Content Sampler/Regular',
        'binge_watched_episodes': 'Count of episodes watched in succession',
        'content_completion_rate': 'Ratio of content watched to completion'
      },
      'Platform Usage': {
        'platform_segment': 'Multi-Platform/TV Purist/Mobile First/Hybrid',
        'device_types_used': 'Number of different devices used',
        'preferred_device': 'Most frequently used device type'
      }
    }
  }
};

// Add these constants after segmentationViews
const sqlQueries = {
  userProfile: {
    code: `CREATE OR REPLACE VIEW user_360_profile AS
SELECT 
    u.user_id,
    u.create_date AS user_create_date,
    u.user_age_range,
    u.user_gender,
    u.registration_platform,
    u.user_language,
    g.country_code,
    g.city,
    g.region,
    g.timezone,
    g.dma_code,
    g.postal_code,
    e.entitlement_level,
    e.subscription_status,
    e.subscription_start_date,
    e.billing_status,
    e.trial_status,
    e.last_payment_date,
    CURRENT_DATE() as profile_generated_date
FROM BI.PLUTO_DW.USER_DIM u
LEFT JOIN BI.PLUTO_DW.GEO_DIM g ON u.geo_id = g.geo_id
LEFT JOIN BI.PLUTO_DW.USER_ENTITLEMENTS e ON u.user_id = e.user_id;`,
    explanation: "Creates a unified user profile by joining demographic, geographic, and subscription data"
  },
  viewingBehavior: {
    code: `CREATE OR REPLACE VIEW user_viewing_behavior AS
WITH viewing_stats AS (
    SELECT 
        uvs.user_id,
        -- Recency
        DATE_DIFF(CURRENT_DATE(), MAX(uvs.viewing_date), DAY) as days_since_last_watch,
        -- Frequency
        COUNT(DISTINCT uvs.viewing_date) as viewing_days_count,
        COUNT(DISTINCT uvs.session_id) as total_sessions,
        -- Monetary (viewing time as proxy)
        SUM(uvs.duration_seconds)/3600 as total_hours_watched,
        SUM(CASE WHEN e.content_type = 'MOVIE' THEN uvs.duration_seconds ELSE 0 END)/3600 as movie_hours,
        SUM(CASE WHEN e.content_type = 'SERIES' THEN uvs.duration_seconds ELSE 0 END)/3600 as series_hours,
        -- Additional metrics
        AVG(uvs.duration_seconds)/60 as avg_session_minutes,
        COUNT(DISTINCT e.series_id) as unique_series_watched,
        COUNT(DISTINCT e.episode_id) as unique_episodes_watched
    FROM BI.PLUTO_DW.USER_VIDEO_SEGMENT_FACT uvs
    JOIN BI.PLUTO_DW.EPISODE_DIM e ON uvs.episode_id = e.episode_id
    WHERE uvs.viewing_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
    GROUP BY uvs.user_id
)
SELECT 
    vb.*,
    -- RFM Scoring
    CASE 
        WHEN days_since_last_watch <= 7 THEN 'High'
        WHEN days_since_last_watch <= 30 THEN 'Medium'
        ELSE 'Low'
    END as recency_score,
    CASE 
        WHEN viewing_days_count >= 20 THEN 'High'
        WHEN viewing_days_count >= 10 THEN 'Medium'
        ELSE 'Low'
    END as frequency_score,
    CASE 
        WHEN total_hours_watched >= 50 THEN 'High'
        WHEN total_hours_watched >= 20 THEN 'Medium'
        ELSE 'Low'
    END as monetary_score,
    CURRENT_TIMESTAMP() as metrics_calculated_at
FROM viewing_stats vb;`,
    explanation: "Analyzes user viewing patterns including recency, frequency, and content type preferences with RFM scoring"
  },
  contentPreferences: {
    code: `CREATE OR REPLACE VIEW user_content_preferences AS
WITH content_affinity AS (
    SELECT 
        uvs.user_id,
        e.primary_genre,
        e.content_type,
        e.content_rating,
        e.release_year,
        COUNT(*) as view_count,
        SUM(uvs.duration_seconds) as total_duration,
        AVG(uvs.duration_seconds/e.total_duration) as avg_completion_rate,
        ROW_NUMBER() OVER (PARTITION BY uvs.user_id ORDER BY COUNT(*) DESC) as genre_rank,
        ROW_NUMBER() OVER (PARTITION BY uvs.user_id ORDER BY SUM(uvs.duration_seconds) DESC) as time_rank
    FROM BI.PLUTO_DW.USER_VIDEO_SEGMENT_FACT uvs
    JOIN BI.PLUTO_DW.EPISODE_DIM e ON uvs.episode_id = e.episode_id
    WHERE uvs.viewing_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
    GROUP BY 
        uvs.user_id, 
        e.primary_genre, 
        e.content_type,
        e.content_rating,
        e.release_year
)
SELECT 
    user_id,
    ARRAY_AGG(IF(genre_rank <= 3, primary_genre, NULL) IGNORE NULLS) as top_genres,
    ARRAY_AGG(IF(time_rank <= 3, primary_genre, NULL) IGNORE NULLS) as top_genres_by_time,
    ARRAY_AGG(STRUCT(
        primary_genre, 
        content_type,
        view_count, 
        total_duration,
        avg_completion_rate,
        content_rating,
        release_year
    )) as content_affinities,
    COUNT(DISTINCT primary_genre) as genre_diversity,
    COUNT(DISTINCT content_type) as content_type_diversity
FROM content_affinity
GROUP BY user_id;`,
    explanation: "Calculates detailed user content preferences and genre affinities based on viewing history and engagement patterns"
  },
  advancedBehavior: {
    code: `CREATE OR REPLACE VIEW user_device_profile AS
SELECT 
    cum.user_id,
    -- Device Usage Patterns
    COUNT(DISTINCT cum.device_id) as total_devices_used,
    COUNT(DISTINCT and.app_name) as total_apps_used,
    MODE(d.device_type) as primary_device_type,
    MODE(and.app_name) as primary_app,
    -- Platform Distribution
    ARRAY_AGG(STRUCT(
        d.device_type,
        COUNT(*) as session_count,
        SUM(uvs.duration_seconds)/3600 as hours_watched
    )) as platform_usage,
    -- Cross-Platform Behavior
    COUNT(DISTINCT d.device_type) as device_type_diversity,
    COUNT(DISTINCT d.platform_os) as os_diversity,
    -- Time-based Patterns
    ARRAY_AGG(STRUCT(
        EXTRACT(HOUR FROM uvs.viewing_start_time) as hour_of_day,
        d.device_type,
        COUNT(*) as session_count
    )) as hourly_device_preference,
    -- Quality Metrics
    AVG(uvs.buffer_ratio) as avg_buffer_ratio,
    AVG(uvs.bitrate) as avg_bitrate,
    COUNT(DISTINCT CASE WHEN uvs.error_count > 0 THEN uvs.session_id END) as error_sessions
FROM BI.PLUTO_DW.CLIENT_USER_MAPPING cum
JOIN BI.PLUTO_DW.APP_NAME_DIM and ON cum.app_id = and.app_id
JOIN ODIN_PRD.DW_ODIN.DEVICE_DIM d ON cum.device_id = d.device_id
LEFT JOIN BI.PLUTO_DW.USER_VIDEO_SEGMENT_FACT uvs ON cum.user_id = uvs.user_id
    AND cum.device_id = uvs.device_id
WHERE uvs.viewing_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
GROUP BY cum.user_id;`,
    explanation: "Analyzes device usage patterns, platform preferences, and streaming quality metrics across different devices"
  },
  enhancedSegments: {
    code: `CREATE OR REPLACE VIEW user_advanced_behavior_metrics AS
WITH user_metrics AS (
    SELECT 
        uvs.user_id,
        -- Time Patterns
        AVG(EXTRACT(HOUR FROM viewing_start_time)) as avg_viewing_hour,
        COUNTIF(EXTRACT(DAYOFWEEK FROM viewing_date) IN (1, 7)) / COUNT(*) as weekend_ratio,
        -- Binge Watching
        COUNT(DISTINCT CASE 
            WHEN duration_seconds >= 1800 AND 
                TIMESTAMP_DIFF(LEAD(viewing_start_time) OVER(
                    PARTITION BY user_id, series_id ORDER BY viewing_start_time
                ), viewing_start_time, MINUTE) <= 30
            THEN episode_id 
        END) as binge_watched_episodes,
        -- Content Completion
        AVG(CASE 
            WHEN duration_seconds/NULLIF(e.total_duration, 0) >= 0.9 THEN 1
            ELSE 0
        END) as content_completion_rate,
        -- Session Analysis
        COUNT(DISTINCT session_id) as total_sessions,
        AVG(duration_seconds) as avg_session_duration,
        -- Series Commitment
        COUNT(DISTINCT series_id) as unique_series_count,
        MAX(episodes_per_series) as max_episodes_per_series,
        -- Social Viewing
        COUNT(DISTINCT CASE WHEN concurrent_viewers > 1 THEN session_id END) as social_viewing_sessions
    FROM BI.PLUTO_DW.USER_VIDEO_SEGMENT_FACT uvs
    JOIN BI.PLUTO_DW.EPISODE_DIM e ON uvs.episode_id = e.episode_id
    CROSS JOIN (
        SELECT 
            user_id,
            series_id,
            COUNT(DISTINCT episode_id) as episodes_per_series
        FROM BI.PLUTO_DW.USER_VIDEO_SEGMENT_FACT
        GROUP BY user_id, series_id
    )
    WHERE viewing_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
    GROUP BY user_id
)
SELECT 
    *,
    -- Advanced Segmentation
    CASE 
        WHEN avg_viewing_hour < 12 THEN 'Morning Viewer'
        WHEN avg_viewing_hour < 17 THEN 'Afternoon Viewer'
        WHEN avg_viewing_hour < 22 THEN 'Prime Time Viewer'
        ELSE 'Night Owl'
    END as viewing_time_segment,
    CASE 
        WHEN weekend_ratio > 0.7 THEN 'Weekend Warrior'
        WHEN weekend_ratio < 0.3 THEN 'Weekday Warrior'
        ELSE 'Balanced Viewer'
    END as viewing_pattern_segment,
    CASE 
        WHEN binge_watched_episodes > 10 AND content_completion_rate > 0.8 THEN 'Binge Watcher'
        WHEN content_completion_rate > 0.9 THEN 'Content Completionist'
        WHEN content_completion_rate < 0.3 THEN 'Content Sampler'
        ELSE 'Regular Viewer'
    END as engagement_type_segment
FROM user_metrics;`,
    explanation: "Generates comprehensive behavioral metrics including viewing patterns, binge-watching behavior, and advanced user segmentation"
  }
};

// Basic Card component replacement
const Card = ({ children, className = '' }) => (
  <div className={`bg-white dark:bg-gray-800 rounded-lg shadow-lg text-sm ${className}`}>
    {children}
  </div>
);

// Update the TabButton component styling
const TabButton = ({ active, icon: Icon, children, onClick }) => (
  <button
    onClick={onClick}
    className={`flex items-center gap-1 px-3 py-1.5 rounded-lg text-sm transition-colors
      ${active 
        ? 'bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300' 
        : 'hover:bg-gray-100 dark:hover:bg-gray-700'
      }`}
  >
    <Icon className="w-3.5 h-3.5" />
    {children}
  </button>
);

// Add this function before the return statement in ParamountDataProduct component
const renderPlaceholderContent = (title) => (
  <Card className="w-full p-8">
    <div className="text-center">
      <h2 className="text-2xl font-semibold mb-4">{title}</h2>
      <p className="text-gray-600 dark:text-gray-400">Content coming soon...</p>
    </div>
  </Card>
);

// Add this constant for SQL flow labels
const sqlFlowLabels = {
  userProfile: 'User Profile',
  viewingBehavior: 'Viewing Behavior',
  contentPreferences: 'Content Preferences',
  advancedBehavior: 'Device Usage',
  enhancedSegments: 'Advanced Behavior Metrics'
};

// Add this constant for step icons
const stepIcons = {
  generate: RefreshCw,
  validate: AlertTriangle,
  results: Check
};

const steps = [
  { id: 'generate', label: 'Generate Synthetic Data' },
  { id: 'validate', label: 'Run Validations' },
  { id: 'results', label: 'View Results' }
];

// Add this constant for generation profiles
const generationProfiles = {
  realistic: {
    label: 'Realistic',
    description: 'Based on production patterns'
  },
  extreme: {
    label: 'Extreme',
    description: 'Edge cases and stress testing'
  },
  random: {
    label: 'Random',
    description: 'Completely randomized data'
  },
  custom: {
    label: 'Custom',
    description: 'Custom configuration'
  }
};

// Add this constant for ML metrics
const mlMetrics = {
  modelPerformance: {
    accuracy: '97.8%',
    precision: '96.5%',
    recall: '95.9%',
    f1Score: '96.2%',
    auc: '0.989'
  },
  trainingMetrics: {
    trainingTime: '2.5 hours',
    epochs: '100',
    batchSize: '256',
    learningRate: '0.001'
  },
  predictionLatency: {
    p50: '45ms',
    p90: '78ms',
    p99: '125ms'
  }
};

// Update the flows constant to include all 5 flows
const flows = {
  userProfile: {
    title: 'User Profile',
    syntheticData: {
      rowCount: 1000,
      sampleData: [
        { user_id: 'U1001', user_age_range: '25-34', country_code: 'US', entitlement_level: 'PREMIUM' },
        { user_id: 'U1002', user_age_range: '18-24', country_code: 'CA', entitlement_level: 'BASIC' }
      ],
      distributions: {
        age_ranges: { '18-24': '20%', '25-34': '35%', '35-44': '25%', '45+': '20%' },
        countries: { 'US': '60%', 'CA': '20%', 'UK': '15%', 'Other': '5%' }
      }
    },
    validations: [
      { 
        name: 'Completeness Check',
        description: 'Verify all required fields are present',
        status: 'passed',
        details: '100% of required fields present'
      },
      {
        name: 'Referential Integrity',
        description: 'Check all foreign key relationships',
        status: 'passed',
        details: 'All relationships validated'
      },
      {
        name: 'Data Type Consistency',
        description: 'Verify data type mappings',
        status: 'warning',
        details: 'Some timezone fields need standardization'
      }
    ]
  },
  viewingBehavior: {
    title: 'Viewing Behavior',
    syntheticData: {
      rowCount: 5000,
      sampleData: [
        { user_id: 'U1001', viewing_date: '2024-03-01', duration_seconds: 3600, content_type: 'MOVIE' },
        { user_id: 'U1002', viewing_date: '2024-03-01', duration_seconds: 1800, content_type: 'SERIES' }
      ],
      distributions: {
        content_types: { 'MOVIE': '40%', 'SERIES': '60%' },
        viewing_times: { 'Morning': '20%', 'Afternoon': '30%', 'Evening': '50%' }
      }
    },
    validations: [
      {
        name: 'Time Series Integrity',
        description: 'Validate viewing date sequences',
        status: 'passed',
        details: 'All timestamps in valid range'
      },
      {
        name: 'Metric Calculations',
        description: 'Verify RFM score calculations',
        status: 'passed',
        details: 'All metrics accurately computed'
      }
    ]
  },
  contentPreferences: {
    title: 'Content Preferences',
    syntheticData: {
      rowCount: 3000,
      sampleData: [
        { user_id: 'U1001', primary_genre: 'ACTION', content_type: 'SERIES', view_count: 45, completion_rate: 0.85 },
        { user_id: 'U1002', primary_genre: 'COMEDY', content_type: 'MOVIE', view_count: 23, completion_rate: 0.92 }
      ],
      distributions: {
        genres: { 'ACTION': '30%', 'COMEDY': '25%', 'DRAMA': '20%', 'OTHER': '25%' },
        content_types: { 'SERIES': '65%', 'MOVIE': '35%' }
      }
    },
    validations: [
      {
        name: 'Genre Distribution Check',
        description: 'Verify genre distribution matches expected patterns',
        status: 'passed',
        details: 'Genre distributions within 2% of expected values'
      },
      {
        name: 'Content Type Analysis',
        description: 'Validate content type distributions',
        status: 'passed',
        details: 'Content type ratios match expected patterns'
      }
    ]
  },
  deviceUsage: {
    title: 'Device Usage',
    syntheticData: {
      rowCount: 4000,
      sampleData: [
        { user_id: 'U1001', device_type: 'SMART_TV', app_name: 'ROKU', session_count: 120 },
        { user_id: 'U1002', device_type: 'MOBILE', app_name: 'IOS_APP', session_count: 85 }
      ],
      distributions: {
        devices: { 'SMART_TV': '45%', 'MOBILE': '30%', 'TABLET': '15%', 'WEB': '10%' },
        platforms: { 'ROKU': '40%', 'IOS_APP': '30%', 'ANDROID_APP': '20%', 'WEB_APP': '10%' }
      }
    },
    validations: [
      {
        name: 'Device Type Validation',
        description: 'Verify device type distributions',
        status: 'passed',
        details: 'Device usage patterns validated'
      },
      {
        name: 'Platform Analysis',
        description: 'Check platform distribution patterns',
        status: 'passed',
        details: 'Platform usage metrics verified'
      }
    ]
  },
  advancedBehavior: {
    title: 'Advanced Behavior Metrics',
    syntheticData: {
      rowCount: 5000,
      sampleData: [
        { user_id: 'U1001', binge_sessions: 12, avg_session_duration: 125, peak_viewing_hour: 20 },
        { user_id: 'U1002', binge_sessions: 8, avg_session_duration: 95, peak_viewing_hour: 21 }
      ],
      distributions: {
        viewing_times: { 'MORNING': '15%', 'AFTERNOON': '25%', 'EVENING': '45%', 'NIGHT': '15%' },
        engagement_levels: { 'HIGH': '20%', 'MEDIUM': '50%', 'LOW': '30%' }
      }
    },
    validations: [
      {
        name: 'Behavioral Pattern Check',
        description: 'Validate viewing patterns and behaviors',
        status: 'passed',
        details: 'Behavioral metrics properly computed'
      },
      {
        name: 'Time-based Analysis',
        description: 'Verify temporal patterns',
        status: 'passed',
        details: 'Time-based metrics validated'
      }
    ]
  }
};

// Add this function before renderPelicanValidate
const renderResults = (selectedValidationFlow) => {
  const metrics = flowQualityMetrics[selectedValidationFlow];

  return (
    <div className="space-y-6">
      <div className="bg-gray-50 p-4 rounded-lg">
        <h3 className="font-semibold mb-4">Comprehensive Data Quality Assessment</h3>
        <div className="grid grid-cols-2 gap-6">
          {/* Data Quality Metrics */}
          <div className="space-y-4">
            <div className="p-4 bg-white rounded-lg">
              <h4 className="font-medium mb-4">Core Data Quality Dimensions</h4>
              <div className="space-y-3">
                {/* Completeness */}
                <div className="border-b pb-3">
                  <h5 className="text-sm font-medium mb-2">Completeness Analysis</h5>
                  <div className="grid grid-cols-2 gap-2 text-sm">
                    <div>Required Fields</div>
                    <div className="text-right font-medium text-green-600">{metrics.completeness.requiredFields}</div>
                    <div>Optional Fields</div>
                    <div className="text-right font-medium text-green-600">{metrics.completeness.optionalFields}</div>
                    <div>Non-null Values</div>
                    <div className="text-right font-medium text-green-600">{metrics.completeness.nonNullValues}</div>
                    <div>Population Coverage</div>
                    <div className="text-right font-medium text-green-600">{metrics.completeness.populationCoverage}</div>
                  </div>
                </div>

                {/* Accuracy */}
                <div className="border-b pb-3">
                  <h5 className="text-sm font-medium mb-2">Accuracy Verification</h5>
                  <div className="grid grid-cols-2 gap-2 text-sm">
                    <div>Value Precision</div>
                    <div className="text-right font-medium text-green-600">99.9%</div>
                    <div>Format Compliance</div>
                    <div className="text-right font-medium text-green-600">100%</div>
                    <div>Range Validation</div>
                    <div className="text-right font-medium text-green-600">99.8%</div>
                    <div>Business Rule Conformity</div>
                    <div className="text-right font-medium text-green-600">99.7%</div>
                  </div>
                </div>

                {/* Consistency */}
                <div className="border-b pb-3">
                  <h5 className="text-sm font-medium mb-2">Data Consistency</h5>
                  <div className="grid grid-cols-2 gap-2 text-sm">
                    <div>Cross-field Validation</div>
                    <div className="text-right font-medium text-green-600">99.7%</div>
                    <div>Referential Integrity</div>
                    <div className="text-right font-medium text-green-600">100%</div>
                    <div>Schema Conformity</div>
                    <div className="text-right font-medium text-green-600">100%</div>
                    <div>Temporal Consistency</div>
                    <div className="text-right font-medium text-green-600">99.9%</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Advanced Validations */}
          <div className="space-y-4">
            {/* Statistical Analysis */}
            <div className="p-4 bg-white rounded-lg">
              <h4 className="font-medium mb-3">Statistical Validation</h4>
              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-sm">Distribution Match</span>
                  <span className="font-medium text-green-600">99.8%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm">Outlier Detection</span>
                  <span className="font-medium text-green-600">99.9%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm">Pattern Recognition</span>
                  <span className="font-medium text-green-600">99.5%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm">Anomaly Detection</span>
                  <span className="font-medium text-green-600">99.7%</span>
                </div>
              </div>
            </div>

            {/* Technical Validation */}
            <div className="p-4 bg-white rounded-lg">
              <h4 className="font-medium mb-3">Technical Quality</h4>
              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-sm">Data Type Consistency</span>
                  <span className="font-medium text-green-600">100%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm">Encoding Validation</span>
                  <span className="font-medium text-green-600">100%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm">Index Effectiveness</span>
                  <span className="font-medium text-green-600">99.8%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm">Query Performance</span>
                  <span className="font-medium text-green-600">99.9%</span>
                </div>
              </div>
            </div>

            {/* Business Rules */}
            <div className="p-4 bg-white rounded-lg">
              <h4 className="font-medium mb-3">Business Rule Validation</h4>
              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-sm">Domain Rules</span>
                  <span className="font-medium text-green-600">99.9%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm">Relationship Rules</span>
                  <span className="font-medium text-green-600">99.8%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm">Computation Rules</span>
                  <span className="font-medium text-green-600">100%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm">Transformation Rules</span>
                  <span className="font-medium text-green-600">99.9%</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Add the WorkflowStep component
const WorkflowStep = ({ icon: Icon, title, description, subSteps, isLast }) => (
  <div className="flex items-center gap-4">
    <div className="w-8 h-8 rounded-full flex items-center justify-center bg-gray-100">
      <Icon className="w-4 h-4 text-gray-600" />
    </div>
    <div>
      <h3 className="font-medium">{title}</h3>
      <p className="text-sm text-gray-600">{description}</p>
      {subSteps && subSteps.length > 0 && (
        <div className="mt-2 space-y-2">
          {subSteps.map((subStep, idx) => (
            <div key={subStep.id} className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-gray-300" />
              <span className="text-sm text-gray-600">{subStep.label}</span>
            </div>
          ))}
        </div>
      )}
      {isLast && (
        <div className="mt-2 h-px bg-gray-300" />
      )}
    </div>
  </div>
);

// Add this constant for flow-specific quality metrics
const flowQualityMetrics = {
  userProfile: {
    completeness: {
      requiredFields: '100%',
      optionalFields: '98.5%',
      nonNullValues: '99.2%',
      populationCoverage: '99.8%'
    },
    accuracy: {
      valuePrecision: '99.9%',
      formatCompliance: '100%',
      rangeValidation: '99.8%',
      businessRuleConformity: '99.7%'
    },
    consistency: {
      crossFieldValidation: '99.7%',
      referentialIntegrity: '100%',
      schemaConformity: '100%',
      temporalConsistency: '99.9%'
    },
    statistical: {
      distributionMatch: '99.8%',
      outlierDetection: '99.9%',
      patternRecognition: '99.5%',
      anomalyDetection: '99.7%'
    },
    technical: {
      dataTypeConsistency: '100%',
      encodingValidation: '100%',
      indexEffectiveness: '99.8%',
      queryPerformance: '99.9%'
    },
    business: {
      domainRules: '99.9%',
      relationshipRules: '99.8%',
      computationRules: '100%',
      transformationRules: '99.9%'
    }
  },
  viewingBehavior: {
    completeness: {
      requiredFields: '99.9%',
      optionalFields: '97.8%',
      nonNullValues: '98.5%',
      populationCoverage: '99.5%'
    },
    accuracy: {
      valuePrecision: '99.7%',
      formatCompliance: '99.9%',
      rangeValidation: '99.6%',
      businessRuleConformity: '98.9%'
    },
    consistency: {
      crossFieldValidation: '99.5%',
      referentialIntegrity: '99.8%',
      schemaConformity: '99.9%',
      temporalConsistency: '100%'
    },
    statistical: {
      distributionMatch: '98.9%',
      outlierDetection: '99.5%',
      patternRecognition: '98.8%',
      anomalyDetection: '99.2%'
    },
    technical: {
      dataTypeConsistency: '99.9%',
      encodingValidation: '99.9%',
      indexEffectiveness: '99.5%',
      queryPerformance: '99.7%'
    },
    business: {
      domainRules: '99.5%',
      relationshipRules: '99.4%',
      computationRules: '99.8%',
      transformationRules: '99.6%'
    }
  },
  contentPreferences: {
    completeness: {
      requiredFields: '99.8%',
      optionalFields: '96.5%',
      nonNullValues: '97.8%',
      populationCoverage: '98.9%'
    },
    accuracy: {
      valuePrecision: '98.9%',
      formatCompliance: '99.7%',
      rangeValidation: '99.2%',
      businessRuleConformity: '98.5%'
    },
    consistency: {
      crossFieldValidation: '98.8%',
      referentialIntegrity: '99.5%',
      schemaConformity: '99.7%',
      temporalConsistency: '99.4%'
    },
    statistical: {
      distributionMatch: '97.8%',
      outlierDetection: '98.9%',
      patternRecognition: '98.2%',
      anomalyDetection: '98.7%'
    },
    technical: {
      dataTypeConsistency: '99.8%',
      encodingValidation: '99.7%',
      indexEffectiveness: '99.2%',
      queryPerformance: '99.5%'
    },
    business: {
      domainRules: '98.9%',
      relationshipRules: '98.7%',
      computationRules: '99.2%',
      transformationRules: '98.9%'
    }
  },
  deviceUsage: {
    completeness: {
      requiredFields: '99.7%',
      optionalFields: '95.8%',
      nonNullValues: '97.2%',
      populationCoverage: '98.5%'
    },
    accuracy: {
      valuePrecision: '98.5%',
      formatCompliance: '99.5%',
      rangeValidation: '98.9%',
      businessRuleConformity: '98.2%'
    },
    consistency: {
      crossFieldValidation: '98.5%',
      referentialIntegrity: '99.2%',
      schemaConformity: '99.5%',
      temporalConsistency: '99.1%'
    },
    statistical: {
      distributionMatch: '97.5%',
      outlierDetection: '98.7%',
      patternRecognition: '97.9%',
      anomalyDetection: '98.4%'
    },
    technical: {
      dataTypeConsistency: '99.7%',
      encodingValidation: '99.5%',
      indexEffectiveness: '98.9%',
      queryPerformance: '99.3%'
    },
    business: {
      domainRules: '98.7%',
      relationshipRules: '98.5%',
      computationRules: '99.0%',
      transformationRules: '98.7%'
    }
  },
  advancedBehavior: {
    completeness: {
      requiredFields: '99.5%',
      optionalFields: '94.8%',
      nonNullValues: '96.5%',
      populationCoverage: '98.2%'
    },
    accuracy: {
      valuePrecision: '98.2%',
      formatCompliance: '99.3%',
      rangeValidation: '98.7%',
      businessRuleConformity: '97.9%'
    },
    consistency: {
      crossFieldValidation: '98.2%',
      referentialIntegrity: '99.0%',
      schemaConformity: '99.3%',
      temporalConsistency: '98.9%'
    },
    statistical: {
      distributionMatch: '97.2%',
      outlierDetection: '98.5%',
      patternRecognition: '97.5%',
      anomalyDetection: '98.2%'
    },
    technical: {
      dataTypeConsistency: '99.5%',
      encodingValidation: '99.3%',
      indexEffectiveness: '98.7%',
      queryPerformance: '99.1%'
    },
    business: {
      domainRules: '98.5%',
      relationshipRules: '98.2%',
      computationRules: '98.8%',
      transformationRules: '98.5%'
    }
  }
};

// Update the useCases constant to match the exact use cases
const useCases = {
  highValueUsers: {
    title: "Target High-Value Users",
    description: "Identify and target users likely to upgrade to premium subscriptions",
    icon: Users
  },
  retentionRisk: {
    title: "Retention Risk Analysis",
    description: "Identify at-risk users for retention campaigns",
    icon: Heart
  },
  contentRecommendations: {
    title: "Content Recommendations",
    description: "Personalize content recommendations based on viewing patterns",
    icon: Cpu
  },
  viewerSegmentation: {
    title: "Viewer Segmentation",
    description: "Tailor marketing campaigns to specific viewer segments",
    icon: Target
  }
};

// Update kpiDefinitions to include icons for all KPIs
const kpiDefinitions = {
  highValueUsers: [
    {
      name: "Premium Conversion Rate",
      description: "% of targeted users who upgrade to premium",
      calculation: "Number of Premium Upgrades / Total Targeted Users * 100",
      icon: TrendingUp
    },
    {
      name: "Average Revenue Per User (ARPU)",
      description: "Monthly revenue per user",
      calculation: "Total Monthly Revenue / Total Active Users",
      icon: DollarSign
    },
    {
      name: "Premium Trial Activation Rate",
      description: "% of users who start premium trial",
      calculation: "Number of Trial Activations / Total Targeted Users * 100",
      icon: Play
    },
    {
      name: "Premium Content Engagement",
      description: "Hours watched of premium content",
      calculation: "Total Hours of Premium Content Watched per User",
      icon: Film
    }
  ],
  retentionRisk: [
    {
      name: "Churn Risk Score",
      description: "ML model probability of churn (0-100%)",
      calculation: "ML Model Churn Probability Score (0-100)",
      icon: AlertTriangle
    },
    {
      name: "Engagement Trend",
      description: "% change in weekly viewing hours",
      calculation: "(Current Week Hours - Previous Week Hours) / Previous Week Hours * 100",
      icon: LineChart
    },
    {
      name: "Days Since Last Watch",
      description: "Inactive days counter",
      calculation: "Current Date - Last Watch Date",
      icon: Clock
    },
    {
      name: "Content Completion Rate",
      description: "% of started content completed",
      calculation: "Number of Completed Views / Number of Started Views * 100",
      icon: CheckCircle
    },
    {
      name: "Platform Visit Frequency",
      description: "Average weekly sessions",
      calculation: "Total Weekly Sessions / Number of Active Users",
      icon: Repeat
    },
    {
      name: "Customer Satisfaction Score",
      description: "User feedback score (1-10)",
      calculation: "Average of User Feedback Scores (1-10 scale)",
      icon: Heart
    }
  ],
  contentRecommendations: [
    {
      name: "Recommendation Click-Through Rate",
      description: "% of recommendations clicked",
      calculation: "Clicks on Recommendations / Total Recommendations Shown * 100",
      icon: MousePointer
    },
    {
      name: "Watch Completion Rate",
      description: "% of recommended content completed",
      calculation: "Completed Recommended Views / Started Recommended Views * 100",
      icon: CheckSquare
    },
    {
      name: "Time to First Watch",
      description: "Minutes until recommended content watched",
      calculation: "Average Time Between Recommendation and First Watch",
      icon: Clock
    },
    {
      name: "Discovery Success Rate",
      description: "% of users finding new content",
      calculation: "Users Watching New Content / Total Users Receiving Recommendations * 100",
      icon: Search
    }
  ],
  viewerSegmentation: [
    {
      name: "Campaign Response Rate",
      description: "% customers within a segment engaging with campaigns",
      calculation: "Number of Campaign Engagements / Total Segment Size * 100",
      icon: BarChart
    },
    {
      name: "Segment Stability Index",
      description: "% of users staying in segment",
      calculation: "Users Remaining in Segment / Initial Segment Size * 100",
      icon: Anchor
    },
    {
      name: "Cross-Segment Migration",
      description: "% of users changing segments",
      calculation: "Users Changed Segments / Total Users * 100",
      icon: GitBranch
    },
    {
      name: "Revenue Impact per Segment",
      description: "Revenue change by segment",
      calculation: "(Current Segment Revenue - Previous Segment Revenue) / Previous Segment Revenue * 100",
      icon: TrendingUp
    }
  ]
};

// Add channels configuration
const activationChannels = {
  highValueUsers: [
    { name: 'Email', icon: Mail },
    { name: 'Mobile', icon: Smartphone },
    { name: 'Ads', icon: Target },
    { name: 'Dashboards', icon: BarChart }
  ],
  retentionRisk: [
    { name: 'Email', icon: Mail },
    { name: 'Mobile', icon: Smartphone },
    { name: 'Web', icon: Globe },
    { name: 'Dashboards', icon: BarChart }
  ],
  contentRecommendations: [
    { name: 'Web', icon: Globe },
    { name: 'Mobile', icon: Smartphone },
    { name: 'Email', icon: Mail }
  ],
  viewerSegmentation: [
    { name: 'Dashboards', icon: BarChart },
    { name: 'Email', icon: Mail },
    { name: 'Ads', icon: Target }
  ]
};

// Update algorithm definitions to include all use cases
const algorithmDefinitions = {
  highValueUsers: [
    {
      name: "Propensity Scoring Model",
      description: "Machine learning model that calculates likelihood scores for users to upgrade to premium subscriptions based on engagement patterns and demographics.",
    },
    {
      name: "Revenue Prediction Algorithm",
      description: "Forecasting model that predicts potential revenue from users based on their viewing habits and subscription history.",
    },
    {
      name: "Premium Content Affinity Analysis",
      description: "Algorithm that analyzes user interaction with premium content to identify potential premium subscribers.",
    },
    {
      name: "User Engagement Scoring",
      description: "Scoring system that evaluates user engagement levels across different content types and platforms.",
    }
  ],
  retentionRisk: [
    {
      name: "Churn Prediction Model",
      description: "Predictive model that identifies users at risk of cancellation using behavioral and engagement signals.",
    },
    {
      name: "Engagement Pattern Analysis",
      description: "Algorithm that detects changes in user engagement patterns that may indicate churn risk.",
    },
    {
      name: "Watch Time Trend Detection",
      description: "Time series analysis that identifies declining trends in user watch time and engagement.",
    },
    {
      name: "Content Drop-off Analysis",
      description: "Algorithm that analyzes where users stop watching content to identify engagement issues.",
    }
  ],
  contentRecommendations: [
    {
      name: "Hybrid Graph Neural Net",
      description: "Advanced deep learning model that combines user-item interactions and content features in a graph structure. Chosen for its ability to capture complex relationships and provide more accurate personalized recommendations.",
    },
    {
      name: "Content Similarity Analysis",
      description: "Analyzes content metadata and viewing patterns to identify similar content. Selected for its effectiveness in finding content with similar themes and attributes.",
    },
    {
      name: "User Preference Learning",
      description: "Dynamic model that learns and adapts to changing user preferences over time. Chosen for its ability to capture evolving user interests and viewing habits.",
    },
    {
      name: "Real-time Recommendation Updates",
      description: "Streaming algorithm that updates recommendations based on recent user interactions. Selected for providing fresh and relevant recommendations as user behavior changes.",
    }
  ],
  viewerSegmentation: [
    {
      name: "Behavioral Clustering Algorithm",
      description: "Machine learning clustering model that groups users based on similar viewing behaviors and preferences.",
    },
    {
      name: "Demographic Segmentation",
      description: "Algorithm that creates user segments based on demographic attributes and subscription types.",
    },
    {
      name: "Viewing Pattern Classification",
      description: "Classification model that categorizes users based on their content consumption patterns.",
    },
    {
      name: "Cross-Channel Analysis",
      description: "Algorithm that analyzes user behavior across different platforms and devices to create unified segments.",
    }
  ]
};

const ParamountDataProduct = () => {
  const [activeTab, setActiveTab] = useState("use-cases");
  const [searchTerm, setSearchTerm] = useState("");
  const [expandedDomains, setExpandedDomains] = useState({});
  const [selectedFlow, setSelectedFlow] = useState(null);
  const [expandedView, setExpandedView] = useState(null);
  const [showTooltip, setShowTooltip] = useState(null);
  const [selectedSqlFlow, setSelectedSqlFlow] = useState('userProfile');
  const [selectedValidationFlow, setSelectedValidationFlow] = useState('userProfile');
  const [activeValidationStep, setActiveValidationStep] = useState('generate');
  const [showValidationResults, setShowValidationResults] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [progress, setProgress] = useState(0);
  const [timeRemaining, setTimeRemaining] = useState(5);
  const [generationComplete, setGenerationComplete] = useState(false);
  const [selectedProfile, setSelectedProfile] = useState('realistic');
  const [isValidationPipelineExpanded, setIsValidationPipelineExpanded] = useState(true);
  const [isVertexAIExpanded, setIsVertexAIExpanded] = useState(true);
  const [selectedUseCase, setSelectedUseCase] = useState('high-value');
  const [selectedPhase, setSelectedPhase] = useState('feature-mgmt');
  const [activationUseCase, setActivationUseCase] = useState(null);
  const [selectedKPI, setSelectedKPI] = useState(null);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [selectedAlgorithm, setSelectedAlgorithm] = useState(null);
  const [isAlgorithmDialogOpen, setIsAlgorithmDialogOpen] = useState(false);
  const [showDataPlatformDialog, setShowDataPlatformDialog] = useState(false);
  const [showBusinessContextDialog, setShowBusinessContextDialog] = useState(false);
  // Add state for dialog visibility
  const [showDataCatalogDialog, setShowDataCatalogDialog] = useState(false);

  const toggleDomain = (domain) => {
    setExpandedDomains(prev => ({
      ...prev,
      [domain]: !prev[domain]
    }));
  };

  const highlightSearchTerm = (text) => {
    if (!searchTerm) return text;
    const parts = text.split(new RegExp(`(${searchTerm})`, 'gi'));
    return parts.map((part, i) => 
      part.toLowerCase() === searchTerm.toLowerCase() 
        ? <span key={i} className="bg-blue-200 dark:bg-blue-800">{part}</span>
        : part
    );
  };

  // Add renderUseCases back inside the component
  const renderUseCases = () => {
    const openKPIDialog = (useCase, kpiIndex) => {
      setSelectedKPI({ useCase, kpi: kpiDefinitions[useCase][kpiIndex] });
      setIsDialogOpen(true);
    };

    return (
      <Card className="w-full">
        <div className="p-6 space-y-6">
          {/* Marketing Message Section */}
          <div className="bg-gray-50 rounded-lg p-8 mb-6">
            <h2 className="text-2xl font-bold mb-3">Propel Enterprise Value with Onix Automation & IP</h2>
            <p className="text-lg text-gray-700">
              Tailored recommendations powered by{' '}
              <a 
                href="https://www.onixnet.com/tme/" 
                target="_blank" 
                rel="noopener noreferrer" 
                className="text-blue-600 hover:text-blue-800 underline"
              >
                industry expertise
              </a>
              ,{' '}
              <a 
                href="https://www.onixnet.com/customer-stories/" 
                target="_blank" 
                rel="noopener noreferrer" 
                className="text-blue-600 hover:text-blue-800 underline"
              >
                proven implementations
              </a>
              , and analysis of your{' '}
              <button 
                onClick={() => setShowDataPlatformDialog(true)}
                className="text-blue-600 hover:text-blue-800 underline"
              >
                data platform metadata
              </button>
              {' '}and{' '}
              <button 
                onClick={() => setShowBusinessContextDialog(true)}
                className="text-blue-600 hover:text-blue-800 underline"
              >
                business context
              </button>
              .
            </p>
          </div>

          {/* Data Platform Dialog */}
          {showDataPlatformDialog && (
            <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
              <div className="bg-white rounded-lg p-6 max-w-md w-full m-4">
                <div className="flex justify-between items-start mb-4">
                  <h3 className="text-lg font-semibold">Data Platform Metadata</h3>
                  <button
                    onClick={() => setShowDataPlatformDialog(false)}
                    className="text-gray-500 hover:text-gray-700"
                  >
                    <X className="w-5 h-5" />
                  </button>
                </div>
                <div className="space-y-4">
                  <p className="text-gray-600">
                    [Placeholder] Detailed information about data platform metadata will be provided here.
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Business Context Dialog */}
          {showBusinessContextDialog && (
            <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
              <div className="bg-white rounded-lg p-6 max-w-md w-full m-4">
                <div className="flex justify-between items-start mb-4">
                  <h3 className="text-lg font-semibold">Business Context</h3>
                  <button
                    onClick={() => setShowBusinessContextDialog(false)}
                    className="text-gray-500 hover:text-gray-700"
                  >
                    <X className="w-5 h-5" />
                  </button>
                </div>
                <div className="space-y-4">
                  <p className="text-gray-600">
                    [Placeholder] Detailed information about business context will be provided here.
                  </p>
                </div>
              </div>
            </div>
          )}

          <div className="grid grid-cols-2 gap-6">
            {Object.entries(useCases).map(([key, useCase]) => (
              <div key={key} className="bg-white p-4 rounded-lg shadow">
                <div className="flex items-start gap-3 mb-4">
                  {React.createElement(useCase.icon, { className: "w-5 h-5 mt-1 flex-shrink-0" })}
                  <div>
                    <h3 className="font-semibold text-base mb-1">{useCase.title}</h3>
                    <p className="text-gray-600 text-sm">{useCase.description}</p>
                  </div>
                </div>
                
                <div className="space-y-2 ml-8">
                  <h4 className="text-xs font-medium text-gray-500 mb-2">KPIs</h4>
                  {kpiDefinitions[key].map((kpi, index) => (
                    <button
                      key={index}
                      onClick={() => openKPIDialog(key, index)}
                      className="text-blue-600 hover:text-blue-800 text-xs flex items-center gap-2 w-full text-left"
                    >
                      {React.createElement(kpi.icon, { className: "w-3 h-3" })}
                      <span>{kpi.name}</span>
                    </button>
                  ))}
                </div>
              </div>
            ))}
          </div>

          {/* KPI Dialog */}
          {isDialogOpen && selectedKPI && (
            <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
              <div className="bg-white rounded-lg p-6 max-w-md w-full m-4">
                <div className="flex justify-between items-start mb-4">
                  <h3 className="text-lg font-semibold">{selectedKPI.kpi.name}</h3>
                  <button
                    onClick={() => setIsDialogOpen(false)}
                    className="text-gray-500 hover:text-gray-700"
                  >
                    <X className="w-5 h-5" />
                  </button>
                </div>
                <div className="space-y-4">
                  <div>
                    <h4 className="font-medium text-sm text-gray-700">Description</h4>
                    <p className="text-sm">{selectedKPI.kpi.description}</p>
                  </div>
                  <div>
                    <h4 className="font-medium text-sm text-gray-700">Calculation</h4>
                    <p className="text-sm font-mono bg-gray-50 p-2 rounded">
                      {selectedKPI.kpi.calculation}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </Card>
    );
  };

  const renderEagleAnalyze = () => {
    const getFilteredDomains = () => {
      if (!searchTerm) return DOMAIN_DATA;

      return Object.entries(DOMAIN_DATA).reduce((acc, [domain, data]) => {
        const filteredCategories = Object.entries(data.categories).reduce((catAcc, [category, tables]) => {
          const filteredTables = tables.filter(table => 
            table.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            table.description.toLowerCase().includes(searchTerm.toLowerCase())
          );
          if (filteredTables.length > 0) {
            catAcc[category] = filteredTables;
          }
          return catAcc;
        }, {});

        if (Object.keys(filteredCategories).length > 0) {
          acc[domain] = { categories: filteredCategories };
        }
        return acc;
      }, {});
    };

    return (
      <Card className="w-full">
        <div className="p-6 space-y-6">
          <div className="flex items-center gap-2 text-2xl font-bold">
            <Database className="w-6 h-6" />
            Pluto TV Data Domain Classification
          </div>

          {/* Updated Eagle - Data Catalog button with lighter blue color */}
          <button
            className="px-4 py-2 bg-blue-50 text-blue-600 rounded-lg hover:bg-blue-100 flex items-center gap-2 border border-blue-200"
            onClick={() => setShowDataCatalogDialog(true)}
          >
            <Database className="w-4 h-4" />
            Eagle - Data Catalog
          </button>

          {/* Data Catalog Dialog */}
          {showDataCatalogDialog && (
            <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
              <div className="bg-white rounded-lg p-6 max-w-4xl w-full m-4 max-h-[90vh] flex flex-col">
                <div className="flex justify-between items-start mb-4">
                  <h3 className="text-xl font-semibold">Eagle - Data Catalog</h3>
                  <button
                    onClick={() => setShowDataCatalogDialog(false)}
                    className="text-gray-500 hover:text-gray-700"
                  >
                    <X className="w-5 h-5" />
                  </button>
                </div>
                <div className="overflow-auto flex-1 pr-4 space-y-6">
                  {/* Overview Section */}
                  <div className="prose max-w-none">
                    <p className="text-gray-700 leading-relaxed">
                      The <span className="font-semibold">CUSTOMER_ATTRIBUTE_CONTENT_ENGAGEMENT</span> table is a comprehensive repository designed for monitoring and analyzing customer content engagement patterns across Paramount's streaming platforms. It plays a crucial role in understanding viewer behavior and content performance. The table includes unique identifiers such as engagement_id and viewer_profile_id, which facilitate precise tracking of viewing sessions across various schemas, including ODIN_PRD.RPT and ODIN_STG.RPT.
                    </p>
                  </div>

                  {/* Key Features Section */}
                  <div>
                    <h4 className="text-lg font-semibold mb-3">Key Features</h4>
                    <div className="grid grid-cols-2 gap-6">
                      <div className="space-y-4">
                        {[
                          {
                            title: "Unique Identifiers",
                            items: ["engagement_id: Unique identifier for each viewing session", "viewer_profile_id: Identifier for streaming profiles"]
                          },
                          {
                            title: "Content Information",
                            items: [
                              "content_id, content_title, content_type_code: Essential for tracking content performance",
                              "genre_code, sub_genre_code, content_rating: Content classification details"
                            ]
                          },
                          {
                            title: "Timestamps for Viewing Lifecycle",
                            items: ["viewing_start_timestamp, viewing_end_timestamp, last_interaction_timestamp: Facilitate real-time monitoring of viewing patterns"]
                          }
                        ].map(section => (
                          <div key={section.title} className="bg-gray-50 p-4 rounded-lg">
                            <h5 className="font-medium mb-2">{section.title}</h5>
                            <ul className="list-disc pl-5 space-y-1">
                              {section.items.map(item => (
                                <li key={item} className="text-sm text-gray-600">{item}</li>
                              ))}
                            </ul>
                          </div>
                        ))}
                      </div>
                      <div className="space-y-4">
                        {[
                          {
                            title: "Content Metrics",
                            items: [
                              "content_duration_minutes, viewed_duration_minutes, completion_percentage: Dimensions of engagement",
                              "buffer_count, quality_switches, bitrate_average: Technical performance metrics"
                            ]
                          },
                          {
                            title: "Engagement Metrics",
                            items: [
                              "pause_count, rewind_count, forward_skip_count: Vital for understanding viewer behavior",
                              "average_volume_level, subtitle_usage: Additional interaction metrics"
                            ]
                          },
                          {
                            title: "Quality Metrics",
                            items: ["stream_quality_score, viewing_experience_rating: Ensure streaming quality measurement"]
                          }
                        ].map(section => (
                          <div key={section.title} className="bg-gray-50 p-4 rounded-lg">
                            <h5 className="font-medium mb-2">{section.title}</h5>
                            <ul className="list-disc pl-5 space-y-1">
                              {section.items.map(item => (
                                <li key={item} className="text-sm text-gray-600">{item}</li>
                              ))}
                            </ul>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>

                  {/* KPIs Section */}
                  <div>
                    <h4 className="text-lg font-semibold mb-3">Key Business Metrics/KPIs</h4>
                    <div className="grid grid-cols-5 gap-4">
                      {[
                        "Total Watch Time",
                        "Content Completion Rate", 
                        "Viewer Retention Score",
                        "Platform Usage Distribution",
                        "Content Discovery Rate"
                      ].map(kpi => (
                        <div key={kpi} className="bg-blue-50 p-3 rounded-lg text-center">
                          <span className="text-sm text-blue-700">{kpi}</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Reports Section */}
                  <div>
                    <h4 className="text-lg font-semibold mb-3">Reports/Dashboards</h4>
                    <div className="grid grid-cols-2 gap-4">
                      {[
                        "Top Performing Content by Genre (Q4 2023)",
                        "Viewer Engagement Patterns (Summer 2023)",
                        "Content Discovery and Recommendation Impact Analysis",
                        "Platform Performance Dashboard"
                      ].map(report => (
                        <div key={report} className="bg-gray-50 p-3 rounded-lg">
                          <span className="text-sm">{report}</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Data Lineage Section */}
                  <div>
                    <h4 className="text-lg font-semibold mb-3">Data Lineage</h4>
                    <div className="space-y-4">
                      <div className="bg-gray-50 p-4 rounded-lg">
                        <h5 className="font-medium mb-2">Source Entity</h5>
                        <p className="text-sm text-gray-600">viewer_engagement_summary_v2_fact (table) located in the ODIN_STG.RPT schema</p>
                      </div>
                      <div className="bg-gray-50 p-4 rounded-lg">
                        <h5 className="font-medium mb-2">Target Entities (Total Count: 26)</h5>
                        <ul className="list-disc pl-5 space-y-1 text-sm text-gray-600">
                          <li>content_performance_tracking_vw (view)</li>
                          <li>movies_engagement_1 (table)</li>
                          <li>series_engagement_2 (table)</li>
                          <li>live_sports_3 (table)</li>
                          <li>premium_subscriber_1101 (table)</li>
                        </ul>
                      </div>
                    </div>
                  </div>

                  {/* Business Terminology Section */}
                  <div>
                    <h4 className="text-lg font-semibold mb-3">Business Terminology</h4>
                    <div className="grid grid-cols-3 gap-4">
                      {[
                        { term: "timestamp_utc", def: "The timestamp representing the date and time in UTC when a viewing event occurred" },
                        { term: "date_utc", def: "The date in UTC, used for event timestamps and tracking purposes" },
                        { term: "abandoned_viewing", def: "When a viewer exits content before reaching a significant completion threshold" },
                        // ... add more terms as needed
                      ].map(({ term, def }) => (
                        <div key={term} className="bg-gray-50 p-3 rounded-lg">
                          <span className="font-medium text-sm block mb-1">{term}</span>
                          <span className="text-sm text-gray-600">{def}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          <div className="relative">
            <Search className="absolute left-2 top-2.5 h-4 w-4 text-gray-500" />
            <input
              type="text"
              placeholder="Search tables, descriptions, or domains..."
              className="w-full pl-8 pr-4 py-2 border rounded-md bg-white dark:bg-gray-700
                dark:border-gray-600 dark:text-white focus:ring-2 focus:ring-blue-500
                focus:border-blue-500 outline-none"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          <div className="space-y-4">
            {Object.entries(getFilteredDomains()).map(([domain, data]) => (
              <div key={domain} className="border rounded-lg overflow-hidden">
                <button
                  className="w-full p-4 text-left bg-gray-50 dark:bg-gray-800 flex items-center justify-between"
                  onClick={() => toggleDomain(domain)}
                >
                  <span className="font-medium flex items-center gap-2">
                    <Database className="w-4 h-4" />
                    {highlightSearchTerm(domain)}
                  </span>
                  {expandedDomains[domain] ? 
                    <ChevronDown className="w-4 h-4" /> : 
                    <ChevronRight className="w-4 h-4" />
                  }
                </button>
                
                {expandedDomains[domain] && (
                  <div className="p-4 space-y-4">
                    {Object.entries(data.categories).map(([category, tables]) => (
                      <div key={category} className="space-y-2">
                        <div className="font-medium text-blue-600 dark:text-blue-400 flex items-center gap-2">
                          <Table className="w-4 h-4" />
                          {highlightSearchTerm(category)}
                        </div>
                        <div className="rounded-lg border overflow-hidden">
                          <table className="w-full">
                            <thead>
                              <tr className="bg-gray-100 dark:bg-gray-800">
                                <th className="w-1/2 p-2 text-left text-xs font-medium text-gray-600 dark:text-gray-300 border-r">
                                  Table Name
                                </th>
                                <th className="w-1/2 p-2 text-left text-xs font-medium text-gray-600 dark:text-gray-300">
                                  Description
                                </th>
                              </tr>
                            </thead>
                            <tbody className="divide-y">
                              {tables.map((table) => (
                                <tr 
                                  key={table.name}
                                  className="hover:bg-gray-50 dark:hover:bg-gray-800"
                                >
                                  <td className="p-2 text-xs font-mono border-r align-top whitespace-normal break-words">
                                    {highlightSearchTerm(table.name)}
                                  </td>
                                  <td className="p-2 text-xs align-top whitespace-normal">
                                    {highlightSearchTerm(table.description)}
                                  </td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </Card>
    );
  };

  const renderActivation = () => {
    return (
      <Card className="w-full">
        <div className="p-6 bg-white">
          {activationUseCase ? (
            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <h2 className="text-2xl font-bold">{useCases[activationUseCase].title}</h2>
                <button
                  onClick={() => setActivationUseCase(null)}
                  className="px-4 py-2 text-gray-600 hover:text-gray-800"
                >
                  Back to Use Cases
                </button>
              </div>

              <div className="grid grid-cols-4 gap-6">
                {/* First three columns remain unchanged */}
                <div className="space-y-4">
                  <h3 className="font-semibold text-lg flex items-center gap-2">
                    <Database className="w-5 h-5" />
                    Consumer Data Product
                  </h3>
                  <div className="space-y-2">
                    {Object.entries(targetViews).map(([key, view]) => (
                      <div key={key} className="p-3 bg-gray-50 rounded-lg">
                        <div className="font-medium">{view}</div>
                        <div className="text-sm text-gray-600">{flowDescriptions[key]}</div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Algorithms column with clickable algorithms for all use cases */}
                <div className="space-y-4">
                  <h3 className="font-semibold text-lg flex items-center gap-2">
                    <Brain className="w-5 h-5" />
                    Algorithms
                  </h3>
                  <div className="space-y-2">
                    {activationTransformations[activationUseCase].map((step, index) => (
                      <div key={index} className="p-3 bg-gray-50 rounded-lg">
                        <button
                          onClick={() => openAlgorithmDialog(activationUseCase, step)}
                          className="text-blue-600 hover:text-blue-800 text-sm text-left"
                        >
                          {step}
                        </button>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="space-y-4">
                  <h3 className="font-semibold text-lg flex items-center gap-2">
                    <LineChart className="w-5 h-5" />
                    Model Metrics
                  </h3>
                  <div className="space-y-2">
                    <div className="p-3 bg-gray-50 rounded-lg">
                      <div className="font-medium">Performance</div>
                      <div className="grid grid-cols-2 gap-2 text-sm">
                        <div>Accuracy:</div>
                        <div className="text-right">{mlMetrics.modelPerformance.accuracy}</div>
                        <div>Precision:</div>
                        <div className="text-right">{mlMetrics.modelPerformance.precision}</div>
                        <div>Recall:</div>
                        <div className="text-right">{mlMetrics.modelPerformance.recall}</div>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="space-y-4">
                  <h3 className="font-semibold text-lg flex items-center gap-2">
                    <Monitor className="w-5 h-5" />
                    Channels
                  </h3>
                  <div className="space-y-2">
                    {activationChannels[activationUseCase].map((channel, index) => (
                      <div key={index} className="p-3 bg-gray-50 rounded-lg flex items-center gap-2">
                        {React.createElement(channel.icon, { className: "w-4 h-4" })}
                        <span>{channel.name}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* Algorithm Dialog */}
              {isAlgorithmDialogOpen && selectedAlgorithm && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                  <div className="bg-white rounded-lg p-6 max-w-md w-full m-4">
                    <div className="flex justify-between items-start mb-4">
                      <h3 className="text-lg font-semibold">{selectedAlgorithm.name}</h3>
                      <button
                        onClick={() => setIsAlgorithmDialogOpen(false)}
                        className="text-gray-500 hover:text-gray-700"
                      >
                        <X className="w-5 h-5" />
                      </button>
                    </div>
                    <p className="text-sm text-gray-600">{selectedAlgorithm.description}</p>
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="grid grid-cols-2 gap-4">
              {Object.entries(useCases).map(([key, useCase]) => (
                <button
                  key={key}
                  onClick={() => setActivationUseCase(key)}
                  className="p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors text-left flex items-start gap-3"
                >
                  {React.createElement(useCase.icon, { className: "w-5 h-5 mt-1 flex-shrink-0" })}
                  <div>
                    <h3 className="font-semibold text-base mb-1">{useCase.title}</h3>
                    <p className="text-gray-600 text-sm">{useCase.description}</p>
                  </div>
                </button>
              ))}
            </div>
          )}
        </div>
      </Card>
    );
  };

  const renderEaglePlan = () => {
    return (
      <Card className="w-full">
        <div className="p-6 space-y-6">
          <h2 className="text-2xl font-bold">Customer Data Product</h2>
          
          {Object.keys(sourceTables).map((flow) => (
            <div 
              key={flow}
              className={`mb-6 p-4 rounded-lg border ${selectedFlow === flow ? 'border-blue-500 bg-blue-50' : 'border-gray-200'}`}
              onClick={() => setSelectedFlow(flow)}
            >
              {/* Add description at the top */}
              <div className="mb-4 text-sm text-gray-600 dark:text-gray-400">
                {flowDescriptions[flow]}
              </div>
              
              <div className="flex items-center space-x-4">
                {/* Source Tables */}
                <div className="w-1/3">
                  <h3 className="font-semibold mb-2">Source Tables</h3>
                  <div className="space-y-1">
                    {sourceTables[flow].map((table) => (
                      <div key={table} className="p-2 bg-gray-100 rounded text-sm">
                        {table}
                      </div>
                    ))}
                  </div>
                </div>

                {/* Arrow and Transformations */}
                <div className="flex-1 flex items-center">
                  <ChevronRight className="w-6 h-6 text-gray-400" />
                  <div className="flex-1 px-4">
                    <h3 className="font-semibold mb-2">Transformations</h3>
                    <div className="space-y-1">
                      {transformations[flow].map((step, idx) => (
                        <div key={idx} className="p-2 bg-blue-100 rounded text-sm">
                          {step}
                        </div>
                      ))}
                    </div>
                  </div>
                  <ChevronRight className="w-6 h-6 text-gray-400" />
                </div>

                {/* Target View */}
                <div className="w-1/4">
                  <h3 className="font-semibold mb-2">Target View</h3>
                  <div className="p-2 bg-green-100 rounded text-sm">
                    {targetViews[flow]}
                  </div>
                </div>
              </div>
            </div>
          ))}
          
          <div className="mt-4 space-y-4">
            <h3 className="font-semibold mb-2">Core & Advanced Customer Segments</h3>
            {Object.entries(segmentationViews).map(([key, view]) => (
              <div key={key} className="border rounded-lg overflow-hidden">
                <div 
                  className={`p-4 cursor-pointer ${expandedView === key ? 'bg-blue-50' : 'bg-gray-50'}`}
                  onClick={() => setExpandedView(expandedView === key ? null : key)}
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="text-lg font-semibold">{view.title}</h3>
                      <p className="text-sm text-gray-600">{view.description}</p>
                    </div>
                    {expandedView === key ? 
                      <ChevronDown className="w-6 h-6 text-gray-400" /> : 
                      <ChevronRight className="w-6 h-6 text-gray-400" />
                    }
                  </div>
                </div>
                
                {expandedView === key && (
                  <div className="p-4">
                    {Object.entries(view.fields).map(([category, fields]) => (
                      <div key={category} className="mb-4">
                        <h4 className="font-semibold mb-2 text-blue-600">{category}</h4>
                        <div className="grid grid-cols-2 gap-4">
                          {Object.entries(fields).map(([field, description]) => (
                            <div key={field} className="p-3 bg-gray-50 rounded">
                              <div className="font-medium">{field}</div>
                              <div className="text-sm text-gray-600">{description}</div>
                            </div>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </Card>
    );
  };

  const renderRavenBuild = () => {
    return (
      <Card className="w-full">
        <div className="p-6 space-y-6">
          <h2 className="text-2xl font-bold">Raven generates BigQuery SQL</h2>
          
          <div className="grid grid-cols-5 gap-4 mb-6">
            {Object.keys(sqlQueries).map((flow) => (
              <button
                key={flow}
                className={`px-4 py-2 rounded-lg transition-colors ${
                  selectedSqlFlow === flow 
                    ? 'bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300' 
                    : 'bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700'
                }`}
                onClick={() => setSelectedSqlFlow(flow)}
              >
                {sqlFlowLabels[flow]}
              </button>
            ))}
          </div>

          <div className="space-y-6">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-2">
                  <Database className="w-5 h-5 text-gray-600 dark:text-gray-400" />
                  <span>Source Tables</span>
                </div>
                <ChevronRight className="w-5 h-5 text-gray-400" />
                <div className="flex items-center space-x-2">
                  <Code className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                  <span>SQL Transformation</span>
                </div>
                <ChevronRight className="w-5 h-5 text-gray-400" />
                <div className="flex items-center space-x-2">
                  <Table className="w-5 h-5 text-green-600 dark:text-green-400" />
                  <span>Target View</span>
                </div>
              </div>
              
              <div 
                className="p-2 bg-blue-100 dark:bg-blue-900 rounded cursor-pointer"
                onMouseEnter={() => setShowTooltip(selectedSqlFlow)}
                onMouseLeave={() => setShowTooltip(null)}
              >
                <Sparkles className="w-5 h-5 text-blue-600 dark:text-blue-400" />
              </div>
            </div>

            <div className="relative">
              {showTooltip && (
                <div className="absolute right-0 top-0 p-4 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 max-w-md">
                  <h3 className="font-semibold mb-2">Transformation Details</h3>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    {sqlQueries[showTooltip].explanation}
                  </p>
                </div>
              )}

              <div className="bg-gray-50 dark:bg-gray-900 rounded-lg overflow-hidden">
                <pre className="p-4 overflow-x-auto">
                  <code className="text-sm font-mono whitespace-pre text-gray-800 dark:text-gray-200">
                    {sqlQueries[selectedSqlFlow].code}
                  </code>
                </pre>
              </div>
            </div>
          </div>
        </div>
      </Card>
    );
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  useEffect(() => {
    let interval;
    if (isGenerating && progress < 100) {
      interval = setInterval(() => {
        setProgress(prev => {
          const newProgress = prev + 2;
          if (newProgress >= 100) {
            clearInterval(interval);
            setIsGenerating(false);
            setGenerationComplete(true);
            return 100;
          }
          return newProgress;
        });
        
        setTimeRemaining(prev => Math.max(0, prev - 0.1));
      }, 100);
    }
    return () => {
      clearInterval(interval);
    };
  }, [isGenerating, progress]);

  const renderPelicanValidate = () => {
    return (
      <Card className="w-full">
        <div className="space-y-6">
          {/* Collapsible Data Validation Pipeline Section */}
          <div className="border rounded-lg overflow-hidden">
            <div 
              className="bg-white p-4 flex items-center justify-between cursor-pointer"
              onClick={() => setIsValidationPipelineExpanded(!isValidationPipelineExpanded)}
            >
              <h2 className="text-2xl font-bold flex items-center gap-2">
                <Target className="w-6 h-6" />
                Data Validation Pipeline
              </h2>
              {isValidationPipelineExpanded ? 
                <ChevronDown className="w-6 h-6 text-gray-500" /> : 
                <ChevronRight className="w-6 h-6 text-gray-500" />
              }
            </div>

            {isValidationPipelineExpanded && (
              <div className="p-6 bg-white border-t">
                <div className="flex space-x-4 mb-8">
                  {Object.keys(flows).map((flow) => (
                    <button
                      key={flow}
                      className={`px-4 py-2 rounded-lg ${
                        selectedValidationFlow === flow 
                          ? 'bg-blue-100 text-blue-700' 
                          : 'bg-gray-100 hover:bg-gray-200'
                      }`}
                      onClick={() => setSelectedValidationFlow(flow)}
                    >
                      {flows[flow].title}
                    </button>
                  ))}
                </div>

                <div className="mb-8">
                  <div className="flex items-center mb-6">
                    {steps.map((step, idx) => (
                      <React.Fragment key={step.id}>
                        <div 
                          className={`flex items-center ${
                            activeValidationStep === step.id ? 'text-blue-600' : 'text-gray-500'
                          }`}
                        >
                          <div className={`
                            w-8 h-8 rounded-full flex items-center justify-center
                            ${activeValidationStep === step.id ? 'bg-blue-100' : 'bg-gray-100'}
                          `}>
                            {React.createElement(stepIcons[step.id], { className: 'w-4 h-4' })}
                          </div>
                          <span className="ml-2">{step.label}</span>
                        </div>
                        {idx < steps.length - 1 && (
                          <div className="w-16 h-px bg-gray-300 mx-4" />
                        )}
                      </React.Fragment>
                    ))}
                  </div>
                </div>

                {activeValidationStep === 'generate' && (
                  <div className="space-y-6">
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <h3 className="font-semibold mb-4">Kingfisher Synthetic Data Generator</h3>

                      {/* Generation Profile section */}
                      <div className="mb-6">
                        <h4 className="font-medium mb-3">Generation Profile</h4>
                        <div className="grid grid-cols-4 gap-4">
                          {Object.entries(generationProfiles).map(([key, profile]) => (
                            <button
                              key={key}
                              className={`p-3 rounded-lg border transition-colors flex flex-col items-center gap-2
                                ${selectedProfile === key 
                                  ? 'border-blue-500 bg-blue-50 text-blue-700' 
                                  : 'border-gray-200 hover:bg-gray-50'}`}
                              onClick={() => setSelectedProfile(key)}
                            >
                              <div className="font-medium">{profile.label}</div>
                              <div className="text-sm text-gray-600 text-center">{profile.description}</div>
                            </button>
                          ))}
                        </div>
                      </div>

                      <div className="grid grid-cols-2 gap-4">
                        <div>
                          <h4 className="font-medium mb-2">Sample Data</h4>
                          <div className="bg-white rounded-lg overflow-x-auto">
                            <table className="w-full">
                              <thead className="bg-gray-50">
                                <tr>
                                  <th className="px-3 py-2 text-left text-xs font-medium text-gray-600">User ID</th>
                                  <th className="px-3 py-2 text-left text-xs font-medium text-gray-600">Age Range</th>
                                  <th className="px-3 py-2 text-left text-xs font-medium text-gray-600">Country</th>
                                  <th className="px-3 py-2 text-left text-xs font-medium text-gray-600">Entitlement</th>
                                </tr>
                              </thead>
                              <tbody className="divide-y divide-gray-200">
                                {flows[selectedValidationFlow].syntheticData.sampleData.map((row, idx) => (
                                  <tr key={idx} className="hover:bg-gray-50">
                                    {Object.values(row).map((value, valueIdx) => (
                                      <td key={valueIdx} className="px-3 py-2 text-xs">
                                        {value === null ? '-' : value.toString()}
                                      </td>
                                    ))}
                                  </tr>
                                ))}
                              </tbody>
                            </table>
                          </div>
                        </div>
                        <div>
                          <h4 className="font-medium mb-2">Data Distributions</h4>
                          {Object.entries(flows[selectedValidationFlow].syntheticData.distributions).map(([key, dist]) => (
                            <div key={key} className="mb-4">
                              <h5 className="text-sm font-medium text-gray-600">{key}</h5>
                              <div className="flex flex-wrap gap-2">
                                {Object.entries(dist).map(([label, value]) => (
                                  <span key={label} className="px-2 py-1 bg-blue-50 rounded text-sm">
                                    {label}: {value}
                                  </span>
                                ))}
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>

                      {!isGenerating && !generationComplete && (
                        <button
                          className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                          onClick={() => {
                            setIsGenerating(true);
                            setProgress(0);
                            setTimeRemaining(5);
                            setGenerationComplete(false);
                          }}
                        >
                          Generate Data
                        </button>
                      )}

                      {/* Progress Bar */}
                      {isGenerating && (
                        <div className="mt-6">
                          <div className="mb-2 flex justify-between">
                            <span>Generation Progress</span>
                            <span>{progress}%</span>
                          </div>
                          <div className="w-full h-4 bg-gray-200 rounded-full">
                            <div 
                              className="h-full bg-blue-500 rounded-full transition-all duration-300"
                              style={{ width: `${progress}%` }}
                            />
                          </div>
                          <div className="mt-2 text-sm text-gray-600">
                            Time Remaining: {formatTime(Math.ceil(timeRemaining))}
                          </div>
                        </div>
                      )}

                      {/* Generation Complete Summary */}
                      {generationComplete && (
                        <div className="mt-6 p-4 border rounded-lg">
                          <h3 className="font-semibold mb-4">Generated Data Summary</h3>
                          <div className="grid grid-cols-3 gap-4">
                            <div className="p-3 bg-gray-50 rounded-lg">
                              <div className="text-sm text-gray-600">Total Records</div>
                              <div className="font-medium">
                                {flows[selectedValidationFlow].syntheticData.rowCount.toLocaleString()}
                              </div>
                            </div>
                            <div className="p-3 bg-gray-50 rounded-lg">
                              <div className="text-sm text-gray-600">Data Size</div>
                              <div className="font-medium">2.5 MB</div>
                            </div>
                            <div className="p-3 bg-gray-50 rounded-lg">
                              <div className="text-sm text-gray-600">Generation Time</div>
                              <div className="font-medium">5 seconds</div>
                            </div>
                          </div>
                          <div className="mt-6 flex justify-end">
                            <button
                              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center gap-2"
                              onClick={() => setActiveValidationStep('validate')}
                            >
                              Next
                              <ChevronRight className="w-4 h-4" />
                            </button>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                )}

                {activeValidationStep === 'validate' && (
                  <div className="space-y-6">
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <h3 className="font-semibold mb-4">Validation Checks</h3>
                      <div className="space-y-4">
                        {flows[selectedValidationFlow].validations.map((validation, idx) => (
                          <div key={idx} className="flex items-start space-x-4 p-4 bg-white rounded-lg">
                            <div className={`w-6 h-6 rounded-full flex items-center justify-center ${
                              validation.status === 'passed' ? 'bg-green-100' : 'bg-yellow-100'
                            }`}>
                              {validation.status === 'passed' ? 
                                <Check className="w-4 h-4 text-green-600" /> :
                                <AlertTriangle className="w-4 h-4 text-yellow-600" />
                              }
                            </div>
                            <div>
                              <h4 className="font-medium">{validation.name}</h4>
                              <p className="text-sm text-gray-600">{validation.description}</p>
                              <p className="text-sm mt-1">{validation.details}</p>
                            </div>
                          </div>
                        ))}
                      </div>
                      <button
                        className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                        onClick={() => setActiveValidationStep('results')}
                      >
                        View Results
                      </button>
                    </div>
                  </div>
                )}

                {activeValidationStep === 'results' && renderResults(selectedValidationFlow)}
              </div>
            )}
          </div>
        </div>
      </Card>
    );
  };

  const renderVertexAI = () => {
    return (
      <Card className="w-full">
        <div className="p-6 bg-white space-y-6">
          {/* New Collapsible Value Proposition Section */}
          <div className="border rounded-lg overflow-hidden">
            <div 
              className="bg-gray-50 p-4 flex items-center justify-between cursor-pointer"
              onClick={() => setIsVertexAIExpanded(!isVertexAIExpanded)}
            >
              <div className="flex items-center gap-2">
                <Brain className="w-6 h-6 text-blue-600" />
                <h2 className="text-xl font-semibold">Phoenix AI Value Proposition</h2>
              </div>
              {isVertexAIExpanded ? 
                <ChevronDown className="w-5 h-5 text-gray-500" /> : 
                <ChevronRight className="w-5 h-5 text-gray-500" />
              }
            </div>
            
            {isVertexAIExpanded && (
              <div className="p-4 border-t space-y-6">
                {/* Existing Value Propositions */}
                <div className="grid grid-cols-3 gap-4">
                  <div className="p-4 bg-blue-50 rounded-lg">
                    <div className="flex items-center gap-2 mb-2">
                      <Clock className="w-5 h-5 text-blue-600" />
                      <h3 className="font-semibold">Accelerate Time to Value</h3>
                    </div>
                    <p className="text-sm text-gray-600">Reduce model development cycles from months to weeks with automated ML pipelines and pre-built solutions.</p>
                  </div>
                  <div className="p-4 bg-green-50 rounded-lg">
                    <div className="flex items-center gap-2 mb-2">
                      <Shield className="w-5 h-5 text-green-600" />
                      <h3 className="font-semibold">Enterprise-Grade Reliability</h3>
                    </div>
                    <p className="text-sm text-gray-600">Production-ready ML infrastructure with built-in monitoring, security, and scalability.</p>
                  </div>
                  <div className="p-4 bg-purple-50 rounded-lg">
                    <div className="flex items-center gap-2 mb-2">
                      <Target className="w-5 h-5 text-purple-600" />
                      <h3 className="font-semibold">Streamlined Operations</h3>
                    </div>
                    <p className="text-sm text-gray-600">End-to-end ML lifecycle management with automated workflows and comprehensive monitoring.</p>
                  </div>
                </div>

                {/* New Differentiators & Accelerators Section */}
                <div className="border-t pt-4">
                  <h3 className="text-lg font-semibold mb-4">Key Differentiators & Accelerators</h3>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="p-4 bg-orange-50 rounded-lg">
                      <div className="flex items-center gap-2 mb-2">
                        <AlertTriangle className="w-5 h-5 text-orange-600" />
                        <h3 className="font-semibold">Automated Data Quality Detection</h3>
                      </div>
                      <p className="text-sm text-gray-600">
                        <span className="inline-flex items-center gap-1">
                          <Bird className="w-4 h-4 text-orange-600" />
                          <strong>Pelican</strong>
                        </span> automatically detects and alerts on data quality issues, ensuring reliable model inputs and reducing production incidents.
                      </p>
                    </div>
                    <div className="p-4 bg-indigo-50 rounded-lg">
                      <div className="flex items-center gap-2 mb-2">
                        <Database className="w-5 h-5 text-indigo-600" />
                        <h3 className="font-semibold">Synthetic Data Generation</h3>
                      </div>
                      <p className="text-sm text-gray-600">
                        <span className="inline-flex items-center gap-1">
                          <Bird className="w-4 h-4 text-indigo-600" />
                          <strong>Kingfisher</strong>
                        </span> generates high-quality synthetic data to improve model accuracy and precision, especially for edge cases and rare scenarios.
                      </p>
                    </div>
                    <div className="p-4 bg-emerald-50 rounded-lg">
                      <div className="flex items-center gap-2 mb-2">
                        <DollarSign className="w-5 h-5 text-emerald-600" />
                        <h3 className="font-semibold">Cost Management</h3>
                      </div>
                      <p className="text-sm text-gray-600">
                        <span className="inline-flex items-center gap-1">
                          <Bird className="w-4 h-4 text-emerald-600" />
                          <strong>Eagle</strong>
                        </span> FinOps optimizes ML infrastructure costs while maintaining performance, providing clear visibility and control over spending.
                      </p>
                    </div>
                    <div className="p-4 bg-blue-50 rounded-lg">
                      <div className="flex items-center gap-2 mb-2">
                        <Sparkles className="w-5 h-5 text-blue-600" />
                        <h3 className="font-semibold">Best Practices Integration</h3>
                      </div>
                      <p className="text-sm text-gray-600">
                        Maximize value from Vertex AI and custom ML through automated implementation of industry best practices and proven patterns.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Commented out button section
          <div className="flex gap-4">
            <button 
              className="px-4 py-2 bg-[#4F46E5] text-white rounded-lg hover:bg-[#4338CA] flex items-center gap-2"
              onClick={() => window.open('http://localhost:3002/', '_blank')}
            >
              <Bot className="w-4 h-4" />
              Data Intelligence Copilot
            </button>
          </div>
          */}

          {/* Existing MLLifecycleDashboard */}
          <MLLifecycleDashboard />
        </div>
      </Card>
    );
  };

  const openAlgorithmDialog = (useCase, algorithmName) => {
    const algorithm = algorithmDefinitions[useCase].find(a => a.name === algorithmName);
    setSelectedAlgorithm(algorithm);
    setIsAlgorithmDialogOpen(true);
  };

  const tabs = [
    { id: 'use-cases', icon: Lightbulb, label: 'Use Cases' },
    { id: 'eagle-analyze', icon: LineChart, label: 'Eagle - Analyze' },
    { id: 'eagle-plan', icon: Calendar, label: 'Eagle - Define' },
    { id: 'raven', icon: Bird, label: 'Raven - Build' },
    { id: 'pelican', icon: CheckCircle, label: 'Pelican - Validate' },
    { id: 'phoenix-ai', icon: Sparkles, label: 'Phoenix AI' },
    { id: 'activation', icon: Zap, label: 'Activation' },
    { id: 'measure', icon: Ruler, label: 'Measure' },
    { id: 'operate', icon: Settings, label: 'Operate' },
    { id: 'resources', icon: Library, label: 'Resources' }
  ];

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-8 font-sans">
      <div className="w-full max-w-7xl mx-auto space-y-8">
        <Card className="p-2">
          <div className="flex gap-2">
            {tabs.map(tab => (
              <TabButton
                key={tab.id}
                active={activeTab === tab.id}
                icon={tab.icon}
                onClick={() => {
                  if (tab.id === 'measure') {
                    window.location.href = '/measure';
                  } else {
                    setActiveTab(tab.id);
                  }
                }}
              >
                {tab.label}
              </TabButton>
            ))}
          </div>
        </Card>

        <div className="mt-8">
          {activeTab === 'use-cases' && renderUseCases()}
          {activeTab === 'eagle-analyze' && renderEagleAnalyze()}
          {activeTab === 'eagle-plan' && renderEaglePlan()}
          {activeTab === 'raven' && renderRavenBuild()}
          {activeTab === 'pelican' && renderPelicanValidate()}
          {activeTab === 'phoenix-ai' && renderVertexAI()}
          {activeTab === 'activation' && renderActivation()}
          {activeTab === 'measure' && (
            <div className="p-6">
              <h2 className="text-2xl font-bold mb-4">Measure</h2>
              <p>Measure functionality coming soon...</p>
            </div>
          )}
          {activeTab === 'operate' && <OperatePage />}
          {activeTab === 'resources' && <ResourcesPage />}
        </div>
      </div>
    </div>
  );
};

export default ParamountDataProduct;
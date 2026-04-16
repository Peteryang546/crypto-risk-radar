"""
Risk Scoring Engine v8.7
5-Dimension Risk Scoring Model
Based on DeFiLlama Risk Assessment Methodology
"""

import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class RiskLevel(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

@dataclass
class RiskMetrics:
    """Risk metrics for a single asset/protocol"""
    symbol: str
    price: float
    market_cap: float
    volume_24h: float
    volatility_30d: float
    # Security metrics
    audited: bool = False
    auditor: str = ""
    exploit_history: List[dict] = None
    # Financial metrics
    tvl: float = 0.0
    revenue_24h: float = 0.0
    # Operational metrics
    team_transparency: int = 50  # 0-100
    governance_score: int = 50   # 0-100
    # Sentiment metrics
    social_sentiment: float = 0.0  # -1 to 1
    news_sentiment: float = 0.0    # -1 to 1

@dataclass
class RiskScore:
    """Complete risk score result"""
    symbol: str
    overall_score: float  # 0-100
    risk_level: RiskLevel
    breakdown: Dict[str, float]
    red_flags: List[str]
    timestamp: str

class RiskScoringEngine:
    """
    5-Dimension Risk Scoring Engine
    
    Weights:
    - Market Risk: 30%
    - Security Risk: 25%
    - Financial Risk: 20%
    - Operational Risk: 15%
    - Sentiment Risk: 10%
    """
    
    WEIGHTS = {
        'market': 0.30,
        'security': 0.25,
        'financial': 0.20,
        'operational': 0.15,
        'sentiment': 0.10
    }
    
    def __init__(self):
        self.red_flags = []
    
    def calculate_market_risk(self, metrics: RiskMetrics) -> float:
        """
        Calculate market risk score (0-100, higher = riskier)
        
        Factors:
        - Volatility (40%)
        - Liquidity risk (30%)
        - Market cap stability (30%)
        """
        scores = []
        
        # Volatility score (0-100)
        # >50% volatility = high risk
        vol_score = min(metrics.volatility_30d * 2, 100)
        scores.append(('volatility', vol_score, 0.40))
        
        if metrics.volatility_30d > 0.50:
            self.red_flags.append(f"High volatility: {metrics.volatility_30d:.1%}")
        
        # Liquidity risk (0-100)
        # Low volume relative to market cap = high risk
        if metrics.market_cap > 0:
            volume_ratio = metrics.volume_24h / metrics.market_cap
            liq_score = max(0, 100 - volume_ratio * 1000)
        else:
            liq_score = 100
        scores.append(('liquidity', liq_score, 0.30))
        
        if liq_score > 70:
            self.red_flags.append("Low liquidity relative to market cap")
        
        # Market cap stability (0-100)
        # Small cap = higher risk
        if metrics.market_cap < 1e6:  # < $1M
            cap_score = 90
        elif metrics.market_cap < 1e7:  # < $10M
            cap_score = 70
        elif metrics.market_cap < 1e8:  # < $100M
            cap_score = 50
        elif metrics.market_cap < 1e9:  # < $1B
            cap_score = 30
        else:
            cap_score = 10
        scores.append(('market_cap', cap_score, 0.30))
        
        # Calculate weighted score
        market_score = sum(score * weight for _, score, weight in scores)
        return min(100, max(0, market_score))
    
    def calculate_security_risk(self, metrics: RiskMetrics) -> float:
        """
        Calculate security risk score (0-100, higher = riskier)
        
        Factors:
        - Audit status (40%)
        - Exploit history (40%)
        - Bug bounty (20%)
        """
        scores = []
        
        # Audit status (0-100)
        if metrics.audited:
            audit_score = 20  # Low risk if audited
        else:
            audit_score = 80  # High risk if not audited
            self.red_flags.append("Contract not audited")
        scores.append(('audit', audit_score, 0.40))
        
        # Exploit history (0-100)
        if metrics.exploit_history:
            exploit_count = len(metrics.exploit_history)
            exploit_score = min(100, exploit_count * 30)
            if exploit_count > 0:
                self.red_flags.append(f"Previous exploits: {exploit_count}")
        else:
            exploit_score = 0
        scores.append(('exploit_history', exploit_score, 0.40))
        
        # Bug bounty (placeholder - 20%)
        # Assume medium risk if no info
        bounty_score = 50
        scores.append(('bug_bounty', bounty_score, 0.20))
        
        security_score = sum(score * weight for _, score, weight in scores)
        return min(100, max(0, security_score))
    
    def calculate_financial_risk(self, metrics: RiskMetrics) -> float:
        """
        Calculate financial risk score (0-100, higher = riskier)
        
        Factors:
        - TVL stability (40%)
        - Revenue sustainability (30%)
        - Treasury health (30%)
        """
        scores = []
        
        # TVL risk (0-100)
        # Very low TVL = higher risk
        if metrics.tvl < 1e6:
            tvl_score = 80
        elif metrics.tvl < 1e7:
            tvl_score = 60
        elif metrics.tvl < 1e8:
            tvl_score = 40
        elif metrics.tvl < 1e9:
            tvl_score = 20
        else:
            tvl_score = 10
        scores.append(('tvl', tvl_score, 0.40))
        
        # Revenue sustainability (0-100)
        # Placeholder - would need historical data
        revenue_score = 50
        scores.append(('revenue', revenue_score, 0.30))
        
        # Treasury health (0-100)
        # Placeholder
        treasury_score = 50
        scores.append(('treasury', treasury_score, 0.30))
        
        financial_score = sum(score * weight for _, score, weight in scores)
        return min(100, max(0, financial_score))
    
    def calculate_operational_risk(self, metrics: RiskMetrics) -> float:
        """
        Calculate operational risk score (0-100, higher = riskier)
        
        Factors:
        - Team transparency (40%)
        - Governance quality (35%)
        - Documentation (25%)
        """
        scores = []
        
        # Team transparency (0-100)
        team_score = 100 - metrics.team_transparency
        if team_score > 70:
            self.red_flags.append("Low team transparency")
        scores.append(('team', team_score, 0.40))
        
        # Governance score (0-100)
        gov_score = 100 - metrics.governance_score
        if gov_score > 70:
            self.red_flags.append("Weak governance structure")
        scores.append(('governance', gov_score, 0.35))
        
        # Documentation (placeholder)
        doc_score = 50
        scores.append(('documentation', doc_score, 0.25))
        
        operational_score = sum(score * weight for _, score, weight in scores)
        return min(100, max(0, operational_score))
    
    def calculate_sentiment_risk(self, metrics: RiskMetrics) -> float:
        """
        Calculate sentiment risk score (0-100, higher = riskier)
        
        Factors:
        - Social sentiment (50%)
        - News sentiment (50%)
        """
        scores = []
        
        # Social sentiment (0-100)
        # Negative sentiment = higher risk
        social_score = (1 - metrics.social_sentiment) * 50
        scores.append(('social', social_score, 0.50))
        
        if metrics.social_sentiment < -0.5:
            self.red_flags.append("Very negative social sentiment")
        
        # News sentiment (0-100)
        news_score = (1 - metrics.news_sentiment) * 50
        scores.append(('news', news_score, 0.50))
        
        if metrics.news_sentiment < -0.5:
            self.red_flags.append("Very negative news sentiment")
        
        sentiment_score = sum(score * weight for _, score, weight in scores)
        return min(100, max(0, sentiment_score))
    
    def calculate_overall_score(self, metrics: RiskMetrics) -> RiskScore:
        """
        Calculate overall risk score using 5-dimension model
        """
        self.red_flags = []  # Reset red flags
        
        # Calculate individual dimension scores
        market_score = self.calculate_market_risk(metrics)
        security_score = self.calculate_security_risk(metrics)
        financial_score = self.calculate_financial_risk(metrics)
        operational_score = self.calculate_operational_risk(metrics)
        sentiment_score = self.calculate_sentiment_risk(metrics)
        
        # Calculate weighted overall score
        overall_score = (
            market_score * self.WEIGHTS['market'] +
            security_score * self.WEIGHTS['security'] +
            financial_score * self.WEIGHTS['financial'] +
            operational_score * self.WEIGHTS['operational'] +
            sentiment_score * self.WEIGHTS['sentiment']
        )
        
        # Determine risk level
        if overall_score <= 25:
            risk_level = RiskLevel.LOW
        elif overall_score <= 50:
            risk_level = RiskLevel.MEDIUM
        elif overall_score <= 75:
            risk_level = RiskLevel.HIGH
        else:
            risk_level = RiskLevel.CRITICAL
        
        return RiskScore(
            symbol=metrics.symbol,
            overall_score=round(overall_score, 1),
            risk_level=risk_level,
            breakdown={
                'market': round(market_score, 1),
                'security': round(security_score, 1),
                'financial': round(financial_score, 1),
                'operational': round(operational_score, 1),
                'sentiment': round(sentiment_score, 1)
            },
            red_flags=self.red_flags.copy(),
            timestamp=datetime.now().isoformat()
        )
    
    def get_risk_level_description(self, level: RiskLevel) -> str:
        """Get description for risk level"""
        descriptions = {
            RiskLevel.LOW: "Low risk - Suitable for conservative investors",
            RiskLevel.MEDIUM: "Medium risk - Monitor closely",
            RiskLevel.HIGH: "High risk - Exercise caution",
            RiskLevel.CRITICAL: "Critical risk - Avoid or minimal exposure"
        }
        return descriptions.get(level, "Unknown risk level")
    
    def format_score_report(self, score: RiskScore) -> str:
        """Format risk score as readable report"""
        lines = [
            f"Risk Assessment Report: {score.symbol}",
            f"{'=' * 50}",
            f"",
            f"Overall Risk Score: {score.overall_score}/100",
            f"Risk Level: {score.risk_level.value}",
            f"Assessment Time: {score.timestamp}",
            f"",
            f"Score Breakdown:",
            f"  - Market Risk:     {score.breakdown['market']}/100 (30%)",
            f"  - Security Risk:   {score.breakdown['security']}/100 (25%)",
            f"  - Financial Risk:  {score.breakdown['financial']}/100 (20%)",
            f"  - Operational Risk:{score.breakdown['operational']}/100 (15%)",
            f"  - Sentiment Risk:  {score.breakdown['sentiment']}/100 (10%)",
            f"",
        ]
        
        if score.red_flags:
            lines.append("Red Flags:")
            for flag in score.red_flags:
                lines.append(f"  [!] {flag}")
        else:
            lines.append("No significant red flags identified.")
        
        lines.append(f"")
        lines.append(f"Recommendation: {self.get_risk_level_description(score.risk_level)}")
        
        return "\n".join(lines)


def main():
    """Test the risk scoring engine"""
    engine = RiskScoringEngine()
    
    # Test with BTC-like metrics
    btc_metrics = RiskMetrics(
        symbol="BTC",
        price=72000,
        market_cap=1.4e12,
        volume_24h=3.5e10,
        volatility_30d=0.35,
        audited=True,
        auditor="N/A (Native)",
        exploit_history=[],
        tvl=0,  # Not applicable
        revenue_24h=0,
        team_transparency=80,
        governance_score=70,
        social_sentiment=0.3,
        news_sentiment=0.2
    )
    
    btc_score = engine.calculate_overall_score(btc_metrics)
    print(engine.format_score_report(btc_score))
    print("\n" + "="*50 + "\n")
    
    # Test with high-risk altcoin
    risky_metrics = RiskMetrics(
        symbol="RISKY",
        price=0.001,
        market_cap=5e5,
        volume_24h=1e4,
        volatility_30d=0.80,
        audited=False,
        auditor="",
        exploit_history=[{"date": "2024-01", "loss": "$1M"}],
        tvl=5e5,
        revenue_24h=100,
        team_transparency=20,
        governance_score=30,
        social_sentiment=-0.6,
        news_sentiment=-0.4
    )
    
    risky_score = engine.calculate_overall_score(risky_metrics)
    print(engine.format_score_report(risky_score))


if __name__ == "__main__":
    main()

"""
DeFi Risk Analyzer v8.7
DeFi Protocol Risk Assessment Module
Based on DeFiLlama Risk Assessment Methodology
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class DeFiRiskLevel(Enum):
    SAFE = "Safe"
    LOW = "Low Risk"
    MEDIUM = "Medium Risk"
    HIGH = "High Risk"
    DANGEROUS = "Dangerous"

@dataclass
class DeFiProtocol:
    """DeFi protocol data structure"""
    name: str
    chain: str
    tvl: float
    apy: float
    apy_base: float  # Base APY without rewards
    apy_reward: float  # Reward APY
    audited: bool
    auditor: str
    audit_date: Optional[str]
    oracle_type: str  # chainlink, twap, custom, etc.
    oracle_count: int
    governance_token: str
    governance_tvl: float
    
    # Risk indicators
    tvl_change_24h: float  # Percentage
    tvl_change_7d: float
    revenue_24h: float

@dataclass
class DeFiRiskScore:
    """DeFi protocol risk assessment result"""
    protocol_name: str
    overall_risk_score: float  # 0-100
    risk_level: DeFiRiskLevel
    
    # Dimension scores
    security_score: float
    oracle_risk_score: float
    financial_score: float
    yield_sustainability_score: float
    governance_score: float
    
    # Red flags
    red_flags: List[str]
    
    # Recommendations
    recommendations: List[str]
    
    timestamp: str

class DeFiRiskAnalyzer:
    """
    DeFi Protocol Risk Analyzer
    
    Risk Dimensions:
    1. Security Risk (Audit status, exploit history)
    2. Oracle Risk (Type, diversity, TVL at risk)
    3. Financial Risk (TVL stability, revenue)
    4. Yield Sustainability (APY vs industry, source)
    5. Governance Risk (Token concentration, timelock)
    """
    
    # Industry average APY for comparison
    INDUSTRY_AVERAGE_APY = 0.05  # 5%
    HIGH_APY_THRESHOLD = 0.20    # 20%
    DANGEROUS_APY_THRESHOLD = 0.50  # 50%
    
    def __init__(self):
        self.red_flags = []
        self.recommendations = []
    
    def fetch_protocol_data(self, protocol_name: str) -> Optional[DeFiProtocol]:
        """
        Fetch protocol data from DeFiLlama API
        """
        try:
            # This is a placeholder - actual implementation would call DeFiLlama API
            # For now, return mock data for testing
            return DeFiProtocol(
                name=protocol_name,
                chain="ethereum",
                tvl=1e8,  # $100M
                apy=0.15,  # 15%
                apy_base=0.05,
                apy_reward=0.10,
                audited=True,
                auditor="Trail of Bits",
                audit_date="2024-06",
                oracle_type="chainlink",
                oracle_count=3,
                governance_token="EXAMPLE",
                governance_tvl=5e7,
                tvl_change_24h=-0.05,
                tvl_change_7d=0.10,
                revenue_24h=50000
            )
        except Exception as e:
            print(f"Error fetching protocol data: {e}")
            return None
    
    def calculate_security_score(self, protocol: DeFiProtocol) -> float:
        """
        Calculate security risk score (0-100, higher = riskier)
        
        Factors:
        - Audit status (50%)
        - Audit recency (30%)
        - Auditor reputation (20%)
        """
        scores = []
        
        # Audit status (0-100)
        if protocol.audited:
            audit_score = 10  # Low risk
        else:
            audit_score = 90  # High risk
            self.red_flags.append("Protocol not audited")
        scores.append(('audit', audit_score, 0.50))
        
        # Audit recency (0-100)
        if protocol.audit_date:
            # Check if audit is recent (< 1 year)
            audit_score = 20  # Recent audit
        else:
            audit_score = 50  # Unknown
        scores.append(('recency', audit_score, 0.30))
        
        # Auditor reputation (0-100)
        reputable_auditors = ['Trail of Bits', 'OpenZeppelin', 'CertiK', 'Consensys']
        if protocol.auditor in reputable_auditors:
            rep_score = 10
        elif protocol.auditor:
            rep_score = 30
        else:
            rep_score = 50
        scores.append(('auditor', rep_score, 0.20))
        
        return sum(score * weight for _, score, weight in scores)
    
    def calculate_oracle_risk(self, protocol: DeFiProtocol) -> float:
        """
        Calculate oracle risk score (0-100, higher = riskier)
        
        Factors:
        - Oracle type (40%)
        - Oracle diversity (40%)
        - TVL at risk (20%)
        """
        scores = []
        
        # Oracle type risk (0-100)
        oracle_type_risk = {
            'chainlink': 10,      # Low risk
            'band': 15,
            'twap': 30,           # Medium risk
            'custom': 70,         # High risk
            'single_source': 90   # Very high risk
        }
        type_score = oracle_type_risk.get(protocol.oracle_type.lower(), 50)
        scores.append(('type', type_score, 0.40))
        
        if type_score > 50:
            self.red_flags.append(f"High-risk oracle type: {protocol.oracle_type}")
        
        # Oracle diversity (0-100)
        if protocol.oracle_count >= 3:
            diversity_score = 10
        elif protocol.oracle_count == 2:
            diversity_score = 30
        elif protocol.oracle_count == 1:
            diversity_score = 70
            self.red_flags.append("Single oracle - single point of failure")
        else:
            diversity_score = 80
            self.red_flags.append("Unknown oracle configuration")
        scores.append(('diversity', diversity_score, 0.40))
        
        # TVL at risk (0-100)
        # Higher TVL = higher risk if oracle fails
        if protocol.tvl > 1e9:
            tvl_risk = 80
        elif protocol.tvl > 1e8:
            tvl_risk = 60
        elif protocol.tvl > 1e7:
            tvl_risk = 40
        else:
            tvl_risk = 20
        scores.append(('tvl_risk', tvl_risk, 0.20))
        
        return sum(score * weight for _, score, weight in scores)
    
    def calculate_financial_score(self, protocol: DeFiProtocol) -> float:
        """
        Calculate financial risk score (0-100, higher = riskier)
        
        Factors:
        - TVL stability (50%)
        - Revenue sustainability (30%)
        - Revenue/TVL ratio (20%)
        """
        scores = []
        
        # TVL stability (0-100)
        # Large drops = high risk
        tvl_drop = abs(min(protocol.tvl_change_24h, protocol.tvl_change_7d))
        stability_score = min(100, tvl_drop * 200)
        scores.append(('stability', stability_score, 0.50))
        
        if protocol.tvl_change_24h < -0.20:
            self.red_flags.append(f"TVL dropped {abs(protocol.tvl_change_24h):.1%} in 24h")
        
        # Revenue sustainability (0-100)
        # Placeholder - would need historical data
        revenue_score = 30
        scores.append(('revenue', revenue_score, 0.30))
        
        # Revenue/TVL ratio (0-100)
        if protocol.tvl > 0:
            ratio = protocol.revenue_24h * 365 / protocol.tvl
            if ratio < 0.01:
                ratio_score = 70  # Very low revenue
            elif ratio < 0.05:
                ratio_score = 40
            else:
                ratio_score = 20
        else:
            ratio_score = 80
        scores.append(('ratio', ratio_score, 0.20))
        
        return sum(score * weight for _, score, weight in scores)
    
    def calculate_yield_sustainability(self, protocol: DeFiProtocol) -> float:
        """
        Calculate yield sustainability score (0-100, higher = riskier)
        
        Factors:
        - APY level vs industry (40%)
        - Reward vs base APY ratio (30%)
        - Revenue source transparency (30%)
        """
        scores = []
        
        # APY level (0-100)
        if protocol.apy > self.DANGEROUS_APY_THRESHOLD:
            apy_score = 95
            self.red_flags.append(f"Dangerously high APY: {protocol.apy:.1%}")
            self.recommendations.append("High APY likely unsustainable - exercise extreme caution")
        elif protocol.apy > self.HIGH_APY_THRESHOLD:
            apy_score = 70
            self.red_flags.append(f"High APY: {protocol.apy:.1%}")
            self.recommendations.append("High APY may be unsustainable - monitor closely")
        elif protocol.apy > self.INDUSTRY_AVERAGE_APY * 2:
            apy_score = 50
        else:
            apy_score = 20
        scores.append(('apy_level', apy_score, 0.40))
        
        # Reward vs base ratio (0-100)
        if protocol.apy_base > 0:
            reward_ratio = protocol.apy_reward / protocol.apy_base
            if reward_ratio > 5:
                reward_score = 80
                self.red_flags.append("Most yield from token rewards - unsustainable")
            elif reward_ratio > 2:
                reward_score = 50
            else:
                reward_score = 20
        else:
            reward_score = 90
            self.red_flags.append("No base yield - entirely from rewards")
        scores.append(('reward_ratio', reward_score, 0.30))
        
        # Source transparency (placeholder)
        transparency_score = 40
        scores.append(('transparency', transparency_score, 0.30))
        
        return sum(score * weight for _, score, weight in scores)
    
    def calculate_governance_score(self, protocol: DeFiProtocol) -> float:
        """
        Calculate governance risk score (0-100, higher = riskier)
        
        Factors:
        - Token concentration (40%)
        - Governance participation (30%)
        - Timelock configuration (30%)
        """
        scores = []
        
        # Token concentration (0-100)
        # Placeholder - would need on-chain data
        concentration_score = 50
        scores.append(('concentration', concentration_score, 0.40))
        
        # Governance participation (0-100)
        participation_score = 40
        scores.append(('participation', participation_score, 0.30))
        
        # Timelock (0-100)
        # Placeholder
        timelock_score = 30
        scores.append(('timelock', timelock_score, 0.30))
        
        return sum(score * weight for _, score, weight in scores)
    
    def assess_protocol(self, protocol: DeFiProtocol) -> DeFiRiskScore:
        """
        Perform complete DeFi protocol risk assessment
        """
        self.red_flags = []
        self.recommendations = []
        
        # Calculate dimension scores
        security = self.calculate_security_score(protocol)
        oracle = self.calculate_oracle_risk(protocol)
        financial = self.calculate_financial_score(protocol)
        yield_sus = self.calculate_yield_sustainability(protocol)
        governance = self.calculate_governance_score(protocol)
        
        # Calculate overall score (weighted average)
        weights = {
            'security': 0.30,
            'oracle': 0.20,
            'financial': 0.20,
            'yield': 0.20,
            'governance': 0.10
        }
        
        overall = (
            security * weights['security'] +
            oracle * weights['oracle'] +
            financial * weights['financial'] +
            yield_sus * weights['yield'] +
            governance * weights['governance']
        )
        
        # Determine risk level
        if overall <= 20:
            level = DeFiRiskLevel.SAFE
        elif overall <= 40:
            level = DeFiRiskLevel.LOW
        elif overall <= 60:
            level = DeFiRiskLevel.MEDIUM
        elif overall <= 80:
            level = DeFiRiskLevel.HIGH
        else:
            level = DeFiRiskLevel.DANGEROUS
        
        # Add default recommendation if none
        if not self.recommendations:
            if level == DeFiRiskLevel.SAFE:
                self.recommendations.append("Protocol appears relatively safe - still conduct own research")
            elif level == DeFiRiskLevel.LOW:
                self.recommendations.append("Low risk but monitor for changes")
            elif level == DeFiRiskLevel.MEDIUM:
                self.recommendations.append("Medium risk - limit exposure and monitor closely")
            elif level == DeFiRiskLevel.HIGH:
                self.recommendations.append("High risk - consider avoiding or minimal exposure")
            else:
                self.recommendations.append("DANGEROUS - Strongly recommend avoiding this protocol")
        
        return DeFiRiskScore(
            protocol_name=protocol.name,
            overall_risk_score=round(overall, 1),
            risk_level=level,
            security_score=round(security, 1),
            oracle_risk_score=round(oracle, 1),
            financial_score=round(financial, 1),
            yield_sustainability_score=round(yield_sus, 1),
            governance_score=round(governance, 1),
            red_flags=self.red_flags.copy(),
            recommendations=self.recommendations.copy(),
            timestamp=datetime.now().isoformat()
        )
    
    def format_assessment_report(self, score: DeFiRiskScore) -> str:
        """Format assessment as readable report"""
        lines = [
            f"DeFi Protocol Risk Assessment: {score.protocol_name}",
            f"{'=' * 60}",
            f"",
            f"Overall Risk Score: {score.overall_risk_score}/100",
            f"Risk Level: {score.risk_level.value}",
            f"Assessment Time: {score.timestamp}",
            f"",
            f"Risk Breakdown:",
            f"  - Security Risk:           {score.security_score}/100 (30%)",
            f"  - Oracle Risk:             {score.oracle_risk_score}/100 (20%)",
            f"  - Financial Risk:          {score.financial_score}/100 (20%)",
            f"  - Yield Sustainability:    {score.yield_sustainability_score}/100 (20%)",
            f"  - Governance Risk:         {score.governance_score}/100 (10%)",
            f"",
        ]
        
        if score.red_flags:
            lines.append("Red Flags:")
            for flag in score.red_flags:
                lines.append(f"  ⚠️  {flag}")
            lines.append("")
        
        if score.recommendations:
            lines.append("Recommendations:")
            for rec in score.recommendations:
                lines.append(f"  💡 {rec}")
            lines.append("")
        
        lines.append("-" * 60)
        lines.append("Disclaimer: This assessment is for educational purposes only.")
        lines.append("Always conduct your own research before investing.")
        
        return "\n".join(lines)


def main():
    """Test the DeFi risk analyzer"""
    analyzer = DeFiRiskAnalyzer()
    
    # Test with safe protocol
    safe_protocol = DeFiProtocol(
        name="SafeProtocol",
        chain="ethereum",
        tvl=5e8,
        apy=0.05,
        apy_base=0.05,
        apy_reward=0.0,
        audited=True,
        auditor="Trail of Bits",
        audit_date="2024-06",
        oracle_type="chainlink",
        oracle_count=3,
        governance_token="SAFE",
        governance_tvl=2e8,
        tvl_change_24h=0.01,
        tvl_change_7d=0.05,
        revenue_24h=100000
    )
    
    safe_score = analyzer.assess_protocol(safe_protocol)
    print(analyzer.format_assessment_report(safe_score))
    print("\n" + "="*60 + "\n")
    
    # Test with dangerous protocol
    dangerous_protocol = DeFiProtocol(
        name="RiskyFarm",
        chain="bsc",
        tvl=1e6,
        apy=1.20,  # 120% APY!
        apy_base=0.02,
        apy_reward=1.18,
        audited=False,
        auditor="",
        audit_date=None,
        oracle_type="custom",
        oracle_count=1,
        governance_token="RISKY",
        governance_tvl=5e5,
        tvl_change_24h=-0.30,
        tvl_change_7d=-0.50,
        revenue_24h=100
    )
    
    dangerous_score = analyzer.assess_protocol(dangerous_protocol)
    print(analyzer.format_assessment_report(dangerous_score))


if __name__ == "__main__":
    main()

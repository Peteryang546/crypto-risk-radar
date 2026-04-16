"""
Risk Matrix Calculator v8.7
Standardized Risk Assessment Matrix
Based on Risk Assessment Framework Methodology
"""

import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class Likelihood(Enum):
    RARE = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4

class Impact(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class RiskPriority(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

@dataclass
class RiskItem:
    """Individual risk item"""
    id: str
    name: str
    description: str
    likelihood: Likelihood
    impact: Impact
    category: str  # market, security, operational, etc.
    mitigation: str
    owner: str

@dataclass
class RiskAssessment:
    """Complete risk assessment result"""
    item: RiskItem
    risk_score: int  # 1-16
    priority: RiskPriority
    action_required: str

class RiskMatrixCalculator:
    """
    Risk Matrix Calculator
    
    Standard 4x4 Risk Matrix:
    
    Likelihood \ Impact | Low(1) | Medium(2) | High(3) | Critical(4)
    -------------------|--------|-----------|---------|------------
    High(4)            |   4    |     8     |    12   |     16
    Medium(3)          |   3    |     6     |     9   |     12
    Low(2)             |   2    |     4     |     6   |      8
    Rare(1)            |   1    |     2     |     3   |      4
    
    Priority:
    - 1-4: Low (Monitor)
    - 5-8: Medium (Plan mitigation)
    - 9-12: High (Implement controls)
    - 13-16: Critical (Immediate action)
    """
    
    # Risk matrix lookup table
    RISK_MATRIX = {
        (Likelihood.HIGH, Impact.CRITICAL): 16,
        (Likelihood.HIGH, Impact.HIGH): 12,
        (Likelihood.HIGH, Impact.MEDIUM): 8,
        (Likelihood.HIGH, Impact.LOW): 4,
        
        (Likelihood.MEDIUM, Impact.CRITICAL): 12,
        (Likelihood.MEDIUM, Impact.HIGH): 9,
        (Likelihood.MEDIUM, Impact.MEDIUM): 6,
        (Likelihood.MEDIUM, Impact.LOW): 3,
        
        (Likelihood.LOW, Impact.CRITICAL): 8,
        (Likelihood.LOW, Impact.HIGH): 6,
        (Likelihood.LOW, Impact.MEDIUM): 4,
        (Likelihood.LOW, Impact.LOW): 2,
        
        (Likelihood.RARE, Impact.CRITICAL): 4,
        (Likelihood.RARE, Impact.HIGH): 3,
        (Likelihood.RARE, Impact.MEDIUM): 2,
        (Likelihood.RARE, Impact.LOW): 1,
    }
    
    def calculate_risk_score(self, likelihood: Likelihood, impact: Impact) -> int:
        """
        Calculate risk score from likelihood and impact
        """
        return self.RISK_MATRIX.get((likelihood, impact), 8)
    
    def get_priority(self, score: int) -> RiskPriority:
        """
        Determine priority level from risk score
        """
        if score <= 4:
            return RiskPriority.LOW
        elif score <= 8:
            return RiskPriority.MEDIUM
        elif score <= 12:
            return RiskPriority.HIGH
        else:
            return RiskPriority.CRITICAL
    
    def get_action_required(self, priority: RiskPriority) -> str:
        """
        Get recommended action for priority level
        """
        actions = {
            RiskPriority.LOW: "Monitor - No immediate action required",
            RiskPriority.MEDIUM: "Plan - Develop mitigation strategy",
            RiskPriority.HIGH: "Act - Implement controls immediately",
            RiskPriority.CRITICAL: "Urgent - Executive attention required"
        }
        return actions.get(priority, "Review required")
    
    def assess_risk(self, item: RiskItem) -> RiskAssessment:
        """
        Perform complete risk assessment
        """
        score = self.calculate_risk_score(item.likelihood, item.impact)
        priority = self.get_priority(score)
        action = self.get_action_required(priority)
        
        return RiskAssessment(
            item=item,
            risk_score=score,
            priority=priority,
            action_required=action
        )
    
    def assess_multiple(self, items: List[RiskItem]) -> List[RiskAssessment]:
        """
        Assess multiple risk items
        """
        return [self.assess_risk(item) for item in items]
    
    def get_crypto_risk_items(self) -> List[RiskItem]:
        """
        Get predefined crypto market risk items
        """
        return [
            RiskItem(
                id="R001",
                name="Token Unlock Event",
                description="Large token unlock causing price dump",
                likelihood=Likelihood.MEDIUM,
                impact=Impact.HIGH,
                category="market",
                mitigation="Monitor unlock schedules, avoid high-unlock tokens",
                owner="Market Analysis"
            ),
            RiskItem(
                id="R002",
                name="Smart Contract Exploit",
                description="Protocol hacked, funds stolen",
                likelihood=Likelihood.LOW,
                impact=Impact.CRITICAL,
                category="security",
                mitigation="Only use audited protocols, diversify",
                owner="Security Team"
            ),
            RiskItem(
                id="R003",
                name="Exchange Insolvency",
                description="CEX unable to process withdrawals",
                likelihood=Likelihood.LOW,
                impact=Impact.CRITICAL,
                category="operational",
                mitigation="Use self-custody, limit CEX exposure",
                owner="Operations"
            ),
            RiskItem(
                id="R004",
                name="Regulatory Action",
                description="Major jurisdiction bans crypto",
                likelihood=Likelihood.LOW,
                impact=Impact.HIGH,
                category="regulatory",
                mitigation="Monitor regulatory developments",
                owner="Compliance"
            ),
            RiskItem(
                id="R005",
                name="Stablecoin Depeg",
                description="Major stablecoin loses peg",
                likelihood=Likelihood.MEDIUM,
                impact=Impact.HIGH,
                category="market",
                mitigation="Diversify stablecoin holdings",
                owner="Market Analysis"
            ),
            RiskItem(
                id="R006",
                name="Rug Pull",
                description="Team abandons project, steals funds",
                likelihood=Likelihood.MEDIUM,
                impact=Impact.CRITICAL,
                category="security",
                mitigation="Research team background, avoid anon teams",
                owner="Security Team"
            ),
            RiskItem(
                id="R007",
                name="Liquidity Crisis",
                description="Unable to exit position due to low liquidity",
                likelihood=Likelihood.MEDIUM,
                impact=Impact.MEDIUM,
                category="market",
                mitigation="Check liquidity depth before investing",
                owner="Market Analysis"
            ),
            RiskItem(
                id="R008",
                name="Oracle Failure",
                description="Price oracle manipulation or failure",
                likelihood=Likelihood.LOW,
                impact=Impact.HIGH,
                category="technical",
                mitigation="Use protocols with multiple oracles",
                owner="Technical Team"
            ),
        ]
    
    def generate_risk_matrix_table(self) -> str:
        """
        Generate ASCII risk matrix table
        """
        lines = [
            "Risk Matrix",
            "=" * 70,
            "",
            "Likelihood \\ Impact |  Low(1)  | Medium(2) |  High(3)  | Critical(4)",
            "-------------------|----------|-----------|-----------|------------"
        ]
        
        for likelihood in [Likelihood.HIGH, Likelihood.MEDIUM, Likelihood.LOW, Likelihood.RARE]:
            row = [f"{likelihood.name:18}"]
            for impact in [Impact.LOW, Impact.MEDIUM, Impact.HIGH, Impact.CRITICAL]:
                score = self.calculate_risk_score(likelihood, impact)
                priority = self.get_priority(score)
                
                # Color coding (ASCII)
                if priority == RiskPriority.CRITICAL:
                    cell = f"[{score:2}] CRIT"
                elif priority == RiskPriority.HIGH:
                    cell = f"[{score:2}] HIGH"
                elif priority == RiskPriority.MEDIUM:
                    cell = f"[{score:2}] MED "
                else:
                    cell = f"[{score:2}] LOW "
                
                row.append(f"{cell:10}")
            
            lines.append(" | ".join(row))
        
        lines.extend([
            "",
            "Priority Levels:",
            "  [1-4]  LOW     - Monitor",
            "  [5-8]  MEDIUM  - Plan mitigation",
            "  [9-12] HIGH    - Implement controls",
            "  [13-16]CRITICAL- Immediate action",
            ""
        ])
        
        return "\n".join(lines)
    
    def format_assessment_report(self, assessments: List[RiskAssessment]) -> str:
        """
        Format multiple assessments as report
        """
        lines = [
            "Risk Assessment Report",
            "=" * 80,
            f"Generated: {datetime.now().isoformat()}",
            "",
            self.generate_risk_matrix_table(),
            "",
            "Identified Risks:",
            "-" * 80,
            ""
        ]
        
        # Sort by priority (highest first)
        sorted_assessments = sorted(
            assessments, 
            key=lambda x: x.risk_score, 
            reverse=True
        )
        
        for i, assessment in enumerate(sorted_assessments, 1):
            item = assessment.item
            lines.extend([
                f"{i}. {item.name} [{item.id}]",
                f"   Category: {item.category}",
                f"   Description: {item.description}",
                f"   Likelihood: {item.likelihood.name} | Impact: {item.impact.name}",
                f"   Risk Score: {assessment.risk_score}/16 | Priority: {assessment.priority.value}",
                f"   Action: {assessment.action_required}",
                f"   Mitigation: {item.mitigation}",
                f"   Owner: {item.owner}",
                ""
            ])
        
        # Summary statistics
        critical = sum(1 for a in assessments if a.priority == RiskPriority.CRITICAL)
        high = sum(1 for a in assessments if a.priority == RiskPriority.HIGH)
        medium = sum(1 for a in assessments if a.priority == RiskPriority.MEDIUM)
        low = sum(1 for a in assessments if a.priority == RiskPriority.LOW)
        
        lines.extend([
            "-" * 80,
            "Summary:",
            f"  Critical: {critical}",
            f"  High:     {high}",
            f"  Medium:   {medium}",
            f"  Low:      {low}",
            f"  Total:    {len(assessments)}",
            ""
        ])
        
        return "\n".join(lines)
    
    def export_to_json(self, assessments: List[RiskAssessment]) -> str:
        """
        Export assessments to JSON
        """
        data = {
            "timestamp": datetime.now().isoformat(),
            "assessments": []
        }
        
        for assessment in assessments:
            data["assessments"].append({
                "id": assessment.item.id,
                "name": assessment.item.name,
                "category": assessment.item.category,
                "likelihood": assessment.item.likelihood.name,
                "impact": assessment.item.impact.name,
                "risk_score": assessment.risk_score,
                "priority": assessment.priority.value,
                "action_required": assessment.action_required,
                "mitigation": assessment.item.mitigation
            })
        
        return json.dumps(data, indent=2)


def main():
    """Test the risk matrix calculator"""
    calculator = RiskMatrixCalculator()
    
    # Print risk matrix
    print(calculator.generate_risk_matrix_table())
    print("\n" + "="*80 + "\n")
    
    # Assess crypto risks
    risk_items = calculator.get_crypto_risk_items()
    assessments = calculator.assess_multiple(risk_items)
    
    print(calculator.format_assessment_report(assessments))
    print("\n" + "="*80 + "\n")
    
    # Export to JSON
    print("JSON Export:")
    print(calculator.export_to_json(assessments))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
KOL Integrity Scoring System
Tracks historical performance of KOLs to calculate credibility scores
"""

import json
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Any
from pathlib import Path

sys.path.insert(0, r'F:\stepclaw\agents\blockchain-analyst')
from config import USE_MOCK_DATA


class KOLScoring:
    """Calculate KOL integrity scores based on historical performance"""
    
    def __init__(self, use_mock_data=False):
        self.use_mock_data = use_mock_data
        self.history_file = Path(r'F:\stepclaw\agents\blockchain-analyst\data\kol_history.json')
        self.kol_list = self._load_kol_list()
        self.history = self._load_history()
    
    def _load_kol_list(self) -> List[Dict]:
        """Load monitored KOLs"""
        kol_file = Path(r'F:\stepclaw\agents\blockchain-analyst\data\kol_list.json')
        if kol_file.exists():
            with open(kol_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('kol_list', [])
        return []
    
    def _load_history(self) -> Dict:
        """Load historical shill data"""
        if self.history_file.exists():
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"shills": [], "last_updated": datetime.now().isoformat()}
    
    def _save_history(self):
        """Save history to file"""
        self.history["last_updated"] = datetime.now().isoformat()
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, indent=2)
    
    def add_shill_record(self, shill: Dict, evidence: Dict):
        """Add a new shill record to history"""
        record = {
            "timestamp": datetime.now().isoformat(),
            "username": shill.get("username"),
            "token": evidence.get("token"),
            "shill_score": shill.get("shill_score", 0),
            "risk_score": evidence.get("risk_score", 0),
            "price_change_24h": evidence.get("price_action", {}).get("change_24h", 0),
            "red_flags": len(evidence.get("pre_shill_wallets", [])) + len(evidence.get("post_shill_transfers", []))
        }
        self.history["shills"].append(record)
        self._save_history()
    
    def calculate_kol_score(self, username: str) -> Dict:
        """Calculate integrity score for a specific KOL"""
        # Filter records for this KOL (last 30 days)
        cutoff = datetime.now() - timedelta(days=30)
        records = [
            r for r in self.history.get("shills", [])
            if r.get("username") == username and 
            datetime.fromisoformat(r.get("timestamp", "2020-01-01")) > cutoff
        ]
        
        if not records:
            # No history - neutral score
            return {
                "username": username,
                "score": 50,
                "total_shills": 0,
                "avg_24h_change": 0,
                "red_flags": 0,
                "risk_level": "Unknown"
            }
        
        # Calculate metrics
        total_shills = len(records)
        avg_price_change = sum(r.get("price_change_24h", 0) for r in records) / total_shills
        total_red_flags = sum(r.get("red_flags", 0) for r in records)
        avg_risk_score = sum(r.get("risk_score", 0) for r in records) / total_shills
        
        # Calculate score (0-100)
        # Start at 50 (neutral)
        score = 50
        
        # Price performance (40% weight)
        if avg_price_change < -30:
            score -= 40
        elif avg_price_change < -15:
            score -= 25
        elif avg_price_change < -5:
            score -= 10
        elif avg_price_change > 10:
            score += 15
        
        # Red flags (30% weight)
        if total_red_flags >= 5:
            score -= 30
        elif total_red_flags >= 3:
            score -= 20
        elif total_red_flags >= 1:
            score -= 10
        
        # Shill frequency (20% weight)
        if total_shills >= 10:
            score -= 20
        elif total_shills >= 5:
            score -= 10
        
        # Average risk score (10% weight)
        if avg_risk_score >= 80:
            score -= 10
        elif avg_risk_score >= 60:
            score -= 5
        
        score = max(0, min(100, score))
        
        # Risk level
        if score >= 80:
            risk_level = "🟢 Trusted"
        elif score >= 60:
            risk_level = "🟡 Neutral"
        elif score >= 40:
            risk_level = "🟠 Suspicious"
        else:
            risk_level = "🔴 High Risk"
        
        return {
            "username": username,
            "score": score,
            "total_shills": total_shills,
            "avg_24h_change": round(avg_price_change, 1),
            "red_flags": total_red_flags,
            "risk_level": risk_level
        }
    
    def generate_leaderboard(self) -> str:
        """Generate KOL integrity leaderboard"""
        if self.use_mock_data:
            # Mock data
            scores = [
                {"username": "MoonPromoter", "score": 8, "total_shills": 7, "avg_24h_change": -32, "red_flags": 5, "risk_level": "🔴 High Risk"},
                {"username": "GemHunter", "score": 22, "total_shills": 4, "avg_24h_change": -18, "red_flags": 2, "risk_level": "🔴 High Risk"},
                {"username": "CryptoWizard", "score": 67, "total_shills": 2, "avg_24h_change": -3, "red_flags": 0, "risk_level": "🟡 Neutral"},
                {"username": "SafeAnalysis", "score": 91, "total_shills": 1, "avg_24h_change": 1, "red_flags": 0, "risk_level": "🟢 Trusted"}
            ]
        else:
            scores = [self.calculate_kol_score(kol.get("username")) for kol in self.kol_list]
            scores.sort(key=lambda x: x["score"], reverse=True)
        
        md = """## 📊 KOL Integrity Leaderboard (Last 30 Days)

**Methodology**: Score based on (1) post-shill price performance 40%, (2) on-chain red flags 30%, (3) shill frequency 20%, (4) avg risk score 10%.

| KOL | Score | 30d Shills | Avg 24h Change | Red Flags | Assessment |
|-----|-------|------------|----------------|-----------|------------|
"""
        
        for s in scores:
            change_emoji = "📉" if s["avg_24h_change"] < -10 else "📈" if s["avg_24h_change"] > 5 else "➡️"
            md += f"| @{s['username']} | {s['score']}/100 | {s['total_shills']} | {change_emoji} {s['avg_24h_change']:+.1f}% | {s['red_flags']} | {s['risk_level']} |\n"
        
        md += """
### Score Interpretation
- **🟢 80-100**: Trusted - Low shill frequency, positive or neutral price action
- **🟡 60-79**: Neutral - Some shills but no clear manipulation pattern
- **🟠 40-59**: Suspicious - Frequent shills with negative price action
- **🔴 0-39**: High Risk - Clear pump-and-dump patterns, multiple red flags

### How to Use This Data
1. **Before following a KOL**: Check their score and history
2. **After seeing a shill**: Verify if this KOL has a pattern of promoting tokens that dump
3. **Long-term tracking**: Scores update daily based on new evidence

*Disclaimer: This is educational research based on public data. Not financial advice.*
"""
        
        return md
    
    def get_kol_details(self, username: str) -> Dict:
        """Get detailed history for a specific KOL"""
        records = [r for r in self.history.get("shills", []) if r.get("username") == username]
        return {
            "username": username,
            "total_records": len(records),
            "records": records[-10:]  # Last 10 records
        }


def main():
    """Test the scoring system"""
    print("="*70)
    print("KOL INTEGRITY SCORING SYSTEM")
    print("="*70)
    
    scoring = KOLScoring(use_mock_data=True)
    print(scoring.generate_leaderboard())


if __name__ == "__main__":
    main()

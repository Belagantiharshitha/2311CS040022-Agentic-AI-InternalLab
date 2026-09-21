from typing import Dict, Any, List
from policy_rules import PolicyRuleEngine, ComplianceResult, Status, get_default_rules

class PolicyComplianceAgent:
    def __init__(self, data: Dict[str, Any]):
        self.engine = PolicyRuleEngine()
        for rule in get_default_rules():
            self.engine.add_rule(rule)
        self.data = data
        self.audit_history: List[ComplianceResult] = []

    def run_full_audit(self) -> Dict[str, Any]:
        results = self.engine.evaluate_all(self.data)
        self.audit_history.extend(results)
        
        fails_and_warns = [r for r in results if r.status in (Status.FAIL, Status.WARNING)]
        passes = [r for r in results if r.status == Status.PASS]
        
        # We define total checks as the sum of all evaluations that resulted in FAIL/WARNING + the logical "PASS" for the rest
        # Let's aggregate for a better report structure.
        
        category_breakdown = {}
        severity_dist = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        
        for r in fails_and_warns:
            severity_dist[r.severity.value] += 1
            cat = next((rule.category for rule in self.engine.all_rules if rule.rule_id == r.rule_id), "Unknown")
            if cat not in category_breakdown:
                category_breakdown[cat] = 0
            category_breakdown[cat] += 1

        total_violations = len(fails_and_warns)
        # Approximate total checks (50 emp * 3 rules + 100 tx * 3 rules + etc. is complex. We'll estimate based on data lengths)
        total_items = len(self.data['employees']) * 3 + len(self.data['transactions']) * 3 + len(self.data['it_systems']) * 3 + len(self.data['data_records']) * 3
        
        compliance_score = max(0.0, 100.0 - (total_violations / max(1, total_items) * 100))
        
        top_violations = sorted(fails_and_warns, key=lambda x: {"CRITICAL":4, "HIGH":3, "MEDIUM":2, "LOW":1}.get(x.severity.value, 0), reverse=True)[:10]

        return {
            "compliance_score": round(compliance_score, 2),
            "total_violations": total_violations,
            "category_breakdown": category_breakdown,
            "severity_distribution": severity_dist,
            "top_violations": top_violations,
            "all_results": results
        }

    def get_recommendations(self, results: List[ComplianceResult]) -> List[str]:
        recommendations = set()
        for r in results:
            if r.status != Status.PASS:
                rule = next((rule for rule in self.engine.all_rules if rule.rule_id == r.rule_id), None)
                if rule:
                    recommendations.add(f"[{rule.category}] {rule.remediation} (Violated rule: {rule.name})")
        return list(recommendations)

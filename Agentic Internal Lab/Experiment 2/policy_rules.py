import os
from dataclasses import dataclass
from typing import Callable, Any, List, Dict
from enum import Enum
import datetime

class Severity(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class Status(Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    WARNING = "WARNING"

@dataclass
class ComplianceResult:
    rule_id: str
    rule_name: str
    status: Status
    details: str
    timestamp: str
    severity: Severity

@dataclass
class PolicyRule:
    rule_id: str
    name: str
    category: str
    description: str
    severity: Severity
    check_function: Callable[[Dict[str, Any]], List[ComplianceResult]]
    remediation: str

class PolicyRuleEngine:
    def __init__(self):
        self.rules: Dict[str, List[PolicyRule]] = {}
        self.all_rules: List[PolicyRule] = []

    def add_rule(self, rule: PolicyRule) -> None:
        if rule.category not in self.rules:
            self.rules[rule.category] = []
        self.rules[rule.category].append(rule)
        self.all_rules.append(rule)

    def evaluate_single(self, rule_id: str, data: Dict[str, Any]) -> List[ComplianceResult]:
        for rule in self.all_rules:
            if rule.rule_id == rule_id:
                return rule.check_function(data)
        raise ValueError(f"Rule {rule_id} not found")

    def evaluate_all(self, data: Dict[str, Any]) -> List[ComplianceResult]:
        results = []
        for rule in self.all_rules:
            results.extend(rule.check_function(data))
        return results

def get_default_rules() -> List[PolicyRule]:
    rules = []
    
    # --- Data Privacy ---
    def check_dp_01(data: Dict[str, Any]) -> List[ComplianceResult]:
        res = []
        for d in data.get('data_records', []):
            if d['contains_pii'] and not d['encrypted']:
                res.append(ComplianceResult("DP-01", "PII Encryption", Status.FAIL, f"Record {d['record_id']} has unencrypted PII", datetime.datetime.now().isoformat(), Severity.CRITICAL))
        if not res: res.append(ComplianceResult("DP-01", "PII Encryption", Status.PASS, "All PII encrypted", datetime.datetime.now().isoformat(), Severity.CRITICAL))
        return res
    rules.append(PolicyRule("DP-01", "PII Encryption", "Data Privacy", "PII data must be encrypted.", Severity.CRITICAL, check_dp_01, "Encrypt records containing PII."))

    def check_dp_02(data: Dict[str, Any]) -> List[ComplianceResult]:
        res = []
        for d in data.get('data_records', []):
            if d['retention_days'] > 365:
                res.append(ComplianceResult("DP-02", "Data Retention", Status.FAIL, f"Record {d['record_id']} exceeds retention period", datetime.datetime.now().isoformat(), Severity.MEDIUM))
        if not res: res.append(ComplianceResult("DP-02", "Data Retention", Status.PASS, "Retention compliant", datetime.datetime.now().isoformat(), Severity.MEDIUM))
        return res
    rules.append(PolicyRule("DP-02", "Data Retention", "Data Privacy", "Data retention must not exceed 1 year.", Severity.MEDIUM, check_dp_02, "Archive or delete old data."))

    def check_dp_03(data: Dict[str, Any]) -> List[ComplianceResult]:
        res = []
        for d in data.get('data_records', []):
            if not d['access_log_enabled']:
                res.append(ComplianceResult("DP-03", "Data Access Logging", Status.FAIL, f"Record {d['record_id']} lacks access logs", datetime.datetime.now().isoformat(), Severity.HIGH))
        if not res: res.append(ComplianceResult("DP-03", "Data Access Logging", Status.PASS, "Access logging enabled", datetime.datetime.now().isoformat(), Severity.HIGH))
        return res
    rules.append(PolicyRule("DP-03", "Data Access Logging", "Data Privacy", "Access logs must be enabled for all data.", Severity.HIGH, check_dp_03, "Enable access logging on data stores."))

    # --- Access Control ---
    def check_ac_01(data: Dict[str, Any]) -> List[ComplianceResult]:
        res = []
        for e in data.get('employees', []):
            if not e['mfa_enabled']:
                res.append(ComplianceResult("AC-01", "MFA Enforcement", Status.FAIL, f"Employee {e['employee_id']} lacks MFA", datetime.datetime.now().isoformat(), Severity.CRITICAL))
        if not res: res.append(ComplianceResult("AC-01", "MFA Enforcement", Status.PASS, "MFA enabled for all", datetime.datetime.now().isoformat(), Severity.CRITICAL))
        return res
    rules.append(PolicyRule("AC-01", "MFA Enforcement", "Access Control", "All employees must use MFA.", Severity.CRITICAL, check_ac_01, "Enforce MFA for user accounts."))

    def check_ac_02(data: Dict[str, Any]) -> List[ComplianceResult]:
        res = []
        for e in data.get('employees', []):
            if e['password_strength_score'] < 80:
                res.append(ComplianceResult("AC-02", "Password Strength", Status.WARNING, f"Employee {e['employee_id']} weak password", datetime.datetime.now().isoformat(), Severity.MEDIUM))
        if not res: res.append(ComplianceResult("AC-02", "Password Strength", Status.PASS, "Password strength sufficient", datetime.datetime.now().isoformat(), Severity.MEDIUM))
        return res
    rules.append(PolicyRule("AC-02", "Password Strength", "Access Control", "Password strength must be >= 80.", Severity.MEDIUM, check_ac_02, "Prompt user to update password."))

    def check_ac_03(data: Dict[str, Any]) -> List[ComplianceResult]:
        res = []
        for e in data.get('employees', []):
            if e['role'] == 'Intern' and e['access_level'] > 1:
                res.append(ComplianceResult("AC-03", "Role-Based Access", Status.FAIL, f"Intern {e['employee_id']} has elevated access", datetime.datetime.now().isoformat(), Severity.HIGH))
        if not res: res.append(ComplianceResult("AC-03", "Role-Based Access", Status.PASS, "RBAC valid", datetime.datetime.now().isoformat(), Severity.HIGH))
        return res
    rules.append(PolicyRule("AC-03", "Role-Based Access", "Access Control", "Interns must have level 1 access.", Severity.HIGH, check_ac_03, "Revoke elevated privileges from interns."))

    # --- Financial Compliance ---
    def check_fc_01(data: Dict[str, Any]) -> List[ComplianceResult]:
        res = []
        for t in data.get('transactions', []):
            if t['amount'] > 10000 and t['approval_status'] != 'Approved':
                res.append(ComplianceResult("FC-01", "Transaction Limit", Status.FAIL, f"Transaction {t['transaction_id']} unapproved but over 10k", datetime.datetime.now().isoformat(), Severity.CRITICAL))
        if not res: res.append(ComplianceResult("FC-01", "Transaction Limit", Status.PASS, "All high-value tx approved", datetime.datetime.now().isoformat(), Severity.CRITICAL))
        return res
    rules.append(PolicyRule("FC-01", "Transaction Limit", "Financial Compliance", "Transactions >10k must be approved.", Severity.CRITICAL, check_fc_01, "Review and approve large transactions."))

    def check_fc_02(data: Dict[str, Any]) -> List[ComplianceResult]:
        res = []
        for t in data.get('transactions', []):
            if not t['has_audit_trail']:
                res.append(ComplianceResult("FC-02", "Audit Trail", Status.FAIL, f"Transaction {t['transaction_id']} missing audit trail", datetime.datetime.now().isoformat(), Severity.HIGH))
        if not res: res.append(ComplianceResult("FC-02", "Audit Trail", Status.PASS, "Audit trails intact", datetime.datetime.now().isoformat(), Severity.HIGH))
        return res
    rules.append(PolicyRule("FC-02", "Audit Trail", "Financial Compliance", "All transactions must have an audit trail.", Severity.HIGH, check_fc_02, "Ensure transaction logging is active."))

    def check_fc_03(data: Dict[str, Any]) -> List[ComplianceResult]:
        res = []
        for t in data.get('transactions', []):
            if t['type'] == 'Refund' and t['amount'] > 5000:
                res.append(ComplianceResult("FC-03", "Refund Limits", Status.WARNING, f"Large refund {t['transaction_id']}", datetime.datetime.now().isoformat(), Severity.MEDIUM))
        if not res: res.append(ComplianceResult("FC-03", "Refund Limits", Status.PASS, "Refunds within limits", datetime.datetime.now().isoformat(), Severity.MEDIUM))
        return res
    rules.append(PolicyRule("FC-03", "Refund Limits", "Financial Compliance", "Refunds over 5k require manual review.", Severity.MEDIUM, check_fc_03, "Flag large refunds for review."))

    # --- HR Policies ---
    def check_hr_01(data: Dict[str, Any]) -> List[ComplianceResult]:
        res = []
        for e in data.get('employees', []):
            if e['working_hours_per_week'] > 60:
                res.append(ComplianceResult("HR-01", "Working Hours", Status.FAIL, f"Employee {e['employee_id']} works {e['working_hours_per_week']}h", datetime.datetime.now().isoformat(), Severity.MEDIUM))
        if not res: res.append(ComplianceResult("HR-01", "Working Hours", Status.PASS, "Working hours normal", datetime.datetime.now().isoformat(), Severity.MEDIUM))
        return res
    rules.append(PolicyRule("HR-01", "Working Hours", "HR Policies", "Max 60 hours per week.", Severity.MEDIUM, check_hr_01, "Review employee workload."))

    def check_hr_02(data: Dict[str, Any]) -> List[ComplianceResult]:
        res = []
        for e in data.get('employees', []):
            if e['leave_balance'] < 0:
                res.append(ComplianceResult("HR-02", "Leave Balance", Status.FAIL, f"Employee {e['employee_id']} negative leave", datetime.datetime.now().isoformat(), Severity.LOW))
        if not res: res.append(ComplianceResult("HR-02", "Leave Balance", Status.PASS, "Leave balances valid", datetime.datetime.now().isoformat(), Severity.LOW))
        return res
    rules.append(PolicyRule("HR-02", "Leave Balance", "HR Policies", "Leave balance cannot be negative.", Severity.LOW, check_hr_02, "Adjust leave records."))

    def check_hr_03(data: Dict[str, Any]) -> List[ComplianceResult]:
        res = []
        six_months_ago = datetime.date.today() - datetime.timedelta(days=180)
        for e in data.get('employees', []):
            if datetime.date.fromisoformat(e['last_training_date']) < six_months_ago:
                res.append(ComplianceResult("HR-03", "Mandatory Training", Status.WARNING, f"Employee {e['employee_id']} training outdated", datetime.datetime.now().isoformat(), Severity.HIGH))
        if not res: res.append(ComplianceResult("HR-03", "Mandatory Training", Status.PASS, "Training up to date", datetime.datetime.now().isoformat(), Severity.HIGH))
        return res
    rules.append(PolicyRule("HR-03", "Mandatory Training", "HR Policies", "Training required every 6 months.", Severity.HIGH, check_hr_03, "Schedule training for employees."))

    # --- IT Security ---
    def check_it_01(data: Dict[str, Any]) -> List[ComplianceResult]:
        res = []
        for s in data.get('it_systems', []):
            if not s['firewall_enabled']:
                res.append(ComplianceResult("IT-01", "Firewall Configuration", Status.FAIL, f"System {s['system_id']} lacks firewall", datetime.datetime.now().isoformat(), Severity.CRITICAL))
        if not res: res.append(ComplianceResult("IT-01", "Firewall Configuration", Status.PASS, "All firewalls enabled", datetime.datetime.now().isoformat(), Severity.CRITICAL))
        return res
    rules.append(PolicyRule("IT-01", "Firewall Configuration", "IT Security", "Firewalls must be enabled on all systems.", Severity.CRITICAL, check_it_01, "Enable firewalls immediately."))

    def check_it_02(data: Dict[str, Any]) -> List[ComplianceResult]:
        res = []
        for s in data.get('it_systems', []):
            if s['backup_frequency_days'] > 1:
                res.append(ComplianceResult("IT-02", "Backup Frequency", Status.WARNING, f"System {s['system_id']} backup > 1 day", datetime.datetime.now().isoformat(), Severity.HIGH))
        if not res: res.append(ComplianceResult("IT-02", "Backup Frequency", Status.PASS, "Daily backups active", datetime.datetime.now().isoformat(), Severity.HIGH))
        return res
    rules.append(PolicyRule("IT-02", "Backup Frequency", "IT Security", "Systems require daily backups.", Severity.HIGH, check_it_02, "Configure daily backups."))

    def check_it_03(data: Dict[str, Any]) -> List[ComplianceResult]:
        res = []
        for s in data.get('it_systems', []):
            if len(s['open_ports']) > 3:
                res.append(ComplianceResult("IT-03", "Open Ports Limit", Status.FAIL, f"System {s['system_id']} has {len(s['open_ports'])} open ports", datetime.datetime.now().isoformat(), Severity.MEDIUM))
        if not res: res.append(ComplianceResult("IT-03", "Open Ports Limit", Status.PASS, "Port limits respected", datetime.datetime.now().isoformat(), Severity.MEDIUM))
        return res
    rules.append(PolicyRule("IT-03", "Open Ports Limit", "IT Security", "Max 3 open ports per system.", Severity.MEDIUM, check_it_03, "Close unnecessary open ports."))

    return rules

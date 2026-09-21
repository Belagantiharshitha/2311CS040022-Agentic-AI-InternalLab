import random
from typing import Dict, Any, List
import datetime

try:
    from faker import Faker
except ImportError:
    pass

class SyntheticDataGenerator:
    def __init__(self, seed: int = 42):
        self.fake = Faker()
        Faker.seed(seed)
        random.seed(seed)
        
    def generate_employees(self, count: int = 50) -> List[Dict[str, Any]]:
        employees = []
        for i in range(count):
            role = random.choice(["Engineer", "Manager", "HR", "Intern", "Analyst"])
            is_non_compliant = random.random() < 0.3
            
            emp = {
                "employee_id": f"EMP-{1000+i}",
                "name": self.fake.name(),
                "email": self.fake.email(),
                "department": random.choice(["Engineering", "Sales", "HR", "Finance", "IT"]),
                "role": role,
                "access_level": 5 if is_non_compliant and role == "Intern" else random.randint(1, 4),
                "mfa_enabled": False if is_non_compliant else True,
                "password_strength_score": random.randint(40, 70) if is_non_compliant else random.randint(80, 100),
                "last_training_date": (datetime.date.today() - datetime.timedelta(days=random.randint(200, 300) if is_non_compliant else random.randint(10, 150))).isoformat(),
                "working_hours_per_week": random.randint(65, 80) if is_non_compliant else random.randint(35, 50),
                "leave_balance": random.randint(-10, -1) if is_non_compliant else random.randint(5, 25),
            }
            employees.append(emp)
        return employees

    def generate_transactions(self, count: int = 100) -> List[Dict[str, Any]]:
        transactions = []
        for i in range(count):
            is_non_compliant = random.random() < 0.3
            amt = random.randint(15000, 50000) if is_non_compliant else random.randint(100, 9000)
            ttype = "Refund" if is_non_compliant and random.random() < 0.5 else random.choice(["Purchase", "Transfer", "Deposit", "Refund"])
            
            if ttype == "Refund" and is_non_compliant:
                amt = random.randint(6000, 10000)
                
            tx = {
                "transaction_id": f"TXN-{10000+i}",
                "employee_id": f"EMP-{random.randint(1000, 1049)}",
                "amount": amt,
                "type": ttype,
                "approval_status": "Pending" if is_non_compliant and amt > 10000 else "Approved",
                "has_audit_trail": False if is_non_compliant else True,
                "timestamp": self.fake.iso8601()
            }
            transactions.append(tx)
        return transactions

    def generate_it_systems(self, count: int = 30) -> List[Dict[str, Any]]:
        systems = []
        for i in range(count):
            is_non_compliant = random.random() < 0.3
            
            sys = {
                "system_id": f"SYS-{100+i}",
                "name": f"Server-{self.fake.word()}",
                "last_update": self.fake.iso8601(),
                "firewall_enabled": False if is_non_compliant else True,
                "backup_frequency_days": random.randint(2, 7) if is_non_compliant else 1,
                "encryption_enabled": False if is_non_compliant else True,
                "open_ports": random.sample([22, 80, 443, 3306, 8080, 5432, 21], random.randint(4, 6) if is_non_compliant else random.randint(1, 3))
            }
            systems.append(sys)
        return systems

    def generate_data_records(self, count: int = 80) -> List[Dict[str, Any]]:
        records = []
        for i in range(count):
            is_non_compliant = random.random() < 0.3
            contains_pii = random.choice([True, False])
            
            if contains_pii and is_non_compliant:
                encrypted = False
            else:
                encrypted = True
                
            rec = {
                "record_id": f"REC-{5000+i}",
                "contains_pii": contains_pii,
                "pii_types": ["Email", "SSN"] if contains_pii else [],
                "retention_days": random.randint(400, 1000) if is_non_compliant else random.randint(30, 360),
                "encrypted": encrypted,
                "access_log_enabled": False if is_non_compliant else True
            }
            records.append(rec)
        return records

    def get_all_data(self) -> Dict[str, Any]:
        return {
            "employees": self.generate_employees(50),
            "transactions": self.generate_transactions(100),
            "it_systems": self.generate_it_systems(30),
            "data_records": self.generate_data_records(80)
        }

# 🛡️ Policy Compliance Agent — Lab Experiment 2

## Experiment Overview

This lab experiment demonstrates an **AI-powered Policy Compliance Agent** that uses **rule-based evaluation** on **synthetic enterprise data** to detect policy violations across five compliance domains. The agent evaluates 260+ records against 15 policy rules and produces a professional multi-page PDF audit report.

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                     main.py (Entry Point)                │
│          Rich CLI: banners, progress bars, tables        │
├──────────────────────────────────────────────────────────┤
│                                                          │
│   ┌─────────────────┐     ┌─────────────────────────┐   │
│   │ synthetic_data.py│────▶│  compliance_agent.py     │   │
│   │ (Data Generator) │     │  (Audit Orchestrator)    │   │
│   │                  │     │                          │   │
│   │ • 50 Employees   │     │ • Runs full audit        │   │
│   │ • 100 Transactions│    │ • Computes scores        │   │
│   │ • 30 IT Systems  │     │ • Generates metrics      │   │
│   │ • 80 Data Records│     │ • Produces recommendations│  │
│   └─────────────────┘     └────────────┬────────────┘   │
│                                         │                │
│   ┌─────────────────┐     ┌────────────▼────────────┐   │
│   │ policy_rules.py  │────▶│  report_generator.py     │   │
│   │ (Rule Engine)    │     │  (PDF Report Builder)    │   │
│   │                  │     │                          │   │
│   │ • 15 Policy Rules│     │ • Matplotlib charts      │   │
│   │ • 5 Categories   │     │ • Multi-page PDF         │   │
│   │ • 4 Severity Lvls│     │ • Tables & appendix      │   │
│   └─────────────────┘     └──────────────────────────┘   │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

## Policy Categories & Rules

| Category | Rules | Severity Range | What It Checks |
|---|---|---|---|
| **Data Privacy** | DP-01, DP-02, DP-03 | CRITICAL – HIGH | PII encryption, data retention, access logging |
| **Access Control** | AC-01, AC-02, AC-03 | CRITICAL – MEDIUM | MFA enforcement, password strength, RBAC validation |
| **Financial Compliance** | FC-01, FC-02, FC-03 | CRITICAL – MEDIUM | Transaction limits, audit trails, refund monitoring |
| **HR Policies** | HR-01, HR-02, HR-03 | HIGH – LOW | Working hours, leave balance, mandatory training |
| **IT Security** | IT-01, IT-02, IT-03 | CRITICAL – MEDIUM | Firewall config, backup frequency, open port limits |

## File Structure

```
Experiment 2/
├── main.py                 # Entry point — run this to execute the experiment
├── policy_rules.py         # Rule engine with 15 policy rules
├── synthetic_data.py       # Synthetic data generator (Faker-based)
├── compliance_agent.py     # Core compliance evaluation agent
├── report_generator.py     # PDF report generator with charts
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── charts/                 # Generated chart images (auto-created)
│   ├── compliance_pie.png
│   ├── category_bar.png
│   └── severity_bar.png
└── Policy_Compliance_Audit_Report.pdf  # Generated audit report (auto-created)
```

## Setup & Execution

### Prerequisites
- Python 3.8 or later
- pip (Python package manager)

### Step 1: Install Dependencies
```bash
cd "e:\Agentic Internal Lab\Experiment 2"
pip install -r requirements.txt
```

### Step 2: Run the Experiment
```bash
python main.py
```

### Step 3: Review Outputs
- **Terminal**: Rich-formatted tables with rule summaries, audit results, and top violations
- **PDF Report**: `Policy_Compliance_Audit_Report.pdf` in the experiment directory
- **Charts**: PNG visualizations in the `charts/` subdirectory

## Expected Output

### Terminal Output
The terminal will display:
1. A styled welcome banner
2. Progress bars during data generation and evaluation
3. A table of all 15 loaded policy rules
4. An audit summary panel with compliance score
5. A top-violations table ranked by severity
6. File path of the generated PDF report

### PDF Report Contents
The generated PDF includes:
- **Title Page** with experiment details and date
- **Executive Summary** with overall compliance score and risk assessment
- **Methodology** section explaining rule-based evaluation approach
- **Audit Visualizations** — pie chart, category bar chart, severity distribution
- **Detailed Findings** — per-category violation tables
- **Severity Summary** — tabular breakdown of violations by severity level
- **Recommendations** — numbered, actionable remediation steps
- **Appendix** — complete policy rule definitions table

## Key Design Decisions

1. **30% Non-Compliance Rate**: Synthetic data intentionally generates ~30% non-compliant records to demonstrate the agent's detection capabilities
2. **Deterministic Seed**: Random seed `42` ensures reproducible results across runs
3. **Category-Based Organization**: Rules and findings are organized by compliance domain for clarity
4. **Severity-Weighted Scoring**: Violations are ranked by severity (CRITICAL > HIGH > MEDIUM > LOW)

## Technologies Used

| Library | Purpose |
|---|---|
| `faker` | Realistic synthetic data generation (names, emails, dates) |
| `fpdf2` | PDF document generation |
| `matplotlib` | Chart and visualization creation |
| `rich` | Terminal UI (progress bars, tables, panels, colored output) |

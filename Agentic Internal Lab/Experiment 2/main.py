import os
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress

from synthetic_data import SyntheticDataGenerator
from policy_rules import get_default_rules
from compliance_agent import PolicyComplianceAgent
from report_generator import ReportGenerator

def main():
    console = Console()
    console.print(Panel.fit("[bold blue]Policy Compliance Agent[/bold blue]\n[green]Lab Experiment 2[/green]", border_style="blue"))
    
    # 1. Init Data
    with Progress() as progress:
        task1 = progress.add_task("[cyan]Generating synthetic data...", total=100)
        generator = SyntheticDataGenerator()
        data = generator.get_all_data()
        for i in range(100):
            time.sleep(0.01)
            progress.update(task1, advance=1)
            
    console.print(f"[bold green]Data Generated:[/bold green] {len(data['employees'])} Employees, {len(data['transactions'])} Transactions, {len(data['it_systems'])} IT Systems, {len(data['data_records'])} Data Records\n")

    # 2. Init Rules
    rules = get_default_rules()
    console.print(f"[bold green]Loaded {len(rules)} Policy Rules[/bold green]")
    rule_table = Table(show_header=True, header_style="bold magenta")
    rule_table.add_column("Rule ID", style="dim", width=12)
    rule_table.add_column("Category")
    rule_table.add_column("Name")
    rule_table.add_column("Severity")
    for r in rules:
        rule_table.add_row(r.rule_id, r.category, r.name, r.severity.value)
    console.print(rule_table)
    console.print()

    # 3. Run Agent
    agent = PolicyComplianceAgent(data)
    with Progress() as progress:
        task2 = progress.add_task("[magenta]Running full compliance audit...", total=100)
        audit_summary = agent.run_full_audit()
        for i in range(100):
            time.sleep(0.01)
            progress.update(task2, advance=1)

    # 4. Display Results
    console.print(Panel(f"Overall Compliance Score: [bold cyan]{audit_summary['compliance_score']}%[/bold cyan]\nTotal Violations: [bold red]{audit_summary['total_violations']}[/bold red]", title="Audit Summary", expand=False))

    top_v_table = Table(title="Top Violations")
    top_v_table.add_column("Rule ID")
    top_v_table.add_column("Severity")
    top_v_table.add_column("Details")
    for v in audit_summary['top_violations'][:5]:
        top_v_table.add_row(v.rule_id, f"[{'red' if v.severity.value == 'CRITICAL' else 'yellow'}]{v.severity.value}[/]", v.details)
    console.print(top_v_table)
    
    # 5. Generate Report
    base_dir = os.path.dirname(os.path.abspath(__file__))
    rg = ReportGenerator(base_dir)
    recs = agent.get_recommendations(audit_summary['all_results'])
    
    with Progress() as progress:
        task3 = progress.add_task("[yellow]Generating PDF report...", total=100)
        report_path = rg.generate_pdf(audit_summary, recs)
        for i in range(100):
            time.sleep(0.01)
            progress.update(task3, advance=1)
            
    console.print(f"\n[bold green]Report saved to:[/bold green] {report_path}")
    console.print("[italic]Experiment complete. Review the PDF for detailed insights.[/italic]")

if __name__ == "__main__":
    main()

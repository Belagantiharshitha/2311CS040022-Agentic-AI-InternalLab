"""
report_generator.py - Professional PDF Report Generator
Generates a comprehensive multi-page audit report with charts, tables, and analysis.
"""

import os
import datetime
from typing import Dict, Any, List
from fpdf import FPDF
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for server/headless environments
import matplotlib.pyplot as plt

from policy_rules import get_default_rules, Status


class AuditReportPDF(FPDF):
    """Custom FPDF subclass with header/footer branding."""

    def header(self):
        if self.page_no() > 1:
            self.set_font("helvetica", "I", 8)
            self.set_text_color(120, 120, 120)
            self.cell(0, 8, "Policy Compliance Audit Report  |  Agentic Internal Lab - Experiment 2", align="L")
            self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")


class ReportGenerator:
    """Generates professional PDF audit reports with embedded charts and tables."""

    def __init__(self, experiment_dir: str):
        self.experiment_dir = experiment_dir
        self.charts_dir = os.path.join(experiment_dir, "charts")
        os.makedirs(self.charts_dir, exist_ok=True)

    # ------------------------------------------------------------------ #
    #  Chart Generation
    # ------------------------------------------------------------------ #
    def generate_charts(self, audit_summary: Dict[str, Any]) -> None:
        """Create matplotlib charts and save them as PNGs."""
        plt.style.use('seaborn-v0_8-whitegrid')

        # 1. Compliance Pie Chart
        total_violations = audit_summary['total_violations']
        total_passes = len([r for r in audit_summary['all_results'] if r.status == Status.PASS])
        labels = ['Compliant', 'Violations']
        sizes = [total_passes, total_violations]
        colors = ['#43A047', '#E53935']
        explode = (0.04, 0.04)

        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors,
               explode=explode, startangle=140, textprops={'fontsize': 12})
        ax.set_title('Overall Compliance Overview', fontsize=14, fontweight='bold', pad=20)
        fig.savefig(os.path.join(self.charts_dir, 'compliance_pie.png'), dpi=150, bbox_inches='tight')
        plt.close(fig)

        # 2. Violations by Category
        cat_data = audit_summary['category_breakdown']
        if cat_data:
            fig, ax = plt.subplots(figsize=(9, 5))
            bars = ax.bar(list(cat_data.keys()), list(cat_data.values()),
                          color=['#1565C0', '#00897B', '#6A1B9A', '#E65100', '#AD1457'])
            ax.set_title('Violations by Category', fontsize=14, fontweight='bold')
            ax.set_ylabel('Number of Violations')
            ax.bar_label(bars, padding=3)
            plt.xticks(rotation=30, ha='right')
            fig.tight_layout()
            fig.savefig(os.path.join(self.charts_dir, 'category_bar.png'), dpi=150, bbox_inches='tight')
            plt.close(fig)

        # 3. Severity Distribution
        sev_data = audit_summary['severity_distribution']
        sev_colors = {'CRITICAL': '#B71C1C', 'HIGH': '#E65100', 'MEDIUM': '#F9A825', 'LOW': '#2E7D32'}
        fig, ax = plt.subplots(figsize=(7, 5))
        bars = ax.bar(list(sev_data.keys()), list(sev_data.values()),
                      color=[sev_colors.get(k, '#757575') for k in sev_data.keys()])
        ax.set_title('Violations by Severity Level', fontsize=14, fontweight='bold')
        ax.set_ylabel('Count')
        ax.bar_label(bars, padding=3)
        fig.tight_layout()
        fig.savefig(os.path.join(self.charts_dir, 'severity_bar.png'), dpi=150, bbox_inches='tight')
        plt.close(fig)

    # ------------------------------------------------------------------ #
    #  PDF Generation
    # ------------------------------------------------------------------ #
    def generate_pdf(self, audit_summary: Dict[str, Any], recommendations: List[str]) -> str:
        """Build and save the full PDF report. Returns the path to the saved file."""
        self.generate_charts(audit_summary)

        pdf = AuditReportPDF()
        pdf.alias_nb_pages()
        today = datetime.date.today().strftime("%B %d, %Y")

        # ===== TITLE PAGE ===== #
        pdf.add_page()
        pdf.ln(40)
        pdf.set_font("helvetica", "B", 28)
        pdf.set_text_color(25, 25, 112)
        pdf.cell(0, 15, "Policy Compliance", ln=True, align="C")
        pdf.cell(0, 15, "Audit Report", ln=True, align="C")
        pdf.ln(10)
        pdf.set_draw_color(25, 25, 112)
        pdf.set_line_width(0.8)
        pdf.line(60, pdf.get_y(), 150, pdf.get_y())
        pdf.ln(10)
        pdf.set_font("helvetica", "", 14)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(0, 10, "Agentic Internal Lab - Experiment 2", ln=True, align="C")
        pdf.cell(0, 10, f"Generated: {today}", ln=True, align="C")
        pdf.ln(8)
        pdf.set_font("helvetica", "I", 11)
        pdf.cell(0, 10, "Rule-Based Evaluation with Synthetic Data", ln=True, align="C")

        # ===== EXECUTIVE SUMMARY ===== #
        pdf.add_page()
        self._section_heading(pdf, "1. Executive Summary")
        score = audit_summary['compliance_score']
        total_v = audit_summary['total_violations']
        total_results = len(audit_summary['all_results'])
        pdf.set_font("helvetica", "", 11)
        pdf.multi_cell(0, 7, (
            f"This report presents the findings of an automated policy compliance audit "
            f"conducted on {today}. The agent evaluated {total_results} compliance checks "
            f"across 15 policy rules spanning 5 categories.\n\n"
            f"Overall Compliance Score:  {score}%\n"
            f"Total Violations Detected: {total_v}\n"
        ))
        pdf.ln(3)

        # Score indicator
        pdf.set_font("helvetica", "B", 12)
        if score >= 80:
            pdf.set_text_color(46, 125, 50)
            indicator = "GOOD"
        elif score >= 60:
            pdf.set_text_color(245, 124, 0)
            indicator = "NEEDS IMPROVEMENT"
        else:
            pdf.set_text_color(198, 40, 40)
            indicator = "CRITICAL - IMMEDIATE ACTION REQUIRED"
        pdf.cell(0, 10, f"Risk Assessment: {indicator}", ln=True)
        pdf.set_text_color(0, 0, 0)
        pdf.ln(5)

        # ===== METHODOLOGY ===== #
        self._section_heading(pdf, "2. Methodology")
        pdf.set_font("helvetica", "", 11)
        pdf.multi_cell(0, 7, (
            "This audit employs a rule-based evaluation methodology. Each policy rule is "
            "defined as a structured object containing:\n"
            "  - A unique rule identifier and descriptive name\n"
            "  - Category classification (Data Privacy, Access Control, Financial, HR, IT Security)\n"
            "  - Severity level (CRITICAL, HIGH, MEDIUM, LOW)\n"
            "  - A deterministic check function that evaluates records against the policy\n"
            "  - A prescribed remediation action\n\n"
            "Synthetic data was generated using the Faker library with a fixed random seed (42) "
            "for reproducibility. Approximately 30% of records were intentionally generated as "
            "non-compliant to validate the agent's detection capabilities.\n\n"
            "Data volumes evaluated:\n"
            "  - 50 employee records (6 HR/Access Control rules)\n"
            "  - 100 financial transaction records (3 financial rules)\n"
            "  - 30 IT system records (3 IT security rules)\n"
            "  - 80 data privacy records (3 data privacy rules)"
        ))
        pdf.ln(5)

        # ===== VISUALIZATIONS ===== #
        pdf.add_page()
        self._section_heading(pdf, "3. Audit Visualizations")
        try:
            pie_path = os.path.join(self.charts_dir, 'compliance_pie.png')
            if os.path.exists(pie_path):
                pdf.image(pie_path, x=55, w=100)
                pdf.ln(5)

            cat_path = os.path.join(self.charts_dir, 'category_bar.png')
            if os.path.exists(cat_path):
                pdf.add_page()
                pdf.image(cat_path, x=30, w=150)
                pdf.ln(5)

            sev_path = os.path.join(self.charts_dir, 'severity_bar.png')
            if os.path.exists(sev_path):
                pdf.image(sev_path, x=35, w=140)
        except Exception as e:
            pdf.set_font("helvetica", "I", 10)
            pdf.cell(0, 10, f"(Charts could not be embedded: {e})", ln=True)
        pdf.ln(5)

        # ===== DETAILED FINDINGS ===== #
        pdf.add_page()
        self._section_heading(pdf, "4. Detailed Findings by Category")

        cat_breakdown = audit_summary['category_breakdown']
        for category, count in cat_breakdown.items():
            pdf.set_font("helvetica", "B", 12)
            pdf.set_text_color(25, 25, 112)
            pdf.cell(0, 9, f"{category}  ({count} violation{'s' if count != 1 else ''})", ln=True)
            pdf.set_text_color(0, 0, 0)

            # Table header
            pdf.set_font("helvetica", "B", 9)
            pdf.set_fill_color(230, 230, 240)
            pdf.cell(22, 7, "Rule ID", border=1, fill=True)
            pdf.cell(35, 7, "Rule Name", border=1, fill=True)
            pdf.cell(20, 7, "Status", border=1, fill=True)
            pdf.cell(20, 7, "Severity", border=1, fill=True)
            pdf.cell(93, 7, "Details", border=1, fill=True, ln=True)

            # Table rows for this category
            pdf.set_font("helvetica", "", 8)
            category_results = [
                r for r in audit_summary['all_results']
                if r.status != Status.PASS and
                any(rule.rule_id == r.rule_id and rule.category == category
                    for rule in get_default_rules())
            ]
            # Limit to first 15 rows per category in the PDF for readability
            for r in category_results[:15]:
                detail_text = (r.details[:55] + "...") if len(r.details) > 55 else r.details
                pdf.cell(22, 6, r.rule_id, border=1)
                pdf.cell(35, 6, r.rule_name[:20], border=1)
                pdf.cell(20, 6, r.status.value, border=1)
                pdf.cell(20, 6, r.severity.value, border=1)
                pdf.cell(93, 6, detail_text, border=1, ln=True)

            if len(category_results) > 15:
                pdf.set_font("helvetica", "I", 8)
                pdf.cell(0, 6, f"  ... and {len(category_results) - 15} more violations in this category", ln=True)
            pdf.ln(4)

        # ===== SEVERITY SUMMARY TABLE ===== #
        pdf.add_page()
        self._section_heading(pdf, "5. Severity Summary")
        sev = audit_summary['severity_distribution']
        pdf.set_font("helvetica", "B", 10)
        pdf.set_fill_color(230, 230, 240)
        pdf.cell(50, 8, "Severity Level", border=1, fill=True)
        pdf.cell(40, 8, "Count", border=1, fill=True)
        pdf.cell(50, 8, "% of Total", border=1, fill=True, ln=True)
        pdf.set_font("helvetica", "", 10)
        total_sev = sum(sev.values()) or 1
        for level, count in sev.items():
            pct = round(count / total_sev * 100, 1)
            pdf.cell(50, 7, level, border=1)
            pdf.cell(40, 7, str(count), border=1)
            pdf.cell(50, 7, f"{pct}%", border=1, ln=True)
        pdf.ln(5)

        # ===== RECOMMENDATIONS ===== #
        self._section_heading(pdf, "6. Actionable Recommendations")
        pdf.set_font("helvetica", "", 10)
        for i, rec in enumerate(recommendations, 1):
            pdf.multi_cell(0, 7, f"{i}. {rec}")
            pdf.ln(1)
        pdf.ln(3)

        # ===== APPENDIX - RULE DEFINITIONS ===== #
        pdf.add_page()
        self._section_heading(pdf, "Appendix A: Complete Policy Rule Definitions")
        rules = get_default_rules()
        pdf.set_font("helvetica", "B", 9)
        pdf.set_fill_color(230, 230, 240)
        pdf.cell(18, 7, "ID", border=1, fill=True)
        pdf.cell(35, 7, "Name", border=1, fill=True)
        pdf.cell(30, 7, "Category", border=1, fill=True)
        pdf.cell(20, 7, "Severity", border=1, fill=True)
        pdf.cell(87, 7, "Description", border=1, fill=True, ln=True)

        pdf.set_font("helvetica", "", 8)
        for rule in rules:
            desc = (rule.description[:52] + "...") if len(rule.description) > 52 else rule.description
            pdf.cell(18, 6, rule.rule_id, border=1)
            pdf.cell(35, 6, rule.name[:22], border=1)
            pdf.cell(30, 6, rule.category[:18], border=1)
            pdf.cell(20, 6, rule.severity.value, border=1)
            pdf.cell(87, 6, desc, border=1, ln=True)
        pdf.ln(5)

        pdf.set_font("helvetica", "I", 9)
        pdf.cell(0, 8, "--- End of Report ---", align="C")

        # Save
        report_path = os.path.join(self.experiment_dir, "Policy_Compliance_Audit_Report.pdf")
        pdf.output(report_path)
        return report_path

    # ------------------------------------------------------------------ #
    #  Helpers
    # ------------------------------------------------------------------ #
    @staticmethod
    def _section_heading(pdf: FPDF, title: str) -> None:
        """Render a styled section heading."""
        pdf.set_font("helvetica", "B", 15)
        pdf.set_text_color(25, 25, 112)
        pdf.cell(0, 12, title, ln=True)
        pdf.set_draw_color(25, 25, 112)
        pdf.set_line_width(0.5)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)
        pdf.set_text_color(0, 0, 0)

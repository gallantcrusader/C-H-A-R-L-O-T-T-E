# ******************************************************************************************
# main.py - Minimal Launcher for CHARLOTTE with Banner and Plugin Hook
# ******************************************************************************************

import os
import sys
import json
from core import cve_lookup
from datetime import datetime
from InquirerPy import inquirer
from agents.triage_agent import run_triage_agent
from core.plugin_manager import run_plugin
from core.charlotte_personality import CharlottePersonality
from InquirerPy.separator import Separator


# Initialize CHARLOTTE personality
charlotte = CharlottePersonality()

# ******************************************************************************************
# Banner Art
# ******************************************************************************************


def print_banner():
    PURPLE = "\033[35m"
    RESET = "\033[0m"
    skull_banner = f"""{PURPLE}
            ☠ ╔═══════════════╗
            ☠ ║   CHARLOTTE   ║
            ☠ ╚═══════════════╝
        🔮 Predict | Triage | Own 🔮

{PURPLE}  The Cybersecurity Assistant  {RESET}
{PURPLE}  Version: 0.1.0  {RESET}   
{RESET}"""
    print(skull_banner)


# ******************************************************************************************
# Plugin Task Mapping
# ******************************************************************************************

PLUGIN_TASKS = {
    "🧠 Reverse Engineer Binary (Symbolic Trace)": "reverse_engineering",
    "🔍 Binary Strings + Entropy Analysis": "binary_strings",
    "🔓 Binary Exploit (ROP Chain)": "binary_exploit",
    "🕵️ CVE Lookup (CHARLOTTE)": "cve_lookup",
    "🚨 Exploit Generator": "exploit_generation",
    "🔗 Link Analysis": "link_analysis",
    "📡 NMAP Scan": "nmap_plugin",
    "🧨 Predict Exploitability": "exploit_predictor",
    "🔎 Search Exploit DB": "exploit_search",
    "💉 SQL Injection Scan": "sql_injection",
    "🧪 Static Analysis (Binary)": "static_analysis",
    "📊 Vulnerability Assessment": "vulnerability_assessment",
    "🧮 Vulnerability Triage (Score + Prioritize)": "triage_agent",
    "🌐 Web Recon (Subdomains)": "web_recon",
    "🧼 XSS Scan": "xss_scan",
}

# ******************************************************************************************
# CVE Lookup Menu Logic
# ******************************************************************************************


def run_cve_lookup():
    print("\n=== HARLOTTE CVE Intelligence Module ===")

    option = inquirer.select(
        message="Choose your CVE query method:",
        choices=[
            "🔎 Lookup by CVE ID",
            "🗂️ Search by Keyword",
            "📅 List CVEs by Product and Year",
            "❌ Back to Main Menu",
        ],
    ).execute()

    if option == "🔎 Lookup by CVE ID":
        cve_id = input("Enter CVE ID (e.g., CVE-2023-12345): ").strip().upper()
        if not cve_id.startswith("CVE-"):
            print("Invalid CVE ID format.")
            return
        result = cve_lookup.fetch_and_cache(cve_id)
        cve_lookup.show_and_export(result)

    elif option == "🗂️ Search by Keyword":
        keyword = (
            input("Enter keyword (e.g., apache, buffer overflow): ").strip().lower()
        )
        results = cve_lookup.search_by_keyword(keyword)
        cve_lookup.show_and_export(results, multiple=True)

    elif option == "📅 List CVEs by Product and Year":
        product = input("Enter product name (e.g., chrome, openssl): ").strip().lower()
        year = input("Enter year (e.g., 2022): ").strip()
        results = cve_lookup.search_by_product_year(product, year)
        cve_lookup.show_and_export(results, multiple=True)

    else:
        return


# ******************************************************************************************
# Main CLI Application Logic
# ******************************************************************************************


def main():
    print_banner()
    # load_plugins()

    task = inquirer.select(
        message="What would you like CHARLOTTE to do?",
        choices=[
            Separator("=== Binary Ops ==="),
            *[k for k in PLUGIN_TASKS.keys() if "Binary" in k],
            Separator("=== Recon ==="),
            *[k for k in PLUGIN_TASKS.keys() if "Scan" in k or "Recon" in k],
            Separator("=== Exploitation ==="),
            *[k for k in PLUGIN_TASKS.keys() if "Exploit" in k],
            Separator("=== Intelligence ==="),
            "🕵️ CVE Lookup (CHARLOTTE)",
            Separator("=== Scoring & Analysis ==="),
            *[k for k in PLUGIN_TASKS.keys() if "Triage" in k or "Assessment" in k],
            Separator(),
            "❌ Exit",
        ],
    ).execute()

    if task == "❌ Exit":
        print("Goodbye, bestie 🖤")
        return

    if task == "🕵️ CVE Lookup (CHARLOTTE)":
        run_cve_lookup()
        return

    # --------------------------------------------------
    # Plugin/Agent Execution Logic
    # --------------------------------------------------
    # --------------------------------------------------
    # Plugin/Agent Execution Logic
    # --------------------------------------------------
    plugin_key = PLUGIN_TASKS.get(task)

    if plugin_key == "triage_agent":
        scan_path = inquirer.text(
            message="Enter path to scan file (press Enter for default: data/findings.json):"
        ).execute()
        scan_path = scan_path.strip() or "data/findings.json"
        run_triage_agent(scan_file=scan_path)

    elif plugin_key == "exploit_predictor":
        from core.logic_modules.exploit_predictor import batch_predict
        from agents.triage_agent import load_findings, save_results

        scan_path = inquirer.text(
            message="Enter path to scan file (press Enter for default: data/findings.json):"
        ).execute()
        scan_path = scan_path.strip() or "data/findings.json"

        try:
            findings = load_findings(scan_path)
            enriched = batch_predict(findings)
            output_path = "data/findings_with_predictions.json"
            save_results(output_path, enriched)

            print(f"\n[✔] Exploit predictions saved to {output_path}")
            print("Use '🧮 Vulnerability Triage' to further refine prioritization.\n")
        except Exception as e:
            print(f"[!] Error processing exploit prediction: {e}")

    else:
        run_plugin(plugin_key)
        print(f"\n[✔] Running plugin: {plugin_key}...\n")
        if plugin_key == "cve_lookup":
            run_cve_lookup()
        else:
            print(f"[✔] Plugin '{plugin_key}' executed successfully.\n")


# ******************************************************************************************
# Entry Point
# ******************************************************************************************

if __name__ == "__main__":
    main()

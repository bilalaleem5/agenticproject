"""
===============================================================
   RESEARCH EVALUATION BENCHMARK — LaunchMind MAS
===============================================================
This script runs the Multi-Agent System against multiple test cases
to generate research data for the IEEE paper.
Metrics: Execution Time, Success Rate, Ethics Score, Latency.
"""

import time
import json
import os
import sys
from datetime import datetime

# Add parent dir to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.ceo_agent import CEOAgent
from agents.message_bus import init_message_bus
from agents.ui_utils import console

TEST_IDEAS = [
    "ZetaMize AI Sales OS - Automated B2B lead generation",
    "EcoTrack - AI-powered carbon footprint tracker for SMEs",
    "EduPulse - Personalized AI tutoring for medical students",
    "SecureScan - Autonomous cybersecurity vulnerability scanner",
    "HealthSync - AI agent for automated clinic scheduling"
]

def run_benchmark():
    init_message_bus()
    results = []
    
    console.print("[bold magenta]STARTING RESEARCH BENCHMARK[/bold magenta]")
    console.print(f"Testing {len(TEST_IDEAS)} startup scenarios...\n")
    
    total_start = time.time()
    
    for i, idea in enumerate(TEST_IDEAS, 1):
        console.print(f"[bold yellow]TEST CASE {i}/{len(TEST_IDEAS)}: {idea}[/bold yellow]")
        
        case_start = time.time()
        ceo = CEOAgent()
        
        success = False
        metrics = {}
        
        try:
            output = ceo.run(idea)
            case_end = time.time()
            
            # Extract metrics from output
            qa_result = output.get("qa_result", {})
            metrics = {
                "idea": idea,
                "status": "success" if qa_result.get("verdict") == "pass" else "partial_fail",
                "latency_seconds": round(case_end - case_start, 2),
                "ethics_score": qa_result.get("ethics_score", 0),
                "pr_created": "pr_url" in output.get("engineer_result", {}),
                "timestamp": datetime.now().isoformat()
            }
            success = True
        except Exception as e:
            console.print(f"[bold red]Test Case Failed:[/bold red] {e}")
            metrics = {
                "idea": idea,
                "status": "fatal_error",
                "error": str(e),
                "latency_seconds": round(time.time() - case_start, 2)
            }
            
        results.append(metrics)
        console.print(f"Completed in {metrics['latency_seconds']}s | Ethics: {metrics.get('ethics_score')}/10\n")
        
        # Short sleep to avoid rate limits
        time.sleep(2)

    total_end = time.time()
    
    # Summary Statistics
    total_time = total_end - total_start
    avg_latency = sum(r['latency_seconds'] for r in results) / len(results)
    success_rate = len([r for r in results if r['status'] == 'success']) / len(results) * 100
    
    report = {
        "benchmark_summary": {
            "total_test_cases": len(TEST_IDEAS),
            "overall_success_rate": f"{success_rate}%",
            "average_latency": f"{round(avg_latency, 2)}s",
            "total_execution_time": f"{round(total_time, 2)}s",
        },
        "detailed_results": results
    }
    
    # Save to file
    with open("evaluation_results.json", "w") as f:
        json.dump(report, f, indent=4)
        
    console.print("\n[bold green]BENCHMARK COMPLETE![/bold green]")
    console.print(f"Results saved to [bold]evaluation_results.json[/bold]")
    
    # Generate a Markdown Summary for the user
    with open("research_data_summary.md", "w") as f:
        f.write("# Research Data Summary\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"**Total Cases:** {len(TEST_IDEAS)}\n")
        f.write(f"**Success Rate:** {success_rate}%\n")
        f.write(f"**Avg Latency:** {round(avg_latency, 2)}s\n\n")
        f.write("## Detailed Metrics\n\n")
        f.write("| Idea | Status | Latency | Ethics Score |\n")
        f.write("|------|--------|---------|--------------|\n")
        for r in results:
            f.write(f"| {r['idea']} | {r['status']} | {r['latency_seconds']}s | {r.get('ethics_score', 'N/A')} |\n")

if __name__ == "__main__":
    run_benchmark()

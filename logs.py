
import requests
from collections import Counter
import csv


# Variables

LOGS_ENDPOINT = "https://latest-960957615762.me-central1.run.app/getlogs"
LOG_FILE = "bank_service_logs.txt"


# Download Logs

def download_logs():
    print(f"Downloading logs from {LOGS_ENDPOINT}...")
    try:
        response = requests.get(LOGS_ENDPOINT, timeout=30)
        response.raise_for_status()
        log_content = response.text

        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            f.write(log_content)

        print(f"Logs saved to '{LOG_FILE}' ({len(log_content)} characters)")
        return log_content
    except requests.RequestException as e:
        print(f"Error downloading logs: {e}")
        return None

# ---------------------------
# Step 2: Parse Logs
# ---------------------------
def parse_logs(log_content):
    if not log_content.strip():
        print("Logs are empty!")
        return None, None


    # Splits the logs into individual lines.
    # Removes empty lines and spaces.
    # Creates a list -> list comprehension

    lines = [line.strip() for line in log_content.splitlines() if line.strip()]
    total_requests = 0
    success_count = 0
    error_count = 0
    warning_count = 0
    # track the detailed breakdown of all outcomes, including specific error types.
    outcome_distribution = Counter()  

    for i, line in enumerate(lines):
        if "Processing GET request" in line:
            total_requests += 1
            next_line = lines[i+1] if i+1 < len(lines) else ""
            if "ERROR" in next_line:
                error_count += 1
                error_type = next_line.split("ERROR")[-1].strip()
                outcome_distribution[f"ERROR: {error_type}"] += 1
            else:
                success_count += 1
                outcome_distribution["SUCCESS"] += 1
        elif "WARNING" in line:
            warning_count += 1

    if warning_count > 0:
        outcome_distribution["WARNING"] = warning_count

    reliability_rate = (success_count / total_requests * 100) if total_requests > 0 else 0

    analysis = {
        'total_requests': total_requests,
        'success_count': success_count,
        'error_count': error_count,
        'warning_count': warning_count,
        'reliability_rate': reliability_rate,
        'outcome_distribution': dict(outcome_distribution)
    }

    return analysis, outcome_distribution


#  Save CSVs

def save_to_csv(analysis, outcome_distribution):
    # Summary CSV
    with open('log_analysis_summary.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Metric', 'Value'])
        writer.writerow(['Total Requests', analysis['total_requests']])
        writer.writerow(['Success Count', analysis['success_count']])
        writer.writerow(['Error Count', analysis['error_count']])
        writer.writerow(['Warning Count', analysis['warning_count']])
        writer.writerow(['Reliability Rate (%)', f"{analysis['reliability_rate']:.2f}"])
    print("Summary saved to 'log_analysis_summary.csv'")

    # Detailed distribution CSV
    with open('outcome_distribution.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Outcome Type', 'Count', 'Percentage'])
        total = analysis['total_requests']
        for outcome, count in outcome_distribution.items():
            percentage = (count / total * 100) if total > 0 else 0
            writer.writerow([outcome, count, f"{percentage:.2f}"])
    print("Detailed distribution saved to 'outcome_distribution.csv'")

def print_analysis(analysis):
    print("\n" + "="*50)
    print("LOG ANALYSIS RESULTS")
    print("="*50)
    print(f"Total Requests: {analysis['total_requests']}")
    print(f"Success: {analysis['success_count']}")
    print(f"Error: {analysis['error_count']}")
    print(f"Warning: {analysis['warning_count']}")
    print(f"Reliability Rate: {analysis['reliability_rate']:.2f}%\n")
    print("Outcome Distribution:")
    for outcome, count in analysis['outcome_distribution'].items():
        total = analysis['total_requests']
        percentage = (count / total * 100) if total > 0 else 0
        print(f"  - {outcome}: {count} ({percentage:.1f}%)")
    print("="*50)


if __name__ == "__main__":
    logs = download_logs()
    if logs:
        analysis, distribution = parse_logs(logs)
        if analysis:
            print_analysis(analysis)
            save_to_csv(analysis, distribution)
        

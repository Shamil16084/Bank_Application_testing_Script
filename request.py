
import requests
import time
from datetime import datetime

# Variables
BALANCE_ENDPOINT = "https://latest-960957615762.me-central1.run.app/getbalance"
NUM_REQUESTS = 100

def response_type(response):
    """describe response based on HTTP status and content."""
    text = response.text.lower()
    # print(f"Response Text: {text}")  # Debug line
    
    if "error" in text:
        if "database connection pool empty" in text:
            return "ERROR Database Connection Pool Empty"
        elif "internal server error" in text:
            return "ERROR Internal Server Error [500]"
        else:
            return "ERROR Other"
    elif "warning" in text:
        return "WARNING Server Latency"
    elif response.status_code == 200:
        return "SUCCESS"
    else:
        return f"ERROR Status {response.status_code}"

def test_balance_service(num_requests):
    print(f"Testing {BALANCE_ENDPOINT} ({num_requests} requests)")
    print("-" * 60)
    
    results = []

    for i in range(num_requests):
        try:
            start_time = time.time()
            response = requests.get(BALANCE_ENDPOINT, timeout=10)
            end_time = time.time()

            description = response_type(response)

            results.append({
                'request_num': i+1,
                'status_code': response.status_code,
                'response_time': round(end_time - start_time, 3),
                'timestamp': datetime.now().isoformat(),
                'description': description
            })

            symbol = "✓" if "SUCCESS" in description else "✗"
            print(f"{symbol} Request {i+1}: {description} ({results[-1]['response_time']}s)")
            # print(f"    Response Content: {response.text}")  # Debug

        except requests.exceptions.Timeout:
            description = "TIMEOUT"
            results.append({
                'request_num': i+1,
                'status_code': 'TIMEOUT',
                'response_time': 10.0,
                'timestamp': datetime.now().isoformat(),
                'description': description
            })
            print(f"✗ Request {i+1}: {description}")

        except Exception as e:
            description = f"ERROR {str(e)}"
            results.append({
                'request_num': i+1,
                'status_code': 'ERROR',
                'response_time': 0,
                'timestamp': datetime.now().isoformat(),
                'description': description
            })
            print(f"✗ Request {i+1}: {description}")

        time.sleep(0.1)

    # Summary
    summary = {"SUCCESS":0, "ERROR Database Connection Pool Empty":0, "ERROR Internal Server Error [500]":0,
               "WARNING Server Latency":0, "ERROR Other":0, "TIMEOUT":0}
    for r in results:
        if r['description'] in summary:
            summary[r['description']] += 1
        else:
            summary["ERROR Other"] += 1

    print("-" * 60)
    print("Summary of outcomes:")
    for key, val in summary.items():
        print(f"  {key}: {val}")
    
    return results

if __name__ == "__main__":
    test_results = test_balance_service(NUM_REQUESTS)

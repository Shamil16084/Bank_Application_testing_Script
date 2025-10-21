
import csv
import matplotlib.pyplot as plt

# Load CSV

summary_file = "log_analysis_summary.csv"
distribution_file = "outcome_distribution.csv"

summary = {}
with open(summary_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        if len(row) == 2:
            key, value = row
            summary[key.strip()] = float(value.strip())


outcome_types = []
counts = []
percentages = []

with open(distribution_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        if len(row) == 3 and row[0].strip():
            outcome_types.append(row[0].strip())
            counts.append(int(row[1].strip()))
            percentages.append(float(row[2].strip()))


# Pie Chart:

labels = ["SUCCESS", "ERROR", "WARNING"]
# get the value or 0 if not found
sizes = [
    int(summary.get("Success Count", 0)),
    int(summary.get("Error Count", 0)),
    int(summary.get("Warning Count", 0))
]

plt.figure(figsize=(8,6))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140,
        colors=['#4CAF50','#F44336','#FFC107'])
plt.title("Banking Service Reliability")
plt.axis('equal')
plt.savefig("reliability_pie_chart.png")
plt.show()

# Bar Chart: Detailed Outcome Distribution

plt.figure(figsize=(12,6))
plt.bar(outcome_types, counts, color='skyblue')
plt.xticks(rotation=45, ha='right')
plt.ylabel("Count")
plt.title("Detailed Outcome Distribution")
plt.tight_layout()
plt.savefig("detailed_outcome_bar_chart.png")
plt.show()

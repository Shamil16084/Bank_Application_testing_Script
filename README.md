[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=21177331&assignment_repo_type=AssignmentRepo)

<br>
<br>

**Video Link**: [ADA SharePoint](https://adauniversity.sharepoint.com/:v:/s/assignment2/EZNweqeIUwxLuIY4V_hoOcABv5-M8ubrcaaCKX_uZWBwgQ?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJTdHJlYW1XZWJBcHAiLCJyZWZlcnJhbFZpZXciOiJTaGFyZURpYWxvZy1MaW5rIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXcifX0%3D&e=YcUq8Q)

<br>

Note: I create 3 different python files, for each step. To run them basically write python <filenam>
<br>


Service Testing and Log Analysis


The focus was to develop a performance as well as reliability analysis of a live banking service API with two methods: live traffic generation along with retrospective log analysis.

Organization

It uses three main segments of code in order to perform a thorough performance evaluation:

1. Verification of Live Services (Simulated Traffic)

**Code File: request.py (first block)**

Functionality: Makes 100 consecutive calls to the /getbalance service.

Key Output: Evaluates the duration of the response and categorizes the outcome of each request (Success, DB Pool Error, Internal Server Error, or Timeout) to the console in its entirety.

2. Log Analyses

**Code File: logs.py (second block)**

It downloads historical logs from /getlogs endpoint. It goes through these logs to determine total requests, individual Success/Error/Warning quantities, and compute total Reliability Rate.

Instrument: Uses the Counter object to create a detailed count of any unique error category that is identified within those logs.

Output: Produces log_analysis_summary.csv and outcome_distribution.

3. Visualization

**Code File: graph.py**

The algorithm includes using csv to read information from the created CSV files and then using matplotlib to build two charts.

Diagrams:

Reliability Pie Chart: Plots overall distribution of percentages of Success, Error, and Warning categories.

Comprehensive Outcome Bar Chart: Uses the detailed output to display the occurrence rate of each unique error type, thus aiding in finding the root causes of bottleneck situations.

Shamil Abbasov, ID:16084

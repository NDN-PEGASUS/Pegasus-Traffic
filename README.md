<!-- # Pegasus-Traffic

This is the code repository for Pegasus's preprocessing of real traffic and the computation of the optimal parsable name format.

Steps:

- First, download the traffic data from `2023-04-19` to `2023-05-26` from [https://github.com/tntech-ngin/ndn-traffic-traces](https://github.com/tntech-ngin/ndn-traffic-traces) and place them in the `ndn-traffic-traces` directory.

- Enter the `ndn-traffic-traces` directory and run the `readZst.py` script (with `scapy` version == 2.5.0) to extract NDN names and write them into text files in the `ndn_names` directory. 

- Enter the `ndn_names` directory and run the `cntNdn.py` script to count the occurrences of all names and write the results to the `name_counts.txt` file in the `statistics` directory.

- Enter the `statistics` directory and run the `statistics_xxx.py` scripts as needed to observe the parsable name ratio under different name parsing schemes.

- In the `statistics` directory, run the `format_counts.py` script to generate the `format_counts.txt` file, which counts the occurrences of different name formats.

- In the `statistics` directory, run the `optimal_format.py` script to obtain the optimal parsable name format under Tofino2 programmable switch hardware constraints. -->

# Pegasus-Traffic

> Preprocessing and analysis pipeline for real-world NDN traffic traces to determine the **optimal parsable name format** for Tofino2 programmable switches.

---

## 📌 Overview

This repository is part of the **Pegasus** project, a cross-plane forwarding acceleration architecture for Named Data Networking (NDN). It provides a workflow to:

- Extract NDN names from real traffic traces.
- Count name occurrences.
- Analyze name format parsability under different schemes.
- Compute the optimal name format for Tofino2 switch parsing.

---

## 📁 Directory Structure
```
Pegasus-Traffic/
├── ndn-traffic-traces/       # Directory for raw traffic data
│   └── readZst.py            # Extracts NDN names from traces
├── ndn_names/                # Stores extracted name lists
│   └── cntNdn.py             # Counts name occurrences
├── statistics/               # Scripts for analyzing formats
│   ├── statistics_*.py       # Format parsing evaluation scripts
│   ├── format_counts.py      # Counts format pattern frequencies
│   └── optimal_format.py     # Computes the optimal parsable format
└── README.md
```

## 🚀 Quick Start

### Step 1: Download Traffic Traces

Download traces from:

📥 https://github.com/tntech-ngin/ndn-traffic-traces

Focus on the date range: `2023-04-19` to `2023-05-26`.

Place all files in the `ndn-traffic-traces/` directory.

### Step 2: Extract NDN Names

```shell
cd ndn-traffic-traces
python3 readZst.py
```
Output will be saved in `../ndn_names/`. 

Note that this script has been tested and verified only on `scapy==2.5.0`. Use of other versions may lead to unexpected behavior.

### Step 3: Count Name Frequencies

```shell
cd ../ndn_names
python3 cntNdn.py
```
Generates `name_counts.txt` in `../statistics/`.

### Step 4: Analyze Name Format Parsability

```shell
cd ../statistics
python3 statistics_xxx.py   # analyze for xxx scheme
```
Use different scripts to evaluate parsability statistics of different schemes.

### Step 5: Count Format Occurrences

```shell
python3 format_counts.py
```
Generates `format_counts.txt`, summarizing the frequency of each name format.

### Step 6: Determine Optimal Format

```shell
python3 optimal_format.py
```
Outputs the optimal name format under hardware constraints of Tofino2.
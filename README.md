# ArduPilot GSoC 2026: AI-Assisted Log Diagnosis (PoC)

This repository contains a Python-based data extraction and visualization pipeline using `pymavlink` and `matplotlib`. It parses ArduPilot `.bin` telemetry logs generated via SITL and automatically detects hardware/flight failures based on Z-axis acceleration thresholds. 

This serves as the foundational data-engineering phase for my GSoC 2026 proposal to build an Unsupervised Machine Learning anomaly detection model.

## Visual Proof of Concept

### 1. Baseline: Normal Flight
During a standard guided takeoff and RTL sequence, Z-axis acceleration remains within nominal gravity limits. The script correctly parses the telemetry with zero false positives.

![Normal Flight](flight_log.jpg) 

### 2. Anomaly: Catastrophic Motor Failure (Crash)
Upon intentionally cutting the motors at 30 meters (switching to Stabilize and dropping RC 3 to 1000), the SITL drone experiences a freefall. The script successfully catches the 15.9 m/s impact, automatically isolating and flagging the multi-frame failure window in red.

![Crash Analysis](crash-log.jpg)

## How to Run
```bash
pip install matplotlib
python3 visualize_anomalies.py <path_to_bin_log>

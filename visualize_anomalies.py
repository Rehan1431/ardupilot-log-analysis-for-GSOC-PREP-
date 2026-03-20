import sys
from pymavlink import mavutil
import matplotlib.pyplot as plt

def analyze_and_plot(log_path, anomaly_threshold=25.0):
    print(f"Analyzing SITL log: {log_path}...")
    
    # Open the .bin log file
    mlog = mavutil.mavlink_connection(log_path)
    
    timestamps = []
    acc_z_data = []
    anomaly_times = []
    anomaly_values = []
    
    # Extract IMU data
    while True:
        msg = mlog.recv_match(type='IMU', blocking=False)
        if not msg:
            break
            
        # Convert microseconds to seconds for readability
        time_s = msg.TimeUS / 1e6  
        acc_z = msg.AccZ
        
        timestamps.append(time_s)
        acc_z_data.append(acc_z)
        
        # Flag anomaly if the Z-axis acceleration exceeds our threshold (e.g., a crash)
        if abs(acc_z) > anomaly_threshold:
            anomaly_times.append(time_s)
            anomaly_values.append(acc_z)

    if not timestamps:
        print("No IMU data found in this log.")
        return

    print(f"Extraction complete. Found {len(anomaly_times)} anomaly points.")

    # Generate the Professional Graph
    plt.figure(figsize=(12, 6))
    
    # Plot normal flight data in clean blue
    plt.plot(timestamps, acc_z_data, label='IMU Z-Axis (Normal Flight)', color='#1f77b4', alpha=0.8)
    
    # Plot anomalies in bright red
    if anomaly_times:
        plt.scatter(anomaly_times, anomaly_values, color='red', s=50, label='Detected Anomaly (Crash)', zorder=5)
        # Highlight the exact time window of the failure
        plt.axvspan(min(anomaly_times) - 2, max(anomaly_times) + 2, color='red', alpha=0.15, label='Failure Window')

    # Format the graph to look like a professional engineering spec
    plt.title('ArduPilot SITL Telemetry: Automated AI Anomaly Detection (PoC)', fontsize=14, fontweight='bold')
    plt.xlabel('Flight Time (seconds)', fontsize=12)
    plt.ylabel('Z-Axis Acceleration (m/s²)', fontsize=12)
    plt.legend(loc='upper right')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    
    # Display the graph
    plt.show()

if __name__ == "__main__":
    # To run this, replace '00000001.bin' with your actual log file name
    # Example: python visualize_anomalies.py normal_flight.bin
    
    if len(sys.argv) < 2:
        print("Usage: python log_inspector.py <path_to_bin_file>")
    else:
        log_file = sys.argv[1]
        analyze_and_plot(log_file)

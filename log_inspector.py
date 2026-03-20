import sys
from pymavlink import mavutil

def inspect_bin_log(filepath):
    print("\n[+] Starting ArduPilot Log Inspector...")
    print(f"[+] Target File: {filepath}")

    try:
        # Open the high-resolution Dataflash .bin file
        mlog = mavutil.mavlink_connection(filepath)
    except Exception as e:
        print(f"[-] Error opening file: {e}")
        return

    imu_count = 0
    high_vibration_count = 0
    # 30.0 m/s/s is a standard warning threshold for high vibrations
    vibration_threshold = 30.0 

    print("[+] Scanning IMU (Inertial Measurement Unit) messages for anomalies...")

    while True:
        try:
            m = mlog.recv_match(type=['IMU'], blocking=False)
            if m is None:
                break # Reached the end of the log
            
            imu_count += 1
            
            # Check the Z-axis accelerometer for severe spikes
            accel_z = abs(m.AccZ)
            if accel_z > vibration_threshold:
                high_vibration_count += 1
        except Exception as e:
            # Sometimes corrupted log chunks throw errors, we skip them
            pass

    print("\n=== Log Diagnostics Report ===")
    print(f"Total IMU data points analyzed: {imu_count}")
    
    if imu_count == 0:
        print("[-] Error: No IMU data found. Is this a valid SITL .bin file?")
    elif high_vibration_count > 0:
        print(f"[!] WARNING: {high_vibration_count} instances of extreme Z-axis vibration (>{vibration_threshold} m/s/s) detected.")
        print("[!] Recommendation: Review physical dampening or SITL physics parameters.")
    else:
        print("[+] SUCCESS: Vibration levels are within acceptable flight parameters.")
    print("==============================\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 log_inspector.py <path_to_your_log.bin>")
    else:
        log_file_path = sys.argv[1]
        inspect_bin_log(log_file_path)
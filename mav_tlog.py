from pymavlink import mavutil

# Point to the log you just generated
log_file = "mav.tlog"

print(f"Loading {log_file}...")
mlog = mavutil.mavlink_connection(log_file)

print("Searching for Takeoff Data...\n")
max_alt = 0.0

while True:
    # Grab the next message
    msg = mlog.recv_match(blocking=False)
    if msg is None:
        break # End of log

    # VFR_HUD contains the easy-to-read altitude and speed data
    if msg.get_type() == 'VFR_HUD':
        current_alt = msg.alt
        
        # Keep track of the highest altitude
        if current_alt > max_alt:
            max_alt = current_alt
            
        # Print when it crosses specific thresholds
        if 14.8 < current_alt < 15.2:
            print(f"[{msg._timestamp}] Drone passed 15m altitude! Speed: {msg.groundspeed} m/s")

print(f"\nLog Analysis Complete. Maximum Altitude Reached: {max_alt} meters.")
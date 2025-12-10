import time
import starlink_grpc
from grpc import RpcError
from datetime import datetime

def print_stats():
    try: 
        status_data = starlink_grpc.status_data('192.168.100.1')
        state = status_data.get('state', {})
        info = status_data.get('device_info', {})
        
        print("Test Results:")
        print(f"TIME:                  {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}")
        print(f"DEVICE ID:             {info.get('id', 'N/A')}")
        print(f"HARDWARE:              {info.get('hardware_version', 'N/A')}")
        print(f"SOFTWARE:              {info.get('software_version', 'N/A')}")
        print(f"DROP RATE:             {state.get('pop_ping_drop_rate', 0.0) * 100:.2f} %")
        print(f"DOWNLINK THROUGHPUT:   {state.get('downlink_throughput_bps', 0.0) / 1e6:.2f} Mbps")
        print(f"UPLINK THROUGHPUT:     {state.get('uplink_throughput_bps', 0.0) / 1e6:.2f} Mbps\n------------------------------")
        print(f"LATENCY:               {state.get('pop_ping_latency_ms', 0.0):.2f} ms")
        print(f"USER DIRECTION:        {state.get('direction_azimuth', 0.0):.2f}")   #NEEDS GPS TO BE ENABLED TO RUN WITHOUT ERRORS
        print(f"USER ANGLE:            {state.get('direction_elevation', 0.0):.2f}") #NEEDS GPS TO BE ENABLED TO RUN WITHOUT ERRORS
        print(f"NUMBER OF SATELLITES:  {state.get('gps_sats', 0.0):.2f}\n------------------------------")
    except RpcError as e:
        print(f"COMMUNICATION ERROR: {e}")
    except Exception as e:
        print(f"UNEXPECTED ERROR: {e}")

if __name__ == '__main__':
    while True:
        try:
            sec_update = int(input("Update experiment every __ second(s): "))
            if sec_update <= 0:
                raise ValueError("The number of seconds must be greater than zero.")
            break
        except ValueError as e:
            print(f"Invalid input! {e}")
    
    try: 
        while True:
            print_stats()
            time.sleep(sec_update)
    except KeyboardInterrupt:
        print("-------------------\nExperiment ended\n-------------------")

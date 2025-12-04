import importlib.util
import sys
import os
import socket
import time
from datetime import datetime
import starlink_grpc
from grpc import RpcError

def run():
    def get_stats(): 
        status_data = starlink_grpc.status_data('192.168.100.1')
        state = status_data.get('state', {})
        return {
            'id': state.get('id', 'N/A'),
            'hardware': state.get('hardware_version', 'N/A'),
            'software': state.get('software_version', 'N/A'),
            'latency': state.get('pop_ping_latency_ms', 0.0),
            'droprate': state.get('pop_ping_drop_rate', 0.0),
            'downlink_throughput': state.get('downlink_throughput_bps', 0.0),
            'uplink_throughput': state.get('uplink_throughput_bps', 0.0)
        }
        
    def return_stats(tester):
        print("Test Results:")
        print(f"DEVICE ID:             {tester['id']}")
        print(f"HARDWARE:              {tester['hardware']}")
        print(f"SOFTWARE:              {tester['software']}")
        print(f"LATENCY:               {tester['latency']:.2f} ms")
        print(f"DROP RATE:             {tester['droprate'] * 100:.2f} %")
        print(f"DOWNLINK THROUGHPUT:   {tester['downlink_throughput'] / 1e6:.2f} Mbps")
        print(f"UPLINK THROUGHPUT:     {tester['uplink_throughput'] / 1e6:.2f} Mbps")
        print("---------------------")

    try: 
    while True:
        tester = get_stats()
        return_stats(tester)
        time.sleep(1)
    except KeyboardInterrupt:
        print("-------------------\nExperiment ended")

if __name__ == '__main__':
    run()

import platform
import socket
import os
import psutil
import time
import argparse

"""
The script collects system information. including the following:
- Operating system Version, hostname and user
- CPU usage
- Memory usage
- Runing process
"""

#argpar for user confort, option to choose the argument. the argument is false until the user add him 
parser = argparse.ArgumentParser(description="Get the weather for a city")
parser.add_argument("-os", "--os-info", action='store_true', required=False, help="Display operating system info")
parser.add_argument("-c", "--cpu", action='store_true', required=False, help="Display CPU info")
parser.add_argument("-m", "--mem", action='store_true', required=False, help="Display memory info")
parser.add_argument("-p", "--proc", action='store_true', required=False, help="Display process info")
parser.add_argument("-a", "--all", action='store_true', required=False, help="Display all info")
args = parser.parse_args()
    
#collect the information from the function
class SystemInfo:
    def __init__(self):
        self.result = {}
        self.result['OS'] = {}
        self.result['CPU'] = {}
        self.result['MEM'] = {}
        self.result['Processes'] = {}
        self.get_os_info()
        self.get_cpu_info()
        self.get_memory_info()
        self.get_process_info()

    # Determine the operating system, hostname, and user
    def get_os_info(self):
        os_info = platform.system()
        hostname = socket.gethostname()
        user = os.getlogin()
        self.result['OS']['Hostname'] = hostname
        self.result['OS']['User'] = user
        self.result['OS']['Operating System'] = os_info

    # Get CPU usage info
    def get_cpu_info(self):
        cpu_count = psutil.cpu_count(logical=True)
        cpu_percent = psutil.cpu_percent(interval=1)
        self.result['CPU']['Count'] = cpu_count
        self.result['CPU']['Usage'] = f"{cpu_percent}%"

    # Get memory usage info
    def get_memory_info(self):
        mem = psutil.virtual_memory()
        total_memory = mem.total / (1024 ** 3)  # Convert from bytes to GB
        used_memory = mem.used / (1024 ** 3)    
        free_memory = mem.free / (1024 ** 3)    
        self.result['MEM']['Total Memory'] = total_memory
        self.result['MEM']['Used Memory'] = used_memory
        self.result['MEM']['Free Memory'] = free_memory

    # Get running/idle processes
    def get_process_info(self):
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'status', 'cpu_percent', 'memory_percent']):
            processes.append(proc.info)
        self.result['Processes'] = processes
    
    def get_info(self, kind):
        print(f'all is {kind}')
        if kind.upper() == 'ALL':
            print(self.result)
        else:
            print(self.result[kind.upper()])
    
system_info = SystemInfo() 
arguments = {"os": args.os_info, "cpu": args.cpu, "mem": args.mem, "proc": args.proc, "all": args.all}

if arguments['all']:
    system_info.get_info('all')
else:
    for arg in arguments:
        if arguments[arg]:
            system_info.get_info(arg)
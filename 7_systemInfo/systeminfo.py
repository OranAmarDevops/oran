import platform
import socket
import os
import psutil
import time

"""
This script collects and displays system information, including:
OS info
User info
CPU info
Memory info
Process info
idle info
HD info
Time info
"""


# Determine the operating system
def get_os_info():
    os_info = platform.system()
    hostname = socket.gethostname()
    user = os.getlogin()
    return os_info, hostname, user

# Get memory usage info
def get_memory_info():
    mem = psutil.virtual_memory()
    total_memory = mem.total / (1024 ** 3)  # Convert from bytes to GB
    used_memory = mem.used / (1024 ** 3)    
    free_memory = mem.free / (1024 ** 3)    
    return total_memory, used_memory, free_memory

# Get running/idle processes
def get_process_info():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'status', 'cpu_percent', 'memory_percent']):
        processes.append(proc.info)
    return processes

# Get hard drive info
def get_hd_info():
    partitions = psutil.disk_partitions()
    hd_info = []
    for part in partitions:
        usage = psutil.disk_usage(part.mountpoint)
        hd_info.append({
            'device': part.device,
            'mountpoint': part.mountpoint,
            'fstype': part.fstype,
            'total': usage.total / (1024 ** 3),  # Convert from bytes to GB
            'used': usage.used / (1024 ** 3),
            'free': usage.free / (1024 ** 3),
            'percent': usage.percent
        })
    return hd_info


# Main function to display all information
def display_system_info():
    os_info, hostname, user = get_os_info()
    print(f"Operating System: {os_info}")
    print(f"Hostname: {hostname}")
    print(f"User: {user}")
    
    cpu_count = psutil.cpu_count(logical=True)
    cpu_percent = psutil.cpu_percent(interval=1)
    print(f"CPU Count: {cpu_count}")
    print(f"CPU Usage: {cpu_percent}%")
    
    total_mem, used_mem, free_mem = get_memory_info()
    print(f"Total Memory: {total_mem:.2f} GB")
    print(f"Used Memory: {used_mem:.2f} GB")
    print(f"Free Memory: {free_mem:.2f} GB")
    
    processes = get_process_info()
    print(f"Number of processes running: {len(processes)}")
    
    hd_info = get_hd_info()
    for hd in hd_info:
        print(f"Disk: {hd['device']}, Total: {hd['total']:.2f} GB, Used: {hd['used']:.2f} GB, Free: {hd['free']:.2f} GB, Usage: {hd['percent']}%")
    
    local_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    boot_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(psutil.boot_time()))
    print(f"Local Time: {local_time}")
    print(f"Boot Time: {boot_time}")


if __name__ == "__main__":
    display_system_info()
import platform
import socket
import os
import psutil
import time
import argparse
import logging
from flask import Flask , render_template, request, jsonify

"""
System Information Monitoring App – Flask-based

This application provides:
1. `/systeminfo` route – returns plain text based on the 'metric' query parameter:
   - 'cpu': CPU information
   - 'memory': Memory usage details
   - 'os_info': Operating system info
   - 'all' (or no parameter): Returns all system data
2. `/systeminfo/json` route – returns all system data in JSON format.
3. Error handling:
   - Custom error pages (404, 500)
   - General exception handling
4. Logging:
   - Logs all requests and errors to the file `flask.systeminfo.log`
Purpose: Allow readable and programmatic access to local system resource information.
"""

app = Flask(__name__)  
@app.route('/')
def home():
    return render_template('base.html')

@app.route('/systeminfo', methods=['GET'])
def system_info():
    os_info = platform.system()
    hostname = socket.gethostname()
    try:
        user = os.getlogin()
    except OSError:
        user = "Unknown"
    cpu_count = psutil.cpu_count(logical=True)
    cpu_percent = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    total_memory = mem.total / (1024 ** 3)  # Convert from bytes to GB
    used_memory = mem.used / (1024 ** 3)    
    free_memory = mem.free / (1024 ** 3)   
    
    metric = request.args.get("metric")
    print(f"Received metric: {metric}")  
    logging.info(f"Received metric: {metric}") 
    
    if metric == "cpu":
        result = f"CPU Cores: {cpu_count}\nCPU Usage (%): {cpu_percent}%"
    elif metric == "memory":
        result = f"Total Memory (GB): {round(total_memory,2)}\nUsed Memory (GB): {round(used_memory,2)}\nFree Memory (GB): {round(free_memory,2)}"
    elif metric == "os":
        result = f"Operating System: {os_info}\nHostname: {hostname}\nUser: {user}"
    elif metric == "all" or metric is None:
        result = f"""Operating System: {os_info}
Hostname: {hostname}
User: {user}
CPU Cores: {cpu_count}
CPU Usage (%): {cpu_percent}%
Total Memory (GB): {round(total_memory,2)}
Used Memory (GB): {round(used_memory,2)}
Free Memory (GB): {round(free_memory,2)}"""
    else:
        result = "Invalid metric. Please use one of: cpu, mem, os_info, all."  
    return result, 200, {'Content-Type': 'text/plain'}
@app.route('/systeminfo/json', methods=['GET'])
def system_json():
    os_info = platform.system()
    hostname = socket.gethostname()
    user = os.getlogin()
    cpu_count = psutil.cpu_count(logical=True)
    cpu_percent = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    total_memory = mem.total / (1024 ** 3)  
    used_memory = mem.used / (1024 ** 3)    
    free_memory = mem.free / (1024 ** 3)   
    return jsonify({"CPU Cores": cpu_count, "CPU Usage (%)": f"{cpu_percent}%", "Total Memory (GB)": round(total_memory, 2), "Used Memory (GB)": round(used_memory, 2), "Free Memory (GB)": round(free_memory, 2), "Operating System": os_info, "Hostname": hostname, "User": user})


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500

# הגדרת הקובץ שאליו ייכתבו הלוגים
logging.basicConfig(
    filename='flask.systeminfo.log',          # שם הקובץ
    filemode='a',                # 'a' = append, 'w' = overwrite
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO           # רמת הלוגים: DEBUG / INFO / WARNING / ERROR / CRITICAL
)
            
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
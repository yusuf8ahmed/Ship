import re
import os
import sys
import time
import subprocess
import time

# GitHub@jmingtan: https://gist.github.com/jmingtan/1171288/8286cd988b90f0df41b5ed8d8cfc4a185ce95504

# blacklist = ["^\.", "\.swp$"]
# whitelist = []

# def file_filter(name):
#     def run_filters(name, filters):
#         for regex in filters:
#             if re.search(regex, name):
#                 return True
#         return False
#     if len(whitelist) > 0:
#         return run_filters(name, whitelist)
#     else:
#         return not run_filters(name, blacklist)  
        
# def yusuf(path):
#     for top_level in [x for x in os.listdir(path) if not x.startswith(".")]:
#         for file_name in filter(file_filter, top_level):
#             yield os.stat(os.path.join(path, top_level)).st_mtime

# path = '/Users/abdulwahid/Desktop' 
# last_mtime = max(yusuf(path))
# WAIT = 2
# command = "ls"

# while True:
#     max_mtime = max(yusuf(path))
#     if max_mtime > last_mtime:
#         last_mtime = max_mtime
#         print("watchdog directory alert")   
#         process = subprocess.Popen(
#                     ['python3.6', 'ship', 'test_files/test.pdf'],
#                      stdout=subprocess.PIPE, 
#                      stderr=subprocess.PIPE)
#     print("FILE, {}".format(max_mtime))
#     time.sleep(WAIT)

# p = lambda x : print(x)

# from ship import shipapp

# path = 'files/test.txt' 
# t = shipapp.ShipIt(path, qr_option=True, auto_open=True)
# p(t)
# print("hellot")

# def file_stats(path_to_file):
#     full_path_to_file = os.path.join(os.path.dirname(__file__), path)
#     stats_of_file = os.stat(full_path_to_file).st_mtime
#     return stats_of_file

# path = 'files/test.txt' 
# last_mtime = file_stats(path)
# WAIT = 3
# t = shipapp.ShipIt(path, qr_option=True)
# print(t)

# while True:
#     try:
#         max_mtime = file_stats(path)
#         if max_mtime > last_mtime:
#             last_mtime = max_mtime
#             print("Ship: File watch alert: reload webpage") 
#             t = shipapp.ShipIt(path, qr_option=True) 
#             print(t)
#         time.sleep(WAIT)
#     except KeyboardInterrupt as e:
#         break

# from http.server import HTTPServer, BaseHTTPRequestHandler
# import threading

# server = HTTPServer(('', 8080), BaseHTTPRequestHandler)
# thread = threading.Thread(target = server.serve_forever)
# thread.setDaemon = True
# try:
#     thread.start()
#     print("h")
# except KeyboardInterrupt:
#     server.shutdown()
#     sys.exit(0)
    
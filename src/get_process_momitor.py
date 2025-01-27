#!/usr/bin/env python

"""
MIT License
Copyright (c) 2025 Vlad.M
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy,
modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Program Name: OS Process Monitor
Description : A script to monitor OS processes, measure CPU, memory, and disk usage, and provide detailed output.
Author      : Vlad.M
Created On  : 2025-01-20
Version     : 1.0.0
Contact     : vmxsqa@gmail.com

Usage       : python3 src/get_process_monitor.py <process_name> [options]
Example     : 
    1. Terminal output with default settings:
        python3 src/get_process_monitor.py chrome
    
    2. File output with a line limit:
        python3 src/get_process_monitor.py nginx -o file -l 100
    
    3. Colored terminal output:
        python3 src/get_process_monitor.py apache2 -c
    
Options:
    -o, --output         Specify the output type: "file" or "terminal" (default: terminal)
    -l, --line-limit     Limit the number of lines written to the output file (default: unlimited)
    -c, --colored_output Enable colored output for terminal display (default: False)
"""

import time
import psutil
import datetime
import argparse
from colorama import Fore, Style
class ProcessNotFoundError(Exception):
    def __init__(self, name, pid):
        self.name = name
        self.pid = pid
        super().__init__(f"\nProcess Name {Fore.RED + Style.BRIGHT}Match Error:\n{Style.RESET_ALL}"
                         f"Integer Process Id value is Expected:\t{Style.RESET_ALL}"
                         f"{Fore.RED + Style.BRIGHT}{pid}{Style.RESET_ALL} is returned instead:"
                         f"\nThe Process Name: ( {Fore.RED + Style.BRIGHT}{name} {Style.RESET_ALL}) "
                         f"Does not match with any current process names on this system:")


def get_running_processes_by_name(name):
    try:
        matching_processes = psutil.process_iter(attrs=['name', 'create_time', 'pid'])
    except (psutil.AccessDenied, psutil.NoSuchProcess) as process_match_error:
        print(f'\nProcess Matching Error detected:\t--> {process_match_error}')
        raise ProcessNotFoundError(name, None) from process_match_error

    processes_by_name = {}

    for process in matching_processes:
        if name.lower() in process.info['name'].lower():
            pid = process.info['pid']
            ps_name = process.info['name']
            ps_runtime = process.info['create_time']
            if ps_name not in processes_by_name:
                processes_by_name[ps_name] = set()
            processes_by_name[ps_name].add((pid, ps_runtime))

    result = []
    for ps_name, process_set in processes_by_name.items():
        for pid, runtime in process_set:
            runtime_str = datetime.datetime.fromtimestamp(runtime).strftime('%Y-%m-%d %H:%M:%S')
            result.append((ps_name, pid, runtime_str))

    if not result:
        raise ProcessNotFoundError(name, None)
    else:
        return result

def measure_cpu_usage(name):
    try:
        processes = get_running_processes_by_name(name)
        if not processes:
            raise ProcessNotFoundError(name, 'unknown')
        pid = processes[0][1]
        process = psutil.Process(pid)
        cpu_percent = process.cpu_percent(interval=1)
        return cpu_percent
    except ProcessNotFoundError as e:
        print(f'Process ID:{Fore.YELLOW}{e.pid} {Fore.RESET}Does not match given Process Name: {Fore.RED + Style.BRIGHT}{e.name} ')
        return None


def measure_memory_usage(name):
    try: 
        processes = get_running_processes_by_name(name)
        if not processes:
            raise ProcessNotFoundError(name, 'unknown')
        pid = processes[0][1]
        process = psutil.Process(pid)
        memory_info = process.memory_info()
        return memory_info.rss
    except ProcessNotFoundError as e:
        print(f'\n{Fore.RED}Process not found: {e.name} with PID {e.pid}{Fore.RESET}')
        return None


def measure_disk_usage():
    try:
        disk_usage = psutil.disk_usage("/")
        return disk_usage.percent
    except psutil.AccessDenied as e:
        print(f'\n{Fore.RED}Access denied to disk usage: {e}{Fore.RESET}')
        return None


def output_to_file(name, cpu_usage, memory_usage, disk_usage, file, count):
    processes = get_running_processes_by_name(name)
    if not processes:
        return
    
    ram_usage_mb = round(memory_usage / (1024 ** 2), 2)
    ram_usage_gb = round(memory_usage / (1024 ** 3), 3)
    formatted_mb_length = "{:.3f}".format(ram_usage_mb)
    formatted_gb_length = "{:.3f}".format(ram_usage_gb)

    output = f'Date & Time:\t{time.ctime()}\tProcess Name: {processes[0][0]}\tProcess ID:{processes[0][1]}' \
             f'\t\tOS Memory Usage:  in MB {formatted_mb_length}\t in GB {formatted_gb_length}' \
             f'\t\tOS Disk Usage: {disk_usage} %\tOS CPU Usage: {cpu_usage} %\t\tMonitor Count: {count}\n'

    file.write(output)


def output_to_terminal(name, cpu_usage, memory_usage, disk_usage, count, colored_output=False):
    processes = get_running_processes_by_name(name)
    if not processes:
        return

    ram_usage_mb = round(memory_usage / (1024 ** 2), 2)
    ram_usage_gb = round(memory_usage / (1024 ** 3), 3)
    formatted_mb_length = "{:.3f}".format(ram_usage_mb)
    formatted_gb_length = "{:.3f}".format(ram_usage_gb)

    if colored_output:
        output = f'{Fore.RESET} Date & Time: {Fore.YELLOW + Style.BRIGHT}{time.ctime():<25}'\
                 f'{Fore.RESET} PS Name: {Fore.GREEN}{processes[0][0]:<15}'\
                 f'{Fore.RESET} PS ID:  {Fore.GREEN}{processes[0][1]:<6}'\
                 f'{Fore.RESET} OS {Fore.LIGHTCYAN_EX}Memory Usage:'\
                 f'{Fore.MAGENTA}  in MB {Fore.YELLOW}{formatted_mb_length:>3} '\
                 f'{Fore.MAGENTA} in GB {Fore.YELLOW}{formatted_gb_length:>3}'\
                 f'{Fore.RESET}  OS {Fore.LIGHTCYAN_EX}Disk Usage: {Fore.YELLOW}{disk_usage:>6} {Fore.MAGENTA}%'\
                 f'{Fore.RESET}  OS {Fore.LIGHTCYAN_EX}CPU Usage: {Fore.YELLOW}{cpu_usage:>6} {Fore.MAGENTA}%'\
                 f'{Fore.RESET} Monitor Count:{Fore.LIGHTRED_EX} {count:>3}'
    else:
        output = f'Date & Time: {time.ctime():<25}| PS Name: {processes[0][0]:>3} -> PS ID:{processes[0][1]:>5}'\
                 f'RAM Usage: in MB {formatted_mb_length:<6} in GB {formatted_gb_length:>6}'\
                 f'| Disk Usage: {disk_usage:<3}% | OS CPU Usage: {cpu_usage:>4}% Monitor Count: {count:>4}'

    print(output)
    

def convert_to_gb(memory_size):
    if memory_size < 0:
        raise ValueError("Memory size must be a positive number.")
    divisor = pow(1024, 2) if memory_size < pow(1024, 2) else pow(1024, 3)
    return round(memory_size / divisor, 2)


def main(ps_name, line_limit):
    try:
        loop_count = 0
        while True: 
            loop_count += 1
            try:
                ps_init = get_running_processes_by_name(name=ps_name)
                cpu_usage = measure_cpu_usage(name=ps_name)
                memory_usage = measure_memory_usage(name=ps_name)
            except ProcessNotFoundError as e:
                print(e)
                break
            disk_usage = measure_disk_usage()
            if output_type == "file":
                with open(f"monitor_process_{args.process_name}.txt", "a") as file:
                    output_to_file(ps_name, cpu_usage, memory_usage, disk_usage, file, count=loop_count)
                    if 0 < line_limit <= loop_count:
                        print(f'\n{Fore.YELLOW}{Style.BRIGHT}The file write has reached its limit of '
                              f'{Fore.RED}{loop_count} {Fore.YELLOW}lines:\n{Fore.GREEN}Reading file now ...')
                        print(f'{Fore.MAGENTA}-{Fore.RESET}'*167)
                        time.sleep(0.08)
                        with open(f"monitor_process_{args.process_name}.txt", "r") as file:
                            for read_from in file.readlines():
                                time.sleep(0.3)
                                print(read_from.replace('\t', '').splitlines()[0], flush=True)
                            break
            else:
                output_to_terminal(ps_name, cpu_usage, memory_usage, disk_usage,
                                   count=loop_count, colored_output=args.colored_output)
            time.sleep(0.004)
    except KeyboardInterrupt:
        print(f'\n\n[ Ctr + c ] Keyboard Interruption Detected:\n{Style.RESET_ALL}'
              f'Process Monitoring Id: [{Fore.GREEN} {ps_init[0][1]} {Style.RESET_ALL}]'
              f' for [{Fore.GREEN} {ps_name} {Style.RESET_ALL}] Stopped by User:'
              f'\tTotal Monitored Count: {Fore.YELLOW + Style.BRIGHT}{loop_count}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Measure CPU, memory, and disk usage of a process')
    parser.add_argument('process_name', type=str, help='Name of the process to monitor')
    parser.add_argument("-o", "--output", choices=["file", "terminal"],
                        default="terminal", help="The output type (file or terminal). Default is terminal.")
    parser.add_argument("-l", "--line-limit", type=int,
                        default=0, help="The maximum number of lines to write to the file. Default is 0 (unlimited).")
    parser.add_argument("-c", "--colored_output", action="store_true",
                        default=False, help="Colored Output to Terminal: Prints ps_name, ps_id, cpu, ram and count in colores. Default output is set to (no colors).")

    args = parser.parse_args()
    output_type = args.output
    line_limit = args.line_limit
    colored_output = args.colored_output
    main(args.process_name, line_limit)
    
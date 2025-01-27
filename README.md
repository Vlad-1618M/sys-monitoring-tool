# **Process Monitoring Tool**

This Python script is designed to measure the **CPU usage**, **memory usage**, and **disk usage** of a running process on your system. It outputs the results either to the terminal or a file, providing flexible and clear monitoring for system processes.

---

## **Features**
- Monitor **CPU**, **Memory**, and **Disk** usage of any running process.
- Output results to:
  - **Terminal** (with optional colored output).
  - **File** (with an option to limit the number of lines written).
- User-friendly CLI with flexible options.

---

## **Dependencies**
The script requires the following Python libraries:
- `psutil`
- `datetime` (standard library)
- `argparse` (standard library)
- `colorama`

### Install Dependencies
You can install the required libraries using `pip`:

```bash
pip install -r requirements.txt
```
>- usage: get_monitor_process.py [-h] process_name [-o {terminal,file}] [-l LINE_LIMIT] [-c]<br>
>- Measure CPU, Memory, and Disk usage for a given process.<br>
>- positional arguments:
>- process_name          Name of the process to monitor.
>- optional arguments:
>-  -h, --help            Show this help message and exit.
>-  -o, --output          Specify output type: `terminal` (default) or `file`.
>-  -l, --line-limit      Limit the number of lines written to the output file.
>-  -c, --colored_output  Enable colored output for terminal display.

```bash
  python3 get_monitor_process.py python
  python3 get_monitor_process.py nginx -o file
  python3 get_monitor_process.py apache2 -c
  python3 get_monitor_process.py chrome -o file -l 100
```
***

## Screenshots & Examples:
![Colored Terminal Output](automation-tools/example_docs/colored_output.png)


File Output Example
Script Usage Example
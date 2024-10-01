# SystemMonitor Class

A Python class for monitoring system metrics on Linux-based systems, optimized for Raspberry Pi devices.

## Overview

The `SystemMonitor` class provides methods to retrieve various system statistics, making it useful for system monitoring applications, logging tools, or performance analysis. It efficiently collects metrics such as CPU and GPU temperatures, CPU usage, memory information, disk usage, network statistics, system uptime, and more.

## Features

- **CPU Metrics**:
  - **Temperature**: Retrieves CPU temperature with caching and TTL (Time-to-Live) to minimize file access.
  - **Usage**: Provides overall and per-core CPU usage percentages using non-blocking calls.
  - **Frequency**: Retrieves the current CPU frequency.
  - **Statistics**: Gathers comprehensive CPU statistics in one call.

- **GPU Metrics**:
  - **Temperature**: Attempts to read GPU temperature directly from system files before using external commands.

- **Memory Metrics**:
  - Retrieves total, used, free memory in MB and percentage used.

- **Disk Metrics**:
  - Provides disk usage statistics for a specified path, including total, used, free space in GB, and usage percentage.

- **Network Metrics**:
  - Returns network interface statistics, including bytes sent and received for each interface.

- **System Metrics**:
  - **Uptime**: Retrieves system uptime since boot.
  - **Load Average**: Provides system load averages over the last 1, 5, and 15 minutes.
  - **Process Count**: Counts the number of running processes.

- **Battery Metrics**:
  - Retrieves battery status information, if available.

## Optimizations

- **Caching with TTL**: Reduces the frequency of accessing system files for temperature readings.
- **Non-blocking Calls**: Uses non-blocking calls for CPU usage to avoid delays.
- **Asynchronous Programming**: Provides asynchronous methods for metric retrieval using `asyncio`.
- **Threading**: Allows for concurrent metric collection using threads.
- **Batch Metric Collection**: Offers methods to collect all or selected metrics in a single call to reduce overhead.
- **Error Handling**: Includes comprehensive error handling and logging to ensure robustness.

## Installation

Ensure you have Python 3.6 or newer installed.

Install the required dependencies:

```bash
pip install psutil
```

## Usage

```python
from system_monitor import SystemMonitor

def main():
    monitor = SystemMonitor()

    # Get CPU temperature
    cpu_temp = monitor.get_cpu_temperature()
    print(f"CPU Temperature: {cpu_temp}°C")

    # Get all metrics
    metrics = monitor.get_all_metrics()
    print(metrics)

    # Get specific metrics
    selected_metrics = monitor.get_metrics(['cpu_temp', 'cpu_usage'])
    print(selected_metrics)

if __name__ == "__main__":
    main()
```

### Asynchronous Usage

```python
import asyncio
from system_monitor import SystemMonitor

async def main():
    monitor = SystemMonitor()
    metrics = await monitor.get_all_metrics_async()
    print(metrics)

asyncio.run(main())
```

## Methods

### `get_cpu_temperature() -> Optional[float]`

Retrieves the CPU temperature in Celsius, using caching with TTL to minimize file access.

### `get_gpu_temperature() -> Optional[float]`

Retrieves the GPU temperature in Celsius, attempting direct file access before using external commands.

### `get_cpu_usage() -> Optional[float]`

Returns the current CPU usage percentage using a non-blocking call.

### `get_per_core_cpu_usage() -> Optional[List[float]]`

Returns the CPU usage percentage for each core.

### `get_cpu_frequency() -> Optional[float]`

Retrieves the current CPU frequency in MHz.

### `get_memory_info() -> Optional[Dict[str, float]]`

Returns memory usage statistics, including total, used, free memory in MB, and percentage used.

### `get_disk_usage(path: str = '/') -> Optional[Dict[str, float]]`

Provides disk usage statistics for the specified path.

### `get_network_stats() -> Optional[Dict[str, Tuple[float, float]]]`

Returns network interface statistics, including bytes sent and received.

### `get_uptime() -> Optional[float]`

Retrieves the system uptime in seconds since boot.

### `get_load_average() -> Optional[Tuple[float, float, float]]`

Returns the system load averages over the last 1, 5, and 15 minutes.

### `get_process_count() -> Optional[int]`

Returns the number of running processes.

### `get_battery_status() -> Optional[Dict[str, float]]`

Returns battery status information, if available.

### `get_all_metrics() -> Dict[str, Any]`

Collects all system metrics at once to reduce overhead.

### `get_metrics(metrics_list: List[str]) -> Dict[str, Any]`

Collects specified system metrics.

### `async def get_all_metrics_async() -> Dict[str, Any]`

Asynchronously collects all system metrics.

### `get_all_metrics_threaded() -> Dict[str, Any]`

Collects all system metrics using threads.

## Error Handling

Methods return `None` if a metric cannot be retrieved. Errors are logged using the `logging` module.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for suggestions.

## License

This project is licensed under the MIT License.

## Acknowledgments

- [psutil](https://github.com/giampaolo/psutil) - Cross-platform library for retrieving information on running processes and system utilization.

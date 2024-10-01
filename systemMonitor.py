import os
import subprocess
import psutil
import time
import asyncio
from threading import Thread
from typing import Any
from typing import Optional, Dict, List, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR)

class SystemMonitor:
    """
    A class for monitoring system metrics such as CPU temperature, usage, memory stats, and more.

    This class provides methods to retrieve various system statistics, making it useful for system monitoring
    applications, logging tools, or performance analysis.

    Attributes:
        None

    Note:
        Some methods may return `None` if the metric is not available on the system.
    """
    @property
    def cpu_temperature(self) -> Optional[float]:
        current_time = time.time()
        if (current_time - self._cpu_temp_timestamp) > self._cpu_temp_ttl:
            self._cpu_temperature = self.get_cpu_temperature()
            self._cpu_temp_timestamp = current_time
        return self._cpu_temperature



    def __init__(self):
        self._cpu_temperature = None
        self._cpu_temp_timestamp = 0
        self._cpu_temp_ttl = 5  # Time-to-live in seconds

    def get_cpu_temperature(self) -> Optional[float]:
        """
        Reads the CPU temperature from the system file.

        Returns:
            float or None: The CPU temperature in Celsius if available, otherwise None.

        Raises:
            Exception: If an unexpected error occurs while reading the temperature.
        """
        current_time = time.time()
        if current_time - self._cpu_temp_timestamp > self._cpu_temp_ttl:
            try:
                temp_path = "/sys/class/thermal/thermal_zone0/temp"
                with open(temp_path, "r") as f:
                    temp_str = f.readline()
                    temp_c = float(temp_str) / 1000.0
                    self._cpu_temperature = temp_c
                    self._cpu_temp_timestamp = current_time
            except (FileNotFoundError, ValueError) as e:
                logging.error(f"Error reading CPU temperature: {e}")
                self._cpu_temperature = None
        return self._cpu_temperature

    async def get_cpu_temperature_async(self) -> Optional[float]:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.get_cpu_temperature)

    def get_gpu_temperature(self) -> Optional[float]:
        """
        Attempts to read GPU temperature directly from system files before using external commands.
        """
        try:
            temp_path = "/sys/class/thermal/thermal_zone1/temp"
            if os.path.exists(temp_path):
                with open(temp_path, "r") as f:
                    temp_str = f.readline()
                    temp_c = float(temp_str) / 1000.0
                    return temp_c
            else:
                # Fallback to vcgencmd if the system file doesn't exist
                output = subprocess.check_output(["vcgencmd", "measure_temp"]).decode()
                temp_str = output.strip().split('=')[1].split("'")[0]
                temp_c = float(temp_str)
                return temp_c
        except Exception as e:
            logging.error(f"Error getting GPU temperature: {e}")
            return None

    def get_cpu_usage(self) -> Optional[float]:
        """
        Returns the current CPU usage percentage.

        Returns:
            float or None: CPU usage percentage if available, otherwise None.

        Raises:
            Exception: If an unexpected error occurs while retrieving CPU usage.
        """
        try:
            # non-blocking
            cpu_usage = psutil.cpu_percent(interval=None)
            return cpu_usage
        except Exception as e:
            logging.error(f"Error getting CPU usage: {e}")
            return None

    async def get_cpu_usage_async(self) -> Optional[float]:
        """
        Asynchronously gets CPU usage.
        """
        loop = asyncio.get_event_loop()
        cpu_usage = await loop.run_in_executor(None, psutil.cpu_percent, None)
        return cpu_usage

    def get_per_core_cpu_usage(self) -> Optional[List[float]]:
        """
        Returns the CPU usage percentage for each core.

        Returns:
            List[float] or None: A list of CPU usage percentages per core if available, otherwise None.

        Raises:
            Exception: If an unexpected error occurs while retrieving per-core CPU usage.
        """
        try:
            # non blocking
            per_core_usage = psutil.cpu_percent(interval=None, percpu=True)
            return per_core_usage
        except Exception as e:
            logging.error(f"Error getting per-core CPU usage: {e}")
            return None

    def get_cpu_frequency(self) -> Optional[float]:
        """
        Returns the current CPU frequency in MHz.

        Returns:
            float or None: Current CPU frequency in MHz if available, otherwise None.

        Raises:
            Exception: If an unexpected error occurs while retrieving CPU frequency.
        """
        try:
            freq = psutil.cpu_freq()
            if freq:
                return freq.current
            else:
                logging.error("CPU frequency information not available.")
                return None
        except Exception as e:
            logging.error(f"Error getting CPU frequency: {e}")
            return None

    def get_cpu_stats(self) -> Optional[Dict[str, Any]]:
        """
        Retrieves various CPU statistics in one call.
        """
        try:
            cpu_times = psutil.cpu_times_percent(interval=None)
            stats = {
                'user': cpu_times.user,
                'system': cpu_times.system,
                'idle': cpu_times.idle,
                # Add more stats as needed
            }
            return stats
        except Exception as e:
            logging.error(f"Error getting CPU stats: {e}")
            return None

    def get_memory_info(self) -> Optional[Dict[str, float]]:
        """
        Returns memory usage statistics.

        Returns:
            Dict[str, float] or None: A dictionary containing total, used, free memory in MB and usage percentage,
            or None if an error occurs.

        Raises:
            Exception: If an unexpected error occurs while retrieving memory information.
        """
        try:
            mem = psutil.virtual_memory()
            return {
                'total': round(mem.total / (1024 ** 2), 2),
                'used': round(mem.used / (1024 ** 2), 2),
                'free': round(mem.available / (1024 ** 2), 2),
                'percent': round(mem.percent, 2)
            }
        except Exception as e:
            logging.error(f"Error getting memory info: {e}")
            return None

    def get_disk_usage(self, path: str = '/') -> Optional[Dict[str, float]]:
        """
        Returns disk usage statistics for the specified path.

        Args:
            path (str): The filesystem path to check. Defaults to '/'.

        Returns:
            Dict[str, float] or None: A dictionary containing total, used, free disk space in GB and usage percentage,
            or None if an error occurs.

        Raises:
            Exception: If an unexpected error occurs while retrieving disk usage.
        """
        try:
            if os.path.exists(path):
                disk = psutil.disk_usage(path)
                return {
                    'total': disk.total / (1024 ** 3),  # Convert bytes to GB
                    'used': disk.used / (1024 ** 3),
                    'free': disk.free / (1024 ** 3),
                    'percent': disk.percent
                }
            else:
                logging.error(f"Disk path does not exist: {path}")
                return None
        except Exception as e:
            logging.error(f"Error getting disk usage for {path}: {e}")
            return None

    def get_network_stats(self) -> Optional[Dict[str, Tuple[float, float]]]:
        """
        Returns network interface statistics.

        Returns:
            Dict[str, Tuple[float, float]] or None: A dictionary where each key is a network interface name
            and the value is a tuple of bytes sent and bytes received, or None if an error occurs.

        Raises:
            Exception: If an unexpected error occurs while retrieving network statistics.
        """
        try:
            stats = psutil.net_io_counters(pernic=True)
            network_data = {}
            for iface, data in stats.items():
                network_data[iface] = (data.bytes_sent, data.bytes_recv)
            return network_data
        except Exception as e:
            logging.error(f"Error getting network stats: {e}")
            return None

    def get_uptime(self) -> Optional[float]:
        """
        Returns the system uptime in seconds since the epoch.

        Returns:
            float or None: System uptime in seconds if available, otherwise None.

        Raises:
            Exception: If an unexpected error occurs while retrieving system uptime.
        """
        try:
            uptime = psutil.boot_time()
            return uptime
        except Exception as e:
            logging.error(f"Error getting system uptime: {e}")
            return None

    def get_load_average(self) -> Optional[Tuple[float, float, float]]:
        """
        Returns the system load averages over the last 1, 5, and 15 minutes.

        Returns:
            Tuple[float, float, float] or None: A tuple containing the 1, 5, and 15-minute load averages,
            or None if an error occurs.

        Raises:
            Exception: If an unexpected error occurs while retrieving load averages.
        """
        try:
            load_avg = os.getloadavg()
            return load_avg
        except (AttributeError, OSError) as e:
            logging.error(f"Error getting load average: {e}")
            return None

    def get_process_count(self) -> Optional[int]:
        """
        Returns the number of running processes.

        Returns:
            int or None: The number of running processes if available, otherwise None.

        Raises:
            Exception: If an unexpected error occurs while retrieving process count.
        """
        try:
            process_count = len(psutil.pids())
            return process_count
        except Exception as e:
            logging.error(f"Error getting process count: {e}")
            return None

    def get_battery_status(self) -> Optional[Dict[str, float]]:
        """
        Returns battery status information.

        Returns:
            Dict[str, float] or None: A dictionary containing battery percentage, seconds left,
            and power plugged status, or None if battery information is not available.

        Raises:
            Exception: If an unexpected error occurs while retrieving battery status.
        """
        try:
            battery = psutil.sensors_battery()
            if battery:
                return {
                    'percent': battery.percent,
                    'secsleft': battery.secsleft,
                    'power_plugged': battery.power_plugged
                }
            else:
                logging.info("Battery information not available.")
                return None
        except Exception as e:
            logging.error(f"Error getting battery status: {e}")
            return None

    def get_fan_speed(self) -> Optional[int]:
        """
        Returns the fan speed if available.

        Returns:
            int or None: Fan speed in RPM if available, otherwise None.

        Raises:
            Exception: If an unexpected error occurs while retrieving fan speed.
        """
        # Implement if hardware supports fan speed reading
        logging.info("Fan speed reading not implemented.")
        return None

    def get_memory_temperature(self) -> Optional[float]:
        """
        Returns the memory temperature if available.

        Returns:
            float or None: Memory temperature in Celsius if available, otherwise None.

        Raises:
            Exception: If an unexpected error occurs while retrieving memory temperature.
        """
        # Implement if hardware provides memory temperature
        logging.info("Memory temperature reading not implemented.")
        return None

    def get_all_metrics(self) -> Dict[str, Any]:
        """
        Collects all system metrics at once to reduce overhead.
        """
        metrics = {}
        try:
            metrics['cpu_temp'] = self.get_cpu_temperature()
            metrics['cpu_usage'] = psutil.cpu_percent(interval=None)
            cpu_freq = psutil.cpu_freq()
            metrics['cpu_freq'] = cpu_freq.current if cpu_freq else None

            mem = psutil.virtual_memory()
            metrics['memory'] = {
                'total': mem.total / (1024 ** 2),
                'used': mem.used / (1024 ** 2),
                'free': mem.available / (1024 ** 2),
                'percent': mem.percent
            }

            disk = psutil.disk_usage('/')
            metrics['disk'] = {
                'total': disk.total / (1024 ** 3),
                'used': disk.used / (1024 ** 3),
                'free': disk.free / (1024 ** 3),
                'percent': disk.percent
            }

            # Add more metrics as needed
        except Exception as e:
            logging.error(f"Error collecting metrics: {e}")

        return metrics



    def get_metrics(self, metrics_list: List[str]) -> Dict[str, Any]:
        """
        Collects specified system metrics.
        """
        metrics = {}
        for metric in metrics_list:
            if metric == 'cpu_temp':
                metrics['cpu_temp'] = self.get_cpu_temperature()
            elif metric == 'cpu_usage':
                metrics['cpu_usage'] = self.get_cpu_usage()
            # Add other metrics as needed
        return metrics

    async def get_all_metrics_async(self) -> Dict[str, Any]:
        """
        Asynchronously collects all system metrics.
        """
        tasks = [
            self.get_cpu_temperature_async(),
            self.get_cpu_usage_async(),
            # Add other async metric methods
        ]
        results = await asyncio.gather(*tasks)
        metrics = {
            'cpu_temp': results[0],
            'cpu_usage': results[1],
            # Map other results
        }
        return metrics

    def get_all_metrics_threaded(self) -> Dict[str, Any]:
        """
        Collects all system metrics using threads.
        """
        metrics = {}

        def collect_cpu_temp():
            metrics['cpu_temp'] = self.get_cpu_temperature()

        def collect_cpu_usage():
            metrics['cpu_usage'] = self.get_cpu_usage()

        threads = [
            Thread(target=collect_cpu_temp),
            Thread(target=collect_cpu_usage),
            # Add other metric collection threads
        ]

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        return metrics

import unittest
import asyncio
from pi_system_monitor.sys_monitor import SystemMonitor
from typing import Any

class TestSystemMonitor(unittest.TestCase):

    def setUp(self):
        self.monitor = SystemMonitor()

    def test_get_cpu_temperature(self):
        temp = self.monitor.get_cpu_temperature()
        if temp is not None:
            self.assertIsInstance(temp, float)
            self.assertGreaterEqual(temp, -20)  # Assuming possible temperature ranges
            self.assertLessEqual(temp, 150)
        else:
            self.assertIsNone(temp)

    def test_get_cpu_temperature_property(self):
        temp = self.monitor.cpu_temperature
        if temp is not None:
            self.assertIsInstance(temp, float)
            self.assertGreaterEqual(temp, -20)
            self.assertLessEqual(temp, 150)
        else:
            self.assertIsNone(temp)

    def test_get_cpu_temperature_async(self):
        async def run_test():
            temp = await self.monitor.get_cpu_temperature_async()
            if temp is not None:
                self.assertIsInstance(temp, float)
                self.assertGreaterEqual(temp, -20)
                self.assertLessEqual(temp, 150)
            else:
                self.assertIsNone(temp)
        asyncio.run(run_test())

    def test_get_gpu_temperature(self):
        temp = self.monitor.get_gpu_temperature()
        if temp is not None:
            self.assertIsInstance(temp, float)
            self.assertGreaterEqual(temp, -20)
            self.assertLessEqual(temp, 150)
        else:
            self.assertIsNone(temp)

    def test_get_cpu_usage(self):
        usage = self.monitor.get_cpu_usage()
        self.assertIsNotNone(usage)
        self.assertIsInstance(usage, float)
        self.assertGreaterEqual(usage, 0)
        self.assertLessEqual(usage, 100)

    def test_get_cpu_usage_async(self):
        async def run_test():
            usage = await self.monitor.get_cpu_usage_async()
            self.assertIsNotNone(usage)
            self.assertIsInstance(usage, float)
            self.assertGreaterEqual(usage, 0)
            self.assertLessEqual(usage, 100)
        asyncio.run(run_test())

    def test_get_per_core_cpu_usage(self):
        usage_list = self.monitor.get_per_core_cpu_usage()
        self.assertIsNotNone(usage_list)
        self.assertIsInstance(usage_list, list)
        self.assertGreater(len(usage_list), 0)
        for usage in usage_list:
            self.assertIsInstance(usage, float)
            self.assertGreaterEqual(usage, 0)
            self.assertLessEqual(usage, 100)

    def test_get_cpu_frequency(self):
        freq = self.monitor.get_cpu_frequency()
        if freq is not None:
            self.assertIsInstance(freq, float)
            self.assertGreater(freq, 0)
            self.assertLess(freq, 10000)  # Assuming frequency less than 10 GHz
        else:
            self.assertIsNone(freq)

    def test_get_cpu_stats(self):
        stats = self.monitor.get_cpu_stats()
        if stats is not None:
            self.assertIsInstance(stats, dict)
            self.assertIn('user', stats)
            self.assertIn('system', stats)
            self.assertIn('idle', stats)
            for key in ['user', 'system', 'idle']:
                self.assertIsInstance(stats[key], float)
                self.assertGreaterEqual(stats[key], 0)
                self.assertLessEqual(stats[key], 100)
        else:
            self.assertIsNone(stats)

    def test_get_memory_info(self):
        mem_info = self.monitor.get_memory_info()
        self.assertIsNotNone(mem_info)
        self.assertIsInstance(mem_info, dict)
        for key in ['total', 'used', 'free', 'percent']:
            self.assertIn(key, mem_info)
            self.assertIsInstance(mem_info[key], float)
            self.assertGreaterEqual(mem_info[key], 0)

    def test_get_disk_usage(self):
        disk_info = self.monitor.get_disk_usage()
        if disk_info is not None:
            self.assertIsInstance(disk_info, dict)
            for key in ['total', 'used', 'free', 'percent']:
                self.assertIn(key, disk_info)
                self.assertIsInstance(disk_info[key], float)
                self.assertGreaterEqual(disk_info[key], 0)
        else:
            self.assertIsNone(disk_info)

    def test_get_network_stats(self):
        net_stats = self.monitor.get_network_stats()
        if net_stats is not None:
            self.assertIsInstance(net_stats, dict)
            for iface, data in net_stats.items():
                self.assertIsInstance(iface, str)
                self.assertIsInstance(data, tuple)
                self.assertEqual(len(data), 2)
                self.assertIsInstance(data[0], int)
                self.assertIsInstance(data[1], int)
                self.assertGreaterEqual(data[0], 0)
                self.assertGreaterEqual(data[1], 0)
        else:
            self.assertIsNone(net_stats)

    def test_get_uptime(self):
        uptime = self.monitor.get_uptime()
        if uptime is not None:
            self.assertIsInstance(uptime, float)
            self.assertGreaterEqual(uptime, 0)
        else:
            self.assertIsNone(uptime)

    def test_get_load_average(self):
        load_avg = self.monitor.get_load_average()
        if load_avg is not None:
            self.assertIsInstance(load_avg, tuple)
            self.assertEqual(len(load_avg), 3)
            for load in load_avg:
                self.assertIsInstance(load, float)
                self.assertGreaterEqual(load, 0)
        else:
            self.assertIsNone(load_avg)

    def test_get_process_count(self):
        proc_count = self.monitor.get_process_count()
        if proc_count is not None:
            self.assertIsInstance(proc_count, int)
            self.assertGreaterEqual(proc_count, 0)
        else:
            self.assertIsNone(proc_count)

    def test_get_battery_status(self):
        battery_status = self.monitor.get_battery_status()
        if battery_status is not None:
            self.assertIsInstance(battery_status, dict)
            self.assertIn('percent', battery_status)
            self.assertIn('secsleft', battery_status)
            self.assertIn('power_plugged', battery_status)
            self.assertIsInstance(battery_status['percent'], float)
            self.assertGreaterEqual(battery_status['percent'], 0)
            self.assertLessEqual(battery_status['percent'], 100)
            self.assertIsInstance(battery_status['secsleft'], (float, int))
            self.assertIsInstance(battery_status['power_plugged'], bool)
        else:
            self.assertIsNone(battery_status)

    def test_get_fan_speed(self):
        fan_speed = self.monitor.get_fan_speed()
        self.assertIsNone(fan_speed)  # As method is not implemented

    def test_get_memory_temperature(self):
        mem_temp = self.monitor.get_memory_temperature()
        self.assertIsNone(mem_temp)  # As method is not implemented

    def test_get_all_metrics(self):
        metrics = self.monitor.get_all_metrics()
        self.assertIsInstance(metrics, dict)
        # Check for expected keys
        expected_keys = ['cpu_temp', 'cpu_usage', 'cpu_freq', 'memory', 'disk']
        for key in expected_keys:
            self.assertIn(key, metrics)

    def test_get_metrics(self):
        metrics_list = ['cpu_temp', 'cpu_usage']
        metrics = self.monitor.get_metrics(metrics_list)
        self.assertIsInstance(metrics, dict)
        for metric in metrics_list:
            self.assertIn(metric, metrics)

    def test_get_all_metrics_async(self):
        async def run_test():
            metrics = await self.monitor.get_all_metrics_async()
            self.assertIsInstance(metrics, dict)
            self.assertIn('cpu_temp', metrics)
            self.assertIn('cpu_usage', metrics)
        asyncio.run(run_test())

    def test_get_all_metrics_threaded(self):
        metrics = self.monitor.get_all_metrics_threaded()
        self.assertIsInstance(metrics, dict)
        self.assertIn('cpu_temp', metrics)
        self.assertIn('cpu_usage', metrics)

if __name__ == '__main__':
    unittest.main()

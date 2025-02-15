import subprocess
import re
import logging
import time


class IPMIServerInfo:
    def __init__(self, ip, username, password):
        """Initialize IPMI connection parameters"""
        self.ip = ip
        self.username = username
        self.password = password
        self.ipmitool_cmd = [
            "ipmitool",
            "-I",
            "lanplus",
            "-H",
            ip,
            "-U",
            username,
            "-P",
            password,
        ]
        self.setup_logger()

    def setup_logger(self):
        """Set up logger for the class"""
        self.logger = logging.getLogger("IPMIServerInfo")
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def run_command(self, command, retries=3, delay=2):
        """Execute IPMI command with retries"""
        attempt = 0
        while attempt < retries:
            try:
                result = subprocess.run(
                    self.ipmitool_cmd + command.split(),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                self.logger.debug(
                    f"Running command: {' '.join(self.ipmitool_cmd + command.split())}"
                )
                if result.returncode == 0:
                    return result.stdout.strip()
                else:
                    self.logger.error(f"Error: {result.stderr.strip()}")
                    attempt += 1
                    time.sleep(delay)
            except Exception as e:
                self.logger.error(f"Exception: {e}")
                attempt += 1
                time.sleep(delay)
        return None

    def get_fan_speed(self):
        """Get fan speed"""
        output = self.run_command("sensor list")
        if not output:
            self.logger.warning("Failed to retrieve fan speed.")
            return None
        fan_speeds = {}
        for line in output.split("\n"):
            if "Fan" in line or "FAN" in line:
                parts = line.split("|")
                if len(parts) >= 2:
                    name = parts[0].strip()
                    speed = parts[1].strip()
                    fan_speeds[name] = speed
        return fan_speeds

    def get_power_usage(self):
        """Get power usage status"""
        output = self.run_command("dcmi power reading")
        if not output:
            self.logger.warning("Failed to retrieve power usage.")
            return None
        match = re.search(r"Instantaneous power\s*:\s*(\d+)\s*Watts", output)
        return int(match.group(1)) if match else None

    def get_temperatures(self):
        """Get server temperatures"""
        output = self.run_command("sensor list")
        if not output:
            self.logger.warning("Failed to retrieve temperatures.")
            return None
        temperatures = {}
        for line in output.split("\n"):
            if "Temp" in line or "TEMP" in line:
                parts = line.split("|")
                if len(parts) >= 2:
                    name = parts[0].strip()
                    temp = parts[1].strip()
                    temperatures[name] = temp
        return temperatures

    def get_hardware_info(self):
        """Get server hardware info"""
        output = self.run_command("fru print")
        if not output:
            self.logger.warning("Failed to retrieve hardware info.")
            return None
        info = {}

        # CPU
        match = re.search(r"Processor\s*:\s*(.*)", output)
        info["CPU"] = match.group(1).strip() if match else "Unknown"

        # Memory
        match = re.search(r"Total Memory\s*:\s*(.*)", output)
        info["Memory"] = match.group(1).strip() if match else "Unknown"

        # Hard disk (Need original factory support)
        match = re.search(r"Drive\s*:\s*(.*)", output)
        info["Disk"] = match.group(1).strip() if match else "Unknown"

        return info

    def get_chassis_status(self):
        """Get chassis status"""
        output = self.run_command("chassis status")
        if not output:
            self.logger.warning("Failed to retrieve chassis status.")
            return None
        chassis_status = {}
        for line in output.split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                chassis_status[key.strip()] = value.strip()
        return chassis_status, self.check_chassis_status(chassis_status)

    def check_chassis_status(self, data):
        result = ""
        if data.get("System Power", "Unknown") != "on":
            result += "The system is not powered on\n"
        if data.get("Power Overload", "Unknown") != "false":
            result += "Power supply overload\n"
        if data.get("Main Power Fault", "Unknown") != "false":
            result += "Main power fault\n"
        if data.get("Power Control Fault", "Unknown") != "false":
            result += "Power control fault\n"
        if data.get("Drive Fault", "Unknown") != "false":
            result += "Drive fault\n"
        if data.get("Cooling/Fan Fault", "Unknown") != "false":
            result += "Cooling fault\n"
        if not result:
            result = "The server is running normally"
        return result

    def set_fan_speed(self, speed):
        """Set fan speed
        :param speed: Fan speed percentage (0-100), if it is -1, set to automatic mode
        """
        if speed == -1:
            command = "raw 0x30 0x30 0x01 0x00"
        elif 0 <= speed <= 100:
            hex_speed = hex(int(speed * 255 / 100))  # convert 0x00-0xFF
            command = f"raw 0x30 0x30 0x02 0xff {hex_speed}"
        else:
            self.logger.error(
                "Error: The speed value must be between 0-100, or set to automatic mode using -1."
            )
            return False

        output = self.run_command(command)
        if output is not None:
            self.logger.info("The fan speed has been successfully set.")
            return True
        else:
            self.logger.error("Fan speed setting failed.")
            return False

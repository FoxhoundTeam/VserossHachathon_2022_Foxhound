from enum import Enum


class ScanStatus(str, Enum):
    running = "running"
    finished = "finished"
    error = "error"


class PortStatus(str, Enum):
    open = "open"
    closed = "closed"
    filtered = "filtered"


class Protocol(str, Enum):
    tcp = "tcp"
    udp = "udp"

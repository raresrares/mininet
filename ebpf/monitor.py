from bcc import BPF
import ctypes
import socket

bpf = BPF(src_file="monitor_mptcp.c")


class IPv4ConnInfo(ctypes.Structure):
    _fields_ = [
        ("pid", ctypes.c_uint),
        ("saddr", ctypes.c_uint),
        ("daddr", ctypes.c_uint),
        ("sport", ctypes.c_ushort),
        ("dport", ctypes.c_ushort)
    ]


def print_event(data):
    event = ctypes.cast(data, ctypes.POINTER(IPv4ConnInfo)).contents
    pid = event.pid
    saddr = socket.inet_ntoa(ctypes.c_uint.from_buffer_copy(event.saddr).value.to_bytes(4, 'little'))
    daddr = socket.inet_ntoa(ctypes.c_uint.from_buffer_copy(event.daddr).value.to_bytes(4, 'little'))
    sport = event.sport
    dport = event.dport

    print(f"[MPTCP Connection] pid: {pid}, src: {saddr}:{sport}, dst: {daddr}:{dport}")


bpf["ipv4_events"].open_perf_buffer(print_event)

while True:
    bpf.perf_buffer_poll()

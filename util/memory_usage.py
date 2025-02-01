import gc
import os


def df():
    fs_stat = os.statvfs('//')
    return f"{(fs_stat[0] * fs_stat[3]) / 1048576} MB"


def free(full=False):
    mem_free = gc.mem_free()
    mem_alloc = gc.mem_alloc()
    mem_total = mem_free + mem_alloc
    percentage_free = f"{mem_free / mem_total * 100:.2f}%"
    if not full:
        return percentage_free
    else:
        return f"Total:{mem_total} Free:{mem_free} ({percentage_free})"

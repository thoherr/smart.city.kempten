import gc
import os

def flash():
    fs_stat = os.statvfs('//')
    return (fs_stat[0] * fs_stat[3]) / 1048576

def df():
    fs_stat = os.statvfs('//')
    return f"{flash()} MB"

def memory():
    mem_free = gc.mem_free()
    mem_alloc = gc.mem_alloc()
    mem_total = mem_free + mem_alloc
    percentage_free = round(mem_free / mem_total * 100, 2)
    return mem_free, mem_alloc, mem_total, percentage_free

def free(full=False):
    mem_free, mem_alloc, mem_total, percentage_free = memory()
    if not full:
        return percentage_free
    else:
        return f"Total:{mem_total} Free:{mem_free} ({percentage_free}%)"

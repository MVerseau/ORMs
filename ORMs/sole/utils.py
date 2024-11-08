from django.template.defaulttags import register
import os
import psutil
from functools import wraps
@register.filter
def is_string(val):
    return isinstance(val, str)


@register.filter
def is_list(val):
    return isinstance(val, list)

# def process_memory():
#
#     mem_info = process.memory_info()
#     return mem_info.rss
#
# def process_cpu():
#     process


def ps_utils(func):
    def wrapper(*args, **kwargs):
        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss
        result = func(*args, **kwargs)
        mem_after = process.memory_info().rss
        return result, sum(process.cpu_times()), mem_after-mem_before
    return wrapper
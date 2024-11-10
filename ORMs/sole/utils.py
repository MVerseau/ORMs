from django.template.defaulttags import register
import os
import psutil
import contextlib

cpu_interval = 0
iter = 100
filename = 'text.csv'
# file = open(filename, 'w', encoding='utf-8')

@register.filter
def is_string(val):
    return isinstance(val, str)


@register.filter
def is_list(val):
    return isinstance(val, list)


def ps_utils(func):
    def wrapper(*args, **kwargs):
        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss
        result = func(*args, **kwargs)
        mem_after = process.memory_info().rss
        # with open('text.csv', 'a', encoding='utf-8') as file, contextlib.redirect_stdout(file):
        #     psutil.test()
        #     print("\n" * 10)
        return result, process.cpu_percent(interval=cpu_interval), mem_after - mem_before
    return wrapper

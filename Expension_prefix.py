
import ipaddress
import random
from Extract_prefix import *
import concurrent.futures


def compress_prefix(prefix):
    network = ipaddress.IPv6Network(prefix)
    compressed_prefix = network.compressed
    return compressed_prefix


def binary_to_ipv6_prefix(binary_str):
    prefix_length = len(binary_str)
    binary_str = binary_str.ljust(128, '0')
    decimal = int(binary_str, 2)
    ipv6_network = ipaddress.IPv6Network((decimal, prefix_length), strict=False)
    ipv6_prefix = ipv6_network.with_prefixlen
    return str(ipv6_prefix)


def g_prefix(ip, prefix_length,n, bounds):
    binary_address = format(int(ip), '0128b')
    expend_pre = []
    length = 0
    if prefix_length is not None:
        prefix_length = int(prefix_length)
        if prefix_length>0 and prefix_length<64:
            if bounds is not None:
                for bound in bounds:
                    diff=bound-prefix_length
                    if diff==0:
                        if n+prefix_length<=64:
                            for i in range(2 ** n):
                                zeros_and_ones = format(i, f'0{n}b')
                                binary_address = binary_address[:prefix_length] + zeros_and_ones
                                hexp = binary_to_ipv6_prefix(binary_address)
                                expend_pre.append(hexp)
                            break
                        else:
                            n=64-prefix_length
                            for i in range(2 ** n):
                                zeros_and_ones = format(i, f'0{n}b')
                                binary_address = binary_address[:prefix_length] + zeros_and_ones
                                hexp = binary_to_ipv6_prefix(binary_address)
                                expend_pre.append(hexp)
                            break
                    elif diff>0 and diff<=n:
                        n= diff+n
                        if n+prefix_length<=64:
                            try:
                                for i in range(2 ** n): 
                                    zeros_and_ones = format(i, f'0{n}b')
                                    binary_address = binary_address[:prefix_length] + zeros_and_ones
                                    hexp = binary_to_ipv6_prefix(binary_address)
                                    expend_pre.append(hexp)
                            except TypeError as e:
                                print("TypeError occurred:", e)
                            break
                        else:
                            n=64-prefix_length
                            for i in range(2 ** n):
                                zeros_and_ones = format(i, f'0{n}b')
                                binary_address = binary_address[:prefix_length] + zeros_and_ones
                                hexp = binary_to_ipv6_prefix(binary_address)
                                expend_pre.append(hexp)
                            break
                    elif diff>n:
                        length=n
                        for i in range(2 ** length):
                            zeros_and_ones = format(i, f'0{length}b')
                            binary_address = binary_address[:prefix_length] + zeros_and_ones
                            hexp = binary_to_ipv6_prefix(binary_address)
                            expend_pre.append(hexp)
        else:
            length=0
            for i in range(2 ** length):
                zeros_and_ones = format(i, f'0{length}b')
                binary_address = binary_address[:prefix_length-1] + zeros_and_ones
                hexp = binary_to_ipv6_prefix(binary_address)
                expend_pre.append(hexp)
    return expend_pre


def process_prefix(prefix, n, cor):
    # expendedpre=[]
    pres = []
    if prefix is not None:
        address, prefix_length = prefix.split('/')
        ip = ipaddress.IPv6Address(address)
        pres.extend(g_prefix(ip, prefix_length, n, cor))
    return pres

def chanpre(prefixes, n, cor):
    pres = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = [executor.submit(process_prefix, prefix, n, cor) for prefix in prefixes]
        for future in concurrent.futures.as_completed(results):
            pres.extend(future.result())
            print(pres)
    return list(set(pres))


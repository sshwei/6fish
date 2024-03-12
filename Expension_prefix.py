
import ipaddress
import random
from Extract_prefix import *
import concurrent.futures


def compress_prefix(prefix):
    network = ipaddress.IPv6Network(prefix)
    compressed_prefix = network.compressed
    return compressed_prefix


def add_random_zeros_and_ones(binary_address, prefix_length,length):
    zeros_and_ones = ''.join(random.choice('01')for _ in range (length))
    result = binary_address[:prefix_length] + zeros_and_ones
    return result


def binary_to_ipv6_prefix(binary_str):
    prefix_length = len(binary_str)
    binary_str = binary_str.ljust(128, '0')
    decimal = int(binary_str, 2)
    ipv6_network = ipaddress.IPv6Network((decimal, prefix_length), strict=False)
    ipv6_prefix = ipv6_network.with_prefixlen
    return str(ipv6_prefix)


def g_prefix(ip, prefix_length,n,cor):
    binary_address = format(int(ip), '0128b')
    expend_pre=[]
    length=0
    if prefix_length is not None:
        prefix_length = int(prefix_length)
        for cores in cor:
            if prefix_length <=cores:
                if cores-prefix_length>=n:
                    length=n
                else:
                    length=cores-prefix_length
                try:
                    for _ in range(2**length):
                        binary_address = add_random_zeros_and_ones(binary_address, prefix_length, length)
                        hexp = binary_to_ipv6_prefix(binary_address)
                        expend_pre.append(hexp)
                except TypeError as e:
                    print ("TypeError occurred:", e)
            else:
                length=0
                for _ in range(2**length):
                        binary_address = add_random_zeros_and_ones(binary_address, prefix_length, length)
                        hexp = binary_to_ipv6_prefix(binary_address)
                        expend_pre.append(hexp)        
    return expend_pre


def process_prefix(prefix, n, cor):
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
    return list(set(pres))

if __name__ == '__main__':
    n=4
    cor=[32, 39, 45, 48, 51, 64]
    prefixes=['2400:cb00:581::/43']
    prefixes = chanpre(prefixes,n,cor)
    print(len(prefixes))
    print(f"Expanded prefix: {prefixes}")

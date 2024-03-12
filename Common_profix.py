
from Extract_prefix import recover_BGP_prefix
import ipaddress
from genip import gip

def is_global_unicast_ipv6(ipv6_address):
    try:
        ip = ipaddress.ip_address(ipv6_address)
        return ip.is_global and ip.version == 6 and not ip.is_multicast and not ip.is_link_local and not ip.is_loopback and not ip.is_private
    except ValueError:
        return False
    
def binary_to_ipv6(binary_str):
    prefix_length = len(binary_str)
    binary_str = binary_str.ljust(128, '0')
    decimal = int(binary_str, 2)
    ipv6_network = ipaddress.IPv6Network((decimal, prefix_length), strict=False)
    ipv6_prefix = ipv6_network.with_prefixlen
    return str(ipv6_prefix)

def process_nasip(iplist):
    binary_addresses = []
    prefix_ipv6=set()
    for ip in iplist:
        if is_global_unicast_ipv6(ip):
            ip = ipaddress.IPv6Address(ip)
            binary_addresses.append(format(int(ip), '0128b'))
            prefix_ipv6_32=binary_to_ipv6(binary_addresses[0][:32])
            prefix_ipv6.add(prefix_ipv6_32)
    return list(prefix_ipv6)

def extract_common_prefix(addresses):
    # Store IPv6 addresses in binary representation
    binary_addresses = []
    common_prefixes = []
    common_prefix_ipv6_set= set()
    common_prefix_ipv6=[]
    Recprefixes=set()

    # Convert IPv6 addresses to binary representation
    if(len(addresses)==1):
        Recprefixes.add(recover_BGP_prefix(addresses[0]))
    else:
        for addr in addresses:
            Recprefixes.add(recover_BGP_prefix(addr))
            try:
                ip = ipaddress.IPv6Address(addr)
            except ipaddress.AddressValueError:
                print("Invalid IPv6 address:", addr)
                continue  
            binary_addresses.append(format(int(ip), '0128b'))

        # Find common prefixes for adjacent IPv6 address pairs
        for i in range(len(binary_addresses) - 1):
            common_prefix = ''
            for j in range(len(binary_addresses[i])):
                if binary_addresses[i][j] == binary_addresses[i + 1][j]:
                    common_prefix += binary_addresses[i][j]
                else:
                    break
            common_prefixes.append(common_prefix)

        # Convert common prefix to IPv6 representation
        common_prefix_ipv6 = [binary_to_ipv6(prefix) for prefix in common_prefixes]
        #Convert common prefix to IPv6 representation and deduplicate
    for prefix in common_prefix_ipv6:
        if prefix is not None:
            prefix_parts, prefix_length = prefix.split("/")
            prefix_length=int(prefix_length)
            if prefix_length>64 or prefix_length<16:
                result = recover_BGP_prefix(gip(prefix))
                if result is not None:
                    Recprefixes.add(result)
            else:    
                common_prefix_ipv6_set.add(prefix)
    common_prefix_ipv6_set.update(Recprefixes)
    return list(common_prefix_ipv6_set)


if __name__ == '__main__':

    common_prefixess=[]
    addresses=['2400:cb00:581:3::']
    iplist=['2001:7fa:0:1::ca28:a0f6']
    common_prefixess = extract_common_prefix(addresses)
    print('Common prefix:', common_prefixess)
    a=process_nasip(iplist)
    print(a)
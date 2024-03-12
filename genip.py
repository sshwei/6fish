
import ipaddress
import random

def gip(prefix):
    # Parse the prefix into an IPv6Network object
    try:
        # Parse the prefix into an IPv6Network object
        network = ipaddress.IPv6Network(prefix)
    except ValueError:
        print("Invalid IPv6 prefix:", prefix)
        return None
    # Check if the prefix length is valid
    if network.prefixlen < 0 or network.prefixlen > 128:
        print("IPv6 prefix length erro")
        return None
        # Remove /128 if the prefix length is 128
    elif network.prefixlen == 128:
        ipv6_address = str(prefix).split('/')[0]
    # Generate a random host address within the network range
    else:
        host = random.randint(1, network.num_addresses)  # Exclude network and broadcast addresses
        if host <= 0:
            raise ValueError("Empty range of available IP addresses")
            return None
        # Combine the network prefix with the random host address
        ipv6_address = str(network.network_address + host)
    return ipv6_address
    
def gLip(prefix):
    ip,iplenth = prefix.split('/')
    if ip.endswith('::'):
        ip+= '1'
    else:
        segments = ip.split(':')
        segments[-1] = '1'
        ip = ':'.join(segments)
    return ip


    

if __name__ == '__main__':
    pre='2001:1218:6013::/48'
    ret=gip(pre)
    print(ret)


                        

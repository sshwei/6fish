
import sys
sys.path.append('/home/lihongwei/.local/lib/python3.8/site-packages')
import pyasn
import random
from Save_ret import save_selectprefixes ,save_proportion
import ipaddress


asndb = pyasn.pyasn('/home/lihongwei/topo/fish/6fish/data/20240115ipasn.dat') #Enter the absolute path to ipasn

#Query prefix and ASN through pyasn
def extract_BGP_prefix(prefix):
    asn,prefix= asndb.lookup(prefix)
    if prefix is not None and asn is not None :
        return prefix
    else:
        return None

def recover_BGP_prefix(prefix):
    asn,prefix= asndb.lookup(prefix)
    if prefix is not None and asn is not None :
        return prefix
    else:
        return None
    
def get_asn(ip):
    try:
        ip_obj = ipaddress.ip_address(ip)
        if ip_obj.version == 6:
            asn, prefix = asndb.lookup(ip)
            if prefix is not None and asn is not None:
                return asn
            else:
                return None
    except ValueError:
        pass
    
    return None


def compress_prefix(prefix):
    network = ipaddress.IPv6Network(prefix)
    # Obtain compressed prefix
    compressed_prefix = network.compressed
    return compressed_prefix

def random_prefix(prefixes,total_samples):
    prefix_dict = {}
    for prefix in prefixes:
        prefix_parts = prefix.split("/")
        prefix_length = int(prefix_parts[1])
        prefix_value = prefix
        if prefix_length not in prefix_dict:
            prefix_dict[prefix_length] = []
        prefix_dict[prefix_length].append(prefix_value)
    # Calculate the extraction quantity corresponding to each key
    weights = [len(prefix_dict[key]) for key in prefix_dict]
    total_weights = sum(weights)
    normalized_weights = [weight / total_weights for weight in weights]
    sample_counts = [int(weight * total_samples) for weight in normalized_weights]
    # Perform weighted random sampling
    selected_keys = random.choices(list(prefix_dict.keys()), weights=normalized_weights, k=total_samples)
    # Extract corresponding values
    selected_values = [random.choice(prefix_dict[key]) for key in selected_keys]
    save_selectprefixes(selected_values)
    # Print the number and proportion of selected prefixes for each key, and save the results to a file
    save_proportion(prefix_dict,sample_counts,total_samples,len(prefixes))
    return selected_values
    #print(selected_prefix)
    #print(sample_counts)

if __name__ == '__main__':
    prefix='2a07:14c0:0000:000b:0001:0000:0000:0001'
    ret=get_asn(prefix)
    print(ret)

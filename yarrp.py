
import os
from log import logger
import concurrent.futures
import tempfile
import time


YARRP_DIR='/home/lihongwei/topo/fish/yarrp/y1/modified_yarrp/yarrp'#Enter the location of yarrp's startup file
INTERFACE_NAME='ens3'
pps=5000
m=16
l=5
def use_yarrp(YARRP_INPUT_DIR: str, YARRP_OUTPUT_DIR:str ):
    cmd = 'sudo %s -i %s -I %s -t ICMP6 -m %d -r %d -o %s -n %d' % (
        YARRP_DIR, YARRP_INPUT_DIR, INTERFACE_NAME, m,pps, YARRP_OUTPUT_DIR,l)
    try:
        os.system(cmd)
    except Exception as e:
        logger.error("Failure in Calling Yarrp: %s", e)


def process_line(line, topology_list):
    if line[0] != '#':
        lst = line.split()
        try:
            target, hop, ttl = lst[0], lst[6], int(lst[5])
        except ValueError:
            return
        except IndexError:
            print(f"Error: list index out of range in line {line}")
            return
        except Exception as e:
            print("Error:", e)
            return
        if hop != target:#Avoid aliases
            if target not in topology_list:
                topology_list[target] = []
            topology_list[target].append([hop, ttl])

def parse_file(file_path):
    topology_list = {}
    packets = 0
    with open(file_path, 'r') as f:
        for line in f:
            process_line(line, topology_list)
            if line.startswith('# Pkts:'):
                packets = int(line.split(':')[1].strip())
    return topology_list, packets

def parse_yarrp_output(YARRP_OUTPUT_DIR) -> tuple:
    num_processes = 8  
    topology_list = {}
    packets = 0

    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = []
        with open(YARRP_OUTPUT_DIR, 'r') as f:
            lines = f.readlines()
            lines_per_process = len(lines) // num_processes

            for i in range(num_processes):
                start_index = i * lines_per_process
                end_index = start_index + lines_per_process
                if i == num_processes - 1:
                    end_index = None

                with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
                    temp_file.writelines(lines[start_index:end_index])
                    temp_file_path = temp_file.name

                future = executor.submit(parse_file, temp_file_path)
                futures.append(future)

        for future in concurrent.futures.as_completed(futures):
            result_topology, result_packets = future.result()
            for target, hops in result_topology.items():
                if target not in topology_list:
                    topology_list[target] = []
                topology_list[target].extend(hops)
            packets += result_packets

    for target in topology_list:
        topology_list[target] = sorted(topology_list[target], key=lambda x: x[1])
    resultlist = list(topology_list.values())
    return resultlist, packets


if __name__ == '__main__':
    YARRP_OUTPUT_DIR="/home/lihongwei/topo/fish/compare/add_generate_thresholds_cover_g2_auto_cor/data/cor_top6_g2_BGP/yarrp_20240206104216.txt"
    # YARRP_INPUT_DIR="/home/lihongwei/tools/6fish/testadd.txt"
    # use_yarrp(YARRP_INPUT_DIR, YARRP_OUTPUT_DIR )
    start_time=time.time()
    ret,packet=parse_yarrp_output(YARRP_OUTPUT_DIR)
    end_time4=time.time()
    elapsed_time4=end_time4-start_time
    print(elapsed_time4)
    # with open("data/output.json", "w") as file:
    #     json.dump(ret, file)

    # with open("data/output.json", "r") as file:
    #     ret_from_file = json.load(file)

    # print(ret_from_file)
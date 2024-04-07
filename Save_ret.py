import time
import pickle
import os
def save_result(result_name,result):
    timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
    result_file = "data/"+result_name+ timestamp +".txt"
    with open(result_file, "w") as file:
        string_result = [str(item) for item in result]
        file.write("\n".join(list(string_result)) + "\n")

def save_lenth_Disasadd(Disasadd,plength):
     timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
     #Write Disadd to file
     Disadd_file="data/Disasadd_"+"prefix_length_"+str(plength)+"_"+timestamp +".txt"
     with open(Disadd_file, "w") as file:
        file.write("\n".join(list(Disasadd)) + "\n")


def save_proportion(prefix_dict,sample_counts,total_samples,lentotalprefixes):
    timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
    output_file="data/proportion"+ timestamp +".txt"
    with open(output_file, "w") as file:
        for key, count in zip(prefix_dict.keys(), sample_counts):
            proportion = count / total_samples
            totalproportion=count/lentotalprefixes
            result = f"Prefix Length: {key},Number of Prefixes Selected: {count},Proportion to total sampling: {proportion:.2%},Proportion of all prefixes:{totalproportion:.2%}"
            file.write(result + "\n")


def save_topolist(ip_lists):
    timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
    totalprefix_file="data/topolist"+ timestamp +".txt"

    # Recursive function, used to convert a list into a string
    def list_to_string(lst, indent=0):
        result = ""
        for item in lst:
            if isinstance(item, list):
                result += list_to_string(item, indent + 1)
            else:
                result += " " * (4 * indent) + str(item) + "\n"
        return result

    # Convert large lists to strings
    output_text = list_to_string(ip_lists)
    with open(totalprefix_file, 'w') as file:
        file.write(output_text)



def read_accumulate_ases(filename):
    ases = set()
    with open(filename, "r") as file:
        for line in file:
            ases.add(line.strip())
    os.remove(filename)
    return ases

def save_accumulate_NASip(NASip):
    timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
    outputfile="data/NASip"+ timestamp +".txt"
    #Write NASip to file
    with open(outputfile, "w") as file:
        file.write("\n".join(list(NASip)) + "\n")
    return outputfile

def read_accumulate_NASip(filename):
    NASip = set()
    with open(filename, "r") as file:
        for line in file:
            NASip.add(line.strip())
    os.remove(filename)
    return NASip

def save_accumulate_Disasadd(Disasadd):
    timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
     #Write Disadd to file
    Disadd_file="data/Disasadd"+ timestamp +".txt"
    with open(Disadd_file, "w") as file:
        file.write("\n".join(list(Disasadd)) + "\n")
    return Disadd_file

def read_accumulate_Disasadd(filename):
    Disasadd = set()
    with open(filename, "r") as file:
        for line in file:
            Disasadd.add(line.strip())
    os.remove(filename)
    return Disasadd

def save_totalhdaa(hdaa):
    timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
    high_density_file="data/high_density_add_area"+ timestamp +".txt"
    with open(high_density_file, "w") as file:
        file.write("\n".join(list(hdaa)) + "\n")
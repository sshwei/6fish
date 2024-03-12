from yarrp import *
import time

def trcacerout(addresslist):
    timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
    # Write the extracted elements to a file
    filenameinput = "data/gnewaddress" + timestamp + ".txt"
    with open(filenameinput, "w") as file:
        for add in addresslist:
            file.write(add + "\n")
    filenameoutput = "data/yarrp_" + timestamp + ".txt"
    use_yarrp(filenameinput, filenameoutput)
    t, p=parse_yarrp_output(filenameoutput)
    return t,p

#First detection
def first_detect(input_file):
    timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
    output_file = "data/yarrphitadd"+timestamp+".txt"
    use_yarrp(input_file, output_file)
    resultlist, packet = parse_yarrp_output(output_file)
    return resultlist,packet
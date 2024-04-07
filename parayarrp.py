# This script can parse multiple yarrp files
from yarrp_alladd import *
from Save_ret import *
from Extract_prefix import *


Discoveradd=set()
ases=set() 

def operate_yarrp_file(directory):
    files = os.listdir(directory) 
    yarrp_files = [file for file in files if file.startswith("yarrp")] 
    for file in yarrp_files:
        file_path = os.path.join(directory, file)
        tmp1=set()
        as1=set()
        resultlist, p=parse_yarrp_output(file_path)
        for ip_list in resultlist:
            for ip_entry in ip_list:
                ip = ip_entry[0]
                tas=get_asn(ip)
                if tas  and tas not in ases:
                    as1.add(tas)
                    ases.add(tas)
                if ip not in Discoveradd:
                    tmp1.add(ip)
                    Discoveradd.add(ip)
    result_name='Alldisadd'
    save_result(result_name,Discoveradd)
 
if __name__ == '__main__':
    directory_path = "" #Enter the yarrp file directory
    operate_yarrp_file(directory_path)







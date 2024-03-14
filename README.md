TopoMiner is an efficient and simple method for IPv6 topology probing
As a first step, please install pyasn and yarrp in python 3.8 or higher. Of course if you use other probing tools you can also modify the code to adapt to the new probing tools.
For yarrp installation see: https://github.com/cmand/yarrp.git
For pyasn installation, please refer to: https://github.com/hadiasghari/pyasn.git

After the above tools are installed, you need to add the absolute path of the pyasn library to asndb = pyasn.pyasn() in Extract_prefix.py. 
Also you need to add the absolute path of yarrp to YARRP_DIR in yarrp.py and yarrp_alladd.py (must have yarrp at the end)

After that, it's just a matter of setting up the parameters in main.py to suit your needs. You can add target prefixes, target addresses.
You can set the standard value of the high density area, the detection budget, and so on.

For example, the total_budget distribution budget can be set to 1M.
Granularity is the bit of prefix expansion, which can be set to 1 or larger.
bigbuket and buketvol default to 0.
cor is the expansion bounds of prefix expansion, the default setting is [32,64], and it will be adjusted automatically after that.
thresholds is the yield of each type of prefix discovery address. 
It can be set according to the actual situation, but not too large. It is between 0-1. The default is 2%.

Once the above is set up, you just need to run main.py.


After the run is done, there will be many yarrp files, you can use parayarrp.py to parse out all the ip addresses found. This of course includes the alias addresses. If you want to avoid most of the aliases, you don't need to parse the yarrp files. The address file is automatically output after main.py finishes running.

# About

Automation scipts for Juniper JNCIE-SP Bootcamp 12a labs.


Custom lab environment is used: single Linux/KVM server with six vMX virtual machines connected through Linux bridges. 
Requirements: 36+ GBytes of RAM, 32+ logical vCPUs (hyper-threading enabled)
 
Only vMX virtual machines' configs are provided. __JunOS configs are not provided as they are Juniper's intellectual property__ - get them from the bootcamp package (from Juniper). 


# Usage

1. Clone the repository
2. __Modify config.yml__ to reflect your environment and location of JunOS configs
3. Install dependencies 
4. Change directory to where \_\_main__.py is located
5. Execute the directory

```
git clone https://github.com/sgrade/junspbootcamp.git
nano config.yml
pip3 install -r requirements.txt
cd junspbootcamp
python3 .
```

Note: "python3 ." is the same as "python3 \_\_main__.py" 

Note: Last vMX version have a bug influencing behavior of R4 and vrdevice (nodes with 12+ interfaces). 
It binds ge-0/0/12 to correct bridge, but traffic goes to virbr0 instead of this bridge.  
Tested with vMX up to 18.2
This is why I used vMX 17.2 for R4 and vrdevice

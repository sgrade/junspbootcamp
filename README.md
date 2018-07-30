# About

Automation scipts for Juniper JNCIE-SP Bootcamp 12a labs.


Custom lab environment is used: single Linux/KVM server with six vMX virtual machines connected through Linux bridges.
 
Only vMX virtual machines' configs are provided. __JunOS configs are not provided as they are Juniper's intellectual property__ - get them from the bootcamp package (from Juniper). 


# Usage

1. Clone the repository
2. __Modify config.yml__ to reflect your environment and location of JunOS configs 
3. Change directory to where \_\_main__.py is located
4. Execute the directory

```
git clone https://github.com/sgrade/junspbootcamp.git
cd junspbootcamp    
python3 .
```

Note: "python3 ." is the same as "python3 \_\_main__.py" 
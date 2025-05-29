# Batfish  
Batfish is an open source tool for analyzing the network configuration. In addition, you can also check access lists or firewall rules by telling Batfish a source and destination network and it checks the rules based on this information.

## Installation 

First it is recommended to use the following directory structure:

```bash
├── Batfish
│   ├── main.py
│   ├── output
│   │   └── results_sw1.csv
│   ├── snapshots
│   │   └── configs
│   │       └── sw1.cfg
│   └── venv
│       ├── bin
│       ├── include
│       ├── lib
│       └── pyvenv.cfg
```

One of the following folders must exist in the snapshot directory, otherwise Batfish cannot work. Each folder has a different use case:  

- **configs/**: For most physical devices such as Cisco, Juniper, Arista etc.  
- **aws_configs/**: For AWS VPC configurations.  
- **sonic_configs/**: For SONiC-Geräte.  
- **hosts/**: For host models with iptables configurations.

Next step after building the directory structure, download the Docker image:

```bash
docker pull batfish/allinone
```

Then starting the Docker container:

```bash
docker run --name batfish -v batfish-data:/data -p 8888:8888 -p 9996:9996 -p 9997:9997 batfish/allinone
```

Create a Python virtual environment, as recommended when using Batfish:

```bash
python3 -m venv path/to/venv
```

Activate the virtual environment:

```bash
source path/to/venv/bin/activate
```

Install the required Python library for the use of Batfish:

```bash
python3 -m pip install pybatfish
```

If necessary, install setuptools:

```bash
python3 -m pip install setuptools
```

The following script can be used as `main.py`. The question is given here bf.q.'question' this can vary as explained in the section [Possibilities with the question module](#Possibilities-with-the-question-module):

```python
#!/usr/bin/env python

# Modules
from pybatfish.client.session import Session
import os

# Initialize Batfish session
bf = Session()

# Variables
bf_address = "127.0.0.1"
snapshot_path = "/Users/jan/Documents/Batfish/snapshots"
output_dir = "/Users/jan/Documents/Batfish/output"

# Body
if __name__ == "__main__":
    # Setting host to connect (e.g., localhost Batfish service)
    bf.host = bf_address

    # Set network and initialize snapshot
    bf.set_network("home_network")
    bf.init_snapshot(snapshot_path, name="home_snapshot", overwrite=True)

    # Run a question (e.g., node properties)
    r = bf.q.nodeProperties().answer().frame()
    node = (r['Node'][0])

    # Save output to CSV
    if not os.path.exists(output_dir):
        print("Output file could not be stored:")
        print(f"File path {output_dir} does not exist")
        exit()

    r.to_csv(os.path.join(output_dir, f"results_{node}.csv"))
```

The script must then be executed in the virtual environment, which means first activating the “venv” and then executing the Python script:

``` Bash
python3 main.py
```

After executing the script, a .csv file is created which is then located in the “output” folder.

## Possibilities with the question module

The questions are a way to interact with Batfish so that it can validate the configuration. It is possible to ask Batfish different “questions”, an overview can be found here:

https://batfish.readthedocs.io/en/latest/questions.html

In the menu item “Access-lists and firewall rules” the question “Test Filters” can be found. With this question it is possible to give the Python script a source and destination network with the corresponding ports and Batfish checks the ACL contained in the config for a match, so with longer ACLs it can be checked quickly and easily whether the traffic is allowed or forbidden.

## Keep everything up to date

To keep everything up to date, the following must be done:

```bash
source venv/bin/activate
python3 -m pip install --upgrade pybatfish
python3 -m pip install --upgrade setuptools
```

To update the docker container the following is necessary: 

```bash
docker stop batfish
docker rm batfish
docker pull batfish/allinone
docker run --name batfish -v batfish-data:/data -p 8888:8888 -p 9996:9996 -p 9997:9997 batfish/allinone
```


Now have fun trying out and automating your network.
Your welcome to clone this Git repo so that the necessary folder structure is already available, only the venv has to be created in the main directory. 

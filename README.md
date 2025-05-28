# Batfish  
Batfish ist ein Netzwerkanalyse-Tool, das sehr nützlich sein kann, um unter anderem Access-Listen zu prüfen oder Konfigurationen zu validieren.

## Installation  
Zuerst erstellen wir ein Python-virtuelles Environment, wie es bei der Verwendung von Batfish empfohlen wird:

```bash
python3 -m venv path/to/venv
```

Dann das Docker-Image herunterladen:

```bash
docker pull batfish/allinone
```

Das Image starten:

```bash
docker run --name batfish -v batfish-data:/data -p 8888:8888 -p 9996:9996 -p 9997:9997 batfish/allinone
```

Es wird empfohlen, folgende Verzeichnisstruktur zu verwenden:

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

Einer der folgenden Ordner muss im Snapshot-Verzeichnis existieren, sonst kann Batfish nicht arbeiten:  

- **configs/**: Für die meisten physischen Geräte wie Cisco, Juniper, Arista usw.  
- **aws_configs/**: Für AWS VPC-Konfigurationen.  
- **sonic_configs/**: Für SONiC-Geräte.  
- **hosts/**: Für Host-Modelle mit iptables-Konfigurationen.

Das virtuelle Environment aktivieren:

```bash
source venv/bin/activate
```

Die benötigte Python-Bibliothek installieren:

```bash
python3 -m pip install --upgrade pybatfish
```

Falls notwendig, setuptools installieren oder aktualisieren:

```bash
python3 -m pip install --upgrade setuptools
```

Als `main.py` kann folgendes Skript verwendet werden:

```python
#!/usr/bin/env python3

from pybatfish.client.session import Session
import os

# Initialize Batfish session
bf = Session()

# Variables
bf_address = "127.0.0.1"
snapshot_path = "/path/to/snapshot/Batfish/snapshots"
output_dir = "/path/to/output/Batfish/output"

if __name__ == "__main__":
    # Setting host to connect
    bf.host = bf_address

    # Set network and initialize snapshot
    bf.set_network("network")
    bf.init_snapshot(snapshot_path, name="snapshot", overwrite=True)

    # Run a question
    r = bf.q.nodeProperties().answer().frame()
    print(r)
    node = r['Node'][0]
    print(node)

    # Save output to CSV
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    r.to_csv(os.path.join(output_dir, f"results_{node}.csv"))
```



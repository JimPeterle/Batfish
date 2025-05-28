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
    print(r)
    node = (r['Node'][0])
    print (node)

    # Save output to CSV
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    r.to_csv(os.path.join(output_dir, f"results_{node}.csv"))

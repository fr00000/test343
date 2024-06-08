#!/bin/bash

# Command to start the kuzco worker
START_COMMAND="python3 sd-miner-v1.3.0.py --exclude-sdxl"

# Function to start the kuzco worker, wait 5 minutes, then restart
start_and_restart() {
  while true; do
    # Start the kuzco worker in the background
    $START_COMMAND &
    # Save the PID of the kuzco worker
    KUZCO_PID=$!

    # Wait for 5 minutes (300 seconds)
    sleep 3600

    # Kill the kuzco worker process
    kill $KUZCO_PID
    # Wait for the process to terminate
    wait $KUZCO_PID

    # The loop will now restart, running the kuzco worker again
  done
}

# Start the monitoring and restarting loop
start_and_restart

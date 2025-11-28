#!/bin/bash

# Start the scheduler in the background
python scripts/scheduler.py &
SCHEDULER_PID=$!

# Start the web application
gunicorn --bind 0.0.0.0:5000 backend.app:app

# If the web application exits, kill the scheduler
kill $SCHEDULER_PID
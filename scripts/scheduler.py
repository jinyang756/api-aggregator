from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess
import os
from datetime import datetime

def run_data_collector():
    print(f"Running data collector at {datetime.now()}")
    
    # Change to the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    try:
        # Run the data collector script
        result = subprocess.run(['python', 'data_collector.py'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Data collector ran successfully")
            print(result.stdout)
        else:
            print("Data collector failed")
            print(f"Error: {result.stderr}")
            
    except Exception as e:
        print(f"Error running data collector: {e}")

def main():
    print("Starting scheduler...")
    
    scheduler = BlockingScheduler()
    
    # Schedule the data collector to run daily at 2 AM
    scheduler.add_job(run_data_collector, 'cron', hour=2)
    
    # Also run it immediately when the scheduler starts
    scheduler.add_job(run_data_collector, 'date', run_date=datetime.now())
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler stopped")

if __name__ == "__main__":
    main()
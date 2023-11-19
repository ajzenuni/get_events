import sys
from winevt import EventLog
from datetime import datetime

def get_last_runs(task_name, num_events):
    # Event Log Query to find events with the task_name and Task Category=Task Completed(Task=102 & Level=4)
    query_xml = f'''
    *[System[Provider[@Name='Microsoft-Windows-TaskScheduler'] and (Level=4) and (Task = 102)]]
    and
    *[EventData[Data[@Name='TaskName']='\{task_name}']]
    '''

    query = EventLog.Query("Microsoft-Windows-TaskScheduler/Operational",query_xml,"backward")
    
    x = 0
    for event in query:
        if(x >= num_events):
            break
        # Convert the 'SystemTime' string to a datetime object with the correct format
        system_time_datetime = datetime.fromisoformat(event.System.TimeCreated['SystemTime'])

        # Print the datetime object in the desired format
        print(system_time_datetime.strftime("%Y-%m-%d %H:%M:%S"))
        x += 1

    if(x == 0):
        print(f"No events found. Check the task scheduler that your task: {task_name} was scheduled.")
        
def main():
    # handle incorrect num of arguments
    if len(sys.argv) != 3:
        print("Usage: python script.py task_name num_events")
        sys.exit(1)
    task_name = sys.argv[1]

    # handle invalid and negative int
    try:
        num_events = int(sys.argv[2])
        if(num_events <= 0):
            print("The number of events argument was less than or equal to 0.")
            sys.exit(1)
    except (ValueError, TypeError):
        print("The number of events argument was not a integer. Please submit a valid integer like 0,1,2,3,4.")
        sys.exit(1)

    get_last_runs(task_name, num_events)

if __name__ == "__main__":
    main()
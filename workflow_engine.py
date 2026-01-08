import json
import os
import sys
import traceback
import io
import contextlib

def log(message):
    print(f"[LOG] {message}")

def execute_workflow(wf):
    name = wf.get('name', 'Untitled')
    script = wf.get('script', '')
    
    if not script.strip():
        log(f"Skipping {name}: No script content")
        return

    log(f"--- Running Workflow: {name} ---")
    
    # Capture stdout specifically for this script execution if needed, 
    # but currently we pipe global stdout to log.txt, so print() works fine.
    
    # We define a global context for the script
    # We allow imports inside the script to work naturally
    
    try:
        # Execute the script
        # Pass minimal globals. User scripts should import what they need.
        exec(script, {'__name__': '__main__'})
    except Exception as e:
        log(f"Error running workflow {name}: {e}")
        traceback.print_exc()
        
    log(f"--- Workflow Finished ---")

def main():
    try:
        with open('workflows.json', 'r', encoding='utf-8') as f:
            workflows = json.load(f)
    except FileNotFoundError:
        log("No workflows.json found.")
        return

    # Get current event name (schedule or workflow_dispatch)
    event_name = os.environ.get('EVENT_NAME', 'unknown')
    log(f"Triggered by event: {event_name}")

    for wf in workflows:
        if not wf.get('enabled', True):
            continue
        
        # Check explicit trigger settings
        run_on_schedule = wf.get('run_on_schedule', True)
        run_on_dispatch = wf.get('run_on_dispatch', True)

        if event_name == 'schedule' and not run_on_schedule:
            log(f"Skipping {wf.get('name')} (Disabled for schedule)")
            continue
        
        if event_name == 'workflow_dispatch' and not run_on_dispatch:
            log(f"Skipping {wf.get('name')} (Disabled for manual dispatch)")
            continue
            
        execute_workflow(wf)

if __name__ == "__main__":
    main()

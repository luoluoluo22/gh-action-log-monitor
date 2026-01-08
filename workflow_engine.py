import json
import requests
import time
import sys

# Global variables storage
VARIABLES = {}

def log(message):
    print(f"[LOG] {message}")

def execute_step(step):
    step_type = step.get('type')
    
    if step_type == 'log':
        # 支持变量替换，例如 "Title: {story_title}"
        msg = step.get('message', '')
        try:
            # 使用 eval 的 f-string 机制这里比较危险，我们用简单的 format 
            # 但为了支持 complex object indexing (如 {story[title]}), 我们需要更聪明的 render
            formatted_msg = msg.format(**VARIABLES)
        except Exception:
            # Fallback for complex types or keys missing
            # A simple hacky regex replace could be better for production, but let's try strict format first
            # If fail, print raw
            formatted_msg = msg
        
        log(formatted_msg)

    elif step_type == 'http':
        url = step.get('url').format(**VARIABLES) # simple url params injection
        method = step.get('method', 'GET')
        output_var = step.get('output_var')
        
        log(f"HTTP {method} {url}")
        try:
            resp = requests.request(method, url, timeout=10)
            if resp.status_code < 400:
                data = resp.json()
                if output_var:
                    VARIABLES[output_var] = data
            else:
                log(f"Error: HTTP {resp.status_code}")
        except Exception as e:
            log(f"Request Failed: {e}")

    elif step_type == 'python':
        code = step.get('code', '')
        # Allow python code to access 'vars' (VARIABLES) and 'log' function
        local_context = {"vars": VARIABLES, "log": log}
        try:
            exec(code, {}, local_context)
        except Exception as e:
            log(f"Python Execution Error: {e}")

    elif step_type == 'delay':
        seconds = step.get('seconds', 1)
        log(f"Sleeping for {seconds}s...")
        time.sleep(seconds)
        
    elif step_type == 'loop':
        items_key = step.get('items_from_var')
        loop_var_name = step.get('loop_var', 'item')
        sub_steps = step.get('steps', [])
        
        items = VARIABLES.get(items_key, [])
        if not isinstance(items, list):
            log(f"Error: {items_key} is not a list")
            return

        for item in items:
            VARIABLES[loop_var_name] = item
            for sub_step in sub_steps:
                execute_step(sub_step)

def main():
    try:
        with open('workflows.json', 'r', encoding='utf-8') as f:
            workflows = json.load(f)
    except FileNotFoundError:
        log("No workflows.json found.")
        return

    for wf in workflows:
        if not wf.get('enabled', True):
            continue
            
        log(f"--- Running Workflow: {wf.get('name')} ---")
        steps = wf.get('steps', [])
        try:
            for step in steps:
                execute_step(step)
        except Exception as e:
            log(f"Error running workflow {wf.get('name')}: {e}")
        log(f"--- Workflow Finished ---")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import argparse
import itertools
import subprocess
import sys

def list_tasks(args=None):
    """
    List all tasks 
    """
    try:
        print("\n3isec Qubes Tasks:")
        available_cmd = ['sudo', 'qubes-dom0-update', '--action=list', '3isec-qubes*']
        available_result = subprocess.run(available_cmd, capture_output=True, text=True)
        if available_result.returncode == 0:
            if available_result.stdout.strip():
                print(available_result.stdout)
            else:
                print("No available tasks")
        else:
          print(f"Error listing tasks: {result.stderr}", file=sys.stderr)
    except Exception as e:
        print(f"Failed to list tasks: {e}", file=sys.stderr)
        sys.exit(1)
    
def task_info(package):
    """
    Retrieve information about task
    """
    try:
        cmd = ['rpm','-qi',package]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            summary = ''
            description = ''
            for line in lines:
                if line.startswith('Summary'):
                    summary = line.split(':', 1)[1].strip()
                elif line.startswith('Description'):
                    description_lines = []
                    for description_line in lines[lines.index(line)+1:]:
                        description_lines.append(description_line.strip())
                    description = '\n '.join(
                        line for line, group in itertools.groupby(description_lines)
                        if line or group
                    )

            if summary:
                print(f"Summary: {summary}")
            if description:
                print(f"Description: {description}")
        else:
            print("No information")
    except Exception as e:
        print(f"Failed to get information: {e}", file=sys.stderr)
    sys.exit(1)

def task_install(package):   
    try:
        cmd = ['sudo', 'qubes-dom0-update', '--quiet', '--assumeyes', '--allowerasing', package]
        print(f"Installing package: {package}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Succesfully installed package: {package}")
        else:
            print(f"""Something went wrong trying to install package: {package}
Check to see if the package was in fact installed.""")
    except Exception as e:
        print(f"Failed to install package {e}", file=sys.stderr)
        sys.exit(1)
        

def main():
    parser = argparse.ArgumentParser(description='3isec Qubes Task Management',
    usage='''qubes-task <command>

    Commands:
        list    List 3isec-qubes packages
        info    Get detailed information about a 3isec-qubes package
        install Install a 3isec-qubes package
    ''')

    parser.add_argument('command', choices=['list', 'info', 'install'])
    #parser.add_argument('command', nargs='?', choices=['list', 'info'])
    parser.add_argument('package', type=str, nargs='?', help='Name of package')
    args = parser.parse_args()
    
    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    if args.command == 'list':
        list_tasks(args)
    elif args.command == 'info':
        task_info(args.package)
    elif args.command == 'install':
        task_install(args.package)

if __name__ == '__main__':
    main() 

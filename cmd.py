"""
Send command to BK9000 Daemon

Usage:
  python cmd.py on 0
  python cmd.py off 0
  python cmd.py on 0,1,2,3
  python cmd.py all on
  python cmd.py all off
  python cmd.py test
  python cmd.py status
"""
import sys

COMMAND_FILE = "commands.txt"

if len(sys.argv) < 2:
    print(__doc__)
else:
    cmd = " ".join(sys.argv[1:])
    with open(COMMAND_FILE, 'w') as f:
        f.write(cmd + "\n")
    print(f"Sent: {cmd}")

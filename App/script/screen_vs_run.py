import subprocess
import time

subprocess.run(['pkill', 'screen', '-9'])
subprocess.run(['screen', '-wipe'])
subprocess.run(['screen', '-S', 'vs', '-dm', 'bash', '-c', './velocitysniper'])
time.sleep(1.1)
subprocess.run(['screen', '-ls'])
print('Done.')

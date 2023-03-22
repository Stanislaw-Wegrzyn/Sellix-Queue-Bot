from imports import *

def rerun_sniper(host: str, user: str, password: str, token: str):
    # CREATING CONNECTION:
    transport = paramiko.Transport(host)
    transport.connect(username= user, password= password)

    sftp = paramiko.SFTPClient.from_transport(transport)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.load_system_host_keys()
    ssh.connect(host, 22, user, password)

    def run_comm_out(comm: str):
        _, stdout, sterr = ssh.exec_command(comm)
        return str(stdout.read() + sterr.read()).replace("b'", '').replace("'", '').replace('\\t', '    ').replace('\\r',' ').split('\\n')

    # DOWNLOADING config.toml
    filepath = 'config.toml'
    localpath = '../items/ssh/sniper.txt'
    sftp.get(filepath, localpath)

    # REMAKING config.toml
    config_f = open('../items/ssh/sniper.txt', 'r')
    list_of_lines = config_f.readlines()
    old_token_in_config = list_of_lines[1].split('mainToken = "')[1].split('"\n')[0]  # VER FOR LOGGER
    list_of_lines[1] = 'mainToken = "' + token + '"\n'

    config_f = open('../items/ssh/sniper.txt', 'w')
    config_f.writelines(list_of_lines)
    config_f.close()

    # UPLOADING BACK
    sftp.put(localpath, filepath)

    # UPLOADING screen_vs_run.py
    sftp.put('screen_vs_run.py', 'screen_vs_run.py')

    # RERUNNING velocitysniper
    out = run_comm_out('python3 screen_vs_run.py')
    while run_comm_out('python3 screen_vs_run.py')[-2] != 'Done.':
        out = run_comm_out('python3 screen_vs_run.py')

    # CLOSING CONNECTIONS
    ssh.close()
    sftp.close()
    transport.close()


def stop_sniper(host: str, user: str, password: str):
    # CREATING CONNECTION:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.load_system_host_keys()
    ssh.connect(host, 22, user, password, banner_timeout=150)

    # STOPPING velocitysniper
    ssh.exec_command('pkill screen -9')
    ssh.exec_command('screen -wipe')

    # CLOSING CONNECTIONS
    ssh.close()

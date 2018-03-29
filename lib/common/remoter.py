# coding=utf-8
# copy files from local machine to remote machine
# author: zengyuetian

import paramiko


SSH_PORT = 22


def copy_file_to(remote_ip, user, passwd, local_file_path, remote_file_path):
    ssh = paramiko.Transport(remote_ip, SSH_PORT)
    ssh.connect(username=user, password=passwd)
    sftp = paramiko.SFTPClient.from_transport(ssh)
    print "{0} Local file:".format("127.0.0.1"), local_file_path
    print "{0} Remote file:".format(remote_ip), remote_file_path
    sftp.put(local_file_path, remote_file_path)
    sftp.close()
    ssh.close()


def copy_file_from(remote_ip, user, passwd, remote_file_path, local_file_path):
    ssh = paramiko.Transport(remote_ip, SSH_PORT)
    ssh.connect(username=user, password=passwd)
    sftp = paramiko.SFTPClient.from_transport(ssh)
    print "{0} Local file:".format("127.0.0.1"), local_file_path
    print "{0} Remote file:".format(remote_ip), remote_file_path
    sftp.get(remote_file_path, local_file_path)
    sftp.close()
    ssh.close()


def remote_execute(remote_ip, user, passwd, cmd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(remote_ip, SSH_PORT, user, passwd)
    print "{0} run command :".format(remote_ip), cmd
    ssh.exec_command(cmd)
    ssh.close()


def remote_execute_result(remote_ip, user, passwd, cmd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(remote_ip, SSH_PORT, user, passwd)
    print "{0} run command :".format(remote_ip), cmd
    stdin, stdout, stderr = ssh.exec_command(cmd)
    result = stdout.read().strip()
    # print "Result:", result
    ssh.close()
    return result


def remote_execute_stderr(remote_ip, user, passwd, cmd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(remote_ip, SSH_PORT, user, passwd)
    print "{0} run command :".format(remote_ip), cmd
    stdin, stdout, stderr = ssh.exec_command(cmd)
    result = stderr.read().strip()
    # print "Result:", result
    ssh.close()
    return result

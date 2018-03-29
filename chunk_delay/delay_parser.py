import os

from chunk_delay.collector import get_latest_packet_jitter
from chunk_delay.const import *


def delay_parser(mode):
    client_timestamp = get_latest_packet_jitter(CLIENT_HOST)
    server_timestamp = get_latest_packet_jitter(SERVER_HOST)
    client_file_name = '/' + mode + '_client' + '_packet_jitter-' + client_timestamp
    server_file_name = '/' + mode + '_server' + '_packet_jitter-' + server_timestamp
    delay_file_name = '/' + mode + '_delay-' + server_timestamp
    client_local_file_name = LOCAL_RESULT_PATH + client_file_name
    server_local_file_name = LOCAL_RESULT_PATH + server_file_name
    local_delay_file = LOCAL_RESULT_PATH + delay_file_name

    client_dict = {}
    server_dict = {}

    with open(client_local_file_name, 'r') as reader:
        client_lines = reader.readlines()

    with open(server_local_file_name, 'r') as reader:
        server_lines = reader.readlines()

    for server_line in server_lines:
        if server_line.startswith('SEND-TIME'):
            continue
        server_chunk_id, start_timestamp = server_line.strip('\n').split(': ')
        client_dict[int(server_chunk_id)] = long(start_timestamp)

    print client_lines
    for client_line in client_lines:
        if client_line.startswith('SEND-TIME'):
            continue
        client_chunk_id, timestamps = client_line.strip('\n').split(': ')
        end_timestamp = timestamps.split('   ')[-1]
        server_dict[int(client_chunk_id)] = long(end_timestamp)

    with open(local_delay_file, 'w') as writer:
        chunk_ids = sorted(client_dict.keys())

        for chunk_id in chunk_ids:
            delay = server_dict[chunk_id] - client_dict[chunk_id]
            print chunk_id, delay
            writer.write(str(chunk_id) + ', ' + str(delay) + '\n')


def delay_classifier():
    dc = dict()
    for [root_path, dirs, files] in os.walk(LOCAL_RESULT_PATH):
        for f in files:
            if 'delay' in f:
                file_name = root_path + '/' + f
                with open(file_name, 'r') as reader:
                    lines = reader.readlines()
                    for line in lines:
                        delay = int(line.strip('\n').split(', ')[-1])
                        if delay not in dc:
                            dc[delay] = 1
                        else:
                            dc[delay] += 1
                file_name = file_name.replace('delay', 'classification')
                with open(file_name, 'w') as writer:
                    keys = sorted(dc.keys())
                    for k in keys:
                        # print k, dc[k]
                        writer.write(str(k) + ', ' + str(dc[k]) + '\n')


if __name__ == '__main__':
    # delay_parser('tcp')
    delay_parser('rush')
    delay_classifier()

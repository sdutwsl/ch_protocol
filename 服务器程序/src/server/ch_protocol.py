import struct

Type = {
    'end': 0b00000001,
    'lg': 0b00000010,
    'msg': 0b00000100,
    'dwnf': 0b00001000,
    'sendf': 0b00010000,
    'rgs':32,
    1: 'end',
    2: 'lg',
    4: 'msg',
    8: 'dwnf',
    16: 'sendf',
    32:'rgs'
}


def dump(data):
    print(data)
    packed_data = bytearray()
    packed_data += struct.pack('B', Type[data['type']])
    cnt_flag = bytearray(7)
    cnt = bytearray()

    if 'cnt' in data:
        if 'ur' in data['cnt']:
            cnt_flag[0] = len(data['cnt']['ur'])
            cnt += data['cnt']['ur'].encode('ascii')
        if 'pw' in data['cnt']:
            cnt_flag[1] = len(data['cnt']['pw'])
            cnt += data['cnt']['pw'].encode('ascii')
        if 'msg' in data['cnt']:
            cnt_flag[2] = len(data['cnt']['msg'].encode('utf8'))
            cnt += data['cnt']['msg'].encode('utf8')
        if 'fname' in data['cnt']:
            cnt_flag[3] = len(data['cnt']['fname'].encode('utf8'))
            cnt += data['cnt']['fname'].encode('utf8')
        if 'result' in data['cnt']:
            if data['cnt']['result']:
                cnt_flag[4] = 0
            else:
                cnt_flag[4] = 1
        if 'flist' in data['cnt']:
            fb = bytearray()
            for f in data['cnt']['flist']:
                fb += f.encode('utf8')
                fb.append(0)
            len_list = len(fb)
            cnt_flag[5:] = struct.pack('H', len_list)
            cnt += fb
        if 'fmd5' in data['cnt']:
            cnt += struct.pack('b', 1)
            cnt += data['cnt']['fmd5'].encode('ascii')
        if 'fsize' in data['cnt']:
            cnt += struct.pack('b', 2)
            cnt += struct.pack('Q', data['cnt']['fsize'])
        if 'path' in data['cnt']:
            cnt += data['cnt']['path'].encode('utf8')


    packed_data += cnt_flag
    packed_data += cnt
    return bytes(packed_data)

def parse(data):
    parse_result = {}
    type = data[0]
    parse_result['type'] = Type[type]
    parse_result['cnt'] = {}
    cnt_flag = data[1:1 + 7]

    analog = 8

    if cnt_flag[0]:
        parse_result['cnt']['ur'] = data[analog:analog + cnt_flag[0]].decode('ascii')
        analog = analog + cnt_flag[0]
    if cnt_flag[1]:
        parse_result['cnt']['pw'] = data[analog:analog + cnt_flag[1]].decode('ascii')
        analog += cnt_flag[1]
    if cnt_flag[2]:
        parse_result['cnt']['msg'] = data[analog:analog + cnt_flag[2]].decode('utf8')
        analog += cnt_flag[2]
    if cnt_flag[3]:
        parse_result['cnt']['fname'] = data[analog:analog + cnt_flag[3]].decode('utf8')
        analog += cnt_flag[3]

    if cnt_flag[4]:
        parse_result['cnt']['result'] = False
    else:
        parse_result['cnt']['result'] = True

    if cnt_flag[5] or cnt_flag[6]:
        len_list = struct.unpack('H', cnt_flag[5:])[0]
        flist = data[analog: analog + len_list]
        parse_result['cnt']['flist'] = []
        i, j = 0, 0
        for f in flist:
            if f == 0:
                parse_result['cnt']['flist'].append(flist[j:i].decode('utf8'))
                j = i + 1
            i += 1
        analog += len_list

    if analog < len(data) and data[analog] == 1:
        analog += 1
        parse_result['cnt']['fmd5'] = data[analog: analog + 32].decode('ascii')
        analog += 32

    if analog < len(data) and data[analog] == 2:
        analog += 1
        parse_result['cnt']['fsize'] = struct.unpack('Q', data[analog: analog + 8])[0]
        analog += 8

    if len(data) - analog >= 1:
        parse_result['cnt']['path'] = data[analog:].decode('utf8')
    print(parse_result)
    return parse_result


if __name__ == '__main__':
    data = {'type': 'dwnf', 'cnt': {'ur': 'as', 'path': 'C:/Users/Administrator/PycharmProjects/crosswire/client/client_files', 'fname': 'dd'}}
    bs = dump(data)
    dic = parse(bs)
    print(dic)

class FLVFileHeader:
    """
    parse FLV File Header:
    signature: 3 bytes, usually "FLV"
    version: 1 byte, 'abcdefgh'  h == 1 means video, f == 1 means audio, g and e must be 0.
    flags: 1 byte,
    header_size: 4 bytes, usually 9 bytes;
    """
    def __init__(self):
        self.signature = ''
        self.version = ''
        self.flags = ''
        self.header_size = ''

    def set_header(self, data):
        self.signature = data[0:3]
        self.version = data[3]
        self.flags = data[4]
        self.header_size = data[5:9]


class FLVTagHeader:
    """
    parse FLV Tag Header
    type:   1 byte    8: audio    9:video     18:script
    data_size: 3 bytes
    time_stamp: 3 bytes  integer    ms; will be 0 if type == 18
    time_stamp_ex:  1 byte  expand time_stamp to 4 bytes
    stream_id: 3 bytes    always 0
    """
    def __int__(self):
        self.type = ''
        self.data_size = ''
        self.time_stamp = ''
        self.time_stamp_ex = ''
        self.stream_id = ''
        self.pos = 0
        self.encode_id = 0
        self.is_key = False

    def set_header(self, data, read_pos):
        self.type = ord(data[0])
        self.data_size = data[1:4]
        self.time_stamp = data[4:7]
        self.time_stamp_ex = data[7]
        self.stream_id = data[8:11]
        self.pos = read_pos

    def set_tag_format(self, data):
        if self.type == 8:
            self.encode_id = (ord(data[0]) & 0xF0) >> 4
        elif self.type == 9:
            self.encode_id = ord(data[0]) & 0x0F
            if 1 == (ord(data[0]) & 0xF0) >> 4:
                self.is_key = True
            else:
                self.is_key = False

    def get_data_size(self):
        return self.get_data_size_impl(self.data_size, 3)

    def get_tag_time(self):
        tag_time = self.get_data_size_impl(self.time_stamp, 3)
        tag_time = ord(self.time_stamp_ex) * 16777216 + tag_time
        return tag_time

    def get_data_size_impl(self, data, end):
        data_size = 0
        for i in range(0, end):
            data_size = data_size * 256 + ord(data[i])
        return data_size

    def is_video_tag(self):
        if ord(self.type) == 9:
            return True
        return False


class FLVParse(object):
    """
    parse FLV File tag data
    """

    def __init__(self):
        self.file_header = FLVFileHeader()
        self.tag_header = FLVTagHeader()
        self.state = 0
        self.buffer = ''
        self.pos = 0

    def parse(self, data, on_tag_callback=None):
        self.buffer = ''.join([self.buffer, data])
        # print ("state:", self.state)
        # print ("length:", len(self.buffer))
        while True:
            # file header(9) + pre_tag_size0 (4)
            if self.state == 0:
                if len(self.buffer) >= 13:
                    # print 'flv header', self.pos
                    self.file_header.set_header(self.buffer)
                    self.state = 1
                    self.buffer = self.buffer[13:]
                    self.pos += 13
                else:
                    break
            # tag header
            elif self.state == 1:
                if len(self.buffer) >= 11:
                    # print 'tag header', self.pos
                    self.tag_header.set_header(self.buffer, self.pos)
                    self.state = 2
                    self.buffer = self.buffer[11:]
                    self.pos += 11
                else:
                    break
            # data
            elif self.state == 2:
                # print 'data', self.tag_header.get_data_size()
                if len(self.buffer) >= self.tag_header.get_data_size():
                    # print 'data', self.pos, self.tag_header.get_data_size()
                    self.state = 3
                    self.tag_header.set_tag_format(self.buffer)
                    self.buffer = self.buffer[self.tag_header.get_data_size():]
                    self.pos += self.tag_header.get_data_size()
                else:
                    break
            # pre tag size
            elif self.state == 3:
                if len(self.buffer) >= 4:
                    # print 'pre tag size', self.pos
                    self.state = 1
                    self.buffer = self.buffer[4:]
                    self.pos += 4
                    if on_tag_callback and callable(on_tag_callback):
                        on_tag_callback(self.tag_header.pos, self.tag_header.get_tag_time(),
                                        self.tag_header.type, self.tag_header.get_data_size() + 15)
                else:
                    break

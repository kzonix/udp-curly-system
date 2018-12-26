import msgpack
from io import BytesIO

buf = BytesIO()
for i in range(2):
   buf.write(msgpack.packb(i, use_bin_type=True))

buf.seek(0)

unpacker = msgpack.Unpacker(buf, raw=False)
for unpacked in unpacker:
    print(unpacked)


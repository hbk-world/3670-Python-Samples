#Copyright (c) 2019 Thomas Weiss
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import sounddevice as sd
import sys
import soundfile as sf 
from queue import Queue

BLOCKSIZE = 1024

#print(sd.query_devices())
sd.default.device = 'BKSV USB Audio Asio Driver'
sd.default.samplerate = 96000
sd.default.channels = 8
sd.default.blocksize = BLOCKSIZE

rec_queue = Queue()
counter = 0
stop = False

play_data, fs = sf.read(sys.argv[1], dtype='float32')
def my_callback(indata, outdata, frames, time, status):
    global counter
    global stop
    if status:
        print(status)
    rec_queue.put(indata)
    index_start = counter * BLOCKSIZE
    index_end = index_start + BLOCKSIZE
    if (index_end < len(play_data)):
        outdata[:] = play_data[index_start : index_end, :]
        counter += 1
    else:
        print('stopping...')
        stop = True
        raise sd.CallbackStop()

with sd.Stream(blocksize=BLOCKSIZE, callback=my_callback, channels=[8,2]) as io_stream:
    with sf.SoundFile("recording.wav", mode='w', samplerate=96000, channels=8) as rec_file:
        print('Play and record...')
        while (not stop): # io_stream.active remains true, since input streaming continues after playing file has finished
            rec_file.write(rec_queue.get(timeout=3))
        print('Stopped')
        rec_file.close()



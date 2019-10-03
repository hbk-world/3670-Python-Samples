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
stop = False

with sf.SoundFile(sys.argv[1], mode='r') as play_file:

    def my_callback(indata, outdata, frames, time, status):
        global stop
        if status:
            print(status)
        rec_queue.put(indata)
        view = play_file.read(frames, dtype='float32', out=outdata)
        if (view.size != outdata.size):   # this was the last buffer.
            print('stopping...')
            outdata[view.shape[0]:,:].fill(0.0) # zero the part of outdata not written into  by sf.read()
            stop = True
            raise sd.CallbackStop()

    with sd.Stream(blocksize=BLOCKSIZE, callback=my_callback, channels=[8,2]) as io_stream:
        with sf.SoundFile("recording.wav", mode='w', samplerate=96000, channels=8) as rec_file:
            print('Play and record...')
            while (not stop):   # io_stream.active remains true, since input streaming continues after playing file has finished
                rec_file.write(rec_queue.get(timeout=3))
            print('Stopped')
            rec_file.close()
    play_file.close()

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

BLOCKSIZE = 1024

#print(sd.query_devices())
sd.default.device = 'BKSV USB Audio Asio Driver'
sd.default.samplerate = 96000
sd.default.channels = 8
sd.default.blocksize = BLOCKSIZE

data, fs = sf.read(sys.argv[1], dtype='float32',)
print( "Play and record...")
myrecording = sd.playrec(data, fs)
sd.wait()
print("Stopped")
sf.write("recording.wav", myrecording, samplerate=96000)


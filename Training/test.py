# import pyaudio
#
# CHUNK = 1024
# WIDTH = 2
# CHANNELS = 2
# RATE = 44100
# RECORD_SECONDS = 5
#
# p = pyaudio.PyAudio()
#
# stream = p.open(format=p.get_format_from_width(WIDTH),
#                 channels=CHANNELS,
#                 rate=RATE,
#                 input=True,
#                 output=True,
#                 frames_per_buffer=CHUNK)
#
# print("* recording")
#
# for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#     data = stream.read(CHUNK)
#     stream.write(data, CHUNK)
#
# print("* done")
#
# stream.stop_stream()
# stream.close()
#
# p.terminate()
from Audio import Audio
import threading
import cv2


n = 1


def saveaudio():
    path1 = r'C:\Users\Administrator\Desktop\recording\%s.wav' % n
    time = 5
    Audio.record_audio(time, path1)

# path1 = r'C:\Users\Administrator\Desktop\recording\%s.wav' % n
# time = 5
# Audio.record_audio(time, path1)

while 1:
    n = n+1
    print(n)
    k = cv2.waitKey(100) & 0xFF
    if k == ord('m'):
        t = threading.Thread(target=saveaudio)
        t.start()


# print(n)
# path2 = r'C:\Users\Administrator\Desktop\recording\%s.wav' % n
# Audio.play_audio(path2)
# n = n + 1
# print(n)
# path2 = r'C:\Users\Administrator\Desktop\recording\%s.wav' % n
# Audio.play_audio(path2)
# print(n)
# path2 = r'C:\Users\Administrator\Desktop\recording\%s.wav' % n
# Audio.play_audio(path2)
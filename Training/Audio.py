import pyaudio
import wave
import sys
import time

'''

init初始化的时候，time:要录制的时间，path：保存音频的路径及名称
record_audio:运行一次录制一段时长为time的音频
play_time:运行一次播放一段音频， 这里注意也要传入一个路径

'''


class Audio:
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100

    @staticmethod
    def record_audio(time, path):
        wave_output_filename = path
        p = pyaudio.PyAudio()
        stream = p.open(format=Audio.FORMAT, channels=Audio.CHANNELS,
                        rate=Audio.RATE, input=True,
                        frames_per_buffer=Audio.CHUNK)
        print("* recording")
        frames = []
        for i in range(0, int(Audio.RATE / Audio.CHUNK * time)):
            data = stream.read(Audio.CHUNK)
            frames.append(data)
        print("* done recording")
        stream.stop_stream()
        stream.close()
        p.terminate()
        wf = wave.open(wave_output_filename, 'wb')
        wf.setnchannels(Audio.CHANNELS)
        wf.setsampwidth(p.get_sample_size(Audio.FORMAT))
        wf.setframerate(Audio.RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

    @ staticmethod
    def play_audio(path):
        wf = wave.open(path, 'rb')
        # instantiate PyAudio (1)
        p = pyaudio.PyAudio()
        # define callback (2)

        def callback(in_data, frame_count, time_info, status):
            data = wf.readframes(frame_count)
            return data, pyaudio.paContinue

        # open stream using callback (3)
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True,
                        stream_callback=callback)
        # start the stream (4)
        stream.start_stream()
        # wait for stream to finish (5)
        while stream.is_active():
            time.sleep(0.01)
        # stop stream (6)
        stream.stop_stream()
        stream.close()
        wf.close()
        # close PyAudio (7)
        p.terminate()

# test的时候可以用
# n = 5
# path1 = r'C:\Users\Administrator\Desktop\recording\%s.wav' % n
# Audio.record_audio(10, path1)
# # path2 = r'C:\Users\Administrator\Desktop\recording\output.wav'
# # Audio.play_audio(path2)
# n = n + 1


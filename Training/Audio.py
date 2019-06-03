import pyaudio
import wave


class Audio:
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100

    def __init__(self, time, path):
        self.time = int(time)
        self.path = path

    def record_audio(self):
        wave_output_filename = self.path
        p = pyaudio.PyAudio()
        stream = p.open(format=Audio.FORMAT, channels=Audio.CHANNELS,
                        rate=Audio.RATE, input=True,
                        frames_per_buffer=Audio.CHUNK)
        print("* recording")
        frames = []
        for i in range(0, int(Audio.RATE / Audio.CHUNK * self.time)):
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
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)
        data = wf.readframes(Audio.CHUNK)
        while data != '':
            stream.write(data)
            data = wf.readframes(Audio.CHUNK)
        stream.stop_stream()
        stream.close()
        p.terminate()

    def change_time(self, time):
        self.time = int(time)


n = 1
path1 = r'C:\Users\Administrator\Desktop\recording\%s.wav' % n
audio = Audio(10, path1)
audio.recordaudio()

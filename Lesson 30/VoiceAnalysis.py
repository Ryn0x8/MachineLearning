import threading
import sys

try:
    import pyaudio
    import numpy as np
    import matplotlib.pyplot as plt
    import speech_recognition as sr
    from speech_recognition import AudioData
except ImportError as e:
    print(f"Error importing libraries: {e}")
    sys.exit(1)

stop_event = threading.Event()

def wait_for_enter():
    input("Press Enter to stop recording...")
    stop_event.set()

def record_audio(label):
    stop_event.clear()
    p = pyaudio.PyAudio()
    stream = p.open(format = pyaudio.paInt16, 
                    channels = 1,
                    rate = 16000,
                    input = True,
                    frames_per_buffer = 1024)
    frames = []
    print(f"Recording for {label}. Press Enter to stop.")
    threading.Thread(target=wait_for_enter, daemon = True).start()

    print("Recording...", end = "", flush = True)
    print(" (Speak now)", flush = True)
    while not stop_event.is_set():
        data = stream.read(1024, exception_on_overflow=False)
        frames.append(data)
        print(".", end = "", flush = True)
    print(" Done.")
    stream.stop_stream()
    stream.close()
    width = p.get_sample_size(pyaudio.paInt16)
    p.terminate()
    return b''.join(frames), 16000, width

def analyze_audio(data, rate):
    samples = np.frombuffer(data, dtype = np.int16)
    return {
        'duration': len(samples)/rate,
        'avg_volume': np.mean(np.abs(samples)),
        'max_volume': np.max(np.abs(samples)),
        'samples': samples
    }

def transcribe(data, rate, width):
    recognizer = sr.Recognizer()
    try:
        return recognizer.recognize_google(AudioData(data,rate,width))
    except:
        return "[Could not transcribe]"

def display_stats(stats, text, label):
    print("-"*40)
    print(f"\nStatistics for {label}:")
    print("-"*40)
    print(f"Duration: {stats['duration']:.2f} seconds")
    print(f"Average Volume: {stats['avg_volume']:.2f}")
    print(f"Maximum Volume: {stats['max_volume']:.2f}")
    print(f"Transcription: {text}")

def compare(stats1, stats2):
    print("\n", "="* 40)
    print("Comparison between Recordings:")
    print("="* 40)

    if stats1["duration"]> stats2["duration"]:
        longer = "Recording 1"
        diff = ((stats1["duration"] - stats2["duration"])/stats2["duration"])*100
    else:
        longer = "Recording 2"
        diff = ((stats2["duration"] - stats1["duration"])/stats1["duration"])*100

    print(f"{longer} by {diff:.2f}%")

    if stats1["avg_volume"]> stats2["avg_volume"]:
        louder = "Recording 1"
        diff = ((stats1["avg_volume"] - stats2["avg_volume"])/stats2["avg_volume"])*100
    else:
        louder = "Recording 2"
        diff = ((stats2["avg_volume"] - stats1["avg_volume"])/stats1["avg_volume"])*100

    print(f"{louder} by {diff:.2f}%")

def plot_both(stats1, stats2, rate):
    fig, (ax1, ax2) = plt.subplots(2,1, figsize = (12,6))

    t1 = np.linspace(0, len(stats1['samples'])/rate, len(stats1['samples']))
    ax1.plot(t1, stats1["samples"], color = "blue", linewidth=0.5)
    ax1.set_title(f"Recording 1 (Normal) - Duration: {stats1['duration']:.2f}s, Avg Volume: {stats1['avg_volume']:.2f}")
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Amplitude")
    ax1.grid(True, alpha = 0.3)
    ax1.set_ylim(-35000, 35000)

    t2 = np.linspace(0, len(stats2['samples'])/rate, len(stats2['samples']))
    ax2.plot(t2, stats2["samples"], color = "red", linewidth=0.5)
    ax2.set_title(f"Recording 2 (Loud) - Duration: {stats2['duration']:.2f}s, Avg Volume: {stats2['avg_volume']:.2f}")
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Amplitude")
    ax2.grid(True, alpha = 0.3)
    ax2.set_ylim(-35000, 35000)

    plt.tight_layout()
    plt.show()

def main():
    print("="*40)
    print("Voice Analysis - Record Two Samples")
    print("="*40)
    data1, rate1, width1 = record_audio("Recording 1 (Normal)")
    stats1 = analyze_audio(data1, rate1)
    text1 = transcribe(data1, rate1, width1)
    display_stats(stats1, text1, "Recording 1 (Normal)")

    data2, rate2, width2 = record_audio("Recording 2 (Loud)")
    stats2 = analyze_audio(data2, rate2)
    text2 = transcribe(data2, rate2, width2)
    display_stats(stats2, text2, "Recording 2 (Loud)")

    
    compare(stats1, stats2)
    plot_both(stats1, stats2, rate1)

if __name__ == "__main__":
    main()



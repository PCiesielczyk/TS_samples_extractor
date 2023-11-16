from video_processor import VideoProcessor
from samples_extractor import SamplesExtractor
from gui_initializer import GUIInitializer

frames_dir = 'frames_output'

extract_frames = input('Extract frames (Y/n)? ')
if extract_frames.lower() == 'y':
    video_processor = VideoProcessor('video.mp4', frames_dir, frame_interval=30)
    video_processor.extract_frames()

extract_samples = input('Extract samples (Y/n)? ')
if extract_samples.lower() == 'y':
    samples_extractor = SamplesExtractor(frames_dir, confidence_threshold=0.3)
    samples_extractor.extract_samples()

gui_initializer = GUIInitializer(sample_x_size=128)
gui_initializer.initialize_gui()

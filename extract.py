from video_processor import VideoProcessor
from samples_extractor import SamplesExtractor

frames_dir = 'frames_output'

video_processor = VideoProcessor('video.mp4', frames_dir, frame_interval=30)
video_processor.extract_frames()

samples_extractor = SamplesExtractor(frames_dir, confidence_threshold=0.3)
samples_extractor.extract_samples()

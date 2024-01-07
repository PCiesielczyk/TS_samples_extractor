# TS samples extractor
### Traffic Signs samples extractor is a tool for detecting traffic signs from a video file, labeling them and saving in dataset.
<img src="/images/extractingDiagram.png" alt="extractingDiagram">

## Prerequisites
This repository is submodule for [TSI-DCAI](https://github.com/PCiesielczyk/TSI-DCAI) project which contains `requirements.txt` file with all necessary dependencies. 
It interacts with detection and identification model, but also updates dataset which is defined in [TSI](https://github.com/PCiesielczyk/TSI) submodule. 
To ensure executing pipeline properly the appropriate model weights and file structure is required. 
The video file to be processed should be named `video.mp4` and saved in repository root directory.

## Usage
To start pipeline run `extract.py` script. The user is asked to confirm performing each step:
- Frames extraction: this step saves frames from `video.mp4` file to `frames_output` directory. By default every 25th frame is saved and it can be changed with `frame_interval` parameter in executed file.
- Samples extraction: extracting traffic signs from images involves YOLOv5 detection model and every detection comes with confidence level as a decimal. By default only samples with confidence higher than 0.65 is considered and saved to `temp` directory. The minimum level of confidence can be set with `confidence_threshold` parameter.
- Removing duplicates: removing identical or very similiar samples is based on [SSIM](https://en.wikipedia.org/wiki/Structural_similarity). Similarity takes the value of a decimal and by default every sample with similarity equal or higher than 0.75 to other is removed. This value can be changed with `similarity_threshold` parameter.
- Labeling: in the last step final samples are presented to the user through a GUI. Each detected sample is preliminarily classified by identification model and the user chooses to accepts the sample, sets another class, creates a new one or skips. The sample is then moved to the appropriate directory of the selected class or is deleted, and the GUI loads the next sample
<p align="center">
<img src="/images/labeling.png" alt="labeling" width="50%">
</p>

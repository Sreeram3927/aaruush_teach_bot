import numpy as np
import time
import cv2
from pygame import mixer


Verbose = False

mixer.init()
drum_clap = mixer.Sound('batterrm.wav')
drum_snare = mixer.Sound('button-2.ogg')


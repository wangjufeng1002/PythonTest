import os
import cv2
import numpy as np
import pandas as pd
from PIL import Image
import pytesseract
from pytesseract import Output
from openpyxl import Workbook
from typing import List, Dict, Tuple, Optional


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # 根据实际路径修改
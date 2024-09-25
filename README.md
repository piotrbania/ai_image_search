# What's that
AI assisted image search, checks your images on your hard drives and tries to find whether they match the thing you are looking for (this is OFFLINE processing, no data leaves your computer).
(fun project, just for "learning AI")

# General information

This "intelligent" images searchers using vision-language models (VLMs), to automate the entire process.

- scans a specified input directory for files (recursively or not your call)
- tries to understand the content using the LLaVA-v1.6 vision-language model (VLM), based on Vicuna-7B, to interpret visual files
- displays the output and their similarity (similarity to the search query) in GUI interface, results are clickable :D 

# Installation

Installation:
1) CPU version (slow):

`pip install nexaai --prefer-binary --index-url https://nexaai.github.io/nexa-sdk/whl/cpu --extra-index-url https://pypi.org/simple --no-cache-dir`

or GPU:

Linux:
`CMAKE_ARGS="-DGGML_CUDA=ON -DSD_CUBLAS=ON" pip install nexaai --prefer-binary --index-url https://nexaai.github.io/nexa-sdk/whl/cu124 --extra-index-url https://pypi.org/simple --no-cache-dir`

Windows:
`set CMAKE_ARGS="-DGGML_CUDA=ON -DSD_CUBLAS=ON" & pip install nexaai --prefer-binary --index-url https://nexaai.github.io/nexa-sdk/whl/cu124 --extra-index-url https://pypi.org/simple --no-cache-dir`

after installation make sure the CUDA_PATH env variable is set: 

`echo %CUDA_PATH%
C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v12.6
(if not you need to set it, the CUDA itself can be downloaded from: https://developer.nvidia.com/cuda-toolkit)
`

macOS:
`CMAKE_ARGS="-DGGML_METAL=ON -DSD_METAL=ON" pip install nexaai --prefer-binary --index-url https://nexaai.github.io/nexa-sdk/whl/metal --extra-index-url https://pypi.org/simple --no-cache-dir`

(see more at: https://github.com/NexaAI/nexa-sdk?tab=readme-ov-file#installation )

2) `pip install pytesseract PyMuPDF fitz python-docx python3-tk`


# Sample usage and output

`
F:\lab\ai\file_organizer>python ai_image_search.py F:\lab\ai\file_organizer\sample_dir  -r --query "image of dog"
+ AI assisted image search
+ by piotr bania / piotrbania.com / @piotrbania
+ Starting path: F:\lab\ai\file_organizer\sample_dir
+ Options: recursivity=TRUE
+ Query: "image of dog"
 

Initializing: "llava-v1.6-vicuna-7b:q4_0"
Model llava-v1.6-vicuna-7b:model-q4_0 already exists at C:\Users\piotr\.cache\nexa\hub\official\llava-v1.6-vicuna-7b\model-q4_0.gguf
Model llava-v1.6-vicuna-7b:projector-q4_0 already exists at C:\Users\piotr\.cache\nexa\hub\official\llava-v1.6-vicuna-7b\projector-q4_0.gguf

+ Models initialized!
+ Processing directory "F:\lab\ai\file_organizer\sample_dir"
+ File: "berneseeee.jpg"
+ Match:  100% (100) | graphics file = "F:\lab\ai\file_organizer\sample_dir\berneseeee.jpg"
+ File: "Dykcjacwiczeniawierszykiskonwertowany_968401708236538.pdf"
+ File: "SCTPscan - Finding entry points to SS7 Networks _ Telecommunications Backbones by Philippe Langlois-1.pdf"
+ File: "swinia.png"
+ Match:  0% (0) | graphics file = "F:\lab\ai\file_organizer\sample_dir\swinia.png"
...
+ Processed 36 files and 3 directories! (took 19.69 seconds)
`


![ai_image_search](https://github.com/user-attachments/assets/d6821c3f-7e37-4628-9eae-7bba2d62d2e6)


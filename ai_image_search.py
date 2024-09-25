'''

Installation:
1) CPU version (slow):
pip install nexaai --prefer-binary --index-url https://nexaai.github.io/nexa-sdk/whl/cpu --extra-index-url https://pypi.org/simple --no-cache-dir

or GPU:

Linux:
CMAKE_ARGS="-DGGML_CUDA=ON -DSD_CUBLAS=ON" pip install nexaai --prefer-binary --index-url https://nexaai.github.io/nexa-sdk/whl/cu124 --extra-index-url https://pypi.org/simple --no-cache-dir

Windows:
set CMAKE_ARGS="-DGGML_CUDA=ON -DSD_CUBLAS=ON" & pip install nexaai --prefer-binary --index-url https://nexaai.github.io/nexa-sdk/whl/cu124 --extra-index-url https://pypi.org/simple --no-cache-dir

after installation make sure the CUDA_PATH env variable is set: 
echo %CUDA_PATH%
C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v12.6
(if not you need to set it, the CUDA itself can be downloaded from: https://developer.nvidia.com/cuda-toolkit)


macOS:
CMAKE_ARGS="-DGGML_METAL=ON -DSD_METAL=ON" pip install nexaai --prefer-binary --index-url https://nexaai.github.io/nexa-sdk/whl/metal --extra-index-url https://pypi.org/simple --no-cache-dir

(see more at: https://github.com/NexaAI/nexa-sdk?tab=readme-ov-file#installation )


2) pip install pytesseract python3-tk


'''

import  os
import  sys
import  time
import  shutil
import  argparse 
import  pprint 
import  fitz
import  docx 

import  subprocess
import  tkinter as tk
from    tkinter import ttk

from    nexa.gguf import NexaVLMInference, NexaTextInference

# options 

opt_recursive       = 0
opt_query           = ""



# gui

root                = None 
tree                = None 
out_files           = [] 

# models 
mod_img_path        = "llava-v1.6-vicuna-7b:q4_0"
mod_img             = None 


# reporting 

files_counter       = 0
dir_counter         = 0

        
    

def init():
    global mod_img 
    
    
    if mod_img is not None:
        print("! Modules already initialized!")
        return

    
    print("Initializing: \"%s\"" % mod_img_path)
    mod_img = NexaVLMInference( model_path=mod_img_path,
                local_path=None,
                stop_words=[],
                temperature=0.3,
                max_new_tokens=256,
                top_k=3,
                top_p=0.2,
                profiling=False
            )
            
    print("+ Models initialized!")
    
    
def get_response_from_generator(description_generator):
    description = ""
    # get the response from the generator
    try:
        
        while True:
            response = next(description_generator)
            choices = response.get('choices', [])
            for choice in choices:
                delta = choice.get('delta', {})
                if 'content' in delta:
                    description += delta['content']
                    
    except StopIteration:
        pass
    
    
    return description    
    
    
    

def check_image_by_query(file_path, query):
    description_prompt      = f"""Analyze the given image and compare it with the following user query. Evaluate how similar the image is to the description provided by the user. Return the similarity as a percentage, where 100% means a perfect match and 0% means no similarity.

User query: f"{query}"

Provide only the similarity percentage.
"""

    description_generator   = mod_img._chat(description_prompt, file_path)
    description             = get_response_from_generator(description_generator)
    return description
    
    
def get_image_summary(file_path):
        
    description              = ""
    description_prompt      = "Please provide a detailed description of this image, focus on the main subject and important details."
    description_generator   = mod_img._chat(description_prompt, file_path)

    description             = get_response_from_generator(description_generator)
    
    
    return description
    
    
    


def open_file_location(file_path):
    if os.name == 'nt':  # Windows
        subprocess.run(['explorer', '/select,', file_path])
    elif os.name == 'posix':
        if subprocess.run(['xdg-open', file_path], check=False).returncode != 0:  # Linux
            subprocess.run(['xdg-open', os.path.dirname(file_path)])
    elif os.name == 'darwin':  # MacOS
        subprocess.run(['open', '-R', file_path])

# Funkcja uruchamiana po kliknięciu na element w liście
def on_item_click(event):
    selected_item = tree.focus()
    if selected_item:
        file_path = tree.item(selected_item)['values'][1]
        open_file_location(file_path)


def resize_columns(event):
    total_width = tree.winfo_width()
    tree.column("Similarity", width=int(total_width * 0.1))  
    tree.column("Path", width=int(total_width * 0.9)) 






    
        
def process_dir(path):
    global opt_query, opt_recursive, out_files
    global files_counter, dir_counter
    
    
    first               =   True 
    files_counter       =   0
    dir_counter         =   0
    
    for currentpath, folders, files in os.walk(path):
        print("+ Processing directory \"%s\"" % str(currentpath))
        
        if first == False and opt_recursive == False:
            break
        
        first = False
        dir_counter = dir_counter + 1
        
        
        for file in files:
            print("+ File: \"%s\"" % str(file))
            files_counter   =   files_counter + 1 
    
            match_num       = 0
            
    
            ext             = os.path.splitext(file.lower())[1]
            full_path       = os.path.join(currentpath, file)
        
            file_data       = ""
        
            img_ext         = [".jpg", ".jpeg", ".gif", ".png", ".bmp"]
        
            try:
    
                if ext in img_ext:
                    summary =  "" #get_image_summary(full_path)
                    match = check_image_by_query(full_path, opt_query)
                    match_num = int(match.replace("%", ""))
                    
                    
                    #print("+ Match: %s (%d)" % (match, match_num))
                    #print("+ Summary: \"%s\"" % summary)
                    
                    print("+ Match: %s (%d) | graphics file = \"%s\" " % (match, match_num, full_path))
                    
      
                    if match_num > 0:
                        out_files.append({"path": full_path, "similarity": match_num})
                    
                    
                
            
                    
            except Exception as e:
                print("! Unable to process file \"%s\", error = \"%s\"" % (str(full_path), str(e)))
                
        

                 
            
            
        
        
        
    
    

def main():
    global opt_recursive, opt_write, opt_query, root, tree
    
    print("# AI assisted file organizer ")
    print("# by piotr bania / piotrbania.com / @piotrbania")


    parser = argparse.ArgumentParser(description='AI assisted file searcher')
    
    parser.add_argument('-r', '--recursive',  action='store_true',  help='Recursive file scan')
    #parser.add_argument('-m', '--mode',  action='store', required=True,  help='Search mode (doc, image, both)')
    parser.add_argument('-q', "--query",  action='store', required=True, help='Query to search for')
    parser.add_argument('path', help='Starting path')
    
    
    args = parser.parse_args()
    
    print("+ Starting path: %s" % args.path)
    print("+ Options: recursivity=%s" % (("TRUE" if args.recursive == True else "FALSE")))
    print("+ Query: \"%s\"" % args.query)
    
    if os.path.exists(args.path) == False:
        print("+ Error: Path \"%s\" does not exist. " % str(args.path))
        return
    
    opt_recursive   = args.recursive
    opt_query       = args.query
    
    init()    
    
    
    s_time          = time.time()
    process_dir(args.path)
    e_time          = time.time()
    
    
    
    print(f"+ Processed {files_counter} files and {dir_counter} directories! (took {e_time - s_time:.2f} seconds)")
    
    
    
    root = tk.Tk()
    root.title("Image Similarity")
    root.minsize(800, 600)


    dark_bg             = "#2e2e2e"
    dark_fg             = "#d3d3d3" 
    highlight_color     = "#4a4a4a"  
    root.configure(bg=dark_bg)

    style = ttk.Style()
    style.theme_use("default")

    style.configure("Treeview.Heading", background=highlight_color, foreground=dark_fg)

    style.configure("Treeview", 
                    background=dark_bg, 
                    foreground=dark_fg, 
                    fieldbackground=dark_bg, 
                    rowheight=25)

    style.map('Treeview', 
            background=[('selected', highlight_color)], 
            foreground=[('selected', 'white')])



    tree = ttk.Treeview(root, columns=("Similarity", "Path"), show='headings')
    tree.heading("Similarity", text="Similarity (%)")
    tree.heading("Path", text="File Path")

    tree.column("Similarity", width=20, minwidth=10, anchor='center', stretch=True)
    tree.column("Path", width=400, minwidth=200, stretch=True)


    
    files_sorted = sorted(out_files, key=lambda x: x["similarity"], reverse=True)
    
    for file in files_sorted:
        tree.insert("", "end", values=(file["similarity"], file["path"]))

    tree.pack(expand=True, fill="both")

    tree.bind("<Double-1>", on_item_click)    
    root.bind("<Configure>", resize_columns)

    root.mainloop()




main()
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from functools import partial

#-------------------------------------------
#------------------GUI----------------------
#-------------------------------------------

# Function for opening the file explorer window and returning a path
def browse():
    path = filedialog.askopenfilename(initialdir = "/", title = "Select a PDF-File", filetypes = (("PDF files", "*.pdf*"), ("all files", "*.*")))
    return path

# Browsing a file and changing a label to the path
def browse_and_change_label(label):
    label.configure(text=browse())

# Activates the Button at the delete secion
def trp_browseFiles():
    browse_and_change_label(trp_label_path)
    trp_button_keep_pages['state'] = "active"  

def get_output_name(path, append):
    split_location = path.rsplit('/', 1)
    output_file_location = split_location[0]
    name = split_location[1].split(".")[0] + "-" + append
    return output_file_location + "/" + name + ".pdf"

def tmp_merge():
    # Start merger
    merger = PdfFileMerger()
    # Get File locations
    input_file_location_1 = tmp_label_path_1['text']
    input_file_location_2 = tmp_label_path_2['text']
    #Merge the files 
    merger.append(input_file_location_1)       
    merger.append(input_file_location_2)  

    merger.write(get_output_name(input_file_location_1, "merge"))
    merger.close()

    tmp_label_feedback['foreground'] = "green"
    tmp_label_feedback['text'] = "Edit was saved at " + final_output_name

def delete_pages():
    print("todo")

def keep_pages():
    # Gets pages as strings
    pages_to_keep_as_string = trp_keep_pages.get().split(",")
    # Converts strings to ints
    pages_to_keep = [int(numeric_string) for numeric_string in pages_to_keep_as_string]
    # Get File location
    input_file_location = trp_label_path['text']
    # Get Input File
    infile = PdfFileReader(input_file_location, 'rb')
    output = PdfFileWriter()

    #Add wanted Pages
    try:
        for i in pages_to_keep:
            p = infile.getPage(i)
            output.addPage(p)

        #get output path/name
        final_output_name = get_output_name(input_file_location, "cut")
        with open(final_output_name, 'wb') as f:
            #Create new file
            output.write(f)
        
        #Success
        trp_label_feedback['foreground'] = "green"
        trp_label_feedback['text'] = "Edit was saved at " + final_output_name
    except IndexError:
        #Failure
        trp_label_feedback['foreground'] = "red"
        trp_label_feedback['text'] = "Error: PDF doesn't have that many pages!"   



# Create the root window
window = Tk()
  
# Set window title
window.title('PDFmon')

# Add tabs
tabControl = ttk.Notebook(window)
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)

tabControl.add(tab1, text ='Remove pages')
tabControl.add(tab2, text ='Merge pages')
tabControl.pack(expand = 1, fill ="both")

# Set window size
window.geometry("600x200")
  
#Set window background color
window.config(background = "white")
  
# ELEMENTS FOR TAB 1
trp_button_explore = ttk.Button(tab1, text="Browse", command = trp_browseFiles, width=10)
trp_button_explore.grid(column = 1, row = 1)  

trp_label_path = ttk.Label(tab1, text="", foreground="blue")
trp_label_path.place(x=80, y=0)

trp_label_keep_pages = ttk.Label(tab1, text="Keep Pages:", width=10)
trp_label_keep_pages.grid(column = 1, row = 2) 

trp_keep_pages = StringVar()
trp_input_keep_pages = ttk.Entry(tab1, text="", textvariable = trp_keep_pages, width=30)
trp_input_keep_pages.grid(column = 2, row = 2)  

trp_button_keep_pages = ttk.Button(tab1, text = "Keep", command = keep_pages, state = DISABLED, width=10)
trp_button_keep_pages.grid(column = 3, row = 2)  

trp_label_feedback = ttk.Label(tab1, text = "")
trp_label_feedback.place(x=0, y=80)

trp_button_exit = ttk.Button(tab1, text = "Exit", command = exit, width=10)
trp_button_exit.grid(column = 1, row = 4)  

# ELEMENTS FOR TAB 2
#tmp_button_explore = ttk.Button(tab2, text="Browse PDF 1", command = tmp_browseFiles_1, width=15)

tmp_label_path_1 = ttk.Label(tab2, text="", foreground="blue")
tmp_label_path_1.place(x=120, y=0)

tmp_button_explore = ttk.Button(tab2, text="Browse PDF 1", command=partial(browse_and_change_label, tmp_label_path_1), width=15)
tmp_button_explore.grid(column = 1, row = 1) 

tmp_label_path_2 = ttk.Label(tab2, text="", foreground="blue")
tmp_label_path_2.place(x=120, y=30)

tmp_button_explore = ttk.Button(tab2, text="Browse PDF 2", command=partial(browse_and_change_label, tmp_label_path_2), width=15)
tmp_button_explore.grid(column = 1, row = 2)  

tmp_button_merge = ttk.Button(tab2, text="Merge", command = tmp_merge, width=15)
tmp_button_merge.grid(column = 1, row = 3)  

tmp_label_feedback = ttk.Label(tab2, text = "")
tmp_label_feedback.place(x=0, y=80)

# Let the window wait for any events
window.mainloop()
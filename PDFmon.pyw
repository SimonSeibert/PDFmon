from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from functools import partial
from enum import Enum

#-------------------------------------------
#------------------LOGIC----------------------
#-------------------------------------------
class PageModification(Enum):
    KEEP = 1
    DELETE = 2

# Current selected .pdf files
current_selected_files = []

#
# Browsing (a) file(s) and saving it to current_selected_files
#
def browse_files(multiple_files = False):
    global current_selected_files
    if multiple_files:
        current_selected_files = list(filedialog.askopenfilenames(initialdir = "/", title = "Select a PDF-File", filetypes = (("PDF files", "*.pdf*"), ("all files", "*.*"))))
        for file in current_selected_files :
            tmp_selected_files_list.insert(END, file)
    else:
        current_selected_files = [filedialog.askopenfilename(initialdir = "/", title = "Select PDF-File(s)", filetypes = (("PDF files", "*.pdf*"), ("all files", "*.*")))]


#
# Activates buttons at the delete section after selecting a file
#
def trp_browseFiles(trp_label_path):
    browse_files()
    trp_button_keep_pages['state'] = "active"
    trp_button_delete_pages['state'] = "active"
    trp_label_path['text'] = current_selected_files[0]

#
# Generates the output name for the edited file ("filename_append.pdf")
#
def get_output_name(path, append):
    split_location = path.rsplit('/', 1)
    output_file_location = split_location[0]
    name = split_location[1].split(".")[0] + "-" + append
    return output_file_location + "/" + name + ".pdf"

#
# Merges the selected files to a single file
#
def tmp_merge():
    # Start merger
    merger = PdfFileMerger()
    # append all files from selected_files to the merger
    for file in current_selected_files:
        merger.append(file) 

    final_output_name = get_output_name(current_selected_files[0], "merge")

    merger.write(final_output_name)
    merger.close()

    tmp_label_feedback['foreground'] = "green"
    tmp_label_feedback['text'] = "Merge was saved at " + final_output_name

#
# Converts a string to an array of ints
#
def string_to_numeric_array(string):
    splitted = string.split(",")
    return [int(numeric_string) for numeric_string in splitted]

#
# Deletes or keeps the pages from the selected file
#
def execute_page_modification(page_modification):
    # Converts strings to ints
    pages_to_keep = string_to_numeric_array(trp_pages.get())
    # Decrement each list item by 1 (because the user sees the pages starting at 1)
    for i in range(len(pages_to_keep)):
        pages_to_keep[i] -= 1
    # Get File location
    input_file_location = trp_label_path['text']
    # Get Input File
    infile = PdfFileReader(input_file_location, 'rb')
    output = PdfFileWriter()

    try:
        if(page_modification == PageModification.DELETE):
            # Only add pages that are not on the delete list
            for i in range(infile.numPages):
                if i not in pages_to_keep:
                    output.addPage(infile.getPage(i))
            #get output path/name
            final_output_name = get_output_name(input_file_location, "edit")
            with open(final_output_name, 'wb') as f:
                #Create new file
                output.write(f)
        elif(page_modification == PageModification.KEEP):
            for i in pages_to_keep:
                p = infile.getPage(i)
                output.addPage(p)
            
            #get output path/name
            final_output_name = get_output_name(input_file_location, "edit")
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
    except:
        #Failure
        trp_label_feedback['foreground'] = "red"
        trp_label_feedback['text'] = "Unknown Error"

#
# Move the selected item up or down in the listbox
#
def move_item(listbox, direction):
    selected_item = listbox.curselection()
    if selected_item:
        index = selected_item[0]
        new_index = index + direction
        if 0 <= new_index < listbox.size():
            item = listbox.get(index)
            listbox.delete(index)
            listbox.insert(new_index, item)
            listbox.selection_clear(0, END)
            listbox.selection_set(new_index)

            # Save listbox order to current_selected_files
            global current_selected_files
            print(list(listbox.get(0, END)))
            current_selected_files = list(listbox.get(0, END))
            
#-------------------------------------------
#------------------GUI----------------------
#-------------------------------------------
button_width = 15

# Create the root window
window = Tk()
  
# Set window title
window.title('PDFmon by Simon Seibert')

# Add tabs
tabControl = ttk.Notebook(window)
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)

tabControl.add(tab1, text ='Remove pages')
tabControl.add(tab2, text ='Merge pages')
tabControl.pack(expand = 1, fill ="both")

# Set window size
window.geometry("600x400")
  
#Set window background color
window.config(background = "white")
  
# ELEMENTS FOR TAB 1
trp_label_path = ttk.Label(tab1, text="...", foreground="blue")
trp_button_explore = ttk.Button(tab1, text="Browse PDF", command=partial(trp_browseFiles, trp_label_path), width=button_width)

trp_button_explore.grid(column = 1, row = 1)  
trp_label_path.place(x=110, y=5)

# Here the input is saved
trp_pages = StringVar()

trp_label_remove_pages = ttk.Label(tab1, text="Remove Pages:", width=button_width)
trp_label_remove_pages.grid(column = 1, row = 2) 

trp_input_pages = ttk.Entry(tab1, text="", textvariable = trp_pages, width=30)
trp_input_pages.grid(column = 2, row = 2)  

trp_button_keep_pages = ttk.Button(tab1, text = "Keep Selected Pages", command=partial(execute_page_modification, PageModification.KEEP), state = DISABLED, width=button_width/2)
trp_button_keep_pages.grid(column = 3, row = 2)  

trp_button_delete_pages = ttk.Button(tab1, text = "Delete Selected Pages", command=partial(execute_page_modification, PageModification.DELETE), state = DISABLED, width=button_width/2)
trp_button_delete_pages.grid(column = 4, row = 2)  

trp_label_feedback = ttk.Label(tab1, text = "")
trp_label_feedback.place(x=0, y=50)

# ELEMENTS FOR TAB 2
tmp_button_explore = ttk.Button(tab2, text="Add PDF File(s)", command=partial(browse_files, True), width=button_width)
tmp_button_explore.grid(column=1, row=0, padx=5, pady=5)

tmp_button_merge = ttk.Button(tab2, text="Merge", command = tmp_merge, width=button_width)
tmp_button_merge.grid(column=2, row=0, padx=5, pady=5)  

# Create a listbox widget to hold the filenames
tmp_selected_files_list = Listbox(tab2, selectmode=SINGLE, exportselection=0)
tmp_selected_files_list.grid(column=0, row=1, rowspan=5, columnspan=3, padx=5, pady=5, sticky=N+S+E+W)

# Create up and down buttons to reorder the items
tmp_up_button = ttk.Button(tab2, text="▲", command=lambda: move_item(tmp_selected_files_list, -1))
tmp_up_button.grid(column=3, row=1, padx=5, pady=5, sticky=N)

tmp_down_button = ttk.Button(tab2, text="▼", command=lambda: move_item(tmp_selected_files_list, 1))
tmp_down_button.grid(column=3, row=2, padx=5, pady=5, sticky=S)

tmp_label_feedback = ttk.Label(tab2, text = "")
tmp_label_feedback.place(x=0, y=220)

# Let the window wait for any events
window.mainloop()
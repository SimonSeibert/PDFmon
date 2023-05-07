from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from functools import partial
from enum import Enum
import customtkinter

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
        #Delete all entries in tmp_selected_files_list
        tmp_selected_files_list.delete(0, END)
        #Add new entries to tmp_selected_files_list
        for file in current_selected_files :
            tmp_selected_files_list.insert(END, file)
    else:
        current_selected_files = [filedialog.askopenfilename(initialdir = "/", title = "Select PDF-File(s)", filetypes = (("PDF files", "*.pdf*"), ("all files", "*.*")))]


#
# Activates buttons at the delete section after selecting a file
#
def trp_browseFiles(trp_label_path):
    browse_files()
    trp_button_keep_pages.configure(state = "normal")
    trp_button_delete_pages.configure(state = "normal")
    trp_label_path.configure(text = "Selected: '" + current_selected_files[0] + "'")

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

    tmp_label_feedback.configure(text_color = "green")
    tmp_label_feedback.configure(text = "Merge was saved at " + final_output_name)

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
    global current_selected_files
    input_file_location = current_selected_files[0]
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
        trp_label_feedback.configure(text_color = "green")
        trp_label_feedback.configure(text = "Edit was saved at " + final_output_name)
    except IndexError:
        #Failure
        trp_label_feedback.configure(text_color = "red")
        trp_label_feedback.configure(text = "Error: PDF doesn't have that many pages!")
    except:
        #Failure
        trp_label_feedback.configure(text_color = "red")
        trp_label_feedback.configure(text = "Unknown Error!")

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

#Theme
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

# Create the root window
window = customtkinter.CTk()
  
# Set window title
window.title('PDFmon by Simon Seibert')

# Add tabs
tabControl = customtkinter.CTkTabview(master=window)
tabControl.pack(expand = 1, fill ="both")

tabControl.add('Remove Pages')
tabControl.add('Merge Files')

tab1 = customtkinter.CTkFrame(master=tabControl.tab("Remove Pages"))
tab1.pack(ipadx=200, ipady=10)
tab2 = customtkinter.CTkFrame(master=tabControl.tab("Merge Files"))
tab2.pack(ipadx=200, ipady=10)

# Set window size
window.geometry("600x400")
  
#############################
##### ELEMENTS FOR TAB 1 ####
#############################

# Here the remove input is saved
trp_pages = StringVar()

#
# Create all UI elements
#

#Frames 
trp_frame_remove = customtkinter.CTkFrame(master=tab1)
trp_frame_remove_buttons = customtkinter.CTkFrame(master=tab1)
#tab 1 content
trp_tutorial = customtkinter.CTkLabel(tab1, wraplength=550, text='Here you can remove individual pages from a .pdf file. "Delete" removes the pages you have entered. "Keep" keeps the pages you have entered and removes all others. if you want to delete/keep several pages, you must separate the page numbers with a comma (e.g. 1,3,12).')
trp_label_path = customtkinter.CTkLabel(tab1, text="")
trp_button_browse = customtkinter.CTkButton(tab1, text="Browse PDF", command=partial(trp_browseFiles, trp_label_path), width=button_width)
trp_label_feedback = customtkinter.CTkLabel(tab1, text = "", width = 100)
# trp_remove_frame content
trp_label_remove_pages = customtkinter.CTkLabel(trp_frame_remove, text="Remove Pages:", width=button_width)
trp_input_pages = customtkinter.CTkEntry(trp_frame_remove, textvariable = trp_pages, width=100)
# trp_remove_buttons_frame content
trp_button_keep_pages = customtkinter.CTkButton(trp_frame_remove_buttons, text = "Keep Selected Pages", state = DISABLED, command=partial(execute_page_modification, PageModification.KEEP), width=button_width/2)
trp_button_delete_pages = customtkinter.CTkButton(trp_frame_remove_buttons, text = "Delete Selected Pages", state = DISABLED, command=partial(execute_page_modification, PageModification.DELETE), width=button_width/2)

#
# Pack all UI elements
#
trp_tutorial.pack()
trp_button_browse.pack(pady=5)
trp_label_path.pack()
trp_frame_remove.pack()
trp_label_remove_pages.pack(side="left")
trp_input_pages.pack(side="right", padx=5)
trp_frame_remove_buttons.pack(pady=5)
trp_button_keep_pages.pack(side="left")
trp_button_delete_pages.pack(side="right", padx=5)
trp_label_feedback.pack()

#############################
##### ELEMENTS FOR TAB 2 ####
#############################


#
# Create all UI elements
#

#Frames
tmp_button_frame = customtkinter.CTkFrame(master=tab2) # Create a frame for the buttons to place them horizontally
tmp_file_controll = customtkinter.CTkFrame(master=tab2)
tmp_file_controll_buttons = customtkinter.CTkFrame(master=tmp_file_controll) # Create a frame for the controll buttons
#tab 2 content
tmp_tutorial = customtkinter.CTkLabel(tab2, wraplength=550, text='Here you can select multiple .pdf file and merge them. Use the arrow buttons to change the merge order.')
tmp_selected_files_scrollbar = ttk.Scrollbar(tab2, orient=HORIZONTAL) # Create a horizontal scrollbar for the Listbox
tmp_label_feedback = customtkinter.CTkLabel(tab2, text = "", wraplength=400)
# tmp_button_frame content
tmp_button_explore = customtkinter.CTkButton(tmp_button_frame, text="Add PDF Files", command=partial(browse_files, True), width=button_width)
tmp_button_merge = customtkinter.CTkButton(tmp_button_frame, text="Merge", command = tmp_merge, width=button_width)
# tmp_file_controll_buttons content
tmp_selected_files_list = Listbox(tmp_file_controll, selectmode=SINGLE, exportselection=0) # Create a listbox widget to hold the filenames
tmp_up_button = customtkinter.CTkButton(tmp_file_controll_buttons, text="▲", command=lambda: move_item(tmp_selected_files_list, -1), width=5) # Create up and down buttons to reorder the items in the listbox
tmp_down_button = customtkinter.CTkButton(tmp_file_controll_buttons, text="▼", command=lambda: move_item(tmp_selected_files_list, 1), width=5)

tmp_tutorial.pack(pady=5)
tmp_button_frame.pack(pady=5)
tmp_button_explore.pack(side=LEFT, padx=5, fill=BOTH)
tmp_button_merge.pack(side=RIGHT, padx=5, fill=BOTH)
tmp_file_controll.pack(fill=BOTH, expand=True)
tmp_selected_files_list.pack(fill=BOTH, expand=True, pady=10, side="left")
tmp_selected_files_scrollbar.pack(fill=X, pady=0)
# Set the scrollbar to control the Listbox horizontally
tmp_selected_files_scrollbar.config(command=tmp_selected_files_list.xview)
tmp_file_controll_buttons.pack(fill=BOTH, expand=True, anchor="center")
tmp_up_button.pack(pady=25, padx=5)
tmp_down_button.pack()
tmp_label_feedback.pack()


# Let the window wait for any events
window.mainloop()
from PyPDF2 import PdfFileWriter, PdfFileReader
from tkinter import *
from tkinter import filedialog

#-------------------------------------------
#------------------GUI----------------------
#-------------------------------------------

# Function for opening the
# file explorer window
def browseFiles():
    tmp_filename = filedialog.askopenfilename(initialdir = "/", title = "Select a PDF-File", filetypes = (("PDF files", "*.pdf*"), ("all files", "*.*")))
    filename = tmp_filename
    # Change label contents
    label_file_explorer.configure(text=tmp_filename)
    # Enable Button for cutting
    button_keep_pages['state'] = "active"
      
def deletePages():
    print("todo")

def keepPages():
    # Gets pages as strings
    pages_to_keep_as_string = text_area_keep_pages.get().split(",")
    # Converts strings to ints
    pages_to_keep = [int(numeric_string) for numeric_string in pages_to_keep_as_string]
    # Get File location
    input_file_location = label_file_explorer['text']
    # Get Input File
    infile = PdfFileReader(input_file_location, 'rb')
    output = PdfFileWriter()

    #Add wanted Pages
    try:
        for i in pages_to_keep:
            p = infile.getPage(i)
            output.addPage(p)

        split_location = input_file_location.rsplit('/', 1)
        output_file_location = split_location[0]
        name = split_location[1].split(".")[0] + "-cut"
        final_output_name = output_file_location + "/" + name + ".pdf"
        with open(final_output_name, 'wb') as f:
            output.write(f)
        
        label_feedback['fg'] = "green"
        label_feedback['text'] = "Edit was saved at " + final_output_name
    except IndexError:
        label_feedback['fg'] = "red"
        label_feedback['text'] = "Error: PDF doesn't have that many pages!"   

    

# Create the root window
window = Tk()
  
# Set window title
window.title('PDFmon')
  
# Set window size
window.geometry("600x100")
  
#Set window background color
window.config(background = "white")
  
# Create a File Explorer label
label_file_explorer = Label(window, text = "", fg = "blue")

button_explore = Button(window, text = "Browse Files", command = browseFiles, width=10)
  
button_exit = Button(window, text = "Exit", command = exit, width=10)

label_keep_pages = Label(window, text="Keep Pages:", width=10)

text_area_keep_pages = StringVar()
input_keep_pages = Entry(window, textvariable = text_area_keep_pages, width=30)

button_keep_pages = Button(window, text = "Keep", command = keepPages, state = DISABLED, width=10)

label_delete_pages = Label(window, text="Delete Pages:")

text_area_delete_pages = StringVar()
input_delete_pages = Entry(window, textvariable = text_area_delete_pages, width=30)

button_delete_pages = Button(window, text = "Delete", command = deletePages)

label_feedback = Label(window, text = "", fg = "green")
  
# Grid method is chosen for placing
# the widgets at respective positions
# in a table like structure by
# specifying rows and columns

button_explore.grid(column = 1, row = 1)
label_file_explorer.place(x=80, y=0)

label_keep_pages.grid(column = 1,row = 2)
input_keep_pages.grid(column = 2,row = 2)
button_keep_pages.grid(column = 3,row = 2)

#label_delete_pages.grid(column = 1,row = 6)
#input_delete_pages.grid(column = 1,row = 7)
#button_delete_pages.grid(column = 1,row = 8)

label_feedback.place(x=0, y=80)
button_exit.grid(column = 1,row = 4)

# Let the window wait for any events
window.mainloop()
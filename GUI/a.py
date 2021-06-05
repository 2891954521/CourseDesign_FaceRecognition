import tkinter as tk
from PIL import Image, ImageTk
# python2 使用 Tkinter
#import Tkinter as tk
 
 
root = tk.Tk()

img_open = Image.open()

img = ImageTk.PhotoImage(img_open)

w = tk.Label(root)

w.config(image = img)
w.image = img

w.pack()
 
root.mainloop()
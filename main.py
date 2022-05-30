from tkinter import Tk, PhotoImage, Canvas, filedialog, Menu, NW, BOTH, Toplevel, Label, Entry, Frame, OptionMenu, \
    StringVar
from PIL import Image, ImageFont, ImageDraw
from tkinter.colorchooser import askcolor
from tkmacosx import Button
import glob


class App:
    def __init__(self):
        self.filetypes = (('jpeg files', '*.jpeg'), ('tiff files', '*.tiff'), ('bmp files', '*.bmp'),
                          ('gif files', '*.gif'), ('png files', '*.png'))
        self.img_dic = {}
        self.text_items = {}
        self.top_img_present = False

        # ---------------------------- UI SETUP ------------------------------- #
        # Window
        self.window = Tk()
        self.window.title("Watermarking")
        self.window.minsize(width=600, height=600)

        # Canvas
        self.canvas = Canvas(self.window)
        self.canvas.pack(fill=BOTH, expand=1)

        # MenuBar
        menubar = Menu(self.window)
        self.window.config(menu=menubar)

        # Menu Items
        self.file_menu = Menu(menubar)
        # File Menu
        menubar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Image...", command=self.load_bg_img)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Text Watermarker...", command=self.watermark_text_window, state="disabled")
        self.file_menu.add_command(label="Image Watermarker...", command=self.watermark_img_window, state="disabled")

        # Window's main loop
        self.window.mainloop()

    # Upload the background image
    def load_bg_img(self):
        bg_img_path = filedialog.askopenfilenames(title='Background Image', initialdir='/', filetypes=self.filetypes)

        # Image selected by the user
        if bg_img_path:
            self.img_dic["bg_img_raw_path"] = bg_img_path[0]
            # Enable the menu items
            self.file_menu.entryconfig("Text Watermarker...", state="normal")
            self.file_menu.entryconfig("Image Watermarker...", state="normal")
            self.window.attributes("-fullscreen", True)

            # Save resize photo in the working directory
            img = Image.open(bg_img_path[0])
            img_resize = img.resize((1670, 1030))
            img_resize_name = (self.img_dic["bg_img_raw_path"].rsplit('/', 1)[1]).rsplit('.', 1)[0]
            img_resize.save(f"{img_resize_name}_resize.png")
            self.img_dic["bg_img_resize_path"] = f"{img_resize_name}_resize.png"

            # Use the resize image as new background
            bg_resize_img = PhotoImage(file=self.img_dic["bg_img_resize_path"])
            self.canvas.create_image(20, 20, anchor=NW, image=bg_resize_img)

    # Load the text watermarker
    def watermark_text_window(self):
        # Window
        self.window_watermark = Toplevel(self.window)
        self.window_watermark.grab_set()

        self.window_watermark.title("Add Text Watermarker")
        self.window_watermark.minsize(width=330, height=135)
        self.window_watermark.resizable(False, False)
        self.text_items = {}

        # --- Description --- #
        label_text = Label(self.window_watermark, text="Text")
        label_text.grid(row=0, column=0, pady=3)

        label_font_family = Label(self.window_watermark, text="Font")
        label_font_family.grid(row=1, column=0, pady=3)

        label_color_size = Label(self.window_watermark, text="Color - Size")
        label_color_size.grid(row=2, column=0, pady=3)

        label_pos = Label(self.window_watermark, text="X-Pos - Y-Pos")
        label_pos.grid(row=3, column=0, pady=3)

        # --- Fields --- #
        # Text
        entry_text = Entry(self.window_watermark, width=36)
        entry_text.grid(row=0, column=1)
        self.text_items["text"] = entry_text

        # Font Family
        ttf_list = []
        for ttf_file in glob.glob("./fonts/*.ttf"):
            ttf_list.append(ttf_file.split("./fonts/")[1].split(".ttf")[0])

        value_family = StringVar(self.window_watermark)
        value_family.set(ttf_list[0])
        question_font_family = OptionMenu(self.window_watermark, value_family, *ttf_list)
        question_font_family.config(width=32)
        question_font_family.grid(row=1, column=1, pady=3)
        self.text_items["font"] = value_family

        # Color & Size
        frame_color_size = Frame(self.window_watermark)
        frame_color_size.grid(row=2, column=1)

        btn_color = Button(frame_color_size, width=100, text='Color', command=lambda: self.text_color(btn_color))
        btn_color.grid(row=0, column=0, padx=10)
        self.text_items["color"] = btn_color

        value_size = StringVar(frame_color_size)
        value_size.set("12")
        question_size = OptionMenu(frame_color_size, value_size, *range(1, 100))
        question_size.config(width=6)
        question_size.grid(row=0, column=1,  padx=10)
        self.text_items["size"] = value_size

        # Position X & Y
        frame_pos = Frame(self.window_watermark)
        frame_pos.grid(row=3, column=1)

        value_xpos = StringVar(frame_pos)
        value_xpos.set("1")
        optmenu_xpos = OptionMenu(frame_pos, value_xpos, *range(1, self.window.winfo_screenwidth()))
        optmenu_xpos.config(width=3)
        optmenu_xpos.grid(row=0, column=0,  padx=10)
        self.text_items["xpos"] = value_xpos

        value_ypos = StringVar(frame_pos)
        value_ypos.set("1")
        optmenu_ypos = OptionMenu(frame_pos, value_ypos, *range(1, self.window.winfo_screenheight()))
        optmenu_ypos.config(width=3)
        optmenu_ypos.grid(row=0, column=1, padx=10)
        self.text_items["ypos"] = value_ypos

        # Button confirm
        btn_confirm = Button(self.window_watermark, text='Ok', width=80, command=self.save_text)
        btn_confirm.grid(row=4, column=1, pady=15)

        # Window's main loop
        self.window_watermark.mainloop()

    # Choose text color
    def text_color(self, button):
        colors = askcolor(title="Color Chooser")
        button.configure(bg=colors[1])

    # Save text information
    def save_text(self):
        text_values = {}

        for key, value in self.text_items.items():
            if key == "color":
                text_values[key] = value.cget('bg')
            else:
                text_values[key] = value.get()

        # Make the image editable
        font_text = ImageFont.truetype(f"./fonts/{text_values['font']}.ttf", size=int(text_values["size"]))
        # photo = Image.open("./bg_img_resize.png")
        photo = Image.open(self.img_dic["bg_img_resize_path"])
        drawing = ImageDraw.Draw(photo)
        drawing.text((int(text_values["xpos"]), int(text_values["ypos"])),
                     text_values["text"],
                     font=font_text,
                     fill=text_values["color"])

        # Upload the updated image
        photo.save(self.img_dic["bg_img_resize_path"])
        bg_resize_img = PhotoImage(file=self.img_dic["bg_img_resize_path"])
        self.canvas.create_image(20, 20, anchor=NW, image=bg_resize_img)

        # Close window
        self.window_watermark.destroy()

    # Add another image on top of the background
    def watermark_img_window(self):
        # Window
        self.window_add_img = Toplevel(self.window)
        self.window_add_img.grab_set()

        self.window_add_img.title("Add Image Watermarker")
        self.window_add_img.minsize(width=330, height=135)
        self.window_add_img.resizable(False, False)
        self.top_img_items = {}

        # --- Description --- #
        label_img = Label(self.window_add_img, text="Image")
        label_img.grid(row=0, column=0, pady=3)

        label_resize = Label(self.window_add_img, text="Resize")
        label_resize.grid(row=1, column=0, pady=3)

        label_pos = Label(self.window_add_img, text="Position (X - Y)")
        label_pos.grid(row=2, column=0, pady=3)

        # --- Fields --- #
        # Search for image
        self.btn_top_img = Button(self.window_add_img, text='Search', width=165, command=self.choose_top_img)
        self.btn_top_img.grid(row=0, column=1, pady=15)

        # Resize
        frame_resize = Frame(self.window_add_img)
        frame_resize.grid(row=1, column=1)

        resize_xvalue = StringVar(frame_resize)
        resize_xvalue.set("12")
        optmenu_xvalue = OptionMenu(frame_resize, resize_xvalue, *range(1, self.window.winfo_screenwidth()))
        optmenu_xvalue.config(width=3)
        optmenu_xvalue.grid(row=0, column=0, padx=10)
        self.top_img_items["resize_xvalue"] = resize_xvalue

        resize_yvalue = StringVar(frame_resize)
        resize_yvalue.set("12")
        optmenu_yvalue = OptionMenu(frame_resize, resize_yvalue, *range(1, self.window.winfo_screenheight()))
        optmenu_yvalue.config(width=3)
        optmenu_yvalue.grid(row=0, column=1, padx=10)
        self.top_img_items["resize_yvalue"] = resize_yvalue

        # Position X & Y
        frame_pos = Frame(self.window_add_img)
        frame_pos.grid(row=2, column=1)

        value_xpos = StringVar(frame_pos)
        value_xpos.set("1")
        optmenu_xpos = OptionMenu(frame_pos, value_xpos, *range(1, self.window.winfo_screenwidth()))
        optmenu_xpos.config(width=3)
        optmenu_xpos.grid(row=0, column=0,  padx=10)
        self.top_img_items["xpos"] = value_xpos

        value_ypos = StringVar(frame_pos)
        value_ypos.set("1")
        optmenu_ypos = OptionMenu(frame_pos, value_ypos, *range(1, self.window.winfo_screenheight()))
        optmenu_ypos.config(width=3)
        optmenu_ypos.grid(row=0, column=1, padx=10)
        self.top_img_items["ypos"] = value_ypos

        # Button confirm
        btn_confirm_top_img = Button(self.window_add_img, text='Ok', width=100, command=self.add_top_image)
        btn_confirm_top_img.grid(row=4, column=1, pady=15)

        # Window's main loop
        self.window_add_img.mainloop()

    # Search for Top Image
    def choose_top_img(self):
        top_img_path = filedialog.askopenfilenames(title='Top Image', initialdir='/', filetypes=self.filetypes)

        # Top Image selected by the user
        if top_img_path:
            self.top_img_items["top_img_raw_path"] = top_img_path[0]
            self.btn_top_img['text'] = self.top_img_items["top_img_raw_path"].rsplit('/', 1)[1]
            self.btn_top_img["width"] = len(self.btn_top_img['text']) * 8
            self.btn_top_img["bg"] = "green"

            self.top_img_present = True

    # Add top-image onto the background image
    def add_top_image(self):
        if self.top_img_present:
            # Load the background
            base_image = Image.open(self.img_dic["bg_img_resize_path"])

            # Save resize top-image in the working directory
            img = Image.open(self.top_img_items["top_img_raw_path"])
            img_resize = img.resize(
                (int(self.top_img_items["resize_xvalue"].get()), int(self.top_img_items["resize_yvalue"].get())))
            img_resize_name = (self.top_img_items["top_img_raw_path"].rsplit('/', 1)[1]).rsplit('.', 1)[0]
            img_resize.save(f"{img_resize_name}_resize.png")
            self.top_img_items["top_img_resize_path"] = f"{img_resize_name}_resize.png"

            # Load the resized top-image
            watermark = Image.open(self.top_img_items["top_img_resize_path"])
            base_image.paste(watermark, (int(self.top_img_items["xpos"].get()),
                                         int(self.top_img_items["ypos"].get())))

            # Save the new image
            bg_name = (self.img_dic["bg_img_raw_path"].rsplit('/', 1)[1]).rsplit('.', 1)[0]
            top_name = (self.top_img_items["top_img_raw_path"].rsplit('/', 1)[1]).rsplit('.', 1)[0]
            bg_top_path = f"./{bg_name}_{top_name}.png"
            base_image.save(bg_top_path)

            # Use the resize image as new background
            bg_top_img = PhotoImage(file=bg_top_path)
            self.canvas.create_image(20, 20, anchor=NW, image=bg_top_img)

        # Close window
        self.window_add_img.destroy()


if __name__ == "__main__":
    app = App()

# === main.py ===
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from ui.app_frame import AppFrame

def main():
    app = ttkb.Window(themename="superhero")
    app.title("Wolfkit")
    app.geometry("800x600")
    app.minsize(600, 400)

    frame = AppFrame(app)
    frame.pack(fill=BOTH, expand=YES)

    app.mainloop()

if __name__ == "__main__":
    main()
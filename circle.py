import tkinter as tk
from tkinter.messagebox import askokcancel, showwarning, showinfo
import pyautogui
from math import sin, cos, radians
from time import sleep
from pynput import keyboard

AR_TEN_UNDER = ("Arial", 10, "underline")


class DrawCircle(tk.Tk):
    def __init__(self):
        """Will set up the window with all the buttons and stuff"""

        super().__init__()
        # self.attributes("-topmost", 1)
        self.geometry("500x255")
        self.resizable(False, False)
        self.title("Circle Test Master")
        icon = tk.PhotoImage(file = "circleIcon.png")
        self.iconphoto(False, icon)
        tk.Label(self, text = "Radius of the circle (in pixels)", font = AR_TEN_UNDER).pack(pady = 5)
        self.entry = tk.Entry(self)
        self.entry.pack()

        tk.Label(self, text='', font = ("", 5, "")).pack()
        rbFrame = tk.Frame(self)
        rbFrame.pack()

        tk.Label(rbFrame, text = "Precision", font = AR_TEN_UNDER).grid(columnspan = 3)
        self.rbVar = tk.IntVar()
        rb1 = tk.Radiobutton(rbFrame, text = "Min", variable = self.rbVar, value = 1, tristatevalue = 10)
        rb1.grid(row = 1, column = 0)

        rb2 = tk.Radiobutton(rbFrame, text = "Med", variable = self.rbVar, value = 2, tristatevalue = 10)
        rb2.grid(row = 1, column = 1)

        rb3 = tk.Radiobutton(rbFrame, text = "Max", variable = self.rbVar, value = 3, tristatevalue = 10)
        rb3.grid(row = 1, column = 2)

        startBtn = tk.Button(self, text="Start!", command=self.doTheWork, width=8)
        startBtn.pack(pady=10)

        self.infoBarText = tk.StringVar()
        self.infoBar = tk.Label(self, bg = "#fff", textvariable = self.infoBarText, pady = 10)
        self.infoBar.pack(fill=tk.X)

        rb1.bind("<Enter>", self._forMinEnter)
        rb1.bind("<Leave>", self._forMinLeave)

        rb2.bind("<Enter>", self._forMedEnter)
        rb2.bind("<Leave>", self._forMedLeave)

        rb3.bind("<Enter>", self._forMaxEnter)
        rb3.bind("<Leave>", self._forMaxLeave)


    def _forMinEnter(self, event) -> None:
        """Updates the InfoBar when the mouse pointer enters the Min radioButton"""

        self.infoBarText.set("Circle is jagged, but fastest")
        self.infoBar.update()


    def _forMinLeave(self, event) -> None:
        """Updates the InfoBar when the mouse pointer leaves the Min radioButton"""

        self.infoBarText.set("")
        self.infoBar.update()


    def _forMedEnter(self, event) -> None:
        """Updates the InfoBar when the mouse pointer enters the Med radioButton"""

        self.infoBarText.set("Circle is neater, but slower")
        self.infoBar.update()


    def _forMedLeave(self, event) -> None:
        """Updates the InfoBar when the mouse pointer leaves the Med radioButton"""

        self.infoBarText.set("")
        self.infoBar.update()


    def _forMaxEnter(self, event) -> None:
        """Updates the InfoBar when the mouse pointer enters the Max radioButton"""

        self.infoBarText.set("Circle is neatest, but slowest")
        self.infoBar.update()


    def _forMaxLeave(self, event) -> None:
        """Updates the InfoBar when the mouse pointer leaves the Max radioButton"""

        self.infoBarText.set("")
        self.infoBar.update()


    def _onPress(self, key: keyboard.Key) -> bool:
        """Listens to the keyboard for termination flag. If so, listener and loop are terminated"""

        if key == keyboard.Key.esc:
            self.shouldWeBreakOutOfTheLoop = True
            return False
        return True


    def doTheWork(self) -> None:
        """Will check if all the values entered are as expected or not. Throws error messages accordingly"""

        radius = None
        try: radius = int(self.entry.get())
        except: showwarning("Improper radius", "Please enter a proper INTEGER radius")
        else:
            if int(radius) == 0: showwarning("Zero radius", "Radius cannot be zero")
            if self.rbVar.get() == 0: showwarning("No precision", "Please select a precision level")
            else:
                radius = int(radius)
                okOrNot = askokcancel("Starting", "Drawing will start 5 seconds after you click OK")
                showinfo("Tip", "Drag your mouse to any corner of the screen or press 'esc' to stop")
                self.withdraw()
                if okOrNot: self.actuallyDrawTheCircle(radius, self.rbVar.get())


    def actuallyDrawTheCircle(self, radius: int, precision: int) -> None:
        """Will actually draw the circle my moving the mouse pointer to the proper positions"""

        self.listener = keyboard.Listener(on_press = self._onPress, on_release = None)
        self.listener.start()

        lst1 = [0, 1.0]
        lst0_5 = [0, 0.5, 1.0]
        lst0_1 = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        lstFinal = None
        if precision == 1: lstFinal = lst1
        elif precision == 2: lstFinal = lst0_5
        else: lstFinal = lst0_1
        sleep(5)
        x, y = pyautogui.position()
        pyautogui.move(radius, 0, tween = pyautogui.easeInOutQuad, duration = 1)
        self.shouldWeBreakOutOfTheLoop = False

        angle = 0.0
        while angle != 361:
            for decimal in lstFinal:
                try: pyautogui.dragTo(x + radius*cos(radians(angle + decimal)),
                                      y + radius*sin(radians(angle + decimal)))
                except:
                    self.shouldWeBreakOutOfTheLoop = True
                    break
                else:
                    if decimal == 1.0: angle += 1
            if self.shouldWeBreakOutOfTheLoop: break

        self.update()
        self.deiconify()
        if self.shouldWeBreakOutOfTheLoop: showinfo("Process terminated", "Process terminated successfully")
        else: showinfo("Process Finished", "Circle has been drawn")


def main() -> None:
    """Creates the object of the DrawCircle class and runs the mainloop"""

    drawingObject = DrawCircle()
    drawingObject.mainloop()


if __name__ == "__main__":
    main()

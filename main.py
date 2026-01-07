import tkinter as tk
from screens.login import LoginScreen

def main():
    root = tk.Tk()
    root.title("SiGEEM")
    root.geometry("800x600")
    root.resizable(False, False)
    
    # Centralizar janela
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    app = LoginScreen(root)
    root.mainloop()

if __name__ == "__main__":
    main()
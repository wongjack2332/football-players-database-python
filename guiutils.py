def clear_frame(frame):
    for i in frame.winfo_children():
        i.destroy()

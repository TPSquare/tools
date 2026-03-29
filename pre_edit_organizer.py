import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import vlc
import platform


class PreEditOrganizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Công cụ sắp xếp tiền edit video - Phân vùng 2 danh sách")
        self.root.geometry("950x750")

        self.valid_extensions = {
            ".jpg",
            ".jpeg",
            ".png",
            ".gif",
            ".mp4",
            ".mov",
            ".avi",
            ".mkv",
        }
        self.input_dir = ""
        self.output_dir = ""
        self.file_map = {}

        self.vlc_instance = vlc.Instance()
        self.player = self.vlc_instance.media_player_new()

        self.create_widgets()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):

        frame_top = tk.Frame(self.root)
        frame_top.pack(pady=10, fill=tk.X, padx=20)

        frame_in = tk.Frame(frame_top)
        frame_in.pack(fill=tk.X, pady=2)
        tk.Button(
            frame_in,
            text="1. Chọn thư mục nguồn (input)",
            command=self.select_input,
            width=25,
        ).pack(side=tk.LEFT)
        self.lbl_input = tk.Label(frame_in, text="Chưa chọn...", fg="gray")
        self.lbl_input.pack(side=tk.LEFT, padx=10)

        frame_out = tk.Frame(frame_top)
        frame_out.pack(fill=tk.X, pady=2)
        tk.Button(
            frame_out,
            text="2. Chọn thư mục đích (output)",
            command=self.select_output,
            width=25,
        ).pack(side=tk.LEFT)
        self.lbl_output = tk.Label(frame_out, text="Chưa chọn...", fg="gray")
        self.lbl_output.pack(side=tk.LEFT, padx=10)

        main_frame = tk.Frame(self.root)
        main_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=20)

        left_col = tk.Frame(main_frame)
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        frame_done = tk.LabelFrame(
            left_col,
            text=" File ĐÃ SẮP XẾP (Ưu tiên xuất trước) ",
            fg="green",
            font=("Arial", 10, "bold"),
        )
        frame_done.pack(fill=tk.BOTH, expand=True, pady=(0, 5))

        scroll_done = tk.Scrollbar(frame_done)
        scroll_done.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox_done = tk.Listbox(
            frame_done,
            yscrollcommand=scroll_done.set,
            selectmode=tk.SINGLE,
            font=("Arial", 11),
            bg="#f0fff0",
        )
        self.listbox_done.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_done.config(command=self.listbox_done.yview)

        frame_todo = tk.LabelFrame(
            left_col, text=" File CHƯA SẮP XẾP ", fg="red", font=("Arial", 10, "bold")
        )
        frame_todo.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

        scroll_todo = tk.Scrollbar(frame_todo)
        scroll_todo.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox_todo = tk.Listbox(
            frame_todo,
            yscrollcommand=scroll_todo.set,
            selectmode=tk.SINGLE,
            font=("Arial", 11),
            bg="#fff0f0",
        )
        self.listbox_todo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_todo.config(command=self.listbox_todo.yview)

        self.listbox_done.bind("<<ListboxSelect>>", self.on_done_select)
        self.listbox_todo.bind("<<ListboxSelect>>", self.on_todo_select)

        frame_controls = tk.Frame(left_col)
        frame_controls.pack(pady=10)

        tk.Button(
            frame_controls, text="⬆ Lên chút", command=self.move_up, width=12
        ).pack(side=tk.LEFT, padx=3)
        tk.Button(
            frame_controls, text="⬇ Xuống chút", command=self.move_down, width=12
        ).pack(side=tk.LEFT, padx=3)

        tk.Button(
            frame_controls,
            text="➡ Duyệt file này",
            command=self.quick_move_to_done,
            width=20,
            bg="#c8e6c9",
            font=("Arial", 10, "bold"),
            fg="#2e7d32",
        ).pack(side=tk.LEFT, padx=10)

        right_col = tk.Frame(
            main_frame,
            width=380,
            bg="#e0e0e0",
            highlightbackground="gray",
            highlightthickness=1,
        )
        right_col.pack(side=tk.RIGHT, fill=tk.Y, padx=(20, 0))
        right_col.pack_propagate(False)

        lbl_title_preview = tk.Label(
            right_col,
            text="Xem trước (Preview)",
            bg="#e0e0e0",
            font=("Arial", 10, "bold"),
        )
        lbl_title_preview.pack(pady=(10, 5))

        self.preview_area = tk.Frame(right_col, bg="black")
        self.preview_area.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

        self.lbl_img_preview = tk.Label(
            self.preview_area,
            text="Chọn một file\nđể xem trước",
            bg="#e0e0e0",
            fg="gray",
        )
        self.lbl_img_preview.pack(expand=True, fill=tk.BOTH)

        tk.Button(
            self.root,
            text="3. Xuất files",
            command=self.export_files,
            bg="green",
            fg="white",
            font=("Arial", 12, "bold"),
            height=2,
        ).pack(pady=10, fill=tk.X, padx=50)

    def select_input(self):
        self.input_dir = filedialog.askdirectory(
            title="Chọn thư mục chứa ảnh/video gốc"
        )
        if self.input_dir:
            self.lbl_input.config(text=self.input_dir)
            self.load_files()

    def select_output(self):
        self.output_dir = filedialog.askdirectory(
            title="Chọn thư mục lưu file sau khi sắp xếp"
        )
        if self.output_dir:
            self.lbl_output.config(text=self.output_dir)

    def load_files(self):
        self.listbox_done.delete(0, tk.END)
        self.listbox_todo.delete(0, tk.END)
        self.file_map.clear()
        self.player.stop()
        self.lbl_img_preview.pack(expand=True, fill=tk.BOTH)
        self.lbl_img_preview.config(image="", text="Chọn một file\nđể xem trước")

        try:
            files = os.listdir(self.input_dir)
            valid_files = [
                f
                for f in files
                if os.path.splitext(f)[1].lower() in self.valid_extensions
            ]
            valid_files.sort()
            for f in valid_files:
                self.listbox_todo.insert(tk.END, f)
                self.file_map[f] = os.path.join(self.input_dir, f)

            if valid_files:
                self.listbox_todo.selection_set(0)
                self.show_preview_for_selection(self.listbox_todo)

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể đọc thư mục: {e}")

    def on_done_select(self, event):
        if self.listbox_done.curselection():
            self.listbox_todo.selection_clear(0, tk.END)
            self.show_preview_for_selection(self.listbox_done)

    def on_todo_select(self, event):
        if self.listbox_todo.curselection():
            self.listbox_done.selection_clear(0, tk.END)
            self.show_preview_for_selection(self.listbox_todo)

    def show_preview_for_selection(self, active_listbox):
        selection = active_listbox.curselection()
        if not selection:
            return

        filename = active_listbox.get(selection[0])
        filepath = self.file_map.get(filename)
        if not filepath:
            return

        self.player.stop()
        ext = os.path.splitext(filename)[1].lower()

        try:
            if ext in {".mp4", ".mov", ".avi", ".mkv"}:
                self.lbl_img_preview.pack_forget()
                media = self.vlc_instance.media_new(filepath)
                self.player.set_media(media)

                h = self.preview_area.winfo_id()
                if platform.system() == "Windows":
                    self.player.set_hwnd(h)
                elif platform.system() == "Darwin":
                    self.player.set_nsobject(h)
                else:
                    self.player.set_xwindow(h)

                self.player.play()
            else:
                self.lbl_img_preview.pack(expand=True, fill=tk.BOTH)
                img = Image.open(filepath)
                img.thumbnail((350, 350))
                self.preview_image = ImageTk.PhotoImage(img)
                self.lbl_img_preview.config(image=self.preview_image, text="")
        except Exception as e:
            self.lbl_img_preview.config(image="", text="Lỗi khi load preview")

    def quick_move_to_done(self):
        """Đẩy thẳng file đang chọn ở list dưới lên cuối list trên"""
        sel_todo = self.listbox_todo.curselection()
        if not sel_todo:
            messagebox.showinfo(
                "Thông báo", "Vui lòng chọn một file ở danh sách CHƯA SẮP XẾP!"
            )
            return

        index = sel_todo[0]
        text = self.listbox_todo.get(index)

        self.listbox_todo.delete(index)
        self.listbox_done.insert(tk.END, text)

        if self.listbox_todo.size() > 0:
            next_index = (
                index
                if index < self.listbox_todo.size()
                else self.listbox_todo.size() - 1
            )
            self.listbox_todo.selection_set(next_index)
            self.show_preview_for_selection(self.listbox_todo)
        else:

            self.player.stop()
            self.lbl_img_preview.pack(expand=True, fill=tk.BOTH)
            self.lbl_img_preview.config(image="", text="Đã duyệt hết file!")

    def move_up(self):
        sel_done = self.listbox_done.curselection()
        sel_todo = self.listbox_todo.curselection()

        if sel_done:
            index = sel_done[0]
            if index == 0:
                return
            text = self.listbox_done.get(index)
            self.listbox_done.delete(index)
            self.listbox_done.insert(index - 1, text)
            self.listbox_done.selection_set(index - 1)
            self.show_preview_for_selection(self.listbox_done)

        elif sel_todo:
            index = sel_todo[0]
            text = self.listbox_todo.get(index)

            if index == 0:
                self.listbox_todo.delete(index)
                self.listbox_done.insert(tk.END, text)

                new_index = self.listbox_done.size() - 1
                self.listbox_done.selection_set(new_index)
                self.show_preview_for_selection(self.listbox_done)
            else:
                self.listbox_todo.delete(index)
                self.listbox_todo.insert(index - 1, text)
                self.listbox_todo.selection_set(index - 1)
                self.show_preview_for_selection(self.listbox_todo)

    def move_down(self):
        sel_done = self.listbox_done.curselection()
        sel_todo = self.listbox_todo.curselection()

        if sel_done:
            index = sel_done[0]
            text = self.listbox_done.get(index)

            if index == self.listbox_done.size() - 1:
                self.listbox_done.delete(index)
                self.listbox_todo.insert(0, text)

                self.listbox_todo.selection_set(0)
                self.show_preview_for_selection(self.listbox_todo)
            else:
                self.listbox_done.delete(index)
                self.listbox_done.insert(index + 1, text)
                self.listbox_done.selection_set(index + 1)
                self.show_preview_for_selection(self.listbox_done)

        elif sel_todo:
            index = sel_todo[0]
            if index == self.listbox_todo.size() - 1:
                return
            text = self.listbox_todo.get(index)
            self.listbox_todo.delete(index)
            self.listbox_todo.insert(index + 1, text)
            self.listbox_todo.selection_set(index + 1)
            self.show_preview_for_selection(self.listbox_todo)

    def export_files(self):
        if not self.input_dir or not self.output_dir:
            messagebox.showwarning(
                "Cảnh báo", "Vui lòng chọn cả thư mục nguồn và đích!"
            )
            return

        total_items = self.listbox_done.size() + self.listbox_todo.size()
        if total_items == 0:
            messagebox.showinfo("Thông báo", "Không có file nào để xuất!")
            return

        self.player.stop()

        try:
            items_done = self.listbox_done.get(0, tk.END)
            items_todo = self.listbox_todo.get(0, tk.END)
            all_items = list(items_done) + list(items_todo)

            for new_index, filename in enumerate(all_items):
                old_path = self.file_map[filename]
                ext = os.path.splitext(filename)[1]
                new_filename = f"{new_index + 1:03d}{ext}"
                new_path = os.path.join(self.output_dir, new_filename)
                shutil.copy2(old_path, new_path)

            messagebox.showinfo(
                "Thành công",
                f"Đã xuất thành công {len(all_items)} file vào:\n{self.output_dir}",
            )
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra trong quá trình copy: {e}")

    def on_closing(self):
        self.player.stop()
        self.vlc_instance.release()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = PreEditOrganizer(root)
    root.mainloop()

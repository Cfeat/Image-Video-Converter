import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import subprocess
import os
import threading

class ImageConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("图片格式转换器")
        self.root.geometry("650x450")
        self.root.resizable(False, False)

        self.style = ttk.Style()
        self.style.configure("TLabel", font=("SimHei", 10))
        self.style.configure("TButton", font=("SimHei", 10))
        self.style.configure("TCombobox", font=("SimHei", 10))
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.output_format = tk.StringVar(value="png")
        self.create_widgets()
        self.check_ffmpeg_installed()
    
    def create_widgets(self):
        input_frame = ttk.Frame(self.root, padding="10")
        input_frame.pack(fill=tk.X)
        
        ttk.Label(input_frame, text="输入图片:").pack(side=tk.LEFT, padx=5)
        ttk.Entry(input_frame, textvariable=self.input_path, width=55).pack(side=tk.LEFT, padx=5)
        ttk.Button(input_frame, text="浏览", command=self.browse_input).pack(side=tk.LEFT, padx=5)
        
        output_frame = ttk.Frame(self.root, padding="10")
        output_frame.pack(fill=tk.X)
        
        ttk.Label(output_frame, text="输出格式:").pack(side=tk.LEFT, padx=5)
        formats = ["png", "jpg", "jpeg", "webp", "bmp", "tiff"]
        format_combo = ttk.Combobox(output_frame, textvariable=self.output_format, values=formats, width=10)
        format_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(output_frame, text="设置输出路径", command=self.set_output_path).pack(side=tk.LEFT, padx=5)

        btn_frame = ttk.Frame(self.root, padding="10")
        btn_frame.pack()
        
        self.convert_btn = ttk.Button(btn_frame, text="开始转换", command=self.start_conversion)
        self.convert_btn.pack(side=tk.LEFT, padx=10)
        
        self.batch_btn = ttk.Button(btn_frame, text="批量转换", command=self.start_batch_conversion)
        self.batch_btn.pack(side=tk.LEFT, padx=10)
        
        progress_frame = ttk.Frame(self.root, padding="10")
        progress_frame.pack(fill=tk.X)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X)
        
        status_frame = ttk.Frame(self.root, padding="10")
        status_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(status_frame, text="转换状态:").pack(anchor=tk.W)
        self.status_text = tk.Text(status_frame, height=10, width=75, state=tk.DISABLED)
        self.status_text.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(self.status_text, command=self.status_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.status_text.config(yscrollcommand=scrollbar.set)
    
    def browse_input(self):
        filename = filedialog.askopenfilename(
            filetypes=[
                ("图片文件", "*.png *.jpg *.jpeg *.webp *.bmp *.tiff *.gif"),
                ("所有文件", "*.*")
            ]
        )
        if filename:
            self.input_path.set(filename)
            name, ext = os.path.splitext(filename)
            self.output_path.set(f"{name}.{self.output_format.get()}")
    
    def set_output_path(self):
        if not self.input_path.get():
            messagebox.showwarning("警告", "请先选择输入图片")
            return
            
        default_ext = self.output_format.get()
        filename = filedialog.asksaveasfilename(
            defaultextension=f".{default_ext}",
            filetypes=[(f"{default_ext}文件", f"*.{default_ext}")]
        )
        if filename:
            self.output_path.set(filename)
            _, ext = os.path.splitext(filename)
            if ext:
                self.output_format.set(ext[1:].lower())
    
    def log(self, message):
        self.status_text.config(state=tk.NORMAL)
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.status_text.config(state=tk.DISABLED)
    
    def check_ffmpeg_installed(self):
        try:
            subprocess.run(
                ["ffmpeg", "-version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding='utf-8'
            )
            self.log("FFmpeg已安装，准备就绪")
            return True
        except FileNotFoundError:
            self.log("错误: 未找到FFmpeg。请安装FFmpeg并确保它在系统PATH中。")
            self.log("下载地址: https://ffmpeg.org/download.html")
            return False
    
    def run_conversion(self, input_file, output_file=None):
        if not output_file:
            output_file = self.output_path.get()
            
        if not output_file:
            name, ext = os.path.splitext(input_file)
            output_file = f"{name}.{self.output_format.get()}"
        
        format = self.output_format.get()
        
        # 构建FFmpeg命令
        cmd = [
            "ffmpeg",
            "-i", input_file,         
            "-y",                      
            # "-f", format,             
            output_file           
        ]
        
        self.log(f"开始转换: {os.path.basename(input_file)} -> {os.path.basename(output_file)}")
        self.log(f"执行命令: {' '.join(cmd)}")
        
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding='utf-8'
            )
            
            while True:
                line = process.stderr.readline()
                if not line:
                    break
                self.log(line.strip())
            
            process.wait()
            
            if process.returncode == 0:
                self.log(f"转换完成: {os.path.basename(output_file)}")
                return True
            else:
                self.log(f"转换失败，返回代码: {process.returncode}")
                return False
                
        except Exception as e:
            self.log(f"错误: {str(e)}")
            return False
    
    def run_batch_conversion(self):
        files = filedialog.askopenfilenames(
            filetypes=[
                ("图片文件", "*.png *.jpg *.jpeg *.webp *.bmp *.tiff *.gif"),
                ("所有文件", "*.*")
            ]
        )
        
        if not files:
            self.log("未选择任何文件")
            self.convert_btn.config(state=tk.NORMAL)
            self.batch_btn.config(state=tk.NORMAL)
            return
        
        total = len(files)
        success = 0

        output_dir = filedialog.askdirectory(title="选择输出目录")
        if not output_dir:
            self.log("未选择输出目录，批量转换取消")
            self.convert_btn.config(state=tk.NORMAL)
            self.batch_btn.config(state=tk.NORMAL)
            return
        
        self.log(f"开始批量转换，共 {total} 个文件")
        
        for i, file in enumerate(files, 1):
            self.progress_var.set((i / total) * 100)

            name, _ = os.path.splitext(os.path.basename(file))
            output_file = os.path.join(output_dir, f"{name}.{self.output_format.get()}")
            
            if self.run_conversion(file, output_file):
                success += 1
        
        self.progress_var.set(100)
        self.log(f"批量转换完成，成功 {success}/{total} 个文件")
        messagebox.showinfo("批量转换完成", f"成功 {success}/{total} 个文件")
        
        self.convert_btn.config(state=tk.NORMAL)
        self.batch_btn.config(state=tk.NORMAL)
    
    def start_conversion(self):
        input_file = self.input_path.get()
        
        if not input_file:
            messagebox.showwarning("警告", "请选择输入图片")
            return
        
        if not self.check_ffmpeg_installed():
            return
        
        self.convert_btn.config(state=tk.DISABLED)
        self.batch_btn.config(state=tk.DISABLED)
        self.progress_var.set(0)
        self.status_text.config(state=tk.NORMAL)
        self.status_text.delete(1.0, tk.END)
        self.status_text.config(state=tk.DISABLED)
        
        thread = threading.Thread(
            target=lambda: self._finish_single_conversion(input_file)
        )
        thread.daemon = True
        thread.start()
    
    def _finish_single_conversion(self, input_file):
        result = self.run_conversion(input_file)
        self.progress_var.set(100)
        
        if result:
            messagebox.showinfo("成功", f"转换完成!\n文件保存至: {self.output_path.get()}")
        
        self.convert_btn.config(state=tk.NORMAL)
        self.batch_btn.config(state=tk.NORMAL)
    
    def start_batch_conversion(self):
        if not self.check_ffmpeg_installed():
            return
        
        self.convert_btn.config(state=tk.DISABLED)
        self.batch_btn.config(state=tk.DISABLED)
        self.progress_var.set(0)
        self.status_text.config(state=tk.NORMAL)
        self.status_text.delete(1.0, tk.END)
        self.status_text.config(state=tk.DISABLED)

        thread = threading.Thread(target=self.run_batch_conversion)
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageConverter(root)
    root.mainloop()
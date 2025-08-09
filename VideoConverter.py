import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import subprocess
import os
import re
import threading

class VideoConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("视频格式转换器")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("SimHei", 10))
        self.style.configure("TButton", font=("SimHei", 10))
        self.style.configure("TCombobox", font=("SimHei", 10))
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.output_format = tk.StringVar(value="mp4")
        
        self.create_widgets()
        
        self.check_ffmpeg_installed()
    
    def create_widgets(self):
        input_frame = ttk.Frame(self.root, padding="10")
        input_frame.pack(fill=tk.X)
        
        ttk.Label(input_frame, text="输入文件:").pack(side=tk.LEFT, padx=5)
        ttk.Entry(input_frame, textvariable=self.input_path, width=50).pack(side=tk.LEFT, padx=5)
        ttk.Button(input_frame, text="浏览", command=self.browse_input).pack(side=tk.LEFT, padx=5)
        
        output_frame = ttk.Frame(self.root, padding="10")
        output_frame.pack(fill=tk.X)
        
        ttk.Label(output_frame, text="输出格式:").pack(side=tk.LEFT, padx=5)
        formats = ["mp4", "avi", "mov", "flv", "mkv", "wmv", "webm"]
        format_combo = ttk.Combobox(output_frame, textvariable=self.output_format, values=formats, width=10)
        format_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(output_frame, text="设置输出路径", command=self.set_output_path).pack(side=tk.LEFT, padx=5)
        
        btn_frame = ttk.Frame(self.root, padding="10")
        btn_frame.pack()
        
        self.convert_btn = ttk.Button(btn_frame, text="开始转换", command=self.start_conversion)
        self.convert_btn.pack()
        
        progress_frame = ttk.Frame(self.root, padding="10")
        progress_frame.pack(fill=tk.X)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X)
        
        status_frame = ttk.Frame(self.root, padding="10")
        status_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(status_frame, text="转换状态:").pack(anchor=tk.W)
        self.status_text = tk.Text(status_frame, height=10, width=70, state=tk.DISABLED)
        self.status_text.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(self.status_text, command=self.status_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.status_text.config(yscrollcommand=scrollbar.set)
    
    def browse_input(self):
        filename = filedialog.askopenfilename(
            filetypes=[("视频文件", "*.mp4 *.avi *.mov *.flv *.mkv *.wmv *.webm *.mpeg *.mpg")]
        )
        if filename:
            self.input_path.set(filename)
            name, ext = os.path.splitext(filename)
            self.output_path.set(f"{name}.{self.output_format.get()}")
    
    def set_output_path(self):
        if not self.input_path.get():
            messagebox.showwarning("警告", "请先选择输入文件")
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
                self.output_format.set(ext[1:])
    
    def log(self, message):
        """在状态文本框中添加日志信息"""
        self.status_text.config(state=tk.NORMAL)
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.status_text.config(state=tk.DISABLED)
    
    def check_ffmpeg_installed(self):
        """检查FFmpeg是否安装"""
        try:
            subprocess.run(
                ["ffmpeg", "-version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                # text=True
                encoding='utf-8'
            )
            self.log("FFmpeg已安装，准备就绪")
            return True
        except FileNotFoundError:
            self.log("错误: 未找到FFmpeg。请安装FFmpeg并确保它在系统PATH中。")
            self.log("下载地址: https://ffmpeg.org/download.html")
            return False
    
    def update_progress(self, process):
        duration_re = re.compile(r"Duration: (\d+):(\d+):(\d+\.\d+)")
        time_re = re.compile(r"time=(\d+):(\d+):(\d+\.\d+)")
        
        duration = None
        while True:
            line = process.stderr.readline()
            if not line:
                break
            
            line.encode('utf-8', errors='ignore').decode('utf-8')
            self.log(line.strip())
            
            if not duration:
                match = duration_re.search(line)
                if match:
                    hours, minutes, seconds = match.groups()
                    duration = (
                        int(hours) * 3600 +
                        int(minutes) * 60 +
                        float(seconds)
                    )
            
            if duration:
                match = time_re.search(line)
                if match:
                    hours, minutes, seconds = match.groups()
                    current_time = (
                        int(hours) * 3600 +
                        int(minutes) * 60 +
                        float(seconds)
                    )
                    progress = (current_time / duration) * 100
                    self.progress_var.set(progress)
        
        self.progress_var.set(100)
    
    def run_conversion(self):
        input_file = self.input_path.get()
        output_file = self.output_path.get()
        format = self.output_format.get()
        
        if not input_file or not output_file:
            messagebox.showwarning("警告", "请选择输入文件和输出路径")
            self.convert_btn.config(state=tk.NORMAL)
            return
        
        if not self.check_ffmpeg_installed():
            self.convert_btn.config(state=tk.NORMAL)
            return

        cmd = [
            "ffmpeg",
            "-i", input_file,          
            "-y",                     
            # "-f", format,            
            output_file             
        ]
        
        self.log(f"开始转换: {input_file} -> {output_file}")
        self.log(f"执行命令: {' '.join(cmd)}")
        
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                # text=True
                encoding='utf-8'
            )
            
            self.update_progress(process)
            
            process.wait()
            
            if process.returncode == 0:
                self.log("转换完成!")
                messagebox.showinfo("成功", f"转换完成!\n文件保存至: {output_file}")
            else:
                self.log(f"转换失败，返回代码: {process.returncode}")
                messagebox.showerror("失败", "转换过程中发生错误")
                
        except Exception as e:
            self.log(f"错误: {str(e)}")
            messagebox.showerror("错误", f"发生错误: {str(e)}")
        
        self.convert_btn.config(state=tk.NORMAL)
    
    def start_conversion(self):
        self.convert_btn.config(state=tk.DISABLED)
        self.progress_var.set(0)
        self.status_text.config(state=tk.NORMAL)
        self.status_text.delete(1.0, tk.END)
        self.status_text.config(state=tk.DISABLED)
        
        thread = threading.Thread(target=self.run_conversion)
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoConverter(root)
    root.mainloop()

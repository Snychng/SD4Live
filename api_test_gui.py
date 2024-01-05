import os
import webuiapi
import subprocess
from PIL import Image, ImageTk
from tkinter import ttk
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from ttkbootstrap import Style
import time
import threading
import cv2
from tkinter import Canvas
from queue import Queue, Empty

from config import prompts, negative_prompts, ad_prompts, adetailer

# 全局标志变量，用于控制自动生成的开始和停止
image_count = 0
start_time = None
total_time = 0
progress_stopped = False
generate_running = False
auto_generate_running = False
image_frames = []
image_labels = []
recent_images = []
max_image_history = 8  # 最多显示8张图片

# create API client with custom host, port
api = webuiapi.WebUIApi(host='127.0.0.1', port=7860)
api.set_auth('snychng', '9081726354')
models = api.util_get_model_names()

def start_progress_bar(interval=100):
    global progress_stopped
    progress_stopped = False
    progress_bar['value'] = 0  # 初始化进度条的值为0
    progress_bar['maximum'] = 100  # 设置进度条的最大值为100
    progress_bar.stop()  # 确保停止进度条（如果之前在动）
    
    def progress():
        if progress_bar['value'] < 100 and progress_stopped == False:
            progress_bar['value'] += 1  # 每次调用增加1%
            root.after(interval, progress)  # 间隔一段时间后再次调用自身
        elif progress_stopped == False:
            progress_bar['value'] = 0  # 循环进度条：到达100%后重置为0
            root.after(interval, progress)  # 继续循环
        else:
            progress_bar.stop()

    progress()  # 启动进度条

def stop_progress_bar():
    global progress_stopped
    progress_stopped = True
    progress_bar.stop()  # 停止进度条循环
    progress_bar['value'] = 0  # 重置进度条的值为0
    progress_label.config(text="操作完成")  # 更新状态标签

def set_model(event):
    progress_label.config(text="正在切换模型，请稍等...")
    start_progress_bar()  # 开始进度条动画

    # 在新线程中切换模型以避免阻塞UI
    def switch_model_thread():
        selected_model = model_combobox.get()
        model_index = models.index(selected_model)
        api.util_set_model(models[model_index])
        api.util_wait_for_ready()
        root.after(0, stop_progress_bar)  # 在主线程中停止进度条

    # 启动新线程来切换模型
    threading.Thread(target=switch_model_thread).start()
    
def generate_image():
    global image_count, start_time, total_time, progress_stopped, generate_running, auto_generate_running
    global max_image_history, recent_images

    if not auto_generate_running and generate_running:
        return  # 如果全局变量表示停止，则立即退出函数

    progress_label.config(text="正在生成图像，请稍等...")  # 设置进度条文本
    start_progress_bar()  # 开始进度条动画

    # 在新线程中生成图像以避免阻塞UI
    def generate_image_thread():
        global image_count, start_time, total_time
        if image_count == 0:
            start_time = time.time()

        # 这里是生成图像的API调用
        result = api.txt2img(
            prompt=prompt_text.get('1.0', tk.END),
            negative_prompt=negative_prompt_text.get('1.0', tk.END),
            seed=-1,
            styles=["realistic"],
            cfg_scale=7,
            width=512,
            height=768,
            sampler_index='DPM++ SDE Karras',
            steps=28,
            alwayson_scripts=adetailer,
        )

        output_directory = "./output"
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        
        # 每张图片使用独特的文件名
        file_name = f"image_{image_count}.png"
        file_path = os.path.join(output_directory, file_name)
        result.image.save(file_path)

        # 将新图片路径添加到列表并保持列表长度不超过8
        if len(recent_images) >= max_image_history:
            # 删除最旧的图片文件
            os.remove(recent_images.pop(0))
        
        recent_images.append(file_path)

        def update_ui():
            global image_count
            image = Image.open(file_path)
            
            # 获取原始图像尺寸
            orig_width, orig_height = image.size
            
            # 计算新尺寸为原尺寸的1/4
            new_width = orig_width // 4
            new_height = orig_height // 4
            
            # 缩小图像为新尺寸
            small_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # 为缩小后的图像创建Tkinter PhotoImage对象
            tk_small_image = ImageTk.PhotoImage(small_image)
            
            # 中间面板的图片仍然使用原始大小
            tk_image = ImageTk.PhotoImage(image)

            # 将新图片添加到展示面板
            if image_count < max_image_history:
                img_label = image_labels[image_count]
            else:
                # 移除最旧的图片，并将新图片添加到最后一个位置
                img_label = image_labels.pop(0)
                image_labels.append(img_label)
            
            # 更新图片展示为缩小后的图片
            img_label.configure(image=tk_small_image)
            img_label.image = tk_small_image  # Keep a reference to avoid garbage-collection
            img_label.update()  # 更新图片显示

            # 中间面板图片控件使用原始大小图像
            image_label.configure(image=tk_image)
            image_label.image = tk_image  # Keep a reference

            # ... （后续代码不变）

            image_count += 1
            image_count_label.config(text=f"本次生成的第{image_count}张图像")
            total_time = time.time() - start_time
            average_time = total_time / image_count
            average_time_label.config(text=f"平均每张图片用时：{average_time:.2f}秒")

        # 确保UI更新在主线程中执行
        root.after(0, stop_progress_bar)
        root.after(0, update_ui)

    # 启动新线程生成图像
    threading.Thread(target=generate_image_thread).start()

def single_generate_images():
    global generate_running
    generate_running = True
    generate_image()

def auto_generate_images():
    global auto_generate_running
    while auto_generate_running:
        generate_image()
        # 这里可以根据需要添加延时
        time.sleep(20)
        if not auto_generate_running:
            break  # 如果全局变量表示停止，跳出循环

def start_auto_generate():
    global auto_generate_running
    auto_generate_running = True
    t = threading.Thread(target=auto_generate_images)
    t.start()

def stop_auto_generate():
    global auto_generate_running
    auto_generate_running = False

def run_wss_barrage_service():
    try:
        # 使用subprocess.Popen运行Catch目录内的WssBarrageService.exe，并抑制输出
        subprocess.Popen(
            ["./Catch/WssBarrageService.exe"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        progress_label.config(text="WssBarrageService.exe已启动")
    except Exception as e:
        progress_label.config(text=f"启动失败: {e}")
        
def run_msg_listening():
    try:
        video_player.start()
        # 设置Popen调用，将输出重定向到PIPE，以便可以捕获
        process = subprocess.Popen(
            ["python", "msg_listening.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,  # 以文本模式处理输出和错误
            bufsize=1,  # 行缓冲
            universal_newlines=True  # 适用于所有平台的换行符支持
        )
        progress_label.config(text="msg_listening.py正在运行...")

        # 在一个新的线程中读取输出，以避免冻结UI
        def read_output(process, output_widget):
            while True:
                output_line = process.stdout.readline()
                if output_line == '' and process.poll() is not None:
                    break
                if output_line:
                    # 插入新的输出行到文本控件
                    output_widget.insert(tk.END, output_line)
                    # 自动滚动到最新的输出行
                    output_widget.see(tk.END)
                    
                    # 限制文本控件中的行数为10
                    lines = output_widget.get('1.0', tk.END).splitlines()
                    if len(lines) > 10:
                        # 保留最新的10行，并删除其余的行
                        output_widget.delete('1.0', '2.0')
            process.stdout.close()

        # 启动线程来读取输出
        threading.Thread(target=read_output, args=(process, output_live_text)).start()

    except Exception as e:
        progress_label.config(text=f"运行失败: {e}")

def update_time_labels():
    global start_time, image_count, total_time
    
    if start_time is not None:
        current_time = time.time()
        total_time = current_time - start_time
        if image_count > 0:
            average_time = total_time / image_count
        else:
            average_time = 0

        total_time_label.config(text=f"总共用时：{total_time:.0f}秒")
        

    # 每1000毫秒调用一次自身，以更新时间
    root.after(1000, update_time_labels)

class VideoPlayer(threading.Thread):
    def __init__(self, video_folder, canvas, loop=True):
        super().__init__()
        self.video_folder = video_folder
        self.canvas = canvas
        self.loop = loop
        self.running = True
        self.frame_queue = Queue(maxsize=1)
        self.stop_event = threading.Event()
        self.video_files = self.get_video_files()
        self.current_video_index = 0

    def get_video_files(self):
        # 获取文件夹内所有视频文件
        files = [f for f in os.listdir(self.video_folder) if f.endswith(('.mp4', '.avi', '.mov'))]
        files.sort()  # 可能需要根据实际情况调整排序
        return files

    def run(self):
        while not self.stop_event.is_set():
            if self.current_video_index < len(self.video_files):
                video_path = os.path.join(self.video_folder, self.video_files[self.current_video_index])
                cap = cv2.VideoCapture(video_path)
                while not self.stop_event.is_set():
                    ret, frame = cap.read()
                    if ret:
                        if not self.frame_queue.full():
                            self.frame_queue.put(frame)
                        time.sleep(1 / 30)  # 假设视频是30fps
                    else:
                        break
                cap.release()
                self.current_video_index += 1  # 移动到下一个视频
            else:
                if self.loop:
                    self.current_video_index = 0
                else:
                    self.stop_event.set()

    def update_canvas(self):
        # 检查是否有新的帧到达
        try:
            frame = self.frame_queue.get_nowait()
            
            # 获取当前画布的尺寸
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

            # 将视频帧转换为RGB格式
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # 使用 PIL 将 NumPy 数组转换为图像
            frame_image = Image.fromarray(frame)
            
            # 调整图像大小以适应画布
            frame_image = frame_image.resize((canvas_width, canvas_height), Image.Resampling.LANCZOS)
            
            # 将图像转换为 PhotoImage
            frame_photo = ImageTk.PhotoImage(image=frame_image)
            
            # 在画布上绘制图像
            self.canvas.create_image(0, 0, anchor=tk.NW, image=frame_photo)
            self.canvas.image = frame_photo
            
        except Empty:
            # 如果队列空了，就忽略
            pass

        if self.running:
            # 每隔一段时间调用自身
            self.canvas.after(1, self.update_canvas)

    def start(self):
        super().start()
        self.update_canvas()

    def stop(self):
        self.running = False
        self.stop_event.set()
        # 清空队列以确保 run 方法可以退出
        while not self.frame_queue.empty():
            self.frame_queue.get()

# 使用更加现代的主题
style = Style(theme='minty')

# 创建主窗口
root = style.master
root.title("SD For Live")
root.geometry('1820x901')  # 设置窗口默认大小 '1249x901'


# 定义左侧面板（文本输入）中间面板（图像显示）右侧面板（图像总览）
control_panel = ttk.Frame(root, padding="10", width=401, height=849)
control_panel.grid(row=0, column=0, sticky="nswe")
view_panel = ttk.Frame(root, padding="10", width=532, height=849)
view_panel.grid(row=0, column=1, sticky="nswe")
image_history_panel = ttk.Frame(root, padding="10", width=296, height=849)
image_history_panel.grid(row=0, column=2, sticky="nswe", padx=10)  # 新面板位于第三列
video_panel = ttk.Frame(root, padding="10", width=532, height=849)
video_panel.grid(row=0, column=3, sticky="nswe", padx=10)

# 在你的UI布局代码中添加一个Canvas用于显示视频
video_canvas = Canvas(video_panel, width=532, height=849)
video_canvas.pack(side='right', fill='both', expand=True)

# 创建并启动视频播放器线程
video_folder = './videos'  # 替换为你的视频文件路径
video_player = VideoPlayer(video_folder, video_canvas, loop=True)

# 在其他全局变量定义下面添加进度条和状态标签的声明
progress_label = ttk.Label(root, text="模型状态：未开始", font=("Helvetica", 10))
progress_bar = ttk.Progressbar(root, mode='indeterminate')

# 选择模型
ttk.Label(control_panel, text="模型列表", font=("Helvetica", 10)).grid(row=0, column=0, sticky="w", pady=2)
model_combobox = ttk.Combobox(control_panel, values=models, state="readonly")
model_combobox.grid(row=1, column=0, pady=10, sticky="we")  # Adjust row accordingly
if len(models) > 22:  # 如果有足够多的模型可供选择
    model_combobox.current(22)  # 选择第23个模型（索引为22）
else:
    model_combobox.current(0)  # 否则，默认选择列表中的第一个模型
set_model(None)
stop_progress_bar()
model_combobox.bind('<<ComboboxSelected>>', set_model)

# 正面提示词的标签和文本框
ttk.Label(control_panel, text="正面提示词", font=("Helvetica", 10)).grid(row=2, column=0, sticky="w", pady=2)
prompt_text = ScrolledText(control_panel, height=5, width=50, font=("Helvetica", 10))
prompt_text.grid(row=3, column=0, pady=2, sticky="we")

# 负面提示词的标签和文本框
ttk.Label(control_panel, text="负面提示词", font=("Helvetica", 10)).grid(row=4, column=0, sticky="w", pady=2)
negative_prompt_text = ScrolledText(control_panel, height=5, width=50, font=("Helvetica", 10))
negative_prompt_text.grid(row=5, column=0, pady=2, sticky="we")

# 面部提示词的标签和文本框
ttk.Label(control_panel, text="面部提示词", font=("Helvetica", 10)).grid(row=6, column=0, sticky="w", pady=2)
ad_prompt_text = ScrolledText(control_panel, height=5, width=50, font=("Helvetica", 10))
ad_prompt_text.grid(row=7, column=0, pady=2, sticky="we")

# 修改add_placeholder函数内的颜色设置以符合默认状态
def add_placeholder(text_widget, placeholder):
    def on_focusin(event, placeholder=placeholder):
        if text_widget.get('1.0', 'end-1c') == placeholder:
            text_widget.delete('1.0', 'end')
            text_widget.config(foreground='black')  # 修改这里使用config
    
    def on_focusout(event, placeholder=placeholder):
        if not text_widget.get('1.0', 'end-1c').strip():
            text_widget.insert('1.0', placeholder)
            text_widget.config(foreground='grey')  # 修改这里使用config
    
    # 在这里也设置文本颜色为灰色
    text_widget.insert('1.0', placeholder)
    text_widget.config(foreground='grey')  # 修改这里使用config
    text_widget.bind("<FocusIn>", on_focusin)
    text_widget.bind("<FocusOut>", on_focusout)

# 设置默认提示词
add_placeholder(prompt_text, prompts)
add_placeholder(negative_prompt_text, negative_prompts)

# 添加按钮
generate_button = ttk.Button(control_panel, text="生成图像", command=generate_image)
generate_button.grid(row=8, column=0, pady=10, sticky="we")
start_auto_generate_button = ttk.Button(control_panel, text="开始自动生成", command=start_auto_generate)
start_auto_generate_button.grid(row=9, column=0, pady=10, sticky="we")
stop_auto_generate_button = ttk.Button(control_panel, text="停止自动生成", command=stop_auto_generate)
stop_auto_generate_button.grid(row=10, column=0, pady=10, sticky="we")

# 在GUI中创建按钮并绑定上面的函数
run_wss_service_button = ttk.Button(control_panel, text="启动直播监听", command=run_wss_barrage_service)
run_wss_service_button.grid(row=11, column=0, pady=10, sticky="we")  # 调整行号和列号以适应你的布局

run_msg_listening_button = ttk.Button(control_panel, text="运行抓包输出", command=run_msg_listening)
run_msg_listening_button.grid(row=12, column=0, pady=10, sticky="we")  # 调整行号和列号以适应你的布局

# 直播互动输出
ttk.Label(control_panel, text="直播消息记录", font=("Helvetica", 10)).grid(row=13, column=0, sticky="w", pady=2)
output_live_text = ScrolledText(control_panel, height=5, width=50, font=("Helvetica", 10))
output_live_text.grid(row=14, column=0, pady=2, sticky="we")

# 在UI中添加显示图像计数的标签
image_count_label = ttk.Label(view_panel, text="本次生成的第0张图像")
image_count_label.grid(row=1, column=0, pady=10, sticky="w")  # 左对齐

total_time_label = ttk.Label(view_panel, text="本次生成总用时：0秒")
total_time_label.grid(row=1, column=1, pady=10, sticky="nswe")  # 居中对齐（默认，不需要 "nswe"）

average_time_label = ttk.Label(view_panel, text="平均每张图片用时：0.00秒")
average_time_label.grid(row=1, column=2, pady=10, sticky="e")  # 右对齐

# 美化图像显示区域
default_image = Image.new('RGB', (512, 768), 'white')  # 创建一个默认白色图片
default_photo = ImageTk.PhotoImage(default_image)
image_label = ttk.Label(view_panel, image=default_photo, relief="solid", borderwidth=1)
image_label.grid(row=0, column=0, columnspan=3, pady=10, sticky="nswe")

# 保持图像的宽高比
view_panel.grid_rowconfigure(0, weight=1)
view_panel.grid_columnconfigure(0, weight=1)

# 在布局配置的最后添加进度条和标签
progress_label = ttk.Label(root, text="操作状态：未开始", font=("Helvetica", 10))
progress_bar = ttk.Progressbar(root, mode='indeterminate')
progress_label.grid(row=2, column=0, columnspan=2, sticky='ew', padx=10, pady=5)
progress_bar.grid(row=3, column=0, columnspan=2, sticky='ew', padx=10, pady=5)

# 创建8个图片标签并初始化，以4行2列的形式排列
for i in range(max_image_history):
    row = i // 2  # 确定当前框架的行号
    column = i % 2  # 确定当前框架的列号
    frame = ttk.Frame(image_history_panel, borderwidth=2, relief="groove", width=128, height=192)
    frame.grid(row=row, column=column, padx=5, pady=5)  # 使用grid而不是pack
    frame.grid_propagate(False)  # 防止框架调整到其中组件的大小
    label = ttk.Label(frame)
    label.grid(sticky="nsew")  # 让标签扩展填充整个框架
    image_frames.append(frame)
    image_labels.append(label)

# 配置image_history_panel的网格行列权重，确保它们可以扩展填充空间
for i in range(4):  # 四行
    image_history_panel.grid_rowconfigure(i, weight=1)
for j in range(2):  # 两列
    image_history_panel.grid_columnconfigure(j, weight=1)


# 配置按钮命令
generate_button.configure(command=generate_image)

# 启动定时更新时间标签的函数
update_time_labels()

# 在关闭GUI时停止视频播放线程
def on_closing():
    video_player.stop()
    video_player.join()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# 运行Tkinter事件循环
root.mainloop()
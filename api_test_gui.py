import webuiapi
from PIL import Image, ImageTk
from tkinter import ttk
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from ttkbootstrap import Style  # Import the Style class
import time
import threading

# create API client with custom host, port
api = webuiapi.WebUIApi(host='127.0.0.1', port=7860)
api.set_auth('snychng', '9081726354')

models = api.util_get_model_names()
# print("Available models:")
for idx, model in enumerate(models, 1):
    print(f"{idx}. {model}")

# Set model (find closest match)
api.util_set_model(models[23])

# Wait for job to complete
api.util_wait_for_ready()

# Initialize prompts
prompts = "(intricate details:1.2),(masterpiece:1.3),(best quality:1.4),(ultra high res:1.2),(photography:1.5),HDR,8k resolution,highest quality,detailed and intricate,(real skin texture),<lora:GuoFeng3.2_Lora:0.1>,<lora:fashionGirl_v52:0.1>,<lora:chilloutmixss30_v30:0.15>,<lora:iu_V35:0.15>,<lora:koreanDollLikeness_v15:0.1>,(1girl ),(16yo),(long hair),(skinny:1.31),thin legs,upper body,slender_waist,medium breasts,parted_lips,stirrup_legwear,black_thighhighs,a slender hand,the hand of details,the right hand,"

negative_prompts = "ng_deepnegative_v1_75t,easynegative,paintings,sketches,(worst quality, low quality:1.4),(normal quality:2),lowres,normal quality,((monochrome)),((grayscale)),(duplicate:1.331),(morbid:1.21),(mutilated:1.21),(tranny:1.331),(missing arms:1.331),(extra arms:1.331),no legs,(extra legs:1.331),extra limbs,extra digit,bad hands,bad fingers,extra fingers,(too many fingers:1.61051),missing fingers,deformed fingers,mutated hands,(fused fingers:1.61051),(poorly drawn hands:1.331),(bad anatomy:1.21),bad body,(disfigured:1.331),(bad proportions:1.331),(more than 2 nipples:1.331),skin spots,watermarks,texts,artist name,logo,acnes,skin blemishes,age spot,(outdoor:1.6),manboobs,horror,(fat ass),(bad-artist:0.7),"

ad_prompts = "(intricate details:1.2),(masterpiece:1.3),(best quality:1.4),(ultra high res:1.2),\
    (photography:1.5),HDR,8k resolution,highest quality,detailed and intricate,(real skin texture),\
    <lora:GuoFeng3.2_Lora:0.1>,<lora:fashionGirl_v52:0.1>,<lora:chilloutmixss30_v30:0.15>,\
    <lora:iu_V35:0.15>,<lora:koreanDollLikeness_v15:0.1>"

adetailer = {
    "ADetailer": {
      "args": [
        {
          "ad_model": "face_yolov8n.pt",
          "ad_prompt": ad_prompts,
          "ad_negative_prompt": "",
          "ad_confidence": 0.3,
        }
      ]
    }
  }

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

def generate_image():
    global image_count, start_time, total_time

    # 如果是第一张图片，记录开始时间
    if image_count == 0:
        start_time = time.time()

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
    
    file_path = "D:/SD4Live/output/tmp.png"
    result.image.save(file_path)
    
    # 加载图片并转换为Tkinter可用的格式
    image = Image.open(file_path)
    tk_image = ImageTk.PhotoImage(image)

    # 更新标签来展示新图片
    image_label.configure(image=tk_image)
    image_label.image = tk_image  # Keep a reference

    # 图像计数增加并更新标签
    image_count += 1
    image_count_label.config(text=f"本次生成的第{image_count}张图像")
    total_time = time.time() - start_time
    average_time = total_time / image_count
    average_time_label.config(text=f"平均每张图片用时：{average_time:.2f}秒")

# 全局标志变量，用于控制自动生成的开始和停止
auto_generate_running = False
image_count = 0
start_time = None
total_time = 0

def auto_generate_images():
    global auto_generate_running
    while auto_generate_running:
        generate_image()
        # 这里可以根据需要添加延时
        time.sleep(1)  # 1秒钟生成一张图像，根据实际情况调整

def start_auto_generate():
    global auto_generate_running
    auto_generate_running = True
    t = threading.Thread(target=auto_generate_images)
    t.start()

def stop_auto_generate():
    global auto_generate_running
    auto_generate_running = False


# ... 其余的代码保持不变 ...

# 使用更加现代的主题
style = Style(theme='minty')

# 创建主窗口
root = style.master
root.title("AI Image Generator")
root.geometry('936x800')  # 设置窗口默认大小

# 定义左侧面板（文本输入）和右侧面板（图像显示）
left_panel = ttk.Frame(root, padding="10")
left_panel.grid(row=0, column=0, sticky="nswe")
right_panel = ttk.Frame(root, padding="10")
right_panel.grid(row=0, column=1, sticky="nswe")

# 配置列权重，使右侧面板相对更宽
root.grid_columnconfigure(1, weight=3)
root.grid_rowconfigure(0, weight=1)

# 使用 Grid 布局替代 Pack
def add_labeled_textbox(parent, label, row, font=("Helvetica", 10)):
    ttk.Label(parent, text=label, font=font).grid(row=row, column=0, sticky="w", pady=2)
    text_box = ScrolledText(parent, height=5, width=50, font=font)
    text_box.grid(row=row + 1, column=0, pady=2, sticky="we")
    return text_box

# 输入框和它们的提示
prompt_text = add_labeled_textbox(left_panel, "正面提示词", 0)
negative_prompt_text = add_labeled_textbox(left_panel, "负面提示词", 2)
ad_prompt_text = add_labeled_textbox(left_panel, "面部提示词", 4)

# 设置默认提示词
add_placeholder(prompt_text, prompts)
add_placeholder(negative_prompt_text, negative_prompts)

# 添加按钮
generate_button = ttk.Button(left_panel, text="生成图像")
generate_button.grid(row=6, column=0, pady=10, sticky="we")
start_auto_generate_button = ttk.Button(left_panel, text="开始自动生成", command=start_auto_generate)
start_auto_generate_button.grid(row=7, column=0, pady=10, sticky="we")
stop_auto_generate_button = ttk.Button(left_panel, text="停止自动生成", command=stop_auto_generate)
stop_auto_generate_button.grid(row=8, column=0, pady=10, sticky="we")

# 在UI中添加显示图像计数的标签
image_count_label = ttk.Label(right_panel, text="本次生成的第0张图像")
image_count_label.grid(row=1, column=0, pady=10, sticky="nswe")

total_time_label = ttk.Label(right_panel, text="总共用时：0.00秒")
total_time_label.grid(row=2, column=0, pady=10, sticky="nswe")

average_time_label = ttk.Label(right_panel, text="平均每张图片用时：0.00秒")
average_time_label.grid(row=3, column=0, pady=10, sticky="nswe")

# 美化图像显示区域
default_image = Image.new('RGB', (512, 768), 'white')  # 创建一个默认白色图片
default_photo = ImageTk.PhotoImage(default_image)
image_label = ttk.Label(right_panel, image=default_photo, relief="solid", borderwidth=1)
image_label.grid(row=0, column=0, pady=10, sticky="nswe")

# 保持图像的宽高比
right_panel.grid_rowconfigure(0, weight=1)
right_panel.grid_columnconfigure(0, weight=1)

# 配置按钮命令
generate_button.configure(command=generate_image)

# ... 其余代码不变 ...

# 启动定时更新时间标签的函数
update_time_labels()

# 运行Tkinter事件循环
root.mainloop()
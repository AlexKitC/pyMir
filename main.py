# coding=utf-8
import tkinter as tk
from tkinter import ttk
import json
import os
from tkinter import messagebox
from PIL import Image, ImageTk
import platform

username_var = ""
password_var = ""


# 事件曲线救国
def handler_adaptor(fun, **kwds):
    return lambda event, fun=fun, kwds=kwds: fun(event, **kwds)


class App:
    def __init__(self):
        self.window = tk.Tk()
        os_str = str(platform.platform())
        # 预留 根据后期安装路径设定
        if os_str[0: 7] == "Windows":
            pass
            # self.path = "Y:/PycharmProjects/mirclient"
        elif os_str[0: 5] == "macOS":
            pass
            # self.path = os.getcwd()
        # 用户名
        self.username = ""
        # 密码
        self.password = ""
        # 角色默认性别-男
        self.sex = 0
        # 角色默认职业 0-战士 1-法师 2-道士
        self.job = 0
        # 角色-男战士序列起点
        if self.job == 0:
            self.index = 40
        elif self.job == 1:
            self.index = 80
        elif self.job == 2:
            self.index = 120
        # 屏幕宽度
        self.window_width = self.window.winfo_screenwidth()
        # 屏幕高度
        self.window_height = self.window.winfo_screenheight()
        # 解析配置文件
        # self.parse_setting()
        offsex_x = int((self.window_width - 800) / 2)
        offsex_y = int((self.window_height - 600) / 2)
        self.window.geometry(
            "%dx%d+%d+%d" % (800, 600, offsex_x, offsex_y))
        self.window.title("Alex-黑白的176Mir")
        # 主界面地图实际宽度/高度
        self.main_scene_map_width = 0
        self.main_scene_map_height = 0
        # 初始布局容器
        self.frame = tk.Frame(self.window, width=800, height=600)
        self.frame.pack()
        # 当前场景scene值 0：介绍页 1：登录界面 2开门 3角色选择界面 3主场景
        self.scene = 3
        # 渲染介绍页
        self.render_about_scene()
        # 渲染登录界面 1
        # self.render_login_scene()
        # # 渲染角色选择界面 2
        # self.render_role_scene()
        # 渲染主场景
        # self.render_main_scene(offsex_y)
        # 进入主程序事件循环
        self.window.mainloop()

    # 解析配置文件
    def parse_setting(self):
        # 检测配置文件是否存在
        if os.path.exists("setting.json"):
            # 解析配置信息
            try:
                with open("setting.json", encoding="utf8") as json_file:
                    config_obj = json.load(json_file)
                    window_size = config_obj["window"]
                    if window_size["width"] > self.window_width:
                        self.show_warn("setting.json 配置的width值大于当前窗口的最大分辨率:" + str(self.window_width) + " 当前配置值：" + str(
                            window_size["width"]))
                        self.window.destroy()
                    elif window_size["height"] > self.window_height:
                        self.show_warn(
                            "setting.json 配置的height值大于当前窗口的最大分辨率:" + str(self.window_height) + " 当前配置值：" + str(
                                window_size["height"]))
                        self.window.destroy()
                    else:
                        offsex_x = int((self.window_width - window_size["width"]) / 2)
                        offsex_y = int((self.window_height - window_size["height"]) / 2)
                        self.window.geometry(
                            "%dx%d+%d+%d" % (window_size["width"], window_size["height"], offsex_x, offsex_y))
                        self.window.title(window_size["title"])

            except BaseException as e:
                print(str(e))
                self.show_warn("解析setting.json文件发生错误，请检查配置文件是否是标准的json格式！")
                self.window.destroy()

        else:
            self.show_error("未发现项目配置文件：setting.json")

    # 渲染介绍页
    def render_about_scene(self):
        wepay = self.get_image_container()
        wepay.place(x=32, y=78)
        wepay_sources = self.get_image_sources("./sources/author/wepay.jpg", True, x=207, y=281)
        wepay.config(image=wepay_sources)
        wepay.image = wepay_sources
        alipay = self.get_image_container()
        alipay.place(x=561, y=32)
        alipay_source = self.get_image_sources("./sources/author/alipay.jpg", True, x=207, y=281)
        alipay.config(image=alipay_source)
        alipay.image = alipay_source
        tk.Label(self.frame, text="©️此版本为纯python3.8编写的1.76传奇客户端，支持mac，windows，ubuntu等所有主流系统").place(x=32, y=380)
        tk.Label(self.frame, text="©️由于作者精力有限，欢迎更多传奇爱好者加入进来一起壮大，有条件的可以扫描上方二维码支持一下作者^.^").place(x=32, y=410)
        tk.Label(self.frame, text="©️联系作者 QQ: 392999164").place(x=32, y=440)
        tk.Label(self.frame, text="©️版本持续迭代更新中......").place(x=32, y=470)
        tk.Label(self.frame, text="©️好啦！我了解作者的不容易了，我要").place(x=32, y=500)
        ttk.Button(self.frame, text="直达主题", command=lambda: self.render_login_scene()).place(x=272, y=500)

    # 渲染登录界面
    def render_login_scene(self):
        # 背景底图部分
        self.reload_frame()
        bg = self.get_image_container()
        bg.pack()
        bg_sources = self.get_image_sources("./sources/bg/login_bg.bmp")
        bg.config(image=bg_sources)
        bg.image = bg_sources

        # 中心输入部分
        login_box = self.get_image_container()
        login_box.place(x=250, y=160)
        login_box_sources = self.get_image_sources("./sources/bg/login_box.bmp")
        login_box.config(image=login_box_sources)
        login_box.image = login_box_sources

        # 登录-用户名输入框部分
        global username_var
        username_var = tk.StringVar()
        login_user_input = tk.Entry(self.frame, textvariable=username_var, bg="black", relief="flat",
                                    highlightbackground="black",
                                    bd=0, fg="white", width=17, insertbackground="white")
        login_user_input.place(x=345, y=240)

        # 登录-密码输入框部分
        global password_var
        password_var = tk.StringVar()
        login_pass_input = tk.Entry(self.frame, textvariable=password_var, bg="black", relief="flat",
                                    highlightbackground="black",
                                    bd=0, fg="white", width=17, insertbackground="white", show="*")
        login_pass_input.place(x=345, y=270)

        # 登录按钮部分
        login_btn = self.get_image_container()
        login_btn_sources = self.get_image_sources("./sources/bg/login_btn.bmp")
        login_btn.config(image=login_btn_sources)
        login_btn.image = login_btn_sources
        login_btn.bind("<Button-1>", handler_adaptor(self.do_login))
        login_btn.place(x=420, y=322)

        # 新用户
        new_user_btn = self.get_image_container()
        new_user_btn_sources = self.get_image_sources("./sources/bg/new_user_btn.bmp")
        new_user_btn.config(image=new_user_btn_sources)
        new_user_btn.image = new_user_btn_sources
        new_user_btn.bind("<Button-1>", handler_adaptor(self.do_login))
        new_user_btn.place(x=272, y=365)

        # 关闭客户端部分
        close_client_btn = self.get_image_container()
        close_client_btn_sources = self.get_image_sources("./sources/bg/close_client.bmp")
        close_client_btn.config(image=close_client_btn_sources)
        close_client_btn.image = close_client_btn_sources
        close_client_btn.place(x=502, y=188)
        close_client_btn.bind("<Button-1>", handler_adaptor(self.close_client))

    # 渲染开门界面
    def render_open_door_scene(self):
        self.reload_frame()
        index = 23
        self.bg = self.get_image_container()
        self.bg.pack()
        self.bg.after(30, self.change_door_img, index)

    # 渲染角色选择界面
    def render_role_scene(self):
        # 重制布局
        self.reload_frame()
        # 渲染背景底图
        bg = self.get_image_container()
        bg_sources = self.get_image_sources("./sources/bg/role_container.bmp")
        bg.config(image=bg_sources)
        bg.image = bg_sources
        bg.pack()
        # 开始
        start_btn = self.get_image_container()
        start_btn_sources = self.get_image_sources("./sources/bg/start_btn.bmp")
        start_btn.config(image=start_btn_sources)
        start_btn.image = start_btn_sources
        start_btn.place(x=384, y=458)
        start_btn.bind("<Button-1>", handler_adaptor(self.render_main_scene))
        # 新建角色
        new_role_btn = self.get_image_container()
        new_role_btn_sources = self.get_image_sources("./sources/bg/new_role_btn.bmp")
        new_role_btn.config(image=new_role_btn_sources)
        new_role_btn.image = new_role_btn_sources
        new_role_btn.place(x=348, y=488)
        new_role_btn.bind("<Button-1>", handler_adaptor(self.render_new_role_scene))
        # 删除角色
        del_role_btn = self.get_image_container()
        del_role_btn_sources = self.get_image_sources("./sources/bg/del_role_btn.bmp")
        del_role_btn.config(image=del_role_btn_sources)
        del_role_btn.image = del_role_btn_sources
        del_role_btn.place(x=348, y=510)
        # 制作组
        author_group_btn = self.get_image_container()
        author_group_btn_sources = self.get_image_sources("./sources/bg/author_group_btn.bmp")
        author_group_btn.config(image=author_group_btn_sources)
        author_group_btn.image = author_group_btn_sources
        author_group_btn.place(x=360, y=530)
        # 退出
        exit_btn = self.get_image_container()
        exit_btn_sources = self.get_image_sources("./sources/bg/exit_btn.bmp")
        exit_btn.config(image=exit_btn_sources)
        exit_btn.image = exit_btn_sources
        exit_btn.place(x=380, y=550)
        exit_btn.bind("<Button-1>", handler_adaptor(self.close_client))

    # 渲染新建角色
    def render_new_role_scene(self, event):
        # 渲染左侧角色部分
        self.role_img = self.get_image_container()
        role_img_sources = self.get_image_sources("./sources/role/0/000040.bmp")
        self.role_img.config(image=role_img_sources)
        self.role_img.image = role_img_sources
        self.role_img.place(x=80, y=50)
        # 执行角色动画
        global af
        af = self.role_img.after(100, self.change_role_img, self.index, self.sex)
        # 渲染右侧姓名选项卡等
        role_btn = self.get_image_container()
        role_btn_sources = self.get_image_sources("./sources/bg/edit_role.bmp", True, 260, 360)
        role_btn.config(image=role_btn_sources)
        role_btn.image = role_btn_sources
        role_btn.place(x=468, y=20)
        # 渲染职业-性别选择
        role_job_btn0 = self.get_image_container()
        role_job_btn0_sources = self.get_image_sources("./sources/bg/role0_icon.bmp", True, 38, 32)
        role_job_btn0.config(image=role_job_btn0_sources)
        role_job_btn0.image = role_job_btn0_sources
        role_job_btn0.place(x=510, y=156)
        role_job_btn0.bind("<Button-1>", handler_adaptor(self.switch_role_job, job=0))

        role_job_btn1 = self.get_image_container()
        role_job_btn1_sources = self.get_image_sources("./sources/bg/role1_icon.bmp", True, 38, 32)
        role_job_btn1.config(image=role_job_btn1_sources)
        role_job_btn1.image = role_job_btn1_sources
        role_job_btn1.place(x=548, y=156)
        role_job_btn1.bind("<Button-1>", handler_adaptor(self.switch_role_job, job=1))

        role_job_btn2 = self.get_image_container()
        role_job_btn2_sources = self.get_image_sources("./sources/bg/role2_icon.bmp", True, 38, 32)
        role_job_btn2.config(image=role_job_btn2_sources)
        role_job_btn2.image = role_job_btn2_sources
        role_job_btn2.place(x=586, y=156)
        role_job_btn2.bind("<Button-1>", handler_adaptor(self.switch_role_job, job=2))

    # 渲染游戏主界面
    def render_main_scene(self, event):
        self.scene = 3
        self.reload_frame()
        # bottom_block = self.get_image_container()
        # bottom_block_sources = self.get_image_sources_transparent(self.path + "/sources/bg/bottom_block.bmp", True, width=800, height=251)
        # bottom_block.config(image=bottom_block_sources)
        # bottom_block.image = bottom_block_sources
        # bottom_block.pack(side="bottom")
        self.open_map_bin()

    # 打开map文件
    def open_map_bin(self):
        # 读取地图map文件
        res_map = open("./sources/map/0.map", "rb")
        # byte 索引
        i = 0
        # 解析 0～3 前面4个字节得到宽和高
        while i < 4:
            res_map.seek(i, 0)
            tmp = res_map.read(1)
            # 地图宽度
            if i == 0:
                self.main_scene_map_width = self.main_scene_map_width + int(tmp[0])
            if i == 1:
                self.main_scene_map_width = self.main_scene_map_width + int(tmp[0] << 8)
            # 地图高度
            if i == 2:
                self.main_scene_map_height = self.main_scene_map_height + int(tmp[0])
            if i == 3:
                self.main_scene_map_height = self.main_scene_map_height + int(tmp[0] << 8)
            i = i + 1
        # 开始解析除开map header头【共52 byte以外的字节】 每12byte为一个tile块 800x600需要大约16个tile
        # 定义list保存 [(0,0), (0,1), ...]
        list_map = []
        offset = 53
        for i in range(700):
            if i % 2 == 0:
                tmp_list = []
                for j in range(700):
                    if j % 2 == 0:
                        res_map.seek(offset + j * 14 + i * 14, 0)
                        tmp = res_map.read(1)
                        tmp_byte1 = int(tmp[0])
                        res_map.seek(offset + 1 + j * 14 + i * 14, 0)
                        tmp = res_map.read(1)
                        tmp_byte2 = int(tmp[0] << 8)
                        tmp_list.append(tmp_byte1 + tmp_byte2)
                list_map.append(tmp_list)
        res_map = []
        print(list_map)
        tmp_x = 0
        tmp_y = 64
        for i in range(18):
            if i % 2 == 0:
                for j in range(12):
                    if j % 2 == 0:
                        bg_sources_name = ""
                        if 10 > list_map[i][j] >= 0:
                            bg_sources_name = "./sources/data/tiles/" + '0000' + str(list_map[i][j]) + '.BMP'
                        elif 100 > list_map[i][j] >= 10:
                            bg_sources_name = "./sources/data/tiles/" + '000' + str(list_map[i][j]) + '.BMP'
                        elif 1000 > list_map[i][j] >= 100:
                            bg_sources_name = "./sources/data/tiles/" + '00' + str(list_map[i][j]) + '.BMP'
                        elif 10000 > list_map[i][j] >= 1000:
                            bg_sources_name = "./sources/data/tiles/" + '0' + str(list_map[i][j]) + '.BMP'
                        else:
                            bg_sources_name = "./sources/data/tiles/" + str(list_map[i][j]) + '.BMP'
                        bg = self.get_image_container()
                        bg_sources = self.get_image_sources(bg_sources_name)
                        bg.config(image=bg_sources)
                        bg.image = bg_sources
                        bg.place(x=tmp_x, y=tmp_y)
                        tmp_y = tmp_y + 64
                tmp_y = 0
                tmp_x = tmp_x + 96
        bottom_elem = self.get_image_container()
        bottom_elem_sources = self.get_image_sources("./sources/bg/bottom_block.png")
        bottom_elem.config(image=bottom_elem_sources)
        bottom_elem.image = bottom_elem_sources
        bottom_elem.place(x=0, y=349)

    # 处理黑色转化为透明
    def transparent_back(self, img):
        img = img.convert('RGBA')
        L, H = img.size
        for h in range(H):
            for l in range(L):
                dot = (l, h)
                color_1 = img.getpixel(dot)
                if color_1 == (0, 0, 0, 255):
                    color_1 = color_1[:-1] + (0,)
                    # print(color_1)
                    img.putpixel(dot, (165, 140, 99, 255))
        # img.save("./sources/bg/bottom_block.png")
        return img

    # 重新初始化场景
    def reload_frame(self):
        self.frame.destroy()
        self.frame = tk.Frame(self.window, width=800, height=600)
        self.frame.pack()

    # 开门序列
    def change_door_img(self, index):
        source_name = "./sources/login/0000" + str(index) + ".bmp"
        bg_sources = self.get_image_sources(source_name, True)
        self.bg.config(image=bg_sources)
        self.bg.image = bg_sources
        self.bg.update()
        index = index + 1
        global af
        if index < 33:
            af = self.bg.after(30, self.change_door_img, index)
        else:
            self.bg.after_cancel(af)
            self.render_role_scene()

    # 渲染角色选择界面人物动画
    def change_role_img(self, index, sex):
        source_name = "./sources/role/" + str(self.job) + "/0000" + str(index) + ".bmp"
        if self.job == 2:
            source_name = "./sources/role/2/000" + str(index) + ".bmp"
        global af
        try:
            bg_source = self.get_image_sources(source_name)
            self.role_img.config(image=bg_source)
            self.role_img.image = bg_source
            self.role_img.update()
            self.index = index + 1
            if self.job == 0:
                if index < 55:
                    af = self.role_img.after(100, self.change_role_img, self.index, sex)
                else:
                    self.role_img.after_cancel(af)
                    self.index = 40
                    af = self.role_img.after(100, self.change_role_img, self.index, sex)
            elif self.job == 1:
                if index < 95:
                    af = self.role_img.after(100, self.change_role_img, self.index, sex)
                else:
                    self.role_img.after_cancel(af)
                    self.index = 80
                    af = self.role_img.after(100, self.change_role_img, self.index, sex)
            elif self.job == 2:
                if index < 135:
                    af = self.role_img.after(100, self.change_role_img, self.index, sex)
                else:
                    self.role_img.after_cancel(af)
                    self.index = 120
                    af = self.role_img.after(100, self.change_role_img, self.index, sex)
        except BaseException:
            self.role_img.after_cancel(af)
            af = self.role_img.after(100, self.change_role_img, self.index, sex)

    # 关闭客户端
    def close_client(self, event):
        self.window.destroy()

    # 执行登录动作
    def do_login(self, event):
        global username_var
        self.username = username_var.get()
        if len(self.username) == 0:
            self.show_warn("账户不能为空")
            return False
        elif len(self.username) > 15:
            self.show_warn("账户长度过长")
            return False
        global password_var
        self.password = password_var.get()
        if len(self.password) == 0:
            self.show_warn("密码不能为空")
            return False
        elif len(self.password) > 15:
            self.show_warn("密码长度过长")
            return False
        else:
            # todo...发起请求
            # pass
            self.render_open_door_scene()

    # 切换角色
    def switch_role_job(self, event, job):
        global af
        if job == 0:
            if self.job != 0:
                # 清除原有的图片序列
                self.role_img.after_cancel(af)
                self.change_role_img(index=self.index, sex=self.sex)
            self.job = 0
            self.index = 40
        elif job == 1:
            if self.job != 1:
                # 清除原有的图片序列
                self.role_img.after_cancel(af)
                self.change_role_img(index=self.index, sex=self.sex)
            self.job = 1
            self.index = 80
        elif job == 2:
            if self.job != 2:
                # 清除原有的图片序列
                self.role_img.after_cancel(af)
                self.change_role_img(index=self.index, sex=self.sex)
            self.job = 2
            self.index = 120

    # 返回打开的Image资源
    @staticmethod
    def get_image_sources(path, resize=False, x=800, y=600):
        if resize:
            return ImageTk.PhotoImage(Image.open(path).resize((x, y), Image.ANTIALIAS))
        else:
            return ImageTk.PhotoImage(Image.open(path), Image.ANTIALIAS)

    # 返回打开的Image处理黑色为透明的图片资源
    def get_image_sources_transparent(self, path, resize=False, width=800, height=600):
        if resize:
            return ImageTk.PhotoImage(self.transparent_back(Image.open(path).resize((width, height))))
        else:
            return ImageTk.PhotoImage(self.transparent_back(Image.open(path)))

    # 返回装载Image资源的Label无边框的容器
    def get_image_container(self):
        return tk.Label(self.frame, borderwidth=0, highlightthickness=0)

    # waring
    @staticmethod
    def show_warn(message="", title="警告"):
        messagebox.showwarning(title, message)

    # info
    @staticmethod
    def show_info(message="", title="提示"):
        messagebox.showinfo(title, message)

    # error
    @staticmethod
    def show_error(message="", title="错误"):
        messagebox.showerror(title, message)


# 入口执行
if __name__ == "__main__":
    App()

import pywinauto
from pywinauto.application import Application
import time
import tkinter as tk
from tkinter import ttk, messagebox


class WeChatAutomationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("微信自动化控制台")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        # 创建样式
        self.style = ttk.Style()
        self.style.configure("TButton", padding=6, font=('Arial', 10))
        self.style.configure("Title.TLabel", font=('Arial', 16, 'bold'))
        self.style.configure("Subtitle.TLabel", font=('Arial', 12))
        self.style.configure("Treeview", font=('Arial', 10))
        self.style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))

        # 创建主框架
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 标题
        title_label = ttk.Label(main_frame, text="微信自动化控制台", style="Title.TLabel")
        title_label.pack(pady=10)

        # 副标题
        subtitle_label = ttk.Label(main_frame,
                                   text="使用 PyWinAuto 获取微信所有按钮和输入框控件",
                                   style="Subtitle.TLabel")
        subtitle_label.pack(pady=5)

        # 控制按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)

        # 连接微信按钮
        self.connect_btn = ttk.Button(button_frame, text="连接微信", command=self.connect_wechat)
        self.connect_btn.pack(side=tk.LEFT, padx=5)

        # 获取控件按钮
        self.get_controls_btn = ttk.Button(button_frame, text="获取控件", command=self.get_controls)
        self.get_controls_btn.pack(side=tk.LEFT, padx=5)
        self.get_controls_btn.state(['disabled'])

        # 状态标签
        self.status_var = tk.StringVar(value="状态: 未连接微信")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, font=('Arial', 10))
        status_label.pack(pady=5)

        # 创建树形视图显示控件
        self.tree_frame = ttk.Frame(main_frame)
        self.tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # 创建滚动条
        scrollbar = ttk.Scrollbar(self.tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 创建树形视图
        self.tree = ttk.Treeview(
            self.tree_frame,
            columns=("control_id", "class_name", "text", "rect"),
            show="headings",
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.tree.yview)

        # 设置列标题
        self.tree.heading("control_id", text="控件ID")
        self.tree.heading("class_name", text="类名")
        self.tree.heading("text", text="文本内容")
        self.tree.heading("rect", text="位置和大小")

        # 设置列宽
        self.tree.column("control_id", width=80, anchor=tk.CENTER)
        self.tree.column("class_name", width=120, anchor=tk.CENTER)
        self.tree.column("text", width=250)
        self.tree.column("rect", width=200, anchor=tk.CENTER)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # 底部状态栏
        self.info_var = tk.StringVar(value="就绪")
        info_label = ttk.Label(main_frame, textvariable=self.info_var, font=('Arial', 9))
        info_label.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

        # 存储微信应用对象
        self.app = None

    def connect_wechat(self):
        """连接到微信进程"""
        try:
            self.info_var.set("正在连接微信...")
            self.root.update()

            # 尝试连接到微信进程
            self.app = Application(backend="uia").connect(path="Weixin.exe")
            time.sleep(1)  # 等待连接稳定

            # 获取微信主窗口
            self.wechat_window = self.app.window(title_re=".*微信.*")
            self.status_var.set(f"状态: 已连接到微信 (版本: {self.get_wechat_version()})")
            self.get_controls_btn.state(['!disabled'])
            self.info_var.set("连接成功！点击'获取控件'按钮查看微信界面控件")

        except Exception as e:
            messagebox.showerror("连接错误", f"无法连接到微信进程: {str(e)}\n\n请确保微信已启动并登录")
            self.info_var.set(f"错误: {str(e)}")
            self.status_var.set("状态: 连接失败")

    def get_controls(self):
        """获取微信界面中的所有按钮和输入框控件"""
        if not self.app:
            messagebox.showwarning("未连接", "请先连接微信")
            return

        try:
            self.info_var.set("正在获取微信控件信息...")
            self.root.update()

            # 清空树形视图
            for item in self.tree.get_children():
                self.tree.delete(item)

            # 获取所有按钮控件
            buttons = self.wechat_window.descendants(control_type="Button")
            # 获取所有编辑框控件（输入框）
            edit_boxes = self.wechat_window.descendants(control_type="Edit")

            # 显示控件总数
            self.status_var.set(f"状态: 找到 {len(buttons)} 个按钮, {len(edit_boxes)} 个输入框")

            # 添加按钮到树形视图
            for idx, button in enumerate(buttons):
                try:
                    rect = button.rectangle()
                    rect_str = f"({rect.left}, {rect.top}) - ({rect.right}, {rect.bottom})"
                    self.tree.insert("", tk.END, values=(
                        f"Button-{idx + 1}",
                        button.friendly_class_name(),
                        button.window_text()[:50] or "N/A",
                        rect_str
                    ))
                except Exception as e:
                    print(f"获取按钮信息出错: {str(e)}")

            # 添加输入框到树形视图
            for idx, edit in enumerate(edit_boxes):
                try:
                    rect = edit.rectangle()
                    rect_str = f"({rect.left}, {rect.top}) - ({rect.right}, {rect.bottom})"
                    self.tree.insert("", tk.END, values=(
                        f"Edit-{idx + 1}",
                        edit.friendly_class_name(),
                        edit.window_text()[:50] or "N/A",
                        rect_str
                    ))
                except Exception as e:
                    print(f"获取输入框信息出错: {str(e)}")

            self.info_var.set(f"控件获取完成！共找到 {len(buttons)} 个按钮和 {len(edit_boxes)} 个输入框")

        except Exception as e:
            messagebox.showerror("错误", f"获取控件时出错: {str(e)}")
            self.info_var.set(f"错误: {str(e)}")

    def get_wechat_version(self):
        """获取微信版本信息"""
        try:
            # 尝试获取微信版本信息
            process = self.app.process
            for mod in process.modules():
                if mod.name.lower() == "wechatwin.dll":
                    return mod.FileVersion
            return "未知版本"
        except:
            return "未知版本"


if __name__ == "__main__":
    root = tk.Tk()
    app = WeChatAutomationApp(root)
    root.mainloop()
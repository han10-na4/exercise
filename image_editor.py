import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os

class ImageEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("이미지 편집기")
        self.root.geometry("800x600")
        self.root.minsize(800, 600)
        
        # 스타일 설정
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Segoe UI', 10))
        self.style.configure('TLabel', font=('Segoe UI', 10))
        
        # 변수 초기화
        self.original_image = None
        self.displayed_image = None
        self.photo_image = None
        self.current_width = 0
        self.current_height = 0
        
        self.create_widgets()
        
    def create_widgets(self):
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 상단 도구 모음
        toolbar = ttk.Frame(main_frame)
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        # 파일 버튼
        file_btn = ttk.Button(toolbar, text="파일 열기", command=self.open_file)
        file_btn.pack(side=tk.LEFT, padx=5)
        
        save_btn = ttk.Button(toolbar, text="저장", command=self.save_file)
        save_btn.pack(side=tk.LEFT, padx=5)
        
        # 크기 조정 프레임
        resize_frame = ttk.LabelFrame(toolbar, text="크기 조정", padding="5")
        resize_frame.pack(side=tk.LEFT, padx=20)
        
        # 너비 조정
        ttk.Label(resize_frame, text="너비:").grid(row=0, column=0, padx=5)
        self.width_var = tk.StringVar()
        self.width_entry = ttk.Entry(resize_frame, textvariable=self.width_var, width=8)
        self.width_entry.grid(row=0, column=1, padx=5)
        
        # 높이 조정
        ttk.Label(resize_frame, text="높이:").grid(row=0, column=2, padx=5)
        self.height_var = tk.StringVar()
        self.height_entry = ttk.Entry(resize_frame, textvariable=self.height_var, width=8)
        self.height_entry.grid(row=0, column=3, padx=5)
        
        # 비율 유지 체크박스
        self.keep_ratio = tk.BooleanVar(value=True)
        ttk.Checkbutton(resize_frame, text="비율 유지", variable=self.keep_ratio).grid(row=0, column=4, padx=5)
        
        # 적용 버튼
        apply_btn = ttk.Button(resize_frame, text="적용", command=self.apply_resize)
        apply_btn.grid(row=0, column=5, padx=5)
        
        # 이미지 표시 영역
        self.canvas = tk.Canvas(main_frame, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # 상태 표시줄
        self.status_var = tk.StringVar()
        self.status_var.set("준비")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, pady=(10, 0))
        
    def open_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("이미지 파일", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("모든 파일", "*.*")
            ]
        )
        
        if file_path:
            try:
                self.original_image = Image.open(file_path)
                self.current_width = self.original_image.width
                self.current_height = self.original_image.height
                
                # 현재 크기를 입력 필드에 표시
                self.width_var.set(str(self.current_width))
                self.height_var.set(str(self.current_height))
                
                self.display_image()
                self.status_var.set(f"이미지 로드됨: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("오류", f"이미지를 열 수 없습니다: {str(e)}")
    
    def save_file(self):
        if self.displayed_image is None:
            messagebox.showwarning("경고", "저장할 이미지가 없습니다.")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG 파일", "*.png"),
                ("JPEG 파일", "*.jpg"),
                ("모든 파일", "*.*")
            ]
        )
        
        if file_path:
            try:
                self.displayed_image.save(file_path)
                self.status_var.set(f"이미지 저장됨: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("오류", f"이미지를 저장할 수 없습니다: {str(e)}")
    
    def apply_resize(self):
        if self.original_image is None:
            messagebox.showwarning("경고", "이미지를 먼저 열어주세요.")
            return
            
        try:
            new_width = int(self.width_var.get())
            new_height = int(self.height_var.get())
            
            if new_width <= 0 or new_height <= 0:
                messagebox.showwarning("경고", "크기는 0보다 커야 합니다.")
                return
                
            # 비율 유지가 체크되어 있고 너비가 변경된 경우
            if self.keep_ratio.get() and new_width != self.current_width:
                ratio = new_width / self.current_width
                new_height = int(self.current_height * ratio)
                self.height_var.set(str(new_height))
            
            # 비율 유지가 체크되어 있고 높이가 변경된 경우
            elif self.keep_ratio.get() and new_height != self.current_height:
                ratio = new_height / self.current_height
                new_width = int(self.current_width * ratio)
                self.width_var.set(str(new_width))
            
            self.displayed_image = self.original_image.resize((new_width, new_height), Image.LANCZOS)
            self.current_width = new_width
            self.current_height = new_height
            
            self.display_image()
            self.status_var.set(f"이미지 크기 조정됨: {new_width}x{new_height}")
            
        except ValueError:
            messagebox.showerror("오류", "올바른 숫자를 입력하세요.")
    
    def display_image(self):
        if self.displayed_image is None:
            self.displayed_image = self.original_image
            
        # 캔버스 크기에 맞게 이미지 크기 조정
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # 이미지 비율 유지하면서 캔버스에 맞추기
        img_ratio = self.displayed_image.width / self.displayed_image.height
        canvas_ratio = canvas_width / canvas_height
        
        if img_ratio > canvas_ratio:
            # 이미지가 캔버스보다 더 넓은 경우
            display_width = canvas_width
            display_height = int(canvas_width / img_ratio)
        else:
            # 이미지가 캔버스보다 더 높은 경우
            display_height = canvas_height
            display_width = int(canvas_height * img_ratio)
            
        # 이미지 리사이즈
        resized_image = self.displayed_image.resize((display_width, display_height), Image.LANCZOS)
        self.photo_image = ImageTk.PhotoImage(resized_image)
        
        # 캔버스 지우기
        self.canvas.delete("all")
        
        # 이미지 중앙에 배치
        x = (canvas_width - display_width) // 2
        y = (canvas_height - display_height) // 2
        self.canvas.create_image(x, y, anchor=tk.NW, image=self.photo_image)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditor(root)
    root.mainloop() 
"""
Video Downloader - TikTok / Douyin / YouTube
Simple GUI for downloading videos
Made by WITHYM
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import subprocess
import sys
from datetime import datetime
import hashlib
import base64
import ctypes

# Import download functions
from controller.DouyinExtract import download_tiktok_douyin_video
from controller.ThreadsExtract import download_threads_video, ThreadsDownloadError

# Windows Registry for persistent storage
if sys.platform == "win32":
    import winreg

# Language translations
LANGUAGES = {
    'ko': {
        'title': 'Video Downloader',
        'subtitle': 'TikTok · Douyin · YouTube · Threads',
        'url_label': '비디오 URL',
        'url_placeholder': '링크를 붙여넣으세요...',
        'save_to': '저장 위치',
        'change': '변경',
        'download': '다운로드',
        'made_by': 'Made by WITHYM',
        'status_ready': '준비됨',
        'status_checking': '{} 비디오 확인 중...',
        'status_downloading': '{} 비디오 다운로드 중...',
        'status_complete': '✓ 다운로드 완료: {}',
        'status_failed': '✗ 실패: {}',
        'error_no_url': 'URL을 입력해주세요',
        'error_invalid_url': '올바른 URL이 아닙니다',
        'error_unsupported': '지원하지 않는 플랫폼입니다',
        'complete_title': '완료',
        'complete_message': '다운로드 완료!\n\n폴더를 여시겠습니까?',
        'error_title': '오류',
        'error_message': '다운로드 실패:\n{}',
        'ytdlp_required_title': 'yt-dlp 필요',
        'ytdlp_required_message': 'YouTube 다운로드를 위해 yt-dlp가 필요합니다.\n\n설치 명령어:\npip install yt-dlp\n\n지금 설치하시겠습니까?',
        'ytdlp_installing': 'yt-dlp 설치 중...',
        'ytdlp_success': 'yt-dlp 설치 성공!',
        'ytdlp_failed': '설치 실패',
        'auth_required': '인증 필요',
        'enter_password': '암호를 입력하세요:',
        'auth_failed': '인증 실패',
        'invalid_password': '잘못된 암호입니다.',
        'trial_expired': '사용 기간 만료',
        'trial_expired_message': '30일 사용 기간이 만료되었습니다.\n프로그램을 종료합니다.',
        'days_remaining': '남은 사용 기간: {}일',
        'confirm': '확인',
        'cancel': '취소',
        'attempts_remaining': '남은 시도: {}',
    },
    'en': {
        'title': 'Video Downloader',
        'subtitle': 'TikTok · Douyin · YouTube · Threads',
        'url_label': 'Video URL',
        'url_placeholder': 'Paste link here...',
        'save_to': 'Save to',
        'change': 'Change',
        'download': 'Download',
        'made_by': 'Made by WITHYM',
        'status_ready': 'Ready',
        'status_checking': 'Checking {} video...',
        'status_downloading': 'Downloading {} video...',
        'status_complete': '✓ Downloaded: {}',
        'status_failed': '✗ Failed: {}',
        'error_no_url': 'Please enter a URL',
        'error_invalid_url': 'Invalid URL',
        'error_unsupported': 'Unsupported platform',
        'complete_title': 'Complete',
        'complete_message': 'Download complete!\n\nOpen folder?',
        'error_title': 'Error',
        'error_message': 'Download failed:\n{}',
        'ytdlp_required_title': 'yt-dlp Required',
        'ytdlp_required_message': 'yt-dlp is required for YouTube downloads.\n\nInstall command:\npip install yt-dlp\n\nInstall now?',
        'ytdlp_installing': 'Installing yt-dlp...',
        'ytdlp_success': 'yt-dlp installed successfully!',
        'ytdlp_failed': 'Installation failed',
        'auth_required': 'Authentication Required',
        'enter_password': 'Enter password:',
        'auth_failed': 'Authentication Failed',
        'invalid_password': 'Invalid password.',
        'trial_expired': 'Trial Expired',
        'trial_expired_message': '30-day trial period has expired.\nProgram will exit.',
        'days_remaining': 'Days remaining: {}',
        'confirm': 'Confirm',
        'cancel': 'Cancel',
        'attempts_remaining': 'Attempts remaining: {}',
    },
    'ja': {
        'title': 'Video Downloader',
        'subtitle': 'TikTok · Douyin · YouTube · Threads',
        'url_label': 'ビデオURL',
        'url_placeholder': 'リンクを貼り付けてください...',
        'save_to': '保存先',
        'change': '変更',
        'download': 'ダウンロード',
        'made_by': 'Made by WITHYM',
        'status_ready': '準備完了',
        'status_checking': '{}動画を確認中...',
        'status_downloading': '{}動画をダウンロード中...',
        'status_complete': '✓ ダウンロード完了: {}',
        'status_failed': '✗ 失敗: {}',
        'error_no_url': 'URLを入力してください',
        'error_invalid_url': '無効なURLです',
        'error_unsupported': 'サポートされていないプラットフォームです',
        'complete_title': '完了',
        'complete_message': 'ダウンロード完了！\n\nフォルダを開きますか？',
        'error_title': 'エラー',
        'error_message': 'ダウンロード失敗:\n{}',
        'ytdlp_required_title': 'yt-dlp が必要',
        'ytdlp_required_message': 'YouTubeダウンロードにはyt-dlpが必要です。\n\nインストールコマンド:\npip install yt-dlp\n\n今すぐインストールしますか？',
        'ytdlp_installing': 'yt-dlpをインストール中...',
        'ytdlp_success': 'yt-dlpインストール成功！',
        'ytdlp_failed': 'インストール失敗',
        'auth_required': '認証が必要',
        'enter_password': 'パスワードを入力:',
        'auth_failed': '認証失敗',
        'invalid_password': '無効なパスワードです。',
        'trial_expired': '試用期間終了',
        'trial_expired_message': '30日間の試用期間が終了しました。\nプログラムを終了します。',
        'days_remaining': '残り日数: {}日',
        'confirm': '確認',
        'cancel': 'キャンセル',
        'attempts_remaining': '残り試行回数: {}',
    }
}


class LicenseManager:
    """License and authentication manager"""

    _P_SEGMENTS = (
        "f5004da5",
        "63fb2544",
        "00b4aa3b",
        "6b010767",
    )  # Obfuscated credential hash (MD5 of 'agc')
    _P = "".join(_P_SEGMENTS)
    _TRIAL_DAYS = 30

    if sys.platform == "win32":
        _REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Explorer"
        _REG_KEY_1 = "LayoutState"  # Disguised as Windows setting
        _REG_KEY_2 = "IconUnderline"  # Disguised as Windows setting
        _FILE_DIR = os.path.join(
            os.getenv("LOCALAPPDATA", os.path.expanduser("~")),
            "Microsoft",
            "Explorer"
        )
        _FILE_NAME = "UsageCache.bin"
        _FILE_PATH = os.path.join(_FILE_DIR, _FILE_NAME)

    @staticmethod
    def _hash(text):
        """Hash text"""
        return hashlib.md5(text.encode()).hexdigest()

    @staticmethod
    def _encode(data):
        """Encode data"""
        return base64.b64encode(data.encode()).decode()

    @staticmethod
    def _decode(data):
        """Decode data"""
        try:
            return base64.b64decode(data.encode()).decode()
        except Exception:
            return None

    @staticmethod
    def _get_registry_value(key_name):
        """Get value from Windows Registry"""
        if sys.platform != "win32":
            return None
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, LicenseManager._REG_PATH, 0, winreg.KEY_READ)
            value, _ = winreg.QueryValueEx(key, key_name)
            winreg.CloseKey(key)
            return value
        except Exception:
            return None

    @staticmethod
    def _set_registry_value(key_name, value):
        """Set value in Windows Registry"""
        if sys.platform != "win32":
            return False
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, LicenseManager._REG_PATH, 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, key_name, 0, winreg.REG_SZ, value)
            winreg.CloseKey(key)
            return True
        except FileNotFoundError:
            try:
                key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, LicenseManager._REG_PATH)
                winreg.SetValueEx(key, key_name, 0, winreg.REG_SZ, value)
                winreg.CloseKey(key)
                return True
            except Exception:
                return False
        except Exception:
            return False

    @staticmethod
    def _ensure_file_dir():
        """Ensure hidden storage directory exists"""
        if sys.platform != "win32":
            return False
        try:
            os.makedirs(LicenseManager._FILE_DIR, exist_ok=True)
            return True
        except Exception:
            return False

    @staticmethod
    def _hide_file(path):
        """Mark file as hidden on Windows"""
        if sys.platform != "win32":
            return
        try:
            FILE_ATTRIBUTE_HIDDEN = 0x02
            ctypes.windll.kernel32.SetFileAttributesW(path, FILE_ATTRIBUTE_HIDDEN)
        except Exception:
            pass

    @staticmethod
    def _get_registry_pair():
        """Return encoded activation date and verification hash from registry"""
        if sys.platform != "win32":
            return None, None
        encoded = LicenseManager._get_registry_value(LicenseManager._REG_KEY_1)
        verification_hash = LicenseManager._get_registry_value(LicenseManager._REG_KEY_2)
        return encoded, verification_hash

    @staticmethod
    def _set_registry_pair(encoded, verification_hash):
        """Persist activation data to registry"""
        if sys.platform != "win32":
            return True
        success1 = LicenseManager._set_registry_value(LicenseManager._REG_KEY_1, encoded)
        success2 = LicenseManager._set_registry_value(LicenseManager._REG_KEY_2, verification_hash)
        return success1 and success2

    @staticmethod
    def _get_file_pair():
        """Return encoded activation date and verification hash from hidden file"""
        if sys.platform != "win32":
            return None, None
        try:
            if not os.path.exists(LicenseManager._FILE_PATH):
                return None, None
            with open(LicenseManager._FILE_PATH, "r", encoding="utf-8") as hidden_file:
                raw = hidden_file.read().strip()
            decoded = LicenseManager._decode(raw)
            if not decoded or "|" not in decoded:
                return None, None
            encoded, verification_hash = decoded.split("|", 1)
            return encoded, verification_hash
        except Exception:
            return None, None

    @staticmethod
    def _write_file_pair(encoded, verification_hash):
        """Persist activation data to hidden file"""
        if sys.platform != "win32":
            return True
        try:
            if not LicenseManager._ensure_file_dir():
                return False
            payload = f"{encoded}|{verification_hash}"
            encoded_payload = LicenseManager._encode(payload)
            with open(LicenseManager._FILE_PATH, "w", encoding="utf-8") as hidden_file:
                hidden_file.write(encoded_payload)
            LicenseManager._hide_file(LicenseManager._FILE_PATH)
            return True
        except Exception:
            return False

    @staticmethod
    def _validate_pair(encoded, verification_hash):
        """Validate activation data pair"""
        if not encoded or not verification_hash:
            return False, None
        decoded = LicenseManager._decode(encoded)
        if not decoded:
            return False, None
        expected_hash = LicenseManager._hash(decoded + LicenseManager._P)
        if verification_hash != expected_hash:
            return False, None
        return True, decoded

    @staticmethod
    def _get_activation_info():
        """Return validated activation info and repair missing storage"""
        sources = []
        if sys.platform == "win32":
            reg_encoded, reg_hash = LicenseManager._get_registry_pair()
            file_encoded, file_hash = LicenseManager._get_file_pair()
            sources.extend([
                ("registry", reg_encoded, reg_hash),
                ("file", file_encoded, file_hash)
            ])
        else:
            reg_encoded, reg_hash = LicenseManager._get_registry_pair()
            sources.append(("registry", reg_encoded, reg_hash))

        for source_name, encoded, verification_hash in sources:
            valid, decoded = LicenseManager._validate_pair(encoded, verification_hash)
            if valid:
                if sys.platform == "win32":
                    current_reg = LicenseManager._get_registry_pair()
                    current_file = LicenseManager._get_file_pair()
                    if current_reg != (encoded, verification_hash):
                        LicenseManager._set_registry_pair(encoded, verification_hash)
                    if current_file != (encoded, verification_hash):
                        LicenseManager._write_file_pair(encoded, verification_hash)
                return decoded, encoded, verification_hash

        return None, None, None

    @staticmethod
    def verify_password(password):
        """Verify password"""
        return LicenseManager._hash(password) == LicenseManager._P

    @staticmethod
    def is_activated():
        """Check if application is activated"""
        decoded, _, _ = LicenseManager._get_activation_info()
        return decoded is not None

    @staticmethod
    def activate():
        """Activate the application"""
        today = datetime.now().strftime("%Y%m%d")
        encoded_date = LicenseManager._encode(today)
        verification_hash = LicenseManager._hash(today + LicenseManager._P)

        stored = True
        if sys.platform == "win32":
            stored = LicenseManager._set_registry_pair(encoded_date, verification_hash)
            stored = stored and LicenseManager._write_file_pair(encoded_date, verification_hash)
        else:
            stored = LicenseManager._set_registry_pair(encoded_date, verification_hash)

        return stored

    @staticmethod
    def get_days_remaining():
        """Get remaining trial days"""
        decoded, _, _ = LicenseManager._get_activation_info()
        if not decoded:
            return 0
        try:
            activation_date = datetime.strptime(decoded, "%Y%m%d")
            today = datetime.now()
            days_passed = (today - activation_date).days
            remaining = LicenseManager._TRIAL_DAYS - days_passed
            return max(0, remaining)
        except Exception:
            return 0

    @staticmethod
    def is_trial_valid():
        """Check if trial is still valid"""
        return LicenseManager.get_days_remaining() > 0


class VideoDownloader:
    def __init__(self, root):
        self.root = root
        self.current_lang = 'ko'  # Default: Korean

        # Colors
        self.bg = "#ffffff"
        self.accent = "#4CAF50"
        self.text_dark = "#333333"
        self.text_light = "#666666"
        self.lang_button_bg = "#f0f0f0"

        self.root.configure(bg=self.bg)

        # Fonts - Seoul Hangang
        self.font_family = self.get_korean_font()

        # Try to set icon
        try:
            if os.path.exists('icon.ico'):
                self.root.iconbitmap('icon.ico')
            elif os.path.exists('icon.png'):
                icon_img = tk.PhotoImage(file='icon.png')
                self.root.iconphoto(True, icon_img)
        except:
            pass

        # Download folder
        self.download_folder = os.path.join(os.path.expanduser("~"), "Downloads", "Videos")
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)

        self.is_downloading = False
        self.authenticated = False

        self.setup_ui()
        self.update_language()
        self.check_dependencies()

        self.root.after(10, self.require_authentication)

    def require_authentication(self):
        """Launch password dialog after UI is ready"""
        if self.authenticated:
            return

        if not self.root.winfo_exists():
            return

        try:
            self.root.focus_force()
            self.root.lift()
        except Exception:
            pass

        try:
            self.root.attributes("-disabled", True)
        except Exception:
            pass

        authenticated = self.check_authentication()

        if not self.root.winfo_exists():
            return

        try:
            self.root.attributes("-disabled", False)
        except Exception:
            pass

        if not authenticated:
            self.root.after(0, self.root.destroy)
            return

        self.authenticated = True
        try:
            self.root.focus_force()
            self.root.lift()
        except Exception:
            pass

    def check_authentication(self):
        """Check authentication and trial period"""
        if LicenseManager.is_activated() and not LicenseManager.is_trial_valid():
            messagebox.showerror(
                self.get_text('trial_expired'),
                self.get_text('trial_expired_message')
            )
            return False

        max_attempts = 3
        error_message = None

        for attempt in range(max_attempts):
            attempts_remaining = max_attempts - attempt
            password = self.prompt_password(
                error_message=error_message,
                attempts_remaining=attempts_remaining
            )

            if password is None:
                return False

            if LicenseManager.verify_password(password):
                if not LicenseManager.is_activated():
                    if not LicenseManager.activate():
                        messagebox.showerror(
                            "Error",
                            "Failed to activate. Please try again."
                        )
                        return False

                if not LicenseManager.is_trial_valid():
                    messagebox.showerror(
                        self.get_text('trial_expired'),
                        self.get_text('trial_expired_message')
                    )
                    return False

                days_left = LicenseManager.get_days_remaining()
                messagebox.showinfo(
                    "Success",
                    f"{self.get_text('days_remaining').format(days_left)}"
                )
                return True

            remaining = max_attempts - attempt - 1
            if remaining <= 0:
                messagebox.showerror(
                    self.get_text('auth_failed'),
                    self.get_text('invalid_password')
                )
                return False

            error_message = self.get_text('invalid_password')

        return False

    def prompt_password(self, error_message=None, attempts_remaining=None):
        """Show custom password dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title(self.get_text('auth_required'))
        dialog.configure(bg=self.bg)
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        # Center the dialog on screen
        width, height = 360, 220
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")

        container = tk.Frame(dialog, bg=self.bg, padx=30, pady=25)
        container.pack(fill=tk.BOTH, expand=True)

        title_label = tk.Label(
            container,
            text=self.get_text('auth_required'),
            font=(self.font_family, 16, "bold"),
            bg=self.bg,
            fg=self.text_dark
        )
        title_label.pack(anchor="w")

        message_label = tk.Label(
            container,
            text=self.get_text('enter_password'),
            font=(self.font_family, 12),
            bg=self.bg,
            fg=self.text_light,
            pady=8
        )
        message_label.pack(anchor="w")

        entry = tk.Entry(
            container,
            show="*",
            font=(self.font_family, 12),
            bg="#ffffff",
            fg=self.text_dark,
            relief="flat",
            insertbackground=self.text_dark
        )
        entry.pack(fill=tk.X, ipady=8)
        entry.focus_set()

        underline = tk.Frame(container, bg=self.accent, height=2)
        underline.pack(fill=tk.X, pady=(0, 12))

        error_text = error_message or ""
        error_label = tk.Label(
            container,
            text=error_text,
            font=(self.font_family, 11),
            bg=self.bg,
            fg="#f44336" if error_message else self.text_light,
            wraplength=width - 60,
            justify="left"
        )
        error_label.pack(anchor="w")

        attempts_text = ""
        if attempts_remaining is not None:
            attempts_text = self.get_text('attempts_remaining').format(attempts_remaining)

        attempts_label = tk.Label(
            container,
            text=attempts_text,
            font=(self.font_family, 10),
            bg=self.bg,
            fg=self.text_light
        )
        attempts_label.pack(anchor="w", pady=(4, 0))

        button_frame = tk.Frame(container, bg=self.bg)
        button_frame.pack(fill=tk.X, pady=(20, 0))

        result = {"value": None}

        def submit():
            result["value"] = entry.get().strip()
            dialog.destroy()

        def cancel():
            result["value"] = None
            dialog.destroy()

        cancel_btn = tk.Button(
            button_frame,
            text=self.get_text('cancel'),
            command=cancel,
            bg=self.lang_button_bg,
            fg=self.text_dark,
            font=(self.font_family, 12),
            relief="flat",
            padx=20,
            pady=8,
            activebackground=self.lang_button_bg,
            activeforeground=self.text_dark
        )
        cancel_btn.pack(side=tk.RIGHT, padx=(0, 10))

        confirm_btn = tk.Button(
            button_frame,
            text=self.get_text('confirm'),
            command=submit,
            bg=self.accent,
            fg="#ffffff",
            font=(self.font_family, 12, "bold"),
            relief="flat",
            padx=20,
            pady=8,
            activebackground=self.accent,
            activeforeground="#ffffff"
        )
        confirm_btn.pack(side=tk.RIGHT)

        entry.bind("<Return>", lambda _: submit())
        dialog.bind("<Return>", lambda _: submit())
        dialog.bind("<Escape>", lambda _: cancel())
        dialog.protocol("WM_DELETE_WINDOW", cancel)

        dialog.update_idletasks()
        try:
            dialog.attributes("-topmost", True)
        except Exception:
            pass
        dialog.deiconify()
        dialog.lift()
        dialog.focus_force()
        try:
            dialog.wait_visibility()
        except Exception:
            pass
        def drop_topmost():
            if dialog.winfo_exists():
                try:
                    dialog.attributes("-topmost", False)
                except Exception:
                    pass
        dialog.after(300, drop_topmost)

        self.root.wait_window(dialog)
        return result["value"]

    def get_korean_font(self):
        """Get Seoul Hangang font or fallback"""
        # Try Seoul Hangang fonts
        seoul_fonts = [
            "Seoul Hangang",
            "SeoulHangang",
            "Seoul Hangang M",
            "SeoulHangangM",
            "맑은 고딕",
            "Malgun Gothic",
            "Segoe UI"
        ]

        import tkinter.font as tkfont
        available_fonts = tkfont.families()

        for font in seoul_fonts:
            if font in available_fonts:
                return font

        return "Segoe UI"  # Fallback

    def get_text(self, key):
        """Get translated text"""
        return LANGUAGES[self.current_lang].get(key, key)

    def setup_ui(self):
        """Setup UI"""
        self.root.title("Video Downloader")
        self.root.geometry("650x500")
        self.root.resizable(False, False)

        # Main container
        main = tk.Frame(self.root, bg=self.bg)
        main.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)

        # Language selector (top right - buttons)
        lang_container = tk.Frame(main, bg=self.bg)
        lang_container.pack(anchor=tk.E, pady=(0, 10))

        self.lang_buttons = {}
        languages = [
            ('ko', '한국어'),
            ('en', 'English'),
            ('ja', '日本語')
        ]

        for lang_code, lang_name in languages:
            btn = tk.Button(
                lang_container,
                text=lang_name,
                font=(self.font_family, 9),
                bg=self.lang_button_bg if lang_code != self.current_lang else self.accent,
                fg=self.text_dark if lang_code != self.current_lang else "white",
                relief=tk.FLAT,
                cursor="hand2",
                command=lambda lc=lang_code: self.change_language_direct(lc),
                borderwidth=0,
                padx=12,
                pady=4
            )
            btn.pack(side=tk.LEFT, padx=2)
            self.lang_buttons[lang_code] = btn

        # Title
        self.title_label = tk.Label(
            main,
            text="Video Downloader",
            font=(self.font_family, 28, "bold"),
            bg=self.bg,
            fg=self.text_dark
        )
        self.title_label.pack(pady=(10, 5))

        # Subtitle
        self.subtitle_label = tk.Label(
            main,
            text="TikTok · Douyin · YouTube",
            font=(self.font_family, 11),
            bg=self.bg,
            fg=self.text_light
        )
        self.subtitle_label.pack(pady=(0, 5))

        # WITHYM branding
        withym_label = tk.Label(
            main,
            text="Made by WITHYM",
            font=(self.font_family, 8),
            bg=self.bg,
            fg="#999999",
            cursor="hand2"
        )
        withym_label.pack(pady=(0, 30))

        # URL input
        self.url_label = tk.Label(
            main,
            text="Video URL",
            font=(self.font_family, 10),
            bg=self.bg,
            fg=self.text_dark,
            anchor="w"
        )
        self.url_label.pack(fill=tk.X, pady=(0, 5))

        self.url_entry = tk.Entry(
            main,
            font=(self.font_family, 11),
            relief=tk.SOLID,
            borderwidth=1,
            bg="#fafafa"
        )
        self.url_entry.pack(fill=tk.X, ipady=8)
        self.url_entry.insert(0, self.get_text('url_placeholder'))
        self.url_entry.bind("<FocusIn>", self.clear_placeholder)
        self.url_entry.bind("<FocusOut>", self.add_placeholder)
        self.url_entry.bind("<Return>", lambda e: self.start_download())

        # Folder selection
        folder_frame = tk.Frame(main, bg=self.bg)
        folder_frame.pack(fill=tk.X, pady=(20, 0))

        self.folder_label = tk.Label(
            folder_frame,
            text="Save to",
            font=(self.font_family, 10),
            bg=self.bg,
            fg=self.text_dark
        )
        self.folder_label.pack(side=tk.LEFT)

        self.folder_display = tk.Label(
            folder_frame,
            text=self.shorten_path(self.download_folder),
            font=(self.font_family, 9),
            bg=self.bg,
            fg=self.text_light,
            anchor="w"
        )
        self.folder_display.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        self.change_folder_btn = tk.Button(
            folder_frame,
            text="Change",
            font=(self.font_family, 9),
            bg=self.bg,
            fg=self.accent,
            relief=tk.FLAT,
            cursor="hand2",
            command=self.change_folder,
            borderwidth=0
        )
        self.change_folder_btn.pack(side=tk.RIGHT)

        # Download button
        self.download_btn = tk.Button(
            main,
            text="Download",
            font=(self.font_family, 14, "bold"),
            bg=self.accent,
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.start_download,
            borderwidth=0,
            pady=12
        )
        self.download_btn.pack(fill=tk.X, pady=(30, 0))

        # Status
        self.status_label = tk.Label(
            main,
            text="",
            font=(self.font_family, 10),
            bg=self.bg,
            fg=self.text_light,
            anchor="center"
        )
        self.status_label.pack(pady=(15, 0))

        # Progress bar
        self.progress = ttk.Progressbar(
            main,
            mode="indeterminate",
            length=400
        )
        self.progress.pack(pady=(10, 0))
        self.progress.pack_forget()

    def change_language_direct(self, lang_code):
        """Change language directly"""
        self.current_lang = lang_code
        self.update_language()
        self.update_language_buttons()

    def update_language_buttons(self):
        """Update language button colors"""
        for lang_code, btn in self.lang_buttons.items():
            if lang_code == self.current_lang:
                btn.config(bg=self.accent, fg="white")
            else:
                btn.config(bg=self.lang_button_bg, fg=self.text_dark)

    def update_language(self):
        """Update all text to current language"""
        self.root.title(self.get_text('title'))
        self.title_label.config(text=self.get_text('title'))
        self.subtitle_label.config(text=self.get_text('subtitle'))
        self.url_label.config(text=self.get_text('url_label'))
        self.folder_label.config(text=self.get_text('save_to'))
        self.change_folder_btn.config(text=self.get_text('change'))
        self.download_btn.config(text=self.get_text('download'))

        # Update placeholder if needed
        current_text = self.url_entry.get()
        placeholders = [LANGUAGES[lang]['url_placeholder'] for lang in LANGUAGES]
        if current_text in placeholders:
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, self.get_text('url_placeholder'))

    def shorten_path(self, path):
        """Shorten path for display"""
        if len(path) > 40:
            return "..." + path[-37:]
        return path

    def clear_placeholder(self, event):
        """Clear placeholder"""
        current = self.url_entry.get()
        placeholders = [LANGUAGES[lang]['url_placeholder'] for lang in LANGUAGES]
        if current in placeholders:
            self.url_entry.delete(0, tk.END)
            self.url_entry.config(fg=self.text_dark)

    def add_placeholder(self, event):
        """Add placeholder"""
        if not self.url_entry.get():
            self.url_entry.insert(0, self.get_text('url_placeholder'))
            self.url_entry.config(fg=self.text_light)

    def change_folder(self):
        """Change download folder"""
        folder = filedialog.askdirectory(initialdir=self.download_folder)
        if folder:
            self.download_folder = folder
            self.folder_display.config(text=self.shorten_path(folder))

    def start_download(self):
        """Start download"""
        # Re-check trial period every time
        if not LicenseManager.is_trial_valid():
            messagebox.showerror(
                self.get_text('trial_expired'),
                self.get_text('trial_expired_message')
            )
            self.root.destroy()
            return

        if self.is_downloading:
            return

        url = self.url_entry.get().strip()

        placeholders = [LANGUAGES[lang]['url_placeholder'] for lang in LANGUAGES]
        if not url or url in placeholders:
            self.show_status(self.get_text('error_no_url'), "error")
            return

        if not url.startswith("http"):
            self.show_status(self.get_text('error_invalid_url'), "error")
            return

        # Detect platform
        url_lower = url.lower()

        if "youtube.com" in url_lower or "youtu.be" in url_lower:
            platform = "YouTube"
        elif "tiktok.com" in url_lower:
            platform = "TikTok"
        elif "douyin.com" in url_lower:
            platform = "Douyin"
        elif "threads.net" in url_lower or "threads.com" in url_lower:
            platform = "Threads"
        else:
            self.show_status(self.get_text('error_unsupported'), "error")
            return

        # Update UI
        self.is_downloading = True
        self.download_btn.config(state=tk.DISABLED, bg="#cccccc")
        self.show_status(self.get_text('status_checking').format(platform), "info")
        self.progress.pack(pady=(10, 0))
        self.progress.start(10)

        # Download in background
        thread = threading.Thread(
            target=self.download_worker,
            args=(url, platform),
            daemon=True
        )
        thread.start()

    def download_worker(self, url, platform):
        """Download worker"""
        # Double check trial validity
        if not LicenseManager.is_trial_valid():
            self.root.after(0, lambda: messagebox.showerror(
                self.get_text('trial_expired'),
                self.get_text('trial_expired_message')
            ))
            self.root.after(0, self.root.destroy)
            return

        try:
            self.root.after(0, self.show_status, self.get_text('status_downloading').format(platform), "info")

            if platform in ["TikTok", "Douyin"]:
                # TikTok/Douyin download
                filepath = download_tiktok_douyin_video(url)

                if filepath and os.path.exists(filepath):
                    filename = os.path.basename(filepath)
                    dest_path = os.path.join(self.download_folder, filename)

                    # Handle duplicate files
                    counter = 1
                    base_name, ext = os.path.splitext(dest_path)
                    while os.path.exists(dest_path):
                        dest_path = f"{base_name}_{counter}{ext}"
                        counter += 1

                    os.rename(filepath, dest_path)
                    self.root.after(0, self.download_complete, filename)
                else:
                    self.root.after(0, self.download_failed, "Failed to download")

            elif platform == "YouTube":
                # YouTube download
                success, filename = self.download_youtube(url)

                if success:
                    self.root.after(0, self.download_complete, filename)
                else:
                    self.root.after(0, self.download_failed, "YouTube download failed")

            elif platform == "Threads":
                try:
                    filepath = download_threads_video(url, self.download_folder)
                except ThreadsDownloadError as exc:
                    self.root.after(0, self.download_failed, str(exc))
                    return
                except Exception as exc:
                    self.root.after(0, self.download_failed, str(exc))
                    return

                if filepath and os.path.exists(filepath):
                    filename = os.path.basename(filepath)
                    self.root.after(0, self.download_complete, filename)
                else:
                    self.root.after(0, self.download_failed, "Threads download failed")

        except Exception as e:
            error_msg = str(e)[:50]
            self.root.after(0, self.download_failed, error_msg)

    def download_youtube(self, url):
        """Download YouTube video"""
        try:
            output_template = os.path.join(self.download_folder, "%(title)s_%(id)s.%(ext)s")

            cmd = [
                "yt-dlp",
                "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
                "-o", output_template,
                "--no-playlist",
                "--merge-output-format", "mp4",
                url
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,
                encoding='utf-8',
                errors='replace'
            )

            if result.returncode == 0:
                # Try to extract the actual filename from output
                import re
                import glob

                # Look for "Destination:" or "[download]" in output to get filename
                filename_match = re.search(r'Destination: (.+\.mp4)', result.stdout)
                if not filename_match:
                    filename_match = re.search(r'\[download\] (.+\.mp4)', result.stdout)

                if filename_match:
                    filepath = filename_match.group(1).strip()
                    if os.path.exists(filepath):
                        return True, os.path.basename(filepath)

                # Fallback: find the most recent mp4 file
                files = glob.glob(os.path.join(self.download_folder, "*.mp4"))
                if files:
                    latest_file = max(files, key=os.path.getctime)
                    return True, os.path.basename(latest_file)

                return True, "YouTube video"

            return False, None

        except subprocess.TimeoutExpired:
            return False, None
        except FileNotFoundError:
            self.root.after(0, self.prompt_install_ytdlp)
            return False, None
        except Exception as e:
            print(f"YouTube error: {e}")
            return False, None

    def download_complete(self, filename):
        """Download complete"""
        self.is_downloading = False
        self.download_btn.config(state=tk.NORMAL, bg=self.accent)
        self.progress.stop()
        self.progress.pack_forget()

        self.show_status(self.get_text('status_complete').format(filename), "success")

        # Reset URL entry
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, self.get_text('url_placeholder'))
        self.url_entry.config(fg=self.text_light)

        # Ask to open folder
        if messagebox.askyesno(self.get_text('complete_title'), self.get_text('complete_message')):
            self.open_folder()

    def download_failed(self, error_msg):
        """Download failed"""
        self.is_downloading = False
        self.download_btn.config(state=tk.NORMAL, bg=self.accent)
        self.progress.stop()
        self.progress.pack_forget()

        self.show_status(self.get_text('status_failed').format(error_msg), "error")
        messagebox.showerror(self.get_text('error_title'), self.get_text('error_message').format(error_msg))

    def show_status(self, message, status_type="info"):
        """Show status message"""
        colors = {
            "info": self.text_light,
            "success": "#4CAF50",
            "error": "#f44336"
        }

        self.status_label.config(
            text=message,
            fg=colors.get(status_type, self.text_light)
        )

    def open_folder(self):
        """Open download folder"""
        try:
            if sys.platform == "win32":
                os.startfile(self.download_folder)
            elif sys.platform == "darwin":
                subprocess.run(["open", self.download_folder])
            else:
                subprocess.run(["xdg-open", self.download_folder])
        except Exception as e:
            print(f"Failed to open folder: {e}")

    def check_dependencies(self):
        """Check dependencies"""
        try:
            subprocess.run(
                ["yt-dlp", "--version"],
                capture_output=True,
                timeout=5
            )
        except FileNotFoundError:
            pass
        except Exception:
            pass

    def prompt_install_ytdlp(self):
        """Prompt to install yt-dlp"""
        if messagebox.askyesno(
            self.get_text('ytdlp_required_title'),
            self.get_text('ytdlp_required_message')
        ):
            self.install_ytdlp()

    def install_ytdlp(self):
        """Install yt-dlp"""
        self.show_status(self.get_text('ytdlp_installing'), "info")
        self.progress.pack(pady=(10, 0))
        self.progress.start(10)

        def install():
            try:
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", "yt-dlp"],
                    check=True,
                    capture_output=True
                )
                self.root.after(0, lambda: messagebox.showinfo("Success", self.get_text('ytdlp_success')))
                self.root.after(0, self.show_status, self.get_text('ytdlp_success'), "success")
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"{self.get_text('ytdlp_failed')}:\n{e}"))
                self.root.after(0, self.show_status, self.get_text('ytdlp_failed'), "error")
            finally:
                self.root.after(0, self.progress.stop)
                self.root.after(0, self.progress.pack_forget)

        thread = threading.Thread(target=install, daemon=True)
        thread.start()


def main():
    root = tk.Tk()
    app = VideoDownloader(root)

    try:
        if not root.winfo_exists():
            return

        # Center window
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f'{width}x{height}+{x}+{y}')
    except tk.TclError:
        return

    root.mainloop()


if __name__ == "__main__":
    main()

import os
import webbrowser
import customtkinter as ctk

HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts" if os.name == 'nt' else "/etc/hosts"

lines_to_manage = [
    "127.0.0.1 adclick.g.doubleclick.net",
    "127.0.0.1 adeventtracker.spotify.com",
    "127.0.0.1 ads-fa.spotify.com",
    "127.0.0.1 analytics.spotify.com",
    "127.0.0.1 b.scorecardresearch.com",
    "127.0.0.1 bounceexchange.com",
    "127.0.0.1 bs.serving-sys.com",
    "127.0.0.1 doubleclick.net",
    "127.0.0.1 ds.serving-sys.com",
    "127.0.0.1 googleadservices.com",
    "127.0.0.1 googleads.g.doubleclick.net",
    "127.0.0.1 js.moatads.com",
    "127.0.0.1 log.spotify.com",
    "127.0.0.1 media-match.com",
    "127.0.0.1 omaze.com",
    "127.0.0.1 pagead2.googlesyndication.com",
    "127.0.0.1 partner.googleadservices.com",
    "127.0.0.1 pubads.g.doubleclick.net",
    "127.0.0.1 s0.2mdn.net",
    "127.0.0.1 securepubads.g.doubleclick.net",
    "127.0.0.1 tpc.googlesyndication.com",
    "127.0.0.1 video-ad-stats.googlesyndication.com",
    "127.0.0.1 www.googleadservices.com",
    "127.0.0.1 www.googletagservices.com",
    "127.0.0.1 www.omaze.com",
]

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class SpotifiApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Spotifi")
        self.geometry("520x280")
        self.resizable(False, False)

        self.label = ctk.CTkLabel(self, text="Manage Spotifi Installation:", font=("Segoe UI", 16))
        self.label.pack(pady=15)

        self.btn_frame = ctk.CTkFrame(self)
        self.btn_frame.pack(pady=10)

        self.apply_btn = ctk.CTkButton(self.btn_frame, text="Apply", command=self.apply_tweak, width=120, height=40)
        self.apply_btn.grid(row=0, column=0, padx=20)

        self.remove_btn = ctk.CTkButton(self.btn_frame, text="Remove", command=self.remove_tweak, width=120, height=40)
        self.remove_btn.grid(row=0, column=1, padx=20)

        self.status = ctk.CTkLabel(self, text="", font=("Segoe UI", 14))
        self.status.pack(pady=25)

        self.credit_label = ctk.CTkLabel(
        self,
        text="Made by thunderx with ❤️",
        font=("Segoe UI", 12),
        text_color="gray"
    )
        self.credit_label.pack(side="bottom", pady=5)
        
    def apply_tweak(self):
        try:
            with open(HOSTS_PATH, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except PermissionError:
            self.update_status("Permission denied. Run as administrator/root.", "red")
            return
        except Exception as e:
            self.update_status(f"Error reading hosts file:\n{e}", "red")
            return

        file_lines_set = set(line.strip() for line in lines)
        if all(line in file_lines_set for line in lines_to_manage):
            self.update_status("Tweak already fully applied.", "orange")
            return

        missing_lines = [line for line in lines_to_manage if line not in file_lines_set]
        if not missing_lines:
            self.update_status("No new lines to add.", "orange")
            return

        try:
            with open(HOSTS_PATH, 'a', encoding='utf-8') as f:
                f.write('\n' + '\n'.join(missing_lines) + '\n')
            self.update_status(f"Appended {len(missing_lines)} lines successfully.", "green")
        except PermissionError:
            self.update_status("Permission denied. Run as administrator/root.", "red")
        except Exception as e:
            self.update_status(f"Error writing to hosts file:\n{e}", "red")

    def remove_tweak(self):
        try:
            with open(HOSTS_PATH, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except PermissionError:
            self.update_status("Permission denied. Run as administrator/root.", "red")
            return
        except Exception as e:
            self.update_status(f"Error reading hosts file:\n{e}", "red")
            return

        file_lines_set = set(line.strip() for line in lines)
        if not all(line in file_lines_set for line in lines_to_manage):
            self.update_status("Tweak not fully applied, cannot remove.", "orange")
            return

        new_lines = [line for line in lines if line.strip() not in lines_to_manage]

        try:
            with open(HOSTS_PATH, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            self.update_status("Removed tweak lines successfully.", "green")
        except PermissionError:
            self.update_status("Permission denied. Run as administrator/root.", "red")
        except Exception as e:
            self.update_status(f"Error writing to hosts file:\n{e}", "red")

    def update_status(self, message, color):
        self.status.configure(text=message, text_color=color)


if __name__ == "__main__":
    app = SpotifiApp()
    app.mainloop()

<div align="center">

# ⚡ TELEGRAM AUTO LEAVE & CHAT CLEANUP TOOL ⚡
### *Giải pháp tối ưu quét, rời nhóm, kênh và dọn sạch hội thoại Telegram tự động*

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/Telethon-v1.36%2B-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Telethon">
  <img src="https://img.shields.io/badge/Rich-Terminal%20UI-FF007F?style=for-the-badge&logo=gnometerminal&logoColor=white" alt="Rich UI">
  <img src="https://img.shields.io/badge/Security-Safe%20%26%20Local-success?style=for-the-badge&logo=shield&logoColor=white" alt="Security">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-informational?style=for-the-badge" alt="Platform">
</p>

<p align="center">
  <b>Tốc độ cao • Không sợ Checkpoint • Giao diện CLI hiện đại • Bảo vệ nhóm sở hữu</b>
</p>

---

</div>

## 📌 Tổng quan dự án

Bạn tham gia quá nhiều nhóm airdrop, nhóm chat rác hoặc bị add vào hàng trăm kênh lạ? Việc click rời từng nhóm trên Telegram tốn hàng giờ đồng hồ!

**Telegram Auto Leave & Chat Cleanup Tool** sinh ra để giải quyết triệt để vấn đề này. Ứng dụng chạy trực tiếp qua **Telegram Client API (Telethon)**, cho tốc độ xử lý nhanh gấp **50 lần** so với thao tác web/click chuột thông thường, tích hợp giao diện terminal phong cách **Rich Cyberpunk** và cơ chế bảo vệ tài khoản nghiêm ngặt.

---

## 🌟 Điểm sáng công nghệ & Tính năng độc quyền

| Tính năng | Mô tả chi tiết |
| :--- | :--- |
| 🛡️ **Bảo vệ Chủ sở hữu** | Tự động nhận diện quyền hạn, **tuyệt đối không bao giờ out** những nhóm/kênh do chính bạn làm Chủ nhóm (`Creator`). |
| 🔒 **Bảo vệ Saved Messages** | Tự động cô lập và bảo vệ dữ liệu trong **Tin nhắn đã lưu**, không sợ xóa nhầm dữ liệu quan trọng. |
| ⚡ **Quét & Phân loại đa năng** | Nhận diện tức thì: *Nhóm thường (Chat)*, *Siêu nhóm (Supergroup)*, *Kênh thông báo (Channel)*, *Tin nhắn cá nhân (User DM)* và *Bot*. |
| 💥 **Xóa tin nhắn 2 chiều** | Hỗ trợ xóa sạch tin nhắn cá nhân ở cả **2 phía** (biến mất ở cả máy của bạn và người nhận). |
| ⏱️ **Cơ chế Anti-Flood / Auto-Retry** | Tự động giãn cách an toàn 2.0s mỗi thao tác; nếu gặp giới hạn tốc độ từ Telegram (`FloodWait`), tool tự động đếm ngược và chạy tiếp mà không bị dừng đột ngột. |
| 🔑 **Smart Phone Formatter** | Tự động chuẩn hóa số điện thoại nội địa (VD: `0367...` ➔ `+84367...`), gõ kiểu gì cũng nhận diện chuẩn xác. |
| 💾 **Single-Sign-On Session** | Đăng nhập mã OTP một lần duy nhất, mã hóa phiên vào file `.session` trên máy cục bộ, các lần sau mở lên là dùng ngay. |

---

## 🖥️ Trải nghiệm giao diện CLI Terminal

```text
╭────────────────── TELEGRAM AUTO LEAVE & CLEANUP TOOL ──────────────────╮
│          Hỗ trợ out nhóm, kênh và xóa tin nhắn cá nhân an toàn         │
╰────────────────────────────────────────────────────────────────────────╯

✔ Đăng nhập thành công: Nguyễn Văn A (@nguyenvana) - ID: 123456789

               Danh sách hội thoại, nhóm & kênh đang tham gia
┏━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ STT  ┃ Tên hội thoại / Nhóm       ┃ Loại                   ┃ Vai trò     ┃ ID           ┃
┡━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
│ 1    │ Crypto Trading Group       │ Siêu nhóm (Supergroup) │ Thành viên  │ -10012345678 │
│ 2    │ Kênh Báo Kèo Vip           │ Kênh (Channel)         │ Thành viên  │ -10098765432 │
│ 3    │ Nhóm Anh Em Dev            │ Nhóm thường (Chat)     │ Chủ nhóm    │ -10011223344 │
│ 4    │ Nguyễn Văn B               │ Tin nhắn cá nhân (DM)  │ Cá nhân     │ 1987654321   │
│ 5    │ @SpamBot                   │ Chat Bot               │ Bot         │ 178220800    │
│ 6    │ Saved Messages             │ Tin nhắn đã lưu (Saved)│ Chính bạn   │ 123456789    │
└──────┴────────────────────────────┴────────────────────────┴─────────────┴──────────────┘
```

---

## 🚀 Hướng dẫn cài đặt từng bước

### 📥 Bước 1: Chuẩn bị môi trường Python

1. Tải Python phiên bản mới nhất từ [python.org](https://www.python.org/downloads/) (khuyến nghị **Python 3.10+**).
2. ⚠️ **LƯU Ý:** Khi chạy bộ cài, hãy tick chọn vào ô **`Add Python to PATH`** trước khi bấm **Install Now**.

### 📦 Bước 2: Tải dự án & Cài đặt thư viện

Mở cửa sổ **Terminal / PowerShell** tại thư mục dự án và chạy lệnh:

```bash
# Cài đặt toàn bộ thư viện cần thiết
pip install -r requirements.txt
```

---

## 🔑 Hướng dẫn lấy Telegram API (2 phút)

Để tool kết nối an toàn với tài khoản Telegram của bạn, hãy tạo cặp khóa API chính chủ từ Telegram:

```
[ Truy cập my.telegram.org ] ──> [ Nhập SĐT & OTP ] ──> [ API development tools ] ──> [ Tạo App & Nhận Key ]
```

1. Mở trình duyệt và truy cập: **[https://my.telegram.org](https://my.telegram.org)**.
2. Nhập số điện thoại Telegram của bạn (VD: `+84912345678`) và nhấn **Next**.
3. Mở ứng dụng Telegram, copy mã **Confirmation code** Telegram gửi về và dán vào web để đăng nhập.
4. Chọn mục **API development tools**.
5. Điền thông tin tạo ứng dụng (điền tùy ý):
   * **App title:** `MyCleanupTool`
   * **Short name:** `cleaner`
   * **Platform:** `Desktop`
6. Nhấn nút **Create application**.
7. Lưu lại 2 trường dữ liệu:
   * 🆔 **App api_id:** *(dãy số nguyên, VD: `12345678`)*
   * 🔑 **App api_hash:** *(chuỗi ký tự băm, VD: `0123456789abcdef0123456789abcdef`)*

---

## ⚙️ Cấu hình file `.env`

Sao chép file mẫu [.env.example](file:///c:/Users/Phung%20Quoc%20Viet/Documents/Tool%20_linh_tinh/OutGroupTelegram/.env.example) thành `.env`:

```bash
# Trên Windows CMD:
copy .env.example .env

# Hoặc trên PowerShell:
cp .env.example .env
```

Mở file `.env` và điền thông tin của bạn vào:

```env
API_ID=your_api_id_here
API_HASH=your_api_hash_here
```

---

## 🎮 Hướng dẫn sử dụng Tool

### 1️⃣ Khởi động
* **Trên Windows:** Nhấp đúp chuột trực tiếp vào file **[run.bat](file:///c:/Users/Phung%20Quoc%20Viet/Documents/Tool%20_linh_tinh/OutGroupTelegram/run.bat)**.
* **Hoặc chạy lệnh:**
  ```bash
  python out_groups.py
  ```

### 2️⃣ Đăng nhập lần đầu
* **Nhập số điện thoại:** Bạn có thể nhập `0367890820` hoặc `+84367890820` (tool tự động chuẩn hóa).
* **Nhập mã Code:** Xem mã xác nhận gửi trực tiếp trong tin nhắn app Telegram.
* **Mật khẩu 2FA (nếu có):** Nhập mật khẩu bảo mật (ký tự được ẩn tự động để đảm bảo an toàn).

### 3️⃣ Bảng chức năng Menu điều khiển

| Phím bấm | Chức năng | Cơ chế an toàn |
| :---: | :--- | :--- |
| **`1`** | **Chọn theo số thứ tự (STT)** | Hỗ trợ nhập danh sách hoặc khoảng (VD: `1, 3, 5-10`). |
| **`2`** | **Out toàn bộ Nhóm thường & Siêu nhóm** | Chỉ out các nhóm chat; giữ nguyên các kênh tin tức và chat cá nhân. Tự động bảo vệ nhóm do bạn tạo. |
| **`3`** | **Out toàn bộ Kênh tin tức (Channel)** | Rời sạch các kênh theo dõi; không ảnh hưởng đến nhóm chat cá nhân. |
| **`4`** | **Xóa toàn bộ Tin nhắn cá nhân & Bot** | Dọn sạch hộp thư riêng; hỗ trợ hỏi **xóa 2 chiều** (xóa cả phía đối phương). Giữ lại Saved Messages. |
| **`5`** | **Dọn sạch TẤT CẢ mọi hội thoại** | Quét sạch sẽ từ A-Z (Nhóm + Kênh + DM); bảo vệ nhóm sở hữu & tin nhắn lưu. |
| **`6`** | **Tìm kiếm theo từ khóa** | Lọc theo tên nhóm/người dùng (VD: gõ `kèo`, `crypto`, `bot`) trước khi ra lệnh xóa. |
| **`7`** | **Thoát chương trình** | Ngắt kết nối an toàn khỏi máy chủ Telegram. |

---

## 🛡️ Nguyên tắc vàng về bảo mật (Security Policy)

> [!CAUTION]
> **TUYỆT ĐỐI KHÔNG BAO GIỜ COMMIT HOẶC CHIA SẺ 2 TỆP SAU LÊN GITHUB:**
> 1. File **`.env`**: Chứa `API_ID` và `API_HASH` của bạn.
> 2. File **`telegram_session.session`**: Chứa token phiên đăng nhập của bạn (người có file này có thể vào tài khoản mà không cần OTP).

Dự án đã thiết lập sẵn file **[.gitignore](file:///c:/Users/Phung%20Quoc%20Viet/Documents/Tool%20_linh_tinh/OutGroupTelegram/.gitignore)** tự động ngăn Git track 2 tệp trên. Hãy luôn kiểm tra trước khi push:

```bash
git status
```
*(Nếu màn hình không xuất hiện `.env` và `*.session` màu đỏ/xanh thì bạn hoàn toàn an toàn).*

---

## 🤝 Giấy phép & Đóng góp

* Dự án được phân phối dưới giấy phép **MIT License** - hoàn toàn mở và miễn phí sử dụng cho mục đích cá nhân.
* Mọi đóng góp nâng cấp giao diện, tính năng hoặc báo lỗi đều được hoan nghênh qua phần **Issues / Pull Requests**.

<div align="center">
  <sub>Made with ❤️ & Python • Chúc bạn có một hộp thư Telegram sạch sẽ và ngăn nắp!</sub>
</div>

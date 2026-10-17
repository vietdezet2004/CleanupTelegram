import asyncio
import os
import re
import sys
import time
from typing import List, Dict, Any

from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.tl.types import Channel, Chat, User
from telethon.errors import FloodWaitError, PhoneNumberInvalidError
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
import getpass

console = Console()

def get_phone() -> str:
    """Yêu cầu nhập số điện thoại và tự động chuẩn hóa số điện thoại Việt Nam sang định dạng quốc tế (+84)."""
    while True:
        raw = Prompt.ask("\n[bold cyan]Nhập số điện thoại Telegram của bạn[/bold cyan] (VD: [green]0367890820[/green] hoặc [green]+84367890820[/green])")
        cleaned = re.sub(r"[^\d+]", "", raw.strip())
        if cleaned.startswith("0"):
            cleaned = "+84" + cleaned[1:]
        elif not cleaned.startswith("+"):
            cleaned = "+" + cleaned

        if len(cleaned) >= 10:
            console.print(f"[dim]Số điện thoại chuẩn quốc tế:[/dim] [bold yellow]{cleaned}[/bold yellow]")
            return cleaned
        console.print("[bold red]Số điện thoại quá ngắn hoặc không hợp lệ. Vui lòng nhập lại![/bold red]")


def get_code() -> str:
    """Nhập mã xác nhận (Login code) Telegram gửi về."""
    return Prompt.ask("[bold cyan]Nhập mã xác nhận (Code) Telegram đã gửi về ứng dụng của bạn[/bold cyan]").strip()


def get_password() -> str:
    """Nhập mật khẩu 2 bước (2FA) nếu có."""
    return getpass.getpass("Nhập mật khẩu bảo mật 2 bước (2FA Password): ")


def load_credentials(env_path: str = ".env") -> tuple[int, str]:
    """
    Đọc API_ID và API_HASH từ file .env theo chuẩn (như trong .env.example).
    """
    if os.path.exists(env_path):
        load_dotenv(dotenv_path=env_path)

    api_id_raw = os.getenv("API_ID")
    api_hash = os.getenv("API_HASH")

    if not api_id_raw or not api_hash or api_id_raw == "your_api_id_here" or api_hash == "your_api_hash_here":
        console.print("[bold red]Không tìm thấy API_ID hoặc API_HASH hợp lệ trong file .env![/bold red]")
        console.print("Vui lòng cấu hình file .env theo mẫu trong .env.example:")
        console.print("[cyan]API_ID=12345678\nAPI_HASH=abcdef1234567890[/cyan]")
        sys.exit(1)

    try:
        api_id = int(api_id_raw.strip())
    except ValueError:
        console.print(f"[bold red]API_ID không hợp lệ (phải là số nguyên): {api_id_raw}[/bold red]")
        sys.exit(1)

    return api_id, api_hash.strip()


async def get_dialog_list(client: TelegramClient) -> List[Dict[str, Any]]:
    """Lấy danh sách tất cả các hội thoại (Nhóm, Kênh, Tin nhắn cá nhân, Bot)."""
    items = []
    with console.status("[bold green]Đang quét danh sách hội thoại từ Telegram...[/bold green]"):
        async for dialog in client.iter_dialogs():
            entity = dialog.entity
            item_type = None
            is_creator = False
            is_admin = False
            is_user = False
            is_saved = False

            if isinstance(entity, Chat):
                item_type = "Nhóm thường (Chat)"
                is_creator = getattr(entity, 'creator', False)
            elif isinstance(entity, Channel):
                if entity.megagroup:
                    item_type = "Siêu nhóm (Supergroup)"
                elif entity.broadcast:
                    item_type = "Kênh (Channel)"
                else:
                    item_type = "Nhóm"

                is_creator = getattr(entity, 'creator', False)
                admin_rights = getattr(entity, 'admin_rights', None)
                if admin_rights is not None:
                    is_admin = True
            elif isinstance(entity, User):
                is_user = True
                if getattr(entity, 'is_self', False):
                    item_type = "Tin nhắn đã lưu (Saved)"
                    is_saved = True
                elif getattr(entity, 'bot', False):
                    item_type = "Chat Bot"
                else:
                    item_type = "Tin nhắn cá nhân (DM)"

            if item_type is not None:
                items.append({
                    "dialog": dialog,
                    "entity": entity,
                    "id": dialog.id,
                    "title": dialog.name or "Không tên",
                    "type": item_type,
                    "is_creator": is_creator,
                    "is_admin": is_admin,
                    "is_user": is_user,
                    "is_saved": is_saved,
                    "unread_count": dialog.unread_count
                })

    return items


def display_dialogs_table(dialogs: List[Dict[str, Any]], title: str = "Danh sách hội thoại, nhóm & kênh"):
    """Hiển thị bảng danh sách các hội thoại bằng rich."""
    table = Table(title=title, show_header=True, header_style="bold cyan", border_style="dim")
    table.add_column("STT", style="bold yellow", justify="center", width=6)
    table.add_column("Tên hội thoại / Nhóm", style="bold white", min_width=25)
    table.add_column("Loại", style="magenta", width=25)
    table.add_column("Vai trò", style="green", width=14)
    table.add_column("ID", style="dim", width=15)

    for idx, item in enumerate(dialogs, 1):
        if item.get("is_saved", False):
            role = "[cyan]Chính bạn[/cyan]"
        elif item.get("is_user", False):
            role = "[magenta]Bot[/magenta]" if item["type"] == "Chat Bot" else "[blue]Cá nhân[/blue]"
        elif item["is_creator"]:
            role = "[bold red]Chủ nhóm[/bold red]"
        elif item["is_admin"]:
            role = "[bold yellow]Admin[/bold yellow]"
        else:
            role = "Thành viên"

        table.add_row(
            str(idx),
            item["title"],
            item["type"],
            role,
            str(item["id"])
        )

    console.print(table)


def parse_indices(input_str: str, max_count: int) -> List[int]:
    """Phân tích chuỗi số người dùng nhập (ví dụ: '1, 3, 5-8') thành danh sách index 0-based."""
    indices = set()
    parts = [p.strip() for p in input_str.split(",") if p.strip()]

    for part in parts:
        if "-" in part:
            bounds = part.split("-")
            if len(bounds) == 2 and bounds[0].strip().isdigit() and bounds[1].strip().isdigit():
                start = int(bounds[0].strip())
                end = int(bounds[1].strip())
                for num in range(min(start, end), max(start, end) + 1):
                    if 1 <= num <= max_count:
                        indices.add(num - 1)
        elif part.isdigit():
            num = int(part)
            if 1 <= num <= max_count:
                indices.add(num - 1)

    return sorted(list(indices))


async def delete_dialogs(client: TelegramClient, targets: List[Dict[str, Any]]):
    """Thực hiện rời nhóm hoặc xóa tin nhắn cá nhân với cơ chế chống FloodWait."""
    if not targets:
        console.print("[yellow]Không có mục nào được chọn để out/xóa.[/yellow]")
        return

    # Lọc bỏ tin nhắn đã lưu (Saved Messages) để tránh xóa nhầm
    saved_msgs = [t for t in targets if t.get("is_saved", False)]
    if saved_msgs:
        console.print("[yellow]Lưu ý: 'Tin nhắn đã lưu' (Saved Messages) sẽ được tự động giữ lại để bảo vệ dữ liệu.[/yellow]")
        targets = [t for t in targets if not t.get("is_saved", False)]
        if not targets:
            return

    console.print(f"\n[bold yellow]Sắp out / xóa {len(targets)} hội thoại đã chọn.[/bold yellow]")

    # Nếu có tin nhắn cá nhân, hỏi người dùng có muốn xóa 2 chiều không
    has_dm = any(item.get("is_user", False) for item in targets)
    revoke_dm = False
    if has_dm:
        console.print("[cyan]Trong danh sách có chứa tin nhắn cá nhân / bot.[/cyan]")
        revoke_dm = Confirm.ask("Bạn có muốn xóa 2 chiều (xóa luôn cả phía người nhận) không?", default=False)

    confirm = Confirm.ask("Bạn có chắc chắn muốn thực hiện không?", default=False)
    if not confirm:
        console.print("[bold red]Đã hủy thao tác.[/bold red]")
        return

    delay_sec = 2.0  # Giãn cách 2 giây mỗi lần để tránh rate-limit
    console.print(f"[dim]Tự động giãn cách an toàn: {delay_sec}s mỗi hội thoại...[/dim]\n")

    success_count = 0
    fail_count = 0

    for idx, item in enumerate(targets, 1):
        dialog = item["dialog"]
        title = item["title"]
        is_user = item.get("is_user", False)
        action_verb = "Đang xóa tin nhắn cá nhân" if is_user else "Đang rời nhóm/kênh"

        try:
            console.print(f"[{idx}/{len(targets)}] {action_verb}: [bold cyan]{title}[/bold cyan]...", end=" ")
            if is_user:
                await client.delete_dialog(dialog.entity, revoke=revoke_dm)
            else:
                await client.delete_dialog(dialog.entity)

            console.print("[bold green]✔ Thành công[/bold green]")
            success_count += 1
            await asyncio.sleep(delay_sec)
        except FloodWaitError as e:
            console.print(f"\n[bold red]Bị giới hạn tốc độ (FloodWait) bởi Telegram! Cần chờ {e.seconds} giây...[/bold red]")
            await asyncio.sleep(e.seconds)
            try:
                if is_user:
                    await client.delete_dialog(dialog.entity, revoke=revoke_dm)
                else:
                    await client.delete_dialog(dialog.entity)
                console.print(f"[{idx}/{len(targets)}] {action_verb}: [bold cyan]{title}[/bold cyan]... [bold green]✔ Thành công sau khi chờ[/bold green]")
                success_count += 1
            except Exception as retry_err:
                console.print(f"[bold red]✘ Lỗi: {retry_err}[/bold red]")
                fail_count += 1
        except Exception as e:
            console.print(f"[bold red]✘ Thất bại: {e}[/bold red]")
            fail_count += 1

    console.print(Panel.fit(
        f"[bold green]Hoàn tất![/bold green]\n"
        f"• Thành công: [bold green]{success_count}[/bold green]\n"
        f"• Thất bại / Bỏ qua: [bold red]{fail_count}[/bold red]",
        title="Kết quả"
    ))


async def main():
    console.print(Panel.fit(
        "[bold cyan]TELEGRAM AUTO LEAVE & CLEANUP TOOL[/bold cyan]\n"
        "[dim]Hỗ trợ out nhóm, kênh và xóa tin nhắn cá nhân an toàn[/dim]",
        border_style="cyan"
    ))

    api_id, api_hash = load_credentials(".env")

    # Tạo client Telegram (lưu session vào file telegram_session.session)
    session_file = "telegram_session"
    client = TelegramClient(session_file, api_id, api_hash)

    try:
        await client.start(
            phone=get_phone,
            code_callback=get_code,
            password=get_password
        )
    except PhoneNumberInvalidError:
        console.print("[bold red]Lỗi: Số điện thoại không tồn tại hoặc bị từ chối bởi Telegram! Vui lòng kiểm tra lại.[/bold red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Đăng nhập thất bại: {e}[/bold red]")
        sys.exit(1)

    me = await client.get_me()
    console.print(f"\n[bold green]Đăng nhập thành công tài khoản:[/bold green] [bold yellow]{me.first_name}[/bold yellow] (@{me.username or 'Không có username'}) - ID: {me.id}\n")

    while True:
        dialogs = await get_dialog_list(client)

        if not dialogs:
            console.print("[bold yellow]Tài khoản của bạn hiện không có hội thoại nào.[/bold yellow]")
            break

        display_dialogs_table(dialogs)

        console.print("\n[bold cyan]--- MENU TÙY CHỌN ---[/bold cyan]")
        console.print("1. [bold yellow]Chọn theo STT[/bold yellow] (VD nhập: 1, 3, 5-10 để out / xóa)")
        console.print("2. [bold yellow]Out TẤT CẢ Nhóm thường & Siêu nhóm[/bold yellow] (Bỏ qua kênh và tin nhắn cá nhân)")
        console.print("3. [bold yellow]Out TẤT CẢ Kênh (Channel)[/bold yellow]")
        console.print("4. [bold yellow]Xóa TẤT CẢ Tin nhắn cá nhân & Bot[/bold yellow] (User DM - Bảo vệ Tin nhắn đã lưu)")
        console.print("5. [bold yellow]Out & Xóa TẤT CẢ mọi hội thoại[/bold yellow] (Nhóm, Kênh, Tin nhắn cá nhân)")
        console.print("6. [bold yellow]Tìm kiếm theo từ khóa[/bold yellow] để lọc hội thoại cần xóa")
        console.print("7. [bold red]Thoát chương trình[/bold red]")

        choice = Prompt.ask("\nNhập lựa chọn của bạn", choices=["1", "2", "3", "4", "5", "6", "7"], default="1")

        if choice == "1":
            inp = Prompt.ask("Nhập các số STT cần out / xóa (ví dụ: [bold green]1, 2, 4-7[/bold green])")
            selected_indices = parse_indices(inp, len(dialogs))
            if not selected_indices:
                console.print("[red]Không có STT hợp lệ nào được chọn![/red]")
                continue

            targets = [dialogs[i] for i in selected_indices]
            display_dialogs_table(targets, title="Các hội thoại bạn đã chọn để out/xóa")
            await delete_dialogs(client, targets)

        elif choice == "2":
            # Chỉ out Chat & Supergroup (bỏ qua channel và tin nhắn cá nhân)
            targets = [
                d for d in dialogs 
                if d["type"] in ["Nhóm thường (Chat)", "Siêu nhóm (Supergroup)", "Nhóm"]
                and not d["is_creator"]
            ]
            if not targets:
                console.print("[yellow]Không tìm thấy nhóm chat nào (hoặc chỉ còn nhóm do bạn làm chủ nhóm).[/yellow]")
                continue
            display_dialogs_table(targets, title="Danh sách các Nhóm chat sẽ out")
            await delete_dialogs(client, targets)

        elif choice == "3":
            # Chỉ out Channels
            targets = [
                d for d in dialogs 
                if d["type"] == "Kênh (Channel)" and not d["is_creator"]
            ]
            if not targets:
                console.print("[yellow]Không tìm thấy Kênh nào (hoặc chỉ còn kênh do bạn làm chủ).[/yellow]")
                continue
            display_dialogs_table(targets, title="Danh sách các Kênh sẽ out")
            await delete_dialogs(client, targets)

        elif choice == "4":
            # Xóa tin nhắn cá nhân (User DM & Bot) ngoại trừ Saved Messages
            targets = [
                d for d in dialogs 
                if d.get("is_user", False) and not d.get("is_saved", False)
            ]
            if not targets:
                console.print("[yellow]Không tìm thấy tin nhắn cá nhân nào cần xóa.[/yellow]")
                continue
            display_dialogs_table(targets, title="Danh sách Tin nhắn cá nhân & Bot sẽ xóa")
            await delete_dialogs(client, targets)

        elif choice == "5":
            # Out & xóa tất cả: nhóm (trừ chủ nhóm), kênh, tin nhắn cá nhân (trừ Saved Messages)
            targets = [
                d for d in dialogs 
                if not d["is_creator"] and not d.get("is_saved", False)
            ]
            display_dialogs_table(targets, title="Toàn bộ hội thoại sẽ out & xóa (Đã bảo vệ nhóm của bạn & Saved Messages)")
            await delete_dialogs(client, targets)

        elif choice == "6":
            keyword = Prompt.ask("Nhập từ khóa tìm kiếm trong tên hội thoại").strip().lower()
            if not keyword:
                continue
            filtered = [d for d in dialogs if keyword in d["title"].lower()]
            if not filtered:
                console.print(f"[yellow]Không tìm thấy hội thoại nào chứa từ khóa '{keyword}'[/yellow]")
                continue
            display_dialogs_table(filtered, title=f"Kết quả tìm kiếm cho: '{keyword}'")
            if Confirm.ask("Bạn có muốn out/xóa toàn bộ danh sách tìm kiếm này không?", default=False):
                await delete_dialogs(client, targets=filtered)

        elif choice == "7":
            console.print("[bold green]Tạm biệt![/bold green]")
            break

        if not Confirm.ask("\nBạn có muốn tiếp tục thao tác tiếp không?", default=True):
            break

    await client.disconnect()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[bold red]Đã dừng chương trình bởi người dùng.[/bold red]")

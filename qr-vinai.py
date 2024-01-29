import os
from slack_bolt import App
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bolt.adapter.socket_mode import SocketModeHandler
import threading
import qrcode
from PIL import Image

SLACK_BOT_TOKEN= os.getenv('SLACK_BOT_TOKEN') # xoxb-xyz
SLACK_APP_TOKEN=  os.getenv('SLACK_APP_TOKEN') # xapp-1-xyz
app = App(token=SLACK_BOT_TOKEN)
client = WebClient(token=SLACK_BOT_TOKEN)

def generate_qr_logo(user_id, url):
    try:
        Logo_link = '/app/vinai.png'
        logo = Image.open(Logo_link)
        # taking base width
        basewidth = 100
        # adjust image size
        wpercent = (basewidth/float(logo.size[0]))
        hsize = int((float(logo.size[1])*float(wpercent)))
        logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
        QRcode = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H
        )
        # adding URL or text to QRcode
        QRcode.add_data(url)
        # generating QR code
        QRcode.make()
        # taking color name from user
        QRcolor = (79,135,229)
        # adding color to QR code
        QRimg = QRcode.make_image(
            fill_color=QRcolor, back_color="white").convert('RGB')
        # set size of QR code
        pos = ((QRimg.size[0] - logo.size[0]) // 2,
               (QRimg.size[1] - logo.size[1]) // 2)
        QRimg.paste(logo, pos)
        img_path = f'/tmp/vinai_{user_id}.png'
        QRimg.save(img_path)     
        # save the QR code generated
        return img_path  # Trả về đường dẫn của file QR code
    except Exception as e:
        print(f"Error generating QR code: {e}")
        return None

def generate_qr(user_id,url):
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Save QR code image
        img_path = f'/tmp/{user_id}.png'
        img.save(img_path)
        return img_path  # Trả về đường dẫn của file QR code
    except Exception as e:
        print(f"Error generating QR code: {e}")
        return None

@app.command("/qr-url")
def qr_url(ack, command,say):
    ack()
    channel_id = command["channel_id"]
    user_id = command["user_id"]
    channel_name = command["channel_name"]
    # Lấy thông tin về user và date từ text nhập vào
    text = command["text"]  # Text nhập vào từ người dùng
    parts = text.split()  # Tách text thành các phần
    # Kiểm tra xem có đủ thông tin user và date không
    if len(parts) == 1:
        url = parts[0]  #
        if 'http://' in url or 'https://' in url:
            try:
                print(user_id,'=>',url)
                img_path = generate_qr(user_id, url)
                if img_path:
                    client = WebClient(token=SLACK_BOT_TOKEN)
                    response = client.files_upload(
                        channels=channel_id,
                        file=img_path,
                        title=f'QR Code for {url}',
                        initial_comment=f'QR Code generated for {url}',
                    )
                    
                    # Xóa file QR code sau khi đã gửi
                    os.remove(img_path)                    
                else:
                    say(text=f"Error generating QR code for {url}")
            except SlackApiError as e:
                say(channel=channel_id, text=f"Error disabling user: {e}")
        else:
            say(text="URL must include http:// or https://. Please try again!")
    else:
        say(text="URL not provided. Please try again!")
@app.command("/qr-vinai-url")
def qr_logo_url(ack, command,say):
    ack()
    channel_id = command["channel_id"]
    user_id = command["user_id"]
    channel_name = command["channel_name"]
    # Lấy thông tin về user và date từ text nhập vào
    text = command["text"]  # Text nhập vào từ người dùng
    parts = text.split()  # Tách text thành các phần
    # Kiểm tra xem có đủ thông tin user và date không
    if len(parts) == 1:
        url = parts[0]  #
        if 'http://' in url or 'https://' in url:
            try:
                print(user_id,'=>',url)
                img_path = generate_qr_logo(user_id, url)
                if img_path:
                    client = WebClient(token=SLACK_BOT_TOKEN)
                    response = client.files_upload(
                        channels=channel_id,
                        file=img_path,
                        title=f'QR Code for {url}',
                        initial_comment=f'QR Code generated for {url}',
                    )

                    # Xóa file QR code sau khi đã gửi
                    os.remove(img_path)
                else:
                    say(text=f"Error generating QR code for {url}")
            except SlackApiError as e:
                say(channel=channel_id, text=f"Error disabling user: {e}")
        else:
            say(text="URL must include http:// or https://. Please try again!")
    else:
        say(text="URL not provided. Please try again!")

def run_slack_app():
    while True:
        SocketModeHandler(app, SLACK_APP_TOKEN).start()
# Start your app
if __name__ == "__main__":
    slack_thread = threading.Thread(target=run_slack_app)
    slack_thread.start()


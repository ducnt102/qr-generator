# Sử dụng Python 3.8 làm base image
FROM python:3.8

# Thiết lập thư mục làm việc
WORKDIR /app

# Copy file slack.py vào thư mục /app trong container
COPY  qr-vinai.py /app/qr-vinai.py
COPY  rq.txt /app/rq.txt
COPY vinai.png /app/vinai.png

# Cài đặt Flask và requests
RUN pip install -r /app/rq.txt


# Chạy ứng dụng Flask khi container được khởi động
CMD ["python", "qr-vinai.py"]

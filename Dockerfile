FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /home/vanduong/data/work/Shou/
COPY requirements.txt /home/vanduong/data/work/Shou/
RUN pip install -r requirements.txt
COPY . /home/vanduong/data/work/Shou/
FROM debian:latest
WORKDIR /code
ADD https://bootstrap.pypa.io/get-pip.py get-pip.py
RUN apt update && apt install -y \
        python3 \
        && \
    python3 ./get-pip.py && \
    rm -rf /var/lib/apt/lists/* get-pip.py

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
ENTRYPOINT ["python3", "main.py"]

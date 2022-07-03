FROM python:3.9-slim
RUN apt update && apt install -y jq curl

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["./entrypoint.sh"]
CMD ["pytest", "-rA"]

FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8502
COPY . .

RUN mkdir /root/.streamlit
COPY config.toml /root/.streamlit/

ENTRYPOINT ["streamlit", "run"]
CMD ["🏠_Home.py"]

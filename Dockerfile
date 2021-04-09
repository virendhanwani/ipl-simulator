FROM python:3.6-buster
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD streamlit run simulator.py --server.port $PORT

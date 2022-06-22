FROM python:3.9.7

COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY ./ ./
EXPOSE 80
ENTRYPOINT ["uvicorn", "web_app.entrypoints:app", "--host", "0.0.0.0", "--port", "80", "--reload"]

ENV PYTHONPATH=/web_app:/web_app/adapters:/web_app/entrypoints:/web_app/model:/web_app/service:$PYTHONPATH

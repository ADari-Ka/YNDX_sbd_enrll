FROM python:3.9.7

COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY ./ ./
EXPOSE 8080
ENTRYPOINT ["uvicorn", "web_app.entrypoints:app", "--host", "0.0.0.0", "--port", "8080"]

ENV PYTHONPATH=/web_app:/web_app/adapters:/web_app/entrypoints:/web_app/model:/web_app/service:$PYTHONPATH

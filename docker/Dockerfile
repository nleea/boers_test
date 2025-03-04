FROM python:3.12

WORKDIR /app

COPY ./requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY ./ /app/

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "config.server.wsgi:application"]
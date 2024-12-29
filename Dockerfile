# FROM python:3.11-bookworm


# ENV PYTHONBUFFERED = 1

# WORKDIR /metatask


# COPY requirements.txt requirements.txt

# RUN pip3 install -r requirements.txt

# COPY . .

# CMD python manage.py runserver 0.0.0.0:8000


FROM python:3.11-bookworm

ENV PYTHONUNBUFFERED=1

WORKDIR /metatask

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "metatask.wsgi:application"]
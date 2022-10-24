FROM python:3
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
WORKDIR /app/me
COPY requirements.txt /app/me
RUN pip install -r requirements.txt

COPY . /app/me

# collectstatic will copy the staticfiles_src to staticfiles (published under /staticfiles)
RUN python manage.py collectstatic --noinput

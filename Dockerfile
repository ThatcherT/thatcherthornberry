FROM python:3
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
# Maybe this should only copy the parts that need to be on the running web server
COPY . /app/
# collectstatic will copy the staticfiles_src to staticfiles (published under /static)
RUN python manage.py collectstatic --noinput
FROM python:3
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
WORKDIR /usr/src/spotifly
COPY requirements.txt /app/spotifly
RUN pip install -r requirements.txt --no-cache-dir

RUN mkdir /app/me/staticfiles
RUN python manage.py collectstatic --noinput
# Maybe this should only copy the parts that need to be on the running web server
COPY . /app/spotifly/
# collectstatic will copy the staticfiles_src to staticfiles (published under /static)



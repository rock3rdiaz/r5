FROM python:3.9
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY . /app
RUN apt-get -y update && apt-get -y install nginx
RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile
COPY ./nginx_config.txt /etc/nginx/sites-available/r5
RUN ln -s /etc/nginx/sites-available/r5 /etc/nginx/sites-enabled/r5
RUN chmod +x ./entry_point.sh

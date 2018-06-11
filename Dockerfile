FROM geoffroygivry/tornadoworldcloudmysql
ADD . /code
WORKDIR /code
CMD ["python", "app.py"]


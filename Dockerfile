FROM geoffroygivry/tornadoworldcloudmysql

ADD . /code
WORKDIR /code

RUN apt-get update && apt-get install -y mysql-client

CMD python app.py --mysql_host=mysql 


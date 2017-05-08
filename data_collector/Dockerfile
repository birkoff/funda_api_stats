FROM ubuntu
MAINTAINER Hector ReyesAleman <birkoff.h@gmail.com>

RUN apt-get update
RUN apt-get update
RUN apt-get install -y python python-pip python-mysqldb
RUN pip install requests
RUN pip install boto3
RUN pip install pymysql

## MySQL and API Configuration
ENV DB_HOSTNAME <hostname>
ENV DB_USERNAME <username>
ENV DB_PASSWORD <password>
ENV DB_NAME <db_name>
ENV DB_TABLE <db_table>
ENV API_KEY <api_key>

ADD ./data_collector.py /data_collector.py

CMD ["python", "/data_collector.py"]
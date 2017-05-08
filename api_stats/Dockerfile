FROM amazonlinux:latest
MAINTAINER Hector ReyesAleman <birkoff.h@gmail.com>

RUN yum update -y

# install dependensies
RUN yum install -y curl git unzip nginx  php70 php70-fpm php70-cli php70-mysqlnd kmod kmod-devel kmod-libs

# install dev
RUN yum install -y vim nmap wget

RUN mkdir /var/www/funda_analytics_api && cd /var/www/funda_analytics_api

# install composer
RUN curl -sS https://getcomposer.org/installer | php && mv composer.phar /usr/bin/composer

# Copy Nginx Config File
COPY docker_files/nginx.conf /etc/nginx/nginx.conf
COPY docker_files/www.conf /etc/php-fpm-7.0.d/www.conf
COPY docker_files/bootstrap.sh /bootstrap.sh

## add application source file
ADD ./composer.json /var/www/funda_analytics_api
ADD ./web /var/www/funda_analytics_api/web
ADD ./src /var/www/funda_analytics_api/src
RUN cd /var/www/funda_analytics_api && /usr/bin/composer install

RUN echo "NETWORKING=yes" > /etc/sysconfig/network

EXPOSE 80
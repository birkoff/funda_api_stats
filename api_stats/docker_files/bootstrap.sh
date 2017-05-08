#!/usr/bin/env bash
service php-fpm restart
service nginx restart
echo "Open: http://localhost:8080/funda/topmakelaars?search=amsterdam&page=1"
echo "Open: http://localhost:8080/funda/topmakelaars?search=amsterdam/tuin&page=1"
bash
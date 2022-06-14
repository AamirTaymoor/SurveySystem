from http import server


instatll redis-server
pip install redis
/etc/init.d/redis-server stop
/etc/init.d/redis-server start
/etc/init.d/redis-server restart
# celery -A SurveySystem worker -l info
                          beat

                          
celery -A periodic beat --loglevel=info


pip3 install celery==4.4.2
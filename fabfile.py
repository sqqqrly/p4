from fabric.api import lcd, local

def prepare_deployment(trunk):
    local('manage.py test p4') 
    local('git add -p && git commit') # -p makes add interactive showing differences before adding.

def deploy():
    with lcd('/home/dohlemacher/dev/dj/production/p4/'):
        local('git pull /home/dohlemacher/dev/dj/dev/p4/')
        local('python manage.py migrate polls')
        local('python manage.py test polls')
        local('./manage.py runserver 127.0.0.1:8080')


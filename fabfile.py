from time import sleep

from fabric.api import run, cd, task, env

env.repo_path = '/root/bottle'

def _git_update(branch):
    with cd(env.repo_path):
        run('git fetch --all')
        run('git checkout {}'.format(branch))
        run('git reset --hard origin/{}'.format(branch))

@task
def build_docker_image():
    with cd(env.repo_path):
        run('docker build -t bottle .')

@task
def switch_color():
    old_color = run('ls /etc/nginx/sites-enabled | grep bottle-')
    if old_color == 'bottle-a':
        new_color = 'bottle-b'
        new_port = '8081'
    else:  # old_color == 'bottle-b'
        new_color = 'bottle-a'
        new_port = '8080'

    run('docker run -d -p {new_port}:8080 --name {new_color} bottle'.format(
        new_port=new_port, new_color=new_color))

    # health check
    # wait 1 sec to give time for the container to start
    sleep(1)
    response = run('curl -L http://localhost/stage/')

    if 'Hello world' in response:
        run('rm /etc/nginx/sites-enabled/{}'.format(old_color))
        run('ln -s /etc/nginx/sites-available/{new_color} '
            '/etc/nginx/sites-enabled/{new_color}'.format(
            new_color=new_color))
        run('service nginx reload')

        run('docker stop {}'.format(old_color))
        run('docker rm {}'.format(old_color))
    else:
        run('docker kill {}'.format(new_color))
        run('docker rm {}'.format(new_color))

@task
def deploy(branch="master"):
    _git_update(branch)
    build_docker_image()
    switch_color()

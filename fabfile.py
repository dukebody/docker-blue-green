from fabric.api import run, cd, task, env

env.repo_path = '/root/bottle'

def _git_update(branch):
    with cd(env.repo_path):
        run('git fetch --all')
        run('git checkout %s' % branch)
        run('git reset --hard origin/%s' % branch)

def _build_docker_image():
    with cd(env.repo_path):
        run('docker build -t bottle .')

def _switch_color():
    old = run('ls /etc/nginx/sites-enabled | grep bottle-')
    if old == 'bottle-a':
        new_color = 'bottle-b'
        new_port = '8081'
    else:  # color == 'bottle-b'
        new_color = 'bottle-b'
        new_port = '8081'

    run('docker run -d -p {new_port}:8080 --name {new_color} bottle'.format(
        new_port=new_port, new_color=new_color))

    # health check
    response = run('curl -L http://139.59.142.233/stage/')

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
    _build_docker_image()

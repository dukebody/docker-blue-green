FROM python:3-onbuild
EXPOSE 8080
CMD [ "/usr/local/bin/gunicorn", "-w", "2", "-b", ":8080", "app:app" ]

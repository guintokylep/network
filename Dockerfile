FROM python:3
COPY . /Personal_File/networkApp
WORKDIR /Personal_File/networkApp
RUN pip install --user django
RUN pip install webdriver-manager
RUN pip install get-chrome-driver --upgrade
RUN pip install -r selenium/requirements.txt
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
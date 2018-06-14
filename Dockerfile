FROM python:3.5

LABEL Maintainer=alaxallves@gmail.com,arthur120496@gmail.com

COPY . /home

WORKDIR /home

RUN pip install -r requirements.txt

CMD ["bash", "-c",  "python", "rancherbot.py"]

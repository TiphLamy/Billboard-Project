FROM python:3.6

RUN mkdir /home/dev/ && mkdir /home/dev/code/

WORKDIR /home/dev/code/

ENV http_proxy http://147.215.1.189:3128
ENV https_proxy http://147.215.1.189:3128

COPY . .
RUN  pip install --upgrade pip &&  pip install pipenv && pipenv install --skip-lock

#CMD ["export","FLASK_APP=Projet-billoard/test_flask.py"]

#CMD ["pipenv", "run",  "bash", "run"]

CMD ["pipenv", "run", "jupyter", "notebook", "--ip=0.0.0.0", "--no-browser", "--allow-root", "--NotebookApp.token=''"]
#CMD ["/bin/bash"]


#Pour utiliser flask: l'ajouter dans les éléments à exécuter au dessus et ouvrir ses ports dans docker-compose.yml à la place de jupyter
# "flask" ou "jupyter", "notebook"

#FROM mambaorg/micromamba:0.15.3
#USER root
#RUN mkdir /opt/streamlit-datauploader
#RUN chmod -R 777 /opt/streamlit-datauploader
#WORKDIR /opt/streamlit-datauploader
#USER micromamba
#COPY environment.yml environment.yml
#RUN micromamba install -y -n base -f environment.yml && \
#   micromamba clean --all --yes
#COPY . .
#USER root
#RUN chmod a+x run.sh
#CMD ["./run.sh"]

FROM python:3.8.6
EXPOSE 8501
cmd mkdir -p /app
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
RUN npm install 
COPY . .
RUN chmod +x run.sh
#ENTRYPOINT ["streamlit", "run"]
CMD ["./run.sh"]
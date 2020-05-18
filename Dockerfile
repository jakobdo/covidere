FROM python:3.8-buster
RUN apt-get update && apt-get install -y binutils gdal-bin python3-gdal net-tools
ENV PROJECT_ROOT /app
WORKDIR $PROJECT_ROOT
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
RUN chmod +X entrypoint.sh
RUN chmod 777 entrypoint.sh
CMD ./entrypoint.sh

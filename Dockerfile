FROM python:alpine
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt 
RUN apk add mediainfo
EXPOSE 8836
ENTRYPOINT [ "python" ] 
CMD [ "basedapi.py" ] 

FROM python:3
COPY db ./db
COPY error ./error
COPY helpers ./helpers
COPY screenshot ./screenshot
COPY services ./services
COPY .env ./.env
COPY license ./license
COPY main.py ./main.py
COPY README.md ./README.md
COPY requirements.txt ./requirements.txt
RUN apt-get update
RUN pip3 install -r requirements.txt
CMD ["python3", "main.py", "--crone"]
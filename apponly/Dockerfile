# Use an official Python runtime as a parent image
FROM alpine:3.6

# Set the working directory to /app
WORKDIR /app

#Setup Repositories and install Python and Nodejs 
#RUN sudo apt-get install -y build-essential
RUN apk update && apk upgrade
RUN apk --no-cache add \
    python3 \
    python3-dev \
    build-base \
    postgresql-dev \
    bash \
    git \
    libffi \
    libffi-dev \
    linux-headers

# Setup Python Environment
RUN  if [[ ! -e /usr/bin/python ]];        then ln -sf /usr/bin/python3 /usr/bin/python; fi \
  && if [[ ! -e /usr/bin/python-config ]]; then ln -sf /usr/bin/python3-config /usr/bin/python-config; fi \
  && if [[ ! -e /usr/bin/pydoc ]];         then ln -sf /usr/bin/pydoc3 /usr/bin/pydoc; fi \
  && if [[ ! -e /usr/bin/easy_install ]];  then ln -sf $(ls /usr/bin/easy_install*) /usr/bin/easy_install; fi

RUN easy_install pip \
  && pip install --upgrade pip \
  && if [[ ! -e /usr/bin/pip ]]; then ln -sf /usr/bin/pip3 /usr/bin/pip; fi

# Clone our GitHub Repository
RUN git clone -b worker_executables --single-branch --progress --verbose https://www.github.com/nsacyber/WALKOFF.git ./walkoff
#RUN pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple walkoff[redis]==0.8.3b7 --no-cache-dir

# Setup WALKOFF
#RUN echo "walkoff" | walkoff-setup
WORKDIR /app/walkoff

RUN git reset --hard 0a779cfaeda15782877b67c89389b223378b2fbd

RUN python setup_walkoff.py
RUN pip install redis
RUN pip install psycopg2

# Copy resources to load apps/workflows
#ADD . /app

# Set the working directory to /walkoff
#WORKDIR /app/walkoff

COPY [ "./app.py", "/app/walkoff/apps/HelloWorld" ]
COPY [ "./update_config.py", "/app/walkoff/" ]
COPY [ "./dist", "/app/walkoff/walkoff/client/dist" ]
COPY [ "./node_modules", "/app/walkoff/walkoff/client/node_modules" ]
COPY [ "./.certificates", "/app/walkoff/.certificates" ]

RUN python update_config.py

RUN ping 127.0.0.1 -c 1

# Make port 5000 available to the world outside this container
EXPOSE 80 5556 5557

# Run WALKOFF
#CMD walkoff-run
CMD python walkoff.py -a -c data/walkoff.config
#CMD /bin/bash
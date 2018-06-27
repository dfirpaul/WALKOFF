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
    bash \ 
    git \
    make \
    g++ \
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
#RUN git clone -b development https://www.github.com/iadgov/WALKOFF.git ./walkoff
RUN pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple walkoff==0.8.3b7 --no-cache-dir

# Setup WALKOFF
RUN echo "walkoff" | walkoff-setup

# Copy resources to load apps/workflows
#ADD . /app

# Set the working directory to /walkoff
WORKDIR /app/walkoff

COPY [ "./update_config.py", "/app/walkoff/" ]

RUN python update_config.py

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run WALKOFF
CMD walkoff-run
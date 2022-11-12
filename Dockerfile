# copy the file with the necessary libraries that we want to install
COPY ./requirements.txt /root/requirements.txt

# update pip and install libraries from requirements, --ignore-installed - reinstall packages if they already exist
RUN pip install --upgrade pip && \
    pip install --ignore-installed -r /root/requirements.txt

# creating a working directory
WORKDIR /root/docker_test

# copying all files that are not specified in dockerignore to a new directory
COPY . /root/docker_test

# running the script, install train for a new project.py and make key_load_img: True in the params.yaml file
CMD ["python", "model_pipeline.py"]
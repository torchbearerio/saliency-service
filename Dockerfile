FROM debian:8.5

MAINTAINER Kamil Kwiek <kamil.kwiek@continuum.io>

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

RUN apt-get update --fix-missing && apt-get install -y wget bzip2 ca-certificates \
    libglib2.0-0 libxext6 libsm6 libxrender1 \
    git mercurial subversion

RUN echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh && \
    wget --quiet https://repo.continuum.io/archive/Anaconda2-4.3.1-Linux-x86_64.sh -O ~/anaconda.sh && \
    /bin/bash ~/anaconda.sh -b -p /opt/conda && \
    rm ~/anaconda.sh

ENV PATH /opt/conda/bin:$PATH

RUN apt-get install -y curl grep sed dpkg && \
    TINI_VERSION=`curl https://github.com/krallin/tini/releases/latest | grep -o "/v.*\"" | sed 's:^..\(.*\).$:\1:'` && \
    curl -L "https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini_${TINI_VERSION}.deb" > tini.deb && \
    dpkg -i tini.deb && \
    rm tini.deb && \
    apt-get clean

RUN apt-get install -y libmysqlclient-dev

RUN apt-get install -y build-essential

ADD environment.yml environment.yml
RUN conda env create -f environment.yml
ENV PATH /opt/conda/envs/torchbearer-services/bin:$PATH
RUN pip install git+https://github.com/torchbearerio/python-core.git --upgrade

ADD saliencyservice app

EXPOSE 8080
ENV PORT 8080

ENTRYPOINT [ "/usr/bin/tini", "--" ]
CMD [ "python", "-m", "app" ]

FROM osgeo_custom

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src

RUN apt-get update

RUN apt-get -qq -y install python3 python3-dev gfortran gcc libc-dev musl-dev libffi-dev
RUN apt-get -qq -y install musl-dev


RUN pip install -U pip && python3 -m pip install -U pip

RUN pip install numpy && pip3 install numpy

RUN pip install h5py netCDF4 PyYAML pillow

COPY requirements.txt .

#RUN pip install -r requirements.txt

COPY . .

CMD ["python", "tiff2nc.py"]


# syntax=docker/dockerfile:1
FROM python:3.9.6 as base
LABEL maintainer="AlexMGitHub@gmail.com"
WORKDIR /twe
# Copy over minimum required files to install TheWholeEnchilada package
COPY setup.py  ./
COPY src/__init__.py ./src/__init__.py
# Copy the requirements.txt separately so build cache only busts if requirements.txt changes
COPY docker/bokeh_requirements.txt ./
# Reduce image size by not caching .whl files
RUN pip3 install --no-cache-dir -r bokeh_requirements.txt
# Add and run as non-root user for security reasons (after installation)
RUN useradd -ms /bin/bash bokeh
# Change ownership of Bokeh data directory to bokeh user
#COPY src/bokeh_server/data/ ./data/
#RUN chown bokeh data/
USER bokeh
# Expose Bokeh server default port
EXPOSE 5006
# Bokeh environment variables
ENV BOKEH_ALLOW_WS_ORIGIN=localhost:5000,localhost:5006
ENV BOKEH_SIGN_SESSIONS=yes


FROM base as development
# Copy boot.sh shell script to run commands on container spin-up
COPY src/bokeh_server/boot.sh ./src/bokeh_server/boot.sh
# Development webserver
LABEL build="development"
ENV BOKEH_ENV=development
ENTRYPOINT ["./src/bokeh_server/boot.sh"]


FROM base as production
# Copy entire application to Docker image
COPY . ./
# Production webserver
LABEL build="production"
ENV BOKEH_ENV=production
ENTRYPOINT ["./src/bokeh_server/boot.sh"]
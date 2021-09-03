# syntax=docker/dockerfile:1
FROM python:3.9.6 as base
LABEL maintainer="AlexMGitHub@gmail.com"
WORKDIR /twe
# Copy over minimum required files to install TheWholeEnchilada package
COPY setup.py  ./
COPY src/__init__.py ./src/__init__.py
# Copy the requirements.txt separately so build cache only busts if requirements.txt changes
COPY docker/webapp_requirements.txt ./
# Reduce image size by not caching .whl files
RUN pip3 install --no-cache-dir -r webapp_requirements.txt
# Add and run as non-root user for security reasons (after installation)
RUN useradd -ms /bin/bash webapp
# Copy data directory used as Docker volume between web and bokeh services
COPY src/bokeh_server/data/ src/bokeh_server/data/
# Change ownership of Bokeh data directory from root to webapp user
RUN chown webapp src/bokeh_server/data/
USER webapp
# Expose Flask webapp port
EXPOSE 5000
# Flask environment variables
ENV FLASK_APP=./src/webapp.py
# Listen for connections on public network interface
ENV FLASK_RUN_HOST=0.0.0.0


FROM base as development
# Development webserver
LABEL build="development"
ENV FLASK_ENV=development
ENTRYPOINT ["flask", "run"]


FROM base as production
# Copy entire application to Docker image
COPY . ./
# Production webserver
LABEL build="production"
ENV FLASK_ENV=production
ENTRYPOINT ["waitress-serve", "--port=5000", "webapp:app"]
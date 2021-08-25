# TheWholeEnchilada

- shows all environment vars, including secret vars used as environment variables
 `docker exec <container> env`

- Shows container's secret files
`docker container exec $(docker ps --filter name=<container> -q) ls -l /run/secrets`

- View secret
`docker container exec $(docker ps --filter name=<container> -q) cat /run/secrets/<secret>`

docker container exec $(docker ps --filter name=thewholeenchilada_db_1 -q) cat /run/secrets/db_root_password

- get into container's terminal
`docker exec -it thewholeenchilada_db_1 bash`

## Todo
- Read chapter 3 of mysql connector/python revealed
- Read the entire connector/python guide and tutorial at:
  - https://dev.mysql.com/doc/connector-python/en/connector-python-coding.html
- Refer to docker documentation about running tests - there seems to be a command line way to trigger different behavior when running the dockerfile
  - https://docs.docker.com/language/java/run-tests/
  - Can this be done with docker-compose as well?
- Have pytest write a report to file using
  - `--junitxml=C:\path\to\out_report.xml`
- Search for dockerfile/docker-compose textbook?
- Review yield for fixtures
  - I think my code will work, as the class is returned to the test functions as an instantiated object, and the yield is part of the init of the object
  - But double-check the examples in the pytest book
- Remove storing chapter queries from the pytest fixture
  - The tests can directly instantiate the class from the file under test, and the sql files will only be read once per test

- Found several docker books, and a docker web tutorial:
  - https://realpython.com/dockerizing-flask-with-compose-and-machine-from-localhost-to-the-cloud/

- Need to run pytest programmatically as a subprocess or changes to the test code won't be recognized
  - https://github.com/pytest-dev/pytest/issues/3143

- add pytest commandline options
- https://docs.pytest.org/en/6.2.x/example/simple.html

## Docker commands

The following commands apply to the temporary Machine Learning/working/mysql/ directory

- Run mysql docker image (make sure VPN temporarily disconnected first time this command is run):
`sudo docker-compose up`

- In another terminal tab, access mysql server through command line
`docker exec -it mysql_db_1 bash`

- Log in to MySQL as root:
`mysql -uroot -p`
  - Then enter password (currently `example`)

- Run script to populate database
  - For some reason database is retaining data after the container is shut down
  - What am I misunderstanding about the -it argument?
`mysql -uroot -p < create_databases.sql`

- Need to reference root directory specified in volumes: of docker-compose file
  - e.g. mysql/create_databases.sql

- Can run .sql file from inside MySQL prompt (logged in as root):
`source mysql/create_databases.sql`

- Can also create databases inside

#### Docker Questions

- Once I learn the SQL commands to my satisfaction, the next step is to figure out docker for msql
  - What ports should I use?  I see 8080:8080 but also 3006:3006 or something similar
  - How do I make the database persistent?
  - How do I make the database completely delete when the container spins down?
    - `docker run --rm`
    - `docker-compose down`
  - Refresh on volumes: in my old project I set it to some lib/var folder, but I can also set it to a local directory
    - I remember that wasn't preferred; they'd rather have docker manage the data internally
  - How do I set up docker secrets for the password?
  - How do I set up non-root user accounts?

- Share volume between two containers without using host:
  - https://stackoverflow.com/questions/43559619/docker-compose-how-to-mount-path-from-one-to-another-container
  - Allows me to pickle data and provide it to bokeh server
  - must change owner of data folder in webapp container so that it can write/delete files
  - bokeh can be read only

- Check all existing containers, running or stopped:
`docker ps -a`

`pip install -r requirements.txt`

## Trouble shooting
- Had errors using docker-compose up with mysql
- Started deleting docker images, but received error that the images that I saw user `docker images` did not exist
- According to stackoverflow docker is corrupt and service must be stopped, deleted, and restarted

https://stackoverflow.com/questions/46381888/docker-images-shows-image-docker-rmi-says-no-such-image-or-reference-doe/46386670

```
This means that your docker state is corrupted and you need clear the complete state

sudo service docker stop
sudo rm -rf /var/lib/docker
sudo service docker start

This will start docker fresh without any existing data. Try pulling deleting the image after this and see if all works. If it doesn't then there is some issue that needs to be looked into
```

- Get into MySQL container with a bash shell
`docker exec -it your_container_name_or_id bash`

- Default password of root is a blank password.  This occurs if environment variables from docker-compose file are not being used
`mysql -uroot -p`
https://github.com/docker-library/mysql/issues/275

- Environment variables get overridden or ignored if the mysql db has a volume
  - Volume allows storage of sql files and so environment vars are ignored
  - How do I have persistent storage and not ignore environment vars?
  - https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/docker-mysql-more-topics.html#docker-persisting-data-configuration

https://docs.docker.com/develop/develop-images/dockerfile_best-practices/

https://improveandrepeat.com/2021/01/python-friday-54-create-a-report-for-your-test-results-with-pytest/

- Check if db exists
```
cursor.execute("SHOW DATABASES LIKE 'ap'")
if cursor.rowcount == 0:  # db doesn't exist
  <do something>
```

### Notes
- Use ubuntu:20.04 docker image for python:
  - https://pythonspeed.com/articles/base-image-python-docker-images/
  - https://pythonspeed.com/articles/alpine-docker-python/
  - Alpine is slow with python and doesn't support .whl files, whereas ubuntu;20.04 has up to date python support and is faster according to speed tests

- Todo on docker stuff:
  - Check out multi-stage builds for creating the final build image
    - Need to copy source code to image rather than use volume
  - Connect github to dockerhub?
  - Run final image on Amazon?
- Use config.py or docker secrets for MySQL password?
- Create a MySQL user with non-root privileges for the flask web app
- https://git-scm.com/book/en/v2 git book
- https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
- https://blog.andreiavram.ro/docker-multi-stage-builds-docker-compose/
- https://stackoverflow.com/questions/53093487/multi-stage-build-in-docker-compose/53101932#53101932
- https://docs.docker.com/compose/compose-file/compose-file-v3/#build
- Non-root user for flask container:
  - https://www.patricksoftwareblog.com/using-docker-for-flask-application-development-not-just-production/
- Use bootstrap-flask extension, not flask-bootstrap as the latter is outdated and not maintained
- https://github.com/flask-debugtoolbar/flask-debugtoolbar

## MySQL Default Authentication Method
As of MySQL 8.0, the default authentication method is `caching_sha2_password`.  The example Docker Compose YAML shown on the [Docker MySQL server image on Docker Hub](https://hub.docker.com/_/mysql/) still lists `mysql_native_password`.  This should be changed to `caching_sha2_password` in the YAML file for MySQL 8.0, and specified as the `auth_plugin` when connecting to the server using MySQL Connector/Python.


## Passing Credentials and Sensitive Information using Docker Secrets

The MySQL passwords and Flask secret key should not be hard-coded in plain text in either the Flask Python code or the Docker Compose YAML file.  A common approach in non-Docker contexts is to create a file (typically named `.env`) containing the sensitive information and use [python-dotenv](https://pypi.org/project/python-dotenv/) to load the sensitive data into environment variables.  So long as this `.env` file is not committed to source control or copied to the Docker image it would appear to be a secure method to pass sensitive data to the Docker containers.

The problem with the environment variable approach is that the sensitive information stored in the environment could be viewed by an end user.  This is a potential security risk, and so Docker recommends the so-called "Docker secrets" approach to handling sensitive information that needs to be passed to Docker containers.

Docker secrets encrypts passwords or other sensitive information and only makes it available to services that have been granted explicit access to it.  The key here is that the secrets are only available to *services*, not standalone containers.  This approach will thus only work with Docker Compose and Docker Swarm.  The official documentation for Docker secrets has an [example using Docker Compose](https://docs.docker.com/engine/swarm/secrets/#use-secrets-in-compose) for a MySQL database - exactly my use-case!  The MySQL environment variables in the YAML file can be set to named secret variables, which in turn point to unencrypted files that store the passwords in plain text on the local machine.  The contents of these local files are encrypted and stored in the Docker image.  When a container is created from the image, the contents of the secret files are decrypted and stored in `/run/secrets/` in the memory of the container.  The decrypted information is then accessible by code run inside the container.

The documentation does not provide any information as to the formatting of these files, or whether multiple passwords could be stored in a single file.  I assume that each file can only contain one password.

The final configuration requires four separate files:
- **bokeh_secret_key.txt** to supply a secret key to both the Bokeh and Flask servers
- **db_root_password.txt** to supply the secret root password to the MySQL and Flask servers
- **db_user_password.txt** to supply the secret user password to the MySQL server
- **web_secret_key.txt** to supply a secret key to the Flask webserver for generating CSRF tokens

I've included examples of these files (suffixed with '_example') in this repository for reference.  They are meant to be copied and renamed to the filenames above and filled out with the desired passwords.  All secret files are added to both `.gitignore` and `.dockerignore` so that the sensitive information that they contain does not end up in the Git repository or the Docker image, respectively.


## References

1. Flask Web Development, Miguel Grinberg
2. The Docker Book, James Turnbull
3. Murach's MySQL, 3rd edition, Mike Murach
4. Oracle's MySQL Connector/Python documentation

Cite datasets origin/license if applicable

<div>Icons made by <a href="" title="Icongeek26">Icongeek26</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>

### User
user_loader has to hit database on every pageview, find stackoverflow link
secret key for flask-login
need to run integration tests as root

### Multi-stage Docker Files
Use multi-stage docker file approach for creating development/production builds


### Users currently logged in to MySQL
`docker exec -it thewholeenchilada_db_1 bash`
`mysql -uroot -p`
Enter root password r00tb33rfl0@t

```
SELECT SUBSTRING_INDEX(host, ':', 1) AS host_short,
       GROUP_CONCAT(DISTINCT user) AS users,
       COUNT(*) AS threads
FROM information_schema.processlist
GROUP BY host_short
ORDER BY COUNT(*), host_short;
```


### MySQL commands

- Check docker container's timezone
`docker exec -it thewholeenchilada_web_1 cat /etc/timezone`

- First create bash terminal
`docker exec -it thewholenchilada_db_1 bash`

- Change directory to mysql volume
`cd mysql`

- Dump entire database to a file
`mysqldump -uroot -p --all-databases > dump.sql`

- Load dump into mysql database:
`mysql -uroot -p < dump.sql`


## Website notes
- Dashboard welcomes user by name, has bootstrap features page with all the stuff you can do
  - https://getbootstrap.com/docs/5.1/examples/features/
- Datasets main page will have a dropdown menu of available datasets
  - summary statistics of selected dataset, maybe a plot of a few features
  - load databases sidebar sub-option
  - header of first 5 or 10 items in dataset
  - maybe describe results showing data types?
  - EDA?
- Train: should give model options for selected dataset
  - Tune hyper parameters?  Maybe use settings icon for sidebar sub-option
  - available models linear regression, ridge/lasso, svm, k-nearest neighbors, etc
  - Distinguish between classification/regression problems?
- Charts - results from trained model
  - accuracy/error - or should this be in train?
  - Bokeh charts
  - confusion matrices - should this be in train?
- Testing
  - Dev only feature?


### Bokeh
- Use webgl option to speed up rendering
- Use tabs for different ML models?
- bokeh authentication
- “We write the JavaScript, so you don’t have to”

`Bokeh` is a Python data visualization library that links with `BokehJS`, a JavaScript client library that actually renders the visuals in a web browser.  `Bokeh` allows you to create interactive plots and widgets in Python that can be deployed in web apps or Jupyter notebooks, while handling all of the JavaScript behind the scenes.  Their documentation states _**“We write the JavaScript, so you don’t have to."**_

`Bokeh` will generate all of the HTML and JavaScript necessary to create beautiful interactive plots with dropdown menus, tabs, slider bars, radio buttons, and other types of widgets.  However, there is a catch: callback functions are required to make the widgets interactive.  The standalone HTML file generated by `Bokeh` will work fine for simple plots that only require zooming and panning, but if widgets are desired a `Bokeh` server must be run to set up event handlers.  As stated in the documentation:

> The primary purpose of the Bokeh server is to synchronize data between the underlying Python environment and the BokehJS library running in the browser.

The only other option is to write [JavaScript callbacks](https://docs.bokeh.org/en/latest/docs/user_guide/interaction/callbacks.html#userguide-interaction-jscallbacks) that can be embedded in the page along with the visualization itself.  Seeing as that would violate the spirit of `Bokeh` (and because I don't want write JavaScript) I chose to run a `Bokeh` server in a separate Docker container to serve my plots.

#### Setting up a Bokeh server
Setting up the `Bokeh` server ended up being trickier than I had imagined.  The `Bokeh` server must be accessible to both the `Flask` webserver residing inside the Docker network, and to the client (browser) viewing the `Bokeh` visualizations.  Per the documentation:

> To reduce the risk of cross-site misuse, the Bokeh server will only initiate WebSocket connections from the origins that are explicitly allowed. Requests with Origin headers that are not on the allowed list will generate HTTP 403 error responses.

And so in the `Bokeh` Dockerfile I added `ENV BOKEH_ALLOW_WS_ORIGIN=localhost:5000,localhost:5006` to allow access to requests originating from the `Flask` webserver and the user's browser, respectively.  But there's another gotcha: within the Docker network, `Flask` connects to the `Bokeh` server at `http://bokeh:5006/bokeh`.  However, the client (browser) will connect to the `Bokeh` server at `http://localhost:5006/`.  This causes a problem, because the script embedded into the `Jinja` template will contain an invalid URL!  To fix this, I simply use the Python `replace()` function to swap out the URLs before rendering the `Jinja` template.  This allows me to successfully serve a `Bokeh` visualization (with callbacks) from my `Flask` webserver.

#### Securing access to Bokeh server
However, this means that an unauthenticated user could gain access to the `Bokeh` visualizations just by navigating to `http://localhost:5006/bokeh` in their browser.  The `Bokeh` documentation discusses using [signed session IDs](https://docs.bokeh.org/en/latest/docs/user_guide/server.html?highlight=session_id%20options#signed-session-ids) to embed a `Bokeh` application inside a `Flask` webapp in such a way that *only* requests authorized by your webapp are accepted by the `Bokeh` server.  [This Stackoverflow post](https://stackoverflow.com/questions/43183531/simple-username-password-protection-of-a-bokeh-server) goes into greater detail on how to go about implementing this feature.  A secret key must be supplied to the `Bokeh` server and the `Flask` webapp.  A secure secret key can be conveniently generated for your use by typing `bokeh secret` into the terminal after installing `Bokeh`.  I passed the secret key to both containers using Docker secrets and set the `Bokeh` container's `BOKEH_SIGN_SESSIONS` environment variable to `yes` (documentation sometimes says to use `True`).  I set the `ENTRYPOINT` of the `Bokeh` Dockerfile to run a bash script to set the secret key as an environment variable.  I built the images, spun up the containers, and navigated my browser to the appropriate webapp route - but it didn't work!

Even after hours of fiddling with the code I continued to receive an error claiming that I had an invalid token signature when I attempted to serve a visualization through `Flask`.  After a great deal of frustrated web searching, I came across [this post](https://discourse.bokeh.org/t/flask-bokeh-externally-signed-sessions-invalid-token-signature-error/7059/4) that pointed out an omission in the documentation: the `BOKEH_SIGN_SESSIONS=yes` environment variable must also be passed to `Flask`!  If it's not, the session ID generated using `generate_session_id()` will not be signed, even if the `signed=True` argument is set in the function call!  Once I set this environment variable I was finally able to securely&dagger; serve `Bokeh` visualizations through my webapp with support for callbacks.

&dagger; *Not as securely as I would like, as the secret key must be contained in an environment variable as plain text.  Unfortunately, until the above bug is fixed there does not appear to be any other way to make the signed session ID approach work.*

#### Limitations of the Bokeh server
Not designed for multiple apps.
serve multiple apps by doing something like:

```bash
bokeh serve `ls *.py` --address 0.0.0.0 --session-ids external-signed
```

#### LRU Cache
- https://github.com/bokeh/bokeh/blob/branch-2.4/examples/app/stocks/main.py
- uses "least recently used" cache from functools
- caches responses so that repeated calls with teh same arguments can be returned without recalculating (memoization)
-

### Checking if the Bokeh plot has rendered
Large Bokeh visualizations take a few seconds to load, and so I added a Bootstrap spinner to my Jinja template to give a visual indication to the user that something is happening.  However, hiding the spinner once the visualization rendered again proved trickier than I expected.  I assumed that I could write a JavaScript function that is called on a `document.onreadystatechange` event to hide the spinner once the visualization renders, but that approach didn't work.  The document is considered to be completely loaded (`document.readyState === "complete"`) before the visualization is rendered, and so the spinner never appears on the page.  After some experimentation, I found that I could wrap the injected Bokeh JavaScript code in a `<div>` and use `ResizeObserver` to check if the height of the `<div>` was greater than zero.  If so, the visualization has rendered and the spinner can be hidden.

### Citation Policy:

If you publish material based on databases obtained from this repository, then, in your acknowledgements, please note the assistance you received by using this repository. This will help others to obtain the same data sets and replicate your experiments. We suggest the following pseudo-APA reference format for referring to this repository:

    Dua, D. and Graff, C. (2019). UCI Machine Learning Repository [http://archive.ics.uci.edu/ml]. Irvine, CA: University of California, School of Information and Computer Science.

https://www.kaggle.com/shwetabh123/mall-customers/version/1

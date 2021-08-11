# TheWholeEnchilada

- shows all environment vars, including secret vars used as environment variables
 `docker exec <container> env`

- Shows container's secret files
`docker container exec $(docker ps --filter name=<container> -q) ls -l /run/secrets`


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


## Credentials and Sensitive Information

The MySQL root and user passwords should not be hard-coded in plain text in either the Flask Python code or the Docker Compose YAML file.  A common approach is to use environment variables to securely pass credentials to Python code.  Corey Schafer's [environment variable tutorial](https://www.youtube.com/watch?v=5iWhQWVXosU) stores the MySQL credentials in `.bash_profile` and accesses them using `os.environ` in the Flask code.  This is a good way to go about it, but I ended up using [python-dotenv](https://pypi.org/project/python-dotenv/) instead.  It's essentially the same idea, but `python-dotenv` can create environment variables from any user-specified file (typically named `.env`).  It's a more general approach as it is not operating system dependent like using `.bash_profile`, and it allows the use of multiple files to store information.  This could be useful where a `.env` file stores non-sensitive environment variables that can be committed to source control, and a file like `.env_secrets` contains sensitive information like credentials that will not be committed to source control.

This allows me to securely pass the MySQL credentials to my Flask app, but the Docker [MySQL server image](https://hub.docker.com/_/mysql/) requires that the server's root password be passed to it as an environment variable in the Docker Compose YAML file.  This is also a potential security risk, and so Docker recommends the so-called "Docker secrets" approach to handling sensitive information that needs to be passed to Docker containers.

Docker secrets encrypts passwords or other sensitive information and only makes it available to services that have been granted explicit access to it.  The key here is that the secrets are only available to *services*, not standalone containers.  This approach will thus only work with Docker Compose and Docker Swarm.  I found the official documentation for Docker secrets to be confusing, but luckily at the very end of the documentation there is an [example using Docker Compose](https://docs.docker.com/engine/swarm/secrets/#use-secrets-in-compose) for a MySQL database - exactly what I needed!  The MySQL environment variables in the YAML file can be set to named secret variables, which in turn point to unencrypted files that store the passwords in plain text.  The documentation does not provide any information as to the formatting of these files, or whether multiple passwords could be stored in a single file.  I assume that each file can only contain one password.

The final configuration requires three separate files:
- **.env_secrets** to securely supply the MySQL login credentials and a secret key to my Flask app
- **db_root_password.txt** to supply the secret root password to the MySQL server
- **db_user_password.txt** to supply the secret user password to the MySQL server

I've included examples of these files (suffixed with '_example') in this repository for reference.  They are meant to be copied and renamed to the filenames above and filled out with the desired MySQL passwords.  All three secret files are added to both `.gitignore` and `.dockerignore` so that the sensitive information that they contain does not end up in the Git repository or the Docker image, respectively.

It would be nice to have some way of combining all of these password files into a single file, but I couldn't find a way to do so.  I suppose I could have the Flask app log into the database with a plain text root password and configure all of these parameters manually as a one-time configuration step.  However, I like having the root and user passwords set to a known quantity immediately on the MySQL server's first startup.  It also conveniently creates a specified database on image startup, along with a user account that has superuser access to the database.

## References

1. Flask Web Development, Miguel Grinberg
2. The Docker Book, James Turnbull
3. Murach's MySQL, 3rd edition, Mike Murach
4. Oracle's MySQL Connector/Python documentation

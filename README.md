### Docker
```shell
docker build -t vote_service .
docker compose up -d
```
### Swagger
```shell
localhost:8000/docs/
```
### Tests
```shell
pytest -v -rP
```
### Coverage
```shell
coverage erase && coverage run -m pytest && coverage report
```

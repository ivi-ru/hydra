PROJECT=openapi

# собрать docker контейнер
build:
	docker build -t $(PROJECT) -f Dockerfile .

# запустить сервис
run:
	docker run -it --rm -p 5000:5000 -v "$(shell pwd):/opt" $(PROJECT)

# собрать документацию
html:
	redoc-cli bundle -o index.html docs.yaml

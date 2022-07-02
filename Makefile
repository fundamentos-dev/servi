init:
	cp .env.example
build:
	docker-compose build --no-cache
	docker-compose up -d
	docker-compose logs -f
rebuild:
	docker-compose down --remove-orphans --volumes
	sudo rm -rf data
	make build
run: 
	docker-compose down
	docker-compose up -d
	docker-compose logs -f
logs: 
	docker-compose logs -f
down: 
	docker-compose down --remove-orphans --volumes
migrate:
	docker exec -it servi_app bash -c "python manage.py migrate"
terminal:
	docker exec -it servi_app bash
colectstatic:
	docker exec -it servi_app bash -c "python manage.py collectstatic"
seed:
	docker exec -it servi_app bash -c " \
		python manage.py loaddata bloco.yaml && \
		python manage.py loaddata estado_civil.yaml && \
		python manage.py loaddata funcao.yaml && \
		python manage.py loaddata motivo_afastamento.yaml && \
		python manage.py loaddata nivel_servico.yaml && \
		python manage.py loaddata profissao.yaml && \
		python manage.py loaddata origem_discipulo.yaml"
	docker exec -it servi_app bash -c "python manage.py shell < app/seed.py"	
connect:
	docker exec -it servi_db bash -c "psql -U postgres"
superuser:
	docker exec -it servi_app bash -c "python manage.py createsuperuser"
sass:
	docker exec -it servi_app bash -c "python manage.py sass /usr/src/app/static/scss/ /usr/src/app/static/css/ --watch"
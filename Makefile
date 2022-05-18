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
		python manage.py loaddata estado_civil.yml && \
		python manage.py loaddata funcao.yml && \
		python manage.py loaddata motivo_afastamento.yml && \
		python manage.py loaddata nivel_servico.yml && \
		python manage.py loaddata origem_discipulo.yml"
	docker exec -it servi_app bash -c "python manage.py migrate shell < app/seed.py"	

	
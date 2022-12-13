Run With Docker
=====================
Comand:

`docker-compose --file docker-compose.yml up -d`

Endpoints:
- Swagger GET `http://127.0.0.1:8001/swagger/`
- Decode the VIN GET `http://127.0.0.1:8001/api/vin-decode-views-style/<VIN Code>/`
- Decode the VIN with class based style GET `http://127.0.0.1:8001/api/vin-decode-class-based-style/<VIN Code>/`
- Cars (CRUD) `http://127.0.0.1:8001/api/cars` and `http://127.0.0.1:8001/api/cars/<pk>/`
- Weight (CRUD) `http://127.0.0.1:8001/api/weights` and `http://127.0.0.1:8001/api/weights/<pk>/`

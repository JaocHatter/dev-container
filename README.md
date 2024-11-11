# Práctica 3

**Nombre y Apellido:** Jared Aristóteles Orihuela Contreras<br>
**Código:** 20220370F
---
## Parte 1: Sistema de Autenticación usando Json Web Tokenss

### Librerías:
- PyJWT
- bcrypt

### Estructura del proyecto:
```bash
|-- main.py
|-- src
|   |-- exceptions.py
|   |-- interfaces
|   |   |-- token_service.py
|   |   `-- user_repository.py
|   |-- models
|   |   `-- user.py
|   |-- repositories
|   |   `-- memory_user_repository.py
|   `-- services
|       |-- authentication_service.py
|       `-- jwt_token_service.py
`-- tests
    |-- test_authentication_service.py
    |-- test_jwt_token_service.py
    `-- test_memory_user.py
```
!(alt text)[images/img1.png]
## Parte 2: Monitor de Sistemas de Archivos


Este conjunto de archivos (HTML, PHP, CSS) forma un sistema completo para el registro y autenticación de vehículos, con interfaz estilo "glass morphism". Permite:

Registro de nuevos vehículos:

Almacena datos del propietario (nombre, teléfono, email)

Registra información del vehículo (placa, marca, modelo, color, año)

Genera un código de bloqueo único

Guarda los datos en base de datos MySQL via XAMPP

Autenticación de usuarios:

Login seguro con email y contraseña

Visualización de datos registrados

Protección contra inyecciones SQL

Componentes clave:

registro.html:

Interfaz principal de registro

Formulario con validaciones

Modal de confirmación post-registro

Enlace a pantalla de login

login.html:

Formulario de autenticación

Visualización de datos del vehículo

Enlace a pantalla de registro

registrar.php:

Backend para procesar registros

Conexión a base de datos MySQL

Generación de códigos únicos

Validación de datos

login.php:

Autenticación segura

Verificación de credenciales

Retorno de datos del vehículo

Flujo del sistema:

Nuevos usuarios → registro.html → registrar.php → Base de datos

Usuarios existentes → login.html → login.php → Visualización de datos

Características técnicas:

Diseño responsive (adaptable a móviles)

Transiciones y efectos visuales suaves

Protección básica contra inyecciones SQL

Almacenamiento seguro de contraseñas (hash)

Validación de campos en frontend y backend

Requisitos:

Servidor XAMPP con:

Apache activado

MySQL funcionando

PHP 7.0+

Base de datos "registro_vehiculos" con tabla "vehiculos"
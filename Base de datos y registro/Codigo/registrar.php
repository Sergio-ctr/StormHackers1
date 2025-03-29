<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST');
header('Access-Control-Allow-Headers: Content-Type');

$response = [
    'success' => false,
    'message' => 'Error desconocido',
    'codigo' => '',
    'error_details' => ''
];

try {
    // Verificar si es una solicitud POST
    if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
        throw new Exception("Método no permitido", 405);
    }

    // Obtener datos del POST
    $json = file_get_contents('php://input');
    if (empty($json)) {
        throw new Exception("No se recibieron datos", 400);
    }

    $data = json_decode($json, true);
    if (json_last_error() !== JSON_ERROR_NONE) {
        throw new Exception("JSON inválido: " . json_last_error_msg(), 400);
    }

    // Validar datos requeridos
    $required = ['nombre', 'apellido', 'telefono', 'email', 'password', 'placa', 'marca', 'modelo'];
    foreach ($required as $field) {
        if (empty($data[$field])) {
            throw new Exception("El campo $field es requerido", 400);
        }
    }

    // Validar formato de email
    if (!filter_var($data['email'], FILTER_VALIDATE_EMAIL)) {
        throw new Exception("El formato del email es inválido", 400);
    }

    // Conexión a la base de datos
    $servername = "localhost";
    $username = "root";
    $password = "";
    $dbname = "registro_vehiculos";

    $conn = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $conn->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);

    // Verificar si el email ya existe
    $stmt = $conn->prepare("SELECT id FROM vehiculos WHERE email = :email");
    $stmt->execute([':email' => $data['email']]);
    if ($stmt->fetch()) {
        throw new Exception("El email ya está registrado", 409);
    }

    // Verificar si la placa ya existe
    $stmt = $conn->prepare("SELECT id FROM vehiculos WHERE placa = :placa");
    $stmt->execute([':placa' => $data['placa']]);
    if ($stmt->fetch()) {
        throw new Exception("La placa ya está registrada", 409);
    }

    // Generar código de bloqueo
    $codigo_bloqueo = str_pad(rand(0, 9999), 4, '0', STR_PAD_LEFT);

    // Insertar en la base de datos
    $stmt = $conn->prepare("INSERT INTO vehiculos 
        (nombre, apellido, telefono, email, password, placa, marca, modelo, color, anio, codigo_bloqueo) 
        VALUES 
        (:nombre, :apellido, :telefono, :email, :password, :placa, :marca, :modelo, :color, :anio, :codigo)");
    
    $stmt->execute([
        ':nombre' => htmlspecialchars($data['nombre'], ENT_QUOTES, 'UTF-8'),
        ':apellido' => htmlspecialchars($data['apellido'], ENT_QUOTES, 'UTF-8'),
        ':telefono' => htmlspecialchars($data['telefono'], ENT_QUOTES, 'UTF-8'),
        ':email' => htmlspecialchars($data['email'], ENT_QUOTES, 'UTF-8'),
        ':password' => password_hash($data['password'], PASSWORD_DEFAULT),
        ':placa' => htmlspecialchars($data['placa'], ENT_QUOTES, 'UTF-8'),
        ':marca' => htmlspecialchars($data['marca'], ENT_QUOTES, 'UTF-8'),
        ':modelo' => htmlspecialchars($data['modelo'], ENT_QUOTES, 'UTF-8'),
        ':color' => isset($data['color']) ? htmlspecialchars($data['color'], ENT_QUOTES, 'UTF-8') : null,
        ':anio' => isset($data['anio']) && is_numeric($data['anio']) ? (int)$data['anio'] : null,
        ':codigo' => $codigo_bloqueo
    ]);

    $response = [
        'success' => true,
        'message' => 'Registro exitoso',
        'codigo' => $codigo_bloqueo,
        'error_details' => ''
    ];

} catch(PDOException $e) {
    $response = [
        'success' => false,
        'message' => 'Error en la base de datos',
        'codigo' => '',
        'error_details' => $e->getMessage()
    ];
    http_response_code(500);
} catch(Exception $e) {
    $response = [
        'success' => false,
        'message' => $e->getMessage(),
        'codigo' => '',
        'error_details' => $e->getCode() . ': ' . $e->getMessage()
    ];
    http_response_code($e->getCode() >= 400 && $e->getCode() < 600 ? $e->getCode() : 400);
}

echo json_encode($response);
?>
<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST');
header('Access-Control-Allow-Headers: Content-Type');

$response = [
    'success' => false,
    'message' => '',
    'vehiculo' => null
];

try {
    // Verificar si es POST
    if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
        throw new Exception("Método no permitido", 405);
    }

    // Obtener datos
    $json = file_get_contents('php://input');
    $data = json_decode($json, true);

    // Validar campos
    if (empty($data['email']) || empty($data['password'])) {
        throw new Exception("Email y contraseña son requeridos", 400);
    }

    // Conexión a BD
    $conn = new PDO("mysql:host=localhost;dbname=registro_vehiculos", "root", "");
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // Buscar usuario
    $stmt = $conn->prepare("SELECT * FROM vehiculos WHERE email = :email");
    $stmt->execute([':email' => $data['email']]);
    $usuario = $stmt->fetch(PDO::FETCH_ASSOC);

    if (!$usuario) {
        throw new Exception("Credenciales incorrectas", 401);
    }

    // Verificar contraseña
    if (!password_verify($data['password'], $usuario['password'])) {
        throw new Exception("Credenciales incorrectas", 401);
    }

    // Eliminar datos sensibles antes de enviar
    unset($usuario['password']);
    unset($usuario['codigo_bloqueo']);

    $response = [
        'success' => true,
        'message' => 'Autenticación exitosa',
        'vehiculo' => $usuario
    ];

} catch(PDOException $e) {
    $response['message'] = 'Error en la base de datos: ' . $e->getMessage();
    http_response_code(500);
} catch(Exception $e) {
    $response['message'] = $e->getMessage();
    http_response_code($e->getCode() >= 400 && $e->getCode() < 600 ? $e->getCode() : 400);
}

echo json_encode($response);
?>
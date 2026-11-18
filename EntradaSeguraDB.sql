CREATE TABLE IF NOT EXISTS rol (
    id_rol INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_rol TEXT NOT NULL UNIQUE,
    descripcion TEXT
);


CREATE TABLE IF NOT EXISTS permiso (
    id_permiso INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_permiso TEXT NOT NULL UNIQUE,
    descripcion TEXT
);


CREATE TABLE IF NOT EXISTS rol_permiso (
    id_rol INTEGER NOT NULL,
    id_permiso INTEGER NOT NULL,
    PRIMARY KEY (id_rol, id_permiso),
    FOREIGN KEY (id_rol) REFERENCES rol(id_rol) ON DELETE CASCADE,
    FOREIGN KEY (id_permiso) REFERENCES permiso(id_permiso) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS usuario (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_completo TEXT NOT NULL,
    correo_electronico TEXT NOT NULL UNIQUE,
    contrasena_hash TEXT NOT NULL,
    id_rol INTEGER NOT NULL,
    estado_cuenta TEXT NOT NULL DEFAULT 'ACTIVA' CHECK (estado_cuenta IN ('ACTIVA', 'INACTIVA', 'BLOQUEADA')),
    FOREIGN KEY (id_rol) REFERENCES rol(id_rol)
);


CREATE TABLE IF NOT EXISTS evento (
    id_evento INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_evento TEXT NOT NULL,
    fecha_hora TEXT NOT NULL, -- Guardado como cadena ISO8601 (YYYY-MM-DD HH:MM:SS)
    lugar TEXT NOT NULL,
    estado_evento TEXT NOT NULL DEFAULT 'PROGRAMADO' CHECK (estado_evento IN ('PROGRAMADO', 'EN_CURSO', 'FINALIZADO', 'CANCELADO'))
);


CREATE TABLE IF NOT EXISTS zona (
    id_zona INTEGER PRIMARY KEY AUTOINCREMENT,
    id_evento INTEGER NOT NULL,
    nombre_zona TEXT NOT NULL,
    capacidad_maxima INTEGER NOT NULL,
    precio REAL NOT NULL,
    disponibilidad_actual INTEGER NOT NULL,
    FOREIGN KEY (id_evento) REFERENCES evento(id_evento) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS entrada (
    id_entrada INTEGER PRIMARY KEY AUTOINCREMENT,
    id_evento INTEGER NOT NULL,
    id_zona INTEGER NOT NULL,
    id_cliente INTEGER NOT NULL,
    codigo_validacion TEXT NOT NULL UNIQUE,
    estado_entrada TEXT NOT NULL DEFAULT 'VENDIDA' CHECK (estado_entrada IN ('DISPONIBLE', 'VENDIDA', 'USADA', 'ANULADA')),
    fecha_emision TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_evento) REFERENCES evento(id_evento),
    FOREIGN KEY (id_zona) REFERENCES zona(id_zona),
    FOREIGN KEY (id_cliente) REFERENCES usuario(id_usuario)
);


CREATE TABLE IF NOT EXISTS registro_auditoria (
    id_registro INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    accion_realizada TEXT NOT NULL,
    fecha_hora_accion TIMESTAMP  DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
); ENGINE=InnoDB;


INSERT OR IGNORE INTO rol (id_rol, nombre_rol, descripcion) VALUES
(1, 'ADMINISTRADOR', 'Acceso total'),
(2, 'ORGANIZADOR', 'Gestión de eventos'),
(3, 'CLIENTE', 'Compra de entradas');

INSERT OR IGNORE INTO permiso (id_permiso, nombre_permiso, descripcion) VALUES
(1, 'EVENTO_CREAR', 'Permite registrar nuevos eventos'),
(2, 'EVENTO_EDITAR', 'Permite modificar eventos existentes'),
(3, 'ENTRADA_VALIDAR', 'Permite validar accesos en puerta'),
(4, 'ENTRADA_COMPRAR', 'Permite adquirir entradas para zonas');

INSERT OR IGNORE INTO rol_permiso (id_rol, id_permiso) VALUES
(1, 1), (1, 2), (1, 3), (1, 4),
(2, 1), (2, 2),
(3, 4);

SELECT * FROM rol;
SELECT * FROM usuario;









-- Schema SQL generado desde el modelo físico (MySQL)
-- Charset y motor
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

CREATE DATABASE IF NOT EXISTS `tourpack_db` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `tourpack_db`;

-- Tabla: pais
CREATE TABLE IF NOT EXISTS `pais` (
  `codigopais` VARCHAR(10) NOT NULL,
  `nombre_pais` VARCHAR(30) NOT NULL,
  `continente_pais` VARCHAR(25) DEFAULT NULL,
  PRIMARY KEY (`codigopais`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: ciudad
CREATE TABLE IF NOT EXISTS `ciudad` (
  `codigociudad` VARCHAR(10) NOT NULL,
  `nombre_ciudad` VARCHAR(30) NOT NULL,
  `codigopais` VARCHAR(10) NOT NULL,
  PRIMARY KEY (`codigociudad`),
  KEY `idx_ciudad_pais` (`codigopais`),
  CONSTRAINT `fk_ciudad_pais` FOREIGN KEY (`codigopais`) REFERENCES `pais` (`codigopais`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: tipo_destino
CREATE TABLE IF NOT EXISTS `tipo_destino` (
  `codigotipodestino` VARCHAR(10) NOT NULL,
  `nombre_tipo` VARCHAR(20) NOT NULL,
  `descripcion_tipo` VARCHAR(50) DEFAULT NULL,
  PRIMARY KEY (`codigotipodestino`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: categoria_paquete
CREATE TABLE IF NOT EXISTS `categoria_paquete` (
  `codigocategoria` VARCHAR(10) NOT NULL,
  `nombre_categoria` VARCHAR(20) NOT NULL,
  `descripcion_categoria` VARCHAR(100) DEFAULT NULL,
  PRIMARY KEY (`codigocategoria`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: proveedor
CREATE TABLE IF NOT EXISTS `proveedor` (
  `rucproveedor` VARCHAR(20) NOT NULL,
  `nombre_proveedor` VARCHAR(100) NOT NULL,
  `contacto_proveedor` VARCHAR(100) DEFAULT NULL,
  `codigopais` VARCHAR(10) DEFAULT NULL,
  PRIMARY KEY (`rucproveedor`),
  KEY `idx_proveedor_pais` (`codigopais`),
  CONSTRAINT `fk_proveedor_pais` FOREIGN KEY (`codigopais`) REFERENCES `pais` (`codigopais`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: transporte
CREATE TABLE IF NOT EXISTS `transporte` (
  `codigotransporte` VARCHAR(10) NOT NULL,
  `nombre_transporte` VARCHAR(60) NOT NULL,
  `descripcion` VARCHAR(200) DEFAULT NULL,
  PRIMARY KEY (`codigotransporte`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: paquete (paquete turistico)
CREATE TABLE IF NOT EXISTS `paquete` (
  `numeropaquete` VARCHAR(20) NOT NULL,
  `nombre_paquete` VARCHAR(50) NOT NULL,
  `precio_paquete` DECIMAL(10,2) NOT NULL DEFAULT 0.00,
  `numeros_dias` TINYINT UNSIGNED NOT NULL DEFAULT 1,
  `numero_escalas` TINYINT UNSIGNED DEFAULT 0,
  `descuento_paquete` VARCHAR(200) DEFAULT NULL,
  `codigocategoria` VARCHAR(10) DEFAULT NULL,
  `codigotipodestino` VARCHAR(10) DEFAULT NULL,
  `codigotransporte` VARCHAR(10) DEFAULT NULL,
  `rucproveedor` VARCHAR(20) DEFAULT NULL,
  `cupos_paquete` INT UNSIGNED DEFAULT NULL,
  PRIMARY KEY (`numeropaquete`),
  KEY `idx_paquete_categoria` (`codigocategoria`),
  KEY `idx_paquete_tipo` (`codigotipodestino`),
  KEY `idx_paquete_transporte` (`codigotransporte`),
  KEY `idx_paquete_proveedor` (`rucproveedor`),
  CONSTRAINT `fk_paquete_categoria` FOREIGN KEY (`codigocategoria`) REFERENCES `categoria_paquete` (`codigocategoria`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_paquete_tipo` FOREIGN KEY (`codigotipodestino`) REFERENCES `tipo_destino` (`codigotipodestino`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_paquete_transporte` FOREIGN KEY (`codigotransporte`) REFERENCES `transporte` (`codigotransporte`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_paquete_proveedor` FOREIGN KEY (`rucproveedor`) REFERENCES `proveedor` (`rucproveedor`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: destino_turistico
CREATE TABLE IF NOT EXISTS `destino_turistico` (
  `codigodestinoturistico` VARCHAR(20) NOT NULL,
  `nombre_destino` VARCHAR(50) NOT NULL,
  `descuento_destino` VARCHAR(50) DEFAULT NULL,
  `codigociudad` VARCHAR(10) DEFAULT NULL,
  `codigotipodestino` VARCHAR(10) DEFAULT NULL,
  PRIMARY KEY (`codigodestinoturistico`),
  KEY `idx_destino_ciudad` (`codigociudad`),
  KEY `idx_destino_tipo` (`codigotipodestino`),
  CONSTRAINT `fk_destino_ciudad` FOREIGN KEY (`codigociudad`) REFERENCES `ciudad` (`codigociudad`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_destino_tipo` FOREIGN KEY (`codigotipodestino`) REFERENCES `tipo_destino` (`codigotipodestino`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: paquete_destino (relacion N:N entre paquete y destino)
CREATE TABLE IF NOT EXISTS `paquete_destino` (
  `numeropaquete` VARCHAR(20) NOT NULL,
  `codigodestino` VARCHAR(20) NOT NULL,
  `orden` VARCHAR(30) DEFAULT NULL,
  `numero_dias` VARCHAR(30) DEFAULT NULL,
  PRIMARY KEY (`numeropaquete`,`codigodestino`),
  KEY `idx_paquete_destino_destino` (`codigodestino`),
  CONSTRAINT `fk_pd_paquete` FOREIGN KEY (`numeropaquete`) REFERENCES `paquete` (`numeropaquete`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_pd_destino` FOREIGN KEY (`codigodestino`) REFERENCES `destino_turistico` (`codigodestinoturistico`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: escala
CREATE TABLE IF NOT EXISTS `escala` (
  `codigoescala` VARCHAR(20) NOT NULL,
  `nombre_escala` VARCHAR(50) NOT NULL,
  `codigociudad` VARCHAR(10) DEFAULT NULL,
  PRIMARY KEY (`codigoescala`),
  KEY `idx_escala_ciudad` (`codigociudad`),
  CONSTRAINT `fk_escala_ciudad` FOREIGN KEY (`codigociudad`) REFERENCES `ciudad` (`codigociudad`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: paquete_escala (relacion N:N entre paquete y escala)
CREATE TABLE IF NOT EXISTS `paquete_escala` (
  `numeropaquete` VARCHAR(20) NOT NULL,
  `codigoescala` VARCHAR(20) NOT NULL,
  `orden` VARCHAR(60) DEFAULT NULL,
  `hora_salida` TIME DEFAULT NULL,
  `hora_llegada` TIME DEFAULT NULL,
  PRIMARY KEY (`numeropaquete`,`codigoescala`),
  CONSTRAINT `fk_pe_paquete` FOREIGN KEY (`numeropaquete`) REFERENCES `paquete` (`numeropaquete`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_pe_escala` FOREIGN KEY (`codigoescala`) REFERENCES `escala` (`codigoescala`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: cliente
CREATE TABLE IF NOT EXISTS `cliente` (
  `cedulacliente` VARCHAR(20) NOT NULL,
  `nombre_cliente` VARCHAR(50) NOT NULL,
  `apellido_cliente` VARCHAR(30) DEFAULT NULL,
  `direccion` VARCHAR(50) DEFAULT NULL,
  `correo_cliente` VARCHAR(50) DEFAULT NULL,
  `telefono` VARCHAR(15) DEFAULT NULL,
  PRIMARY KEY (`cedulacliente`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: forma_pago
CREATE TABLE IF NOT EXISTS `forma_pago` (
  `codigoformapago` VARCHAR(20) NOT NULL,
  `nombre_forma` VARCHAR(20) NOT NULL,
  `nombre_banco` VARCHAR(40) DEFAULT NULL,
  PRIMARY KEY (`codigoformapago`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: factura
CREATE TABLE IF NOT EXISTS `factura` (
  `numerofactura` INT NOT NULL AUTO_INCREMENT,
  `subtotal_factura` DECIMAL(12,2) DEFAULT 0.00,
  `iva_factura` DECIMAL(12,2) DEFAULT 0.00,
  `total_factura` DECIMAL(12,2) DEFAULT 0.00,
  `fecha_factura` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `codigoformapago` VARCHAR(20) DEFAULT NULL,
  `cedulacliente` VARCHAR(20) DEFAULT NULL,
  PRIMARY KEY (`numerofactura`),
  KEY `idx_factura_cliente` (`cedulacliente`),
  KEY `idx_factura_forma` (`codigoformapago`),
  CONSTRAINT `fk_factura_cliente` FOREIGN KEY (`cedulacliente`) REFERENCES `cliente` (`cedulacliente`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_factura_forma` FOREIGN KEY (`codigoformapago`) REFERENCES `forma_pago` (`codigoformapago`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: factura_paquete (relacion entre factura y paquete)
CREATE TABLE IF NOT EXISTS `factura_paquete` (
  `numerofactura` INT NOT NULL,
  `numeropaquete` VARCHAR(20) NOT NULL,
  `valor_paquete` DECIMAL(12,2) DEFAULT 0.00,
  `numeros_dias` TINYINT UNSIGNED DEFAULT 1,
  PRIMARY KEY (`numerofactura`,`numeropaquete`),
  CONSTRAINT `fk_fp_factura` FOREIGN KEY (`numerofactura`) REFERENCES `factura` (`numerofactura`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_fp_paquete` FOREIGN KEY (`numeropaquete`) REFERENCES `paquete` (`numeropaquete`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: agente_venta
CREATE TABLE IF NOT EXISTS `agente_venta` (
  `cedulaagente` VARCHAR(20) NOT NULL,
  `nombre_agente` VARCHAR(50) NOT NULL,
  `apellido_agente` VARCHAR(50) DEFAULT NULL,
  `cargo_agente` VARCHAR(50) DEFAULT NULL,
  `comision_agente` DECIMAL(6,2) DEFAULT 0.00,
  PRIMARY KEY (`cedulaagente`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: reserva
CREATE TABLE IF NOT EXISTS `reserva` (
  `numeroreserva` INT NOT NULL AUTO_INCREMENT,
  `fecha_reserva` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `hora_reserva` TIME DEFAULT NULL,
  `fecha_salida` DATE DEFAULT NULL,
  `total_reserva` DECIMAL(12,2) DEFAULT 0.00,
  `iva_reserva` DECIMAL(12,2) DEFAULT 0.00,
  `escalas_reserva` TINYINT UNSIGNED DEFAULT 0,
  `numeropaquete` VARCHAR(20) DEFAULT NULL,
  `cedulacliente` VARCHAR(20) DEFAULT NULL,
  `codigoformapago` VARCHAR(20) DEFAULT NULL,
  PRIMARY KEY (`numeroreserva`),
  KEY `idx_reserva_paquete` (`numeropaquete`),
  KEY `idx_reserva_cliente` (`cedulacliente`),
  CONSTRAINT `fk_reserva_paquete` FOREIGN KEY (`numeropaquete`) REFERENCES `paquete` (`numeropaquete`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_reserva_cliente` FOREIGN KEY (`cedulacliente`) REFERENCES `cliente` (`cedulacliente`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_reserva_forma` FOREIGN KEY (`codigoformapago`) REFERENCES `forma_pago` (`codigoformapago`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SET FOREIGN_KEY_CHECKS = 1;

-- Fin del schema

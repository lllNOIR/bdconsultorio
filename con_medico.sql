-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 27-07-2025 a las 20:59:33
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `con_medico`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `consultorios`
--

CREATE TABLE `consultorios` (
  `CONnumero` int(11) NOT NULL,
  `CONnombre` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `consultorios`
--

INSERT INTO `consultorios` (`CONnumero`, `CONnombre`) VALUES
(1, 'odontologia'),
(2, 'GENERAL');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `medicos`
--

CREATE TABLE `medicos` (
  `MEDidentificacion` int(11) NOT NULL,
  `MEDnombres` varchar(100) NOT NULL,
  `MEDapellidos` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `medicos`
--

INSERT INTO `medicos` (`MEDidentificacion`, `MEDnombres`, `MEDapellidos`) VALUES
(222, 'andres', 'manjares'),
(333, 'FELIPE', 'MASA');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pacientes`
--

CREATE TABLE `pacientes` (
  `PACidentificacion` int(11) NOT NULL,
  `PACnombres` varchar(100) NOT NULL,
  `PACapellidos` varchar(100) NOT NULL,
  `PACfechaNacimiento` date NOT NULL,
  `PACSexo` char(1) NOT NULL,
  `CONnumero` int(11) DEFAULT NULL,
  `MEDidentificacion` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pacientes`
--

INSERT INTO `pacientes` (`PACidentificacion`, `PACnombres`, `PACapellidos`, `PACfechaNacimiento`, `PACSexo`, `CONnumero`, `MEDidentificacion`) VALUES
(2024, 'carlos', 'amaris', '2025-07-08', 'm', NULL, NULL);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `consultorios`
--
ALTER TABLE `consultorios`
  ADD PRIMARY KEY (`CONnumero`);

--
-- Indices de la tabla `medicos`
--
ALTER TABLE `medicos`
  ADD PRIMARY KEY (`MEDidentificacion`);

--
-- Indices de la tabla `pacientes`
--
ALTER TABLE `pacientes`
  ADD PRIMARY KEY (`PACidentificacion`),
  ADD KEY `CONnumero` (`CONnumero`),
  ADD KEY `MEDidentificacion` (`MEDidentificacion`);

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `pacientes`
--
ALTER TABLE `pacientes`
  ADD CONSTRAINT `pacientes_ibfk_1` FOREIGN KEY (`CONnumero`) REFERENCES `consultorios` (`CONnumero`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `pacientes_ibfk_2` FOREIGN KEY (`MEDidentificacion`) REFERENCES `medicos` (`MEDidentificacion`) ON DELETE SET NULL ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

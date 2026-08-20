-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 19-08-2026 a las 23:38:25
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `asistencia`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `descansos`
--

CREATE TABLE `descansos` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `jornada_id` bigint(20) UNSIGNED NOT NULL,
  `tipo` enum('break_manana','lunch','break_tarde') NOT NULL,
  `inicio` time NOT NULL,
  `fin` time DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `descansos`
--

INSERT INTO `descansos` (`id`, `jornada_id`, `tipo`, `inicio`, `fin`, `created_at`, `updated_at`) VALUES
(1, 7, 'break_manana', '11:44:49', '11:46:13', '2026-08-18 21:44:49', '2026-08-18 21:46:13'),
(2, 7, 'lunch', '11:46:48', '11:46:59', '2026-08-18 21:46:48', '2026-08-18 21:46:59'),
(3, 7, 'break_tarde', '11:47:26', '11:47:33', '2026-08-18 21:47:26', '2026-08-18 21:47:33'),
(4, 8, 'break_manana', '11:59:15', '11:59:28', '2026-08-18 21:59:15', '2026-08-18 21:59:28'),
(5, 8, 'lunch', '12:01:57', '12:02:13', '2026-08-18 22:01:57', '2026-08-18 22:02:13'),
(6, 8, 'break_tarde', '12:02:30', '12:02:40', '2026-08-18 22:02:30', '2026-08-18 22:02:40'),
(7, 9, 'break_tarde', '12:03:58', '12:18:59', '2026-08-18 22:03:58', '2026-08-18 22:18:59'),
(8, 9, 'break_manana', '12:20:43', '12:35:44', '2026-08-18 22:20:43', '2026-08-18 22:35:44'),
(9, 9, 'lunch', '12:59:49', '14:19:51', '2026-08-18 22:59:49', '2026-08-19 00:19:51'),
(10, 10, 'break_manana', '15:19:02', '15:34:03', '2026-08-19 01:19:02', '2026-08-19 01:34:03'),
(11, 11, 'lunch', '16:24:34', '09:25:37', '2026-08-19 02:24:34', '2026-08-19 19:25:37'),
(12, 12, 'break_manana', '11:57:26', '12:15:49', '2026-08-19 21:57:26', '2026-08-19 22:15:49'),
(13, 12, 'break_tarde', '12:16:23', '12:31:25', '2026-08-19 22:16:23', '2026-08-19 22:31:25'),
(14, 12, 'lunch', '13:00:08', '14:02:56', '2026-08-19 23:00:08', '2026-08-20 00:02:56'),
(15, 10, 'break_tarde', '14:10:04', '14:27:52', '2026-08-20 00:10:04', '2026-08-20 00:27:52');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `jornadas`
--

CREATE TABLE `jornadas` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `usuario_id` int(10) UNSIGNED NOT NULL,
  `fecha` date NOT NULL,
  `entrada` time NOT NULL,
  `salida` time DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `jornadas`
--

INSERT INTO `jornadas` (`id`, `usuario_id`, `fecha`, `entrada`, `salida`, `created_at`, `updated_at`) VALUES
(2, 1, '2026-08-18', '11:27:49', NULL, '2026-08-18 21:27:49', '2026-08-18 21:27:49'),
(7, 2, '2026-08-18', '11:44:32', '11:59:01', '2026-08-18 21:44:32', '2026-08-18 21:59:01'),
(8, 2, '2026-08-18', '11:59:10', '12:03:53', '2026-08-18 21:59:10', '2026-08-18 22:03:53'),
(9, 2, '2026-08-18', '12:03:57', '16:24:03', '2026-08-18 22:03:57', '2026-08-19 02:24:03'),
(10, 3, '2026-08-18', '15:18:44', '15:02:41', '2026-08-19 01:18:44', '2026-08-20 01:02:41'),
(11, 2, '2026-08-18', '16:24:24', '09:25:53', '2026-08-19 02:24:24', '2026-08-19 19:25:53'),
(12, 2, '2026-08-19', '11:56:26', '14:09:25', '2026-08-19 21:56:26', '2026-08-20 00:09:25'),
(13, 3, '2026-08-19', '15:20:10', '15:20:18', '2026-08-20 01:20:10', '2026-08-20 01:20:18'),
(14, 3, '2026-08-19', '15:44:40', NULL, '2026-08-20 01:44:40', '2026-08-20 01:44:40');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(10) UNSIGNED NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `correo` varchar(50) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `rol` enum('empleado','admin') NOT NULL DEFAULT 'empleado',
  `activo` tinyint(1) NOT NULL DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre`, `correo`, `password_hash`, `rol`, `activo`, `created_at`, `updated_at`) VALUES
(1, 'Administrador', 'admin@techcrg.com', '$2b$12$c8rItTQuWNWFzs9U/lJf0.u9ePyhlbXksdB3UIm7cxzVetrv0.nce', 'admin', 1, '2026-08-18 14:45:39', '2026-08-18 16:17:23'),
(2, 'Diomedes Diaz', 'diome@techcrg.com', '$2b$12$w.VLl2rKVXvM.JbGBdYI2u31J5g8I9vpnOKlfTvzFKPiELXGC0a9S', 'empleado', 1, '2026-08-18 16:33:41', '2026-08-19 21:56:04'),
(3, 'Janer Cervantes', 'janer117@techcrg.com', '$2b$12$yMe/6JK.NAx6x2OEYoimHelsl4zZfOo.D0fxakMMTH5iNWSSNaMZC', 'empleado', 0, '2026-08-19 00:22:43', '2026-08-20 02:04:49'),
(4, 'luiz Diaz', 'diaz@techcrg.com', '$2b$12$IoB2RQaGg1u16ZLpVIAf2uTdI3mhIEjteb5zU3O1egl/fak1Im866', 'empleado', 0, '2026-08-19 19:47:23', '2026-08-19 20:15:57');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `descansos`
--
ALTER TABLE `descansos`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uk_descanso_jornada_tipo` (`jornada_id`,`tipo`),
  ADD KEY `idx_descansos_jornada` (`jornada_id`),
  ADD KEY `idx_descansos_tipo` (`tipo`);

--
-- Indices de la tabla `jornadas`
--
ALTER TABLE `jornadas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_jornadas_usuario_fecha` (`usuario_id`,`fecha`),
  ADD KEY `idx_jornadas_fecha` (`fecha`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `usuario` (`correo`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `descansos`
--
ALTER TABLE `descansos`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de la tabla `jornadas`
--
ALTER TABLE `jornadas`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `descansos`
--
ALTER TABLE `descansos`
  ADD CONSTRAINT `fk_descansos_jornada` FOREIGN KEY (`jornada_id`) REFERENCES `jornadas` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `jornadas`
--
ALTER TABLE `jornadas`
  ADD CONSTRAINT `fk_jornadas_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

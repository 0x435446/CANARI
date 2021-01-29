-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 09, 2020 at 10:17 PM
-- Server version: 10.4.13-MariaDB
-- PHP Version: 7.2.32

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `blockit`
--

-- --------------------------------------------------------

--
-- Table structure for table `connections`
--

CREATE TABLE `connections` (
  `ID` int(11) NOT NULL,
  `ID_event` int(11) NOT NULL,
  `Alert_Type` varchar(256) NOT NULL,
  `Name` varchar(256) NOT NULL DEFAULT 'Connection',
  `IP` varchar(256) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `dns`
--

CREATE TABLE `dns` (
  `ID` int(11) NOT NULL,
  `ID_event` int(11) NOT NULL,
  `Name` varchar(256) NOT NULL DEFAULT 'DNS',
  `Alert_Type` varchar(2048) NOT NULL,
  `Domain` varchar(2048) NOT NULL,
  `Subdomain` varchar(2048) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `dns`
--

INSERT INTO `dns` (`ID`, `ID_event`, `Name`, `Alert_Type`, `Domain`, `Subdomain`) VALUES
(1, 1, 'DNS', 'ALERT! UNKNOWN BASE FOUND!!!', 'google.ro', 'YmxhYmxhYmxh');

-- --------------------------------------------------------

--
-- Table structure for table `events`
--

CREATE TABLE `events` (
  `ID` int(11) NOT NULL,
  `Protocol` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `events`
--

INSERT INTO `events` (`ID`, `Protocol`) VALUES
(1, 'DNS');

-- --------------------------------------------------------

--
-- Table structure for table `ftp`
--

CREATE TABLE `ftp` (
  `ID` int(11) NOT NULL,
  `ID_event` int(11) NOT NULL,
  `Alert_Type` varchar(256) NOT NULL,
  `Name` varchar(256) NOT NULL DEFAULT 'FTP',
  `IP` varchar(256) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `http`
--

CREATE TABLE `http` (
  `ID` int(11) NOT NULL,
  `ID_event` int(11) NOT NULL,
  `Name` varchar(256) NOT NULL DEFAULT 'HTTP',
  `Alert_Type` varchar(256) NOT NULL,
  `Domain` varchar(256) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `https`
--

CREATE TABLE `https` (
  `ID` int(11) NOT NULL,
  `ID_event` int(11) NOT NULL,
  `Name` varchar(256) NOT NULL DEFAULT 'HTTPS',
  `Alert_Type` varchar(256) NOT NULL,
  `Domain` varchar(256) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `icmp`
--

CREATE TABLE `icmp` (
  `ID` int(11) NOT NULL,
  `ID_event` int(11) NOT NULL,
  `Name` varchar(256) NOT NULL DEFAULT 'ICMP',
  `IP` varchar(256) NOT NULL,
  `Alert_Type` varchar(256) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `ip_header`
--

CREATE TABLE `ip_header` (
  `ID` int(11) NOT NULL,
  `ID_event` int(11) NOT NULL,
  `Name` varchar(256) NOT NULL DEFAULT 'IPv4',
  `Alert_Type` varchar(256) NOT NULL,
  `IP` varchar(256) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `listeners`
--

CREATE TABLE `listeners` (
  `ID` int(11) NOT NULL,
  `ID_event` int(11) NOT NULL,
  `Alert_Type` varchar(256) NOT NULL,
  `Name` varchar(256) NOT NULL DEFAULT 'Listener',
  `IP` varchar(256) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `connections`
--
ALTER TABLE `connections`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `Foreign Key` (`ID_event`) USING BTREE;

--
-- Indexes for table `dns`
--
ALTER TABLE `dns`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `Foreign Key` (`ID_event`);

--
-- Indexes for table `events`
--
ALTER TABLE `events`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `ftp`
--
ALTER TABLE `ftp`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `ID_event` (`ID_event`);

--
-- Indexes for table `http`
--
ALTER TABLE `http`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `Foreign Key` (`ID_event`);

--
-- Indexes for table `https`
--
ALTER TABLE `https`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `Foreign Key` (`ID_event`);

--
-- Indexes for table `icmp`
--
ALTER TABLE `icmp`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `Foreign Key` (`ID_event`);

--
-- Indexes for table `ip_header`
--
ALTER TABLE `ip_header`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `Foreign Key` (`ID_event`);

--
-- Indexes for table `listeners`
--
ALTER TABLE `listeners`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `Foreign Key` (`ID_event`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `connections`
--
ALTER TABLE `connections`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `dns`
--
ALTER TABLE `dns`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `events`
--
ALTER TABLE `events`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `ftp`
--
ALTER TABLE `ftp`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `http`
--
ALTER TABLE `http`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `https`
--
ALTER TABLE `https`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `icmp`
--
ALTER TABLE `icmp`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `ip_header`
--
ALTER TABLE `ip_header`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `listeners`
--
ALTER TABLE `listeners`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `dns`
--
ALTER TABLE `dns`
  ADD CONSTRAINT `Foreign Key` FOREIGN KEY (`ID_event`) REFERENCES `events` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `ftp`
--
ALTER TABLE `ftp`
  ADD CONSTRAINT `ftp_ibfk_1` FOREIGN KEY (`ID_event`) REFERENCES `events` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

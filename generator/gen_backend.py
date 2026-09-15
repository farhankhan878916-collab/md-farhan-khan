import os

BASE_DIR = "movie-ticket-booking-system"
BACKEND_DIR = os.path.join(BASE_DIR, "backend")
SRC_JAVA = os.path.join(BACKEND_DIR, "src", "main", "java", "com", "example", "movieticketbooking")
SRC_RESOURCES = os.path.join(BACKEND_DIR, "src", "main", "resources")
SRC_TEST = os.path.join(BACKEND_DIR, "src", "test", "java", "com", "example", "movieticketbooking")

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Generated: {path}")

def generate_backend():
    print("Generating backend files...")
    # pom.xml
    write_file(os.path.join(BACKEND_DIR, "pom.xml"), """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.2.3</version>
        <relativePath/>
    </parent>
    <groupId>com.example</groupId>
    <artifactId>movie-ticket-booking</artifactId>
    <version>1.0.0</version>
    <name>movie-ticket-booking</name>
    <description>Movie Ticket Booking System - Production Backend</description>
    <properties>
        <java.version>17</java.version>
        <jjwt.version>0.11.5</jjwt.version>
    </properties>
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-security</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-validation</artifactId>
        </dependency>
        <dependency>
            <groupId>com.mysql</groupId>
            <artifactId>mysql-connector-j</artifactId>
            <scope>runtime</scope>
        </dependency>
        <dependency>
            <groupId>com.h2database</groupId>
            <artifactId>h2</artifactId>
            <scope>runtime</scope>
        </dependency>
        <dependency>
            <groupId>io.jsonwebtoken</groupId>
            <artifactId>jjwt-api</artifactId>
            <version>${jjwt.version}</version>
        </dependency>
        <dependency>
            <groupId>io.jsonwebtoken</groupId>
            <artifactId>jjwt-impl</artifactId>
            <version>${jjwt.version}</version>
            <scope>runtime</scope>
        </dependency>
        <dependency>
            <groupId>io.jsonwebtoken</groupId>
            <artifactId>jjwt-jackson</artifactId>
            <version>${jjwt.version}</version>
            <scope>runtime</scope>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>org.springframework.security</groupId>
            <artifactId>spring-security-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>""")

    # application.properties
    write_file(os.path.join(SRC_RESOURCES, "application.properties"), """# ===================================================================
# Movie Ticket Booking System - Application Configuration
# ===================================================================
server.port=8080

# Active profile: set to 'mysql' for production MySQL, or 'h2' for quick local in-memory testing
spring.profiles.active=mysql

# MySQL Database Configuration
# REPLACE 'YOUR_DB_USERNAME' and 'YOUR_DB_PASSWORD' below with your actual MySQL credentials:
spring.datasource.url=jdbc:mysql://localhost:3306/movie_booking?useSSL=false&serverTimezone=UTC&allowPublicKeyRetrieval=true
spring.datasource.username=YOUR_DB_USERNAME
spring.datasource.password=YOUR_DB_PASSWORD
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver

# JPA / Hibernate Configuration
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=false
spring.jpa.properties.hibernate.format_sql=true
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.MySQLDialect

# JWT Configuration
app.jwt.secret=9a3f2c4e6b8a1d5e7f0c2b4a6d8e1f3a5c7e9b1d3f5a7c9e1b3d5f7a9c1e3b5a
app.jwt.expiration-ms=86400000

# CORS Configuration
app.cors.allowed-origins=http://localhost:4200,http://127.0.0.1:4200,http://localhost:3000
""")

    # application-h2.properties
    write_file(os.path.join(SRC_RESOURCES, "application-h2.properties"), """# H2 In-Memory Database Configuration for instant development / testing
spring.datasource.url=jdbc:h2:mem:movie_booking;DB_CLOSE_DELAY=-1;DB_CLOSE_ON_EXIT=FALSE
spring.datasource.driverClassName=org.h2.Driver
spring.datasource.username=sa
spring.datasource.password=
spring.jpa.database-platform=org.hibernate.dialect.H2Dialect
spring.jpa.hibernate.ddl-auto=create-drop
spring.h2.console.enabled=true
spring.h2.console.path=/h2-console
""")

    # mvnw and mvnw.cmd scripts
    write_file(os.path.join(BACKEND_DIR, "mvnw"), """#!/bin/sh
exec mvn "$@"
""")
    os.chmod(os.path.join(BACKEND_DIR, "mvnw"), 0o755)

    write_file(os.path.join(BACKEND_DIR, "mvnw.cmd"), """@REM Maven Wrapper Script
@echo off
mvn %*
""")

if __name__ == "__main__":
    generate_backend()

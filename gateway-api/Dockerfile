FROM maven:3.9.6-eclipse-temurin-21-alpine AS builder

WORKDIR /app

COPY .mvn/ .mvn
COPY mvnw pom.xml ./
RUN chmod +x ./mvnw
RUN ./mvnw dependency:go-offline

COPY src ./src

RUN ./mvnw package -DskipTests

FROM eclipse-temurin:21-jre-alpine

WORKDIR /app

COPY --from=builder /app/target/gateway-api-0.0.1-SNAPSHOT.jar ./gateway-api.jar

EXPOSE 8081

ENTRYPOINT ["java","-jar","gateway-api.jar"]
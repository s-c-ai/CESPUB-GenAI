FROM eclipse-temurin:21-jdk-alpine

WORKDIR /app
COPY mvnw pom.xml ./
COPY .mvn .mvn

RUN chmod +x mvnw
RUN ./mvnw dependency:go-offline -B

COPY src ./src
RUN ./mvnw package -DskipTests -B

EXPOSE 8081

CMD ["java", "-jar", "target/gateway-api-0.0.1-SNAPSHOT.jar"]
package scientifcloud.gateway_api;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.reactive.EnableWebFluxSecurity;
import org.springframework.security.config.web.server.ServerHttpSecurity;
import org.springframework.security.web.server.SecurityWebFilterChain;

import java.io.IOException;

@Configuration
@EnableWebFluxSecurity
public class SecurityConfig {

    @Bean
    public SecurityWebFilterChain securityWebFilterChain(ServerHttpSecurity http) throws IOException {
        return http
            .csrf(csrf -> csrf.disable())
            .httpBasic(httpBasic -> httpBasic.disable())
            .formLogin(formLogin -> formLogin.disable())
            .authorizeExchange(exchange -> exchange
                .anyExchange().permitAll() 
            )
            // .addFilterBefore(googleJwtWebFilter(), SecurityWebFiltersOrder.AUTHENTICATION)
            .build();
    }

    //Bean
    @Bean
    public GoogleJwtWebFilter googleJwtWebFilter() throws IOException {
        return new GoogleJwtWebFilter();
    }
}
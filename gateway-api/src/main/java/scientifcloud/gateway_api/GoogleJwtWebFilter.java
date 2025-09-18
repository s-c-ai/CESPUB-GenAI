package scientifcloud.gateway_api;

import com.nimbusds.jose.JOSEException;
import com.nimbusds.jose.jwk.JWKSet;
import com.nimbusds.jose.jwk.source.ImmutableJWKSet;
import com.nimbusds.jose.jwk.source.JWKSource;
import com.nimbusds.jose.proc.*;
import com.nimbusds.jwt.JWTClaimsSet;
import com.nimbusds.jwt.SignedJWT;
import com.nimbusds.jwt.proc.ConfigurableJWTProcessor;
import com.nimbusds.jwt.proc.DefaultJWTProcessor;
import org.springframework.http.HttpCookie;
import org.springframework.http.HttpStatus;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.ReactiveSecurityContextHolder;
import org.springframework.web.server.ServerWebExchange;
import org.springframework.web.server.WebFilter;
import org.springframework.web.server.WebFilterChain;
import reactor.core.publisher.Mono;

import java.io.IOException;
import java.net.URL;
import java.text.ParseException;
import java.util.Collections;

public class GoogleJwtWebFilter implements WebFilter {

    private static final String GOOGLE_JWKS_URL = "https://www.googleapis.com/oauth2/v3/certs";
    private final JWKSource<SecurityContext> keySource;

    public GoogleJwtWebFilter() throws IOException {
        try {
            JWKSet jwkSet = JWKSet.load(new URL(GOOGLE_JWKS_URL));
            this.keySource = new ImmutableJWKSet<>(jwkSet);
        } catch (ParseException e) {
            throw new IOException("Erro ao carregar chaves JWT do Google", e);
        }
    }

    @Override
    public Mono<Void> filter(ServerWebExchange exchange, WebFilterChain chain) {
        String token = extractTokenFromCookie(exchange);

        if (token != null) {
            try {
                SignedJWT jwt = SignedJWT.parse(token);

                ConfigurableJWTProcessor<SecurityContext> jwtProcessor =
                        new DefaultJWTProcessor<>();

                JWSKeySelector<SecurityContext> keySelector =
                        new JWSVerificationKeySelector<>(jwt.getHeader().getAlgorithm(), keySource);

                jwtProcessor.setJWSKeySelector(keySelector);

                JWTClaimsSet claims = jwtProcessor.process(jwt, null);

                // Validar issuer do Google
                if (!"accounts.google.com".equals(claims.getIssuer())
                        && !"https://accounts.google.com".equals(claims.getIssuer())) {
                    throw new SecurityException("Token não veio do Google");
                }

                String username = claims.getSubject();

                Authentication authentication = new UsernamePasswordAuthenticationToken(
                        username, null, Collections.emptyList());

                return chain.filter(exchange)
                        .contextWrite(ReactiveSecurityContextHolder.withAuthentication(authentication));

            } catch (ParseException | JOSEException | BadJOSEException e) {
                // Token inválido - retornar 401
                exchange.getResponse().setStatusCode(HttpStatus.UNAUTHORIZED);
                return exchange.getResponse().setComplete();
            }
        }

        return chain.filter(exchange);
    }

    private String extractTokenFromCookie(ServerWebExchange exchange) {
        HttpCookie cookie = exchange.getRequest().getCookies().getFirst("google_auth_token");
        return cookie != null ? cookie.getValue() : null;
    }
}
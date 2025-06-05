// src/routes/oauth/+server.ts
import { redirect, type RequestHandler } from "@sveltejs/kit";
import { OAuth2Client } from "google-auth-library";
import {
  CLIENT_ID,
  CLIENT_SECRET,
  REDIRECT_WRENAI,
  REDIRECT_OAUTH,
} from "$env/static/private";

export const GET: RequestHandler = async ({ url, cookies }) => {
  const code = url.searchParams.get("code");

  if (!code) {
    return new Response("Missing authorization code", { status: 400 });
  }

  const oAuth2Client = new OAuth2Client(
    CLIENT_ID,
    CLIENT_SECRET,
    REDIRECT_OAUTH
  );

  try {
    // Troca o código pelo token
    const { tokens } = await oAuth2Client.getToken(code);
    oAuth2Client.setCredentials(tokens);

    // Aqui você mantém o acesso a `credentials` como pediu
    const credentials = oAuth2Client.credentials;

    // Se quiser guardar algo do credentials como cookie (ex: id_token)
    if (credentials.id_token) {
      cookies.set("id_token", credentials.id_token, {
        path: "/",
        httpOnly: true,
        secure: true,
        sameSite: "lax",
        maxAge: 60 * 60 * 24
      });
    }

    // Exemplo opcional: obter dados do usuário via access_token
    // (caso queira ir além do credentials depois)
    /*
    if (credentials.access_token) {
      const userInfoRes = await fetch("https://www.googleapis.com/oauth2/v2/userinfo", {
        headers: {
          Authorization: `Bearer ${credentials.access_token}`
        }
      });

      const userData = await userInfoRes.json();
      console.log("Usuário logado:", userData);
    }
    */

    // Redireciona após login
    throw redirect(303, REDIRECT_WRENAI);
  } catch (err) {
    console.error("Erro na autenticação OAuth:", err);
    return new Response(`Erro durante o login: ${err}`, { status: 500 });
  }
};


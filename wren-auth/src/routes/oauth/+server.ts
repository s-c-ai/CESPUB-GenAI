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
  const token = cookies.get("google_auth_token");

  if (!code && !token) {
    throw redirect(303, "/");
  }

  const oAuth2Client = new OAuth2Client(
    CLIENT_ID,
    CLIENT_SECRET,
    REDIRECT_OAUTH,
  );

  if (code) {
    try {
      const response = await oAuth2Client.getToken(code);
      const accessToken = response.tokens.access_token;
      if (!accessToken) {
        throw new Error("Access token not found");
      }

      cookies.set("google_auth_token", accessToken, {
        path:"/",
        httpOnly: true,
        maxAge: 60 * 60 * 24 * 7,
        sameSite: "strict"
      });

      oAuth2Client.setCredentials(response.tokens);
    } catch (err) {
      console.error("Failed to retrieve access token", err);
      return new Response(`Something went wrong: ${err}`, { status: 500 });
    }
  }

  throw redirect(303, REDIRECT_WRENAI);
};

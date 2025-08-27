import { redirect, type Actions } from "@sveltejs/kit";
import { CLIENT_ID, CLIENT_SECRET, REDIRECT_OAUTH } from "$env/static/private";
import { OAuth2Client } from "google-auth-library";

export const actions: Actions = {
  default: async ({}) => {
    const oAuth2Client = new OAuth2Client(
      CLIENT_ID,
      CLIENT_SECRET,
      REDIRECT_OAUTH,
    );

    const authorizeURL = oAuth2Client.generateAuthUrl({
      access_type: "online",
      scope: "https://www.googleapis.com/auth/userinfo.profile openid",
      prompt: "consent",
    });

    throw redirect(303, authorizeURL);
  },
};

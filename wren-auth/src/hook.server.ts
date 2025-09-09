import { redirect, type Handle } from "@sveltejs/kit";
import { sequence } from "@sveltejs/kit/hooks";
import { REDIRECT_WRENAI } from "$env/static/private";

const auth: Handle = async ({ event, resolve }) => {
  const token = event.cookies.get("google_auth_token");
  event.locals.google_auth_token = token || null;
  return resolve(event);
};

const authGuard: Handle = async ({ event, resolve }) => {
  const token = event.locals.google_auth_token;
  const pathname = event.url.pathname;
  const hasCode = event.url.searchParams.has("code");

  if (pathname === "/oauth" && hasCode) {
    return resolve(event);
  }

  if (!token && pathname === "/oauth") {
    throw redirect(303, "/");
  }

  if (token && pathname === "/oauth") {
    throw redirect(303, REDIRECT_WRENAI);
  }

  if (token && pathname === "/") {
    throw redirect(303, REDIRECT_WRENAI);
  }

  if (pathname === "/logout") {
    event.cookies.delete("google_auth_token", { path: "/" });
    throw redirect(303, "/");
  }

  return resolve(event);
};

export const handle: Handle = sequence(auth, authGuard);

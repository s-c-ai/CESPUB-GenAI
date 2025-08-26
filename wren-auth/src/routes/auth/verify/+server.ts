import { json, type RequestHandler } from '@sveltejs/kit';
//resposta para o nginx
export const GET: RequestHandler = async ({ request }) => {
    const cookieHeader = request.headers.get('cookie');
    console.log('Cookie header in verify: ', cookieHeader);
    const token = cookieHeader?.split('; ').find(c => c.startsWith('google_auth_token='))?.split('=')[1];

    if (!token) {
        return json({ status: 'unauthorized' }, { status: 401 });
    }

    return json({ status: 'ok' }, { status: 200 });
};
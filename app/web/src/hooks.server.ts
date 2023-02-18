import type { HandleFetch } from '@sveltejs/kit';
import { PUBLIC_API_PATH } from '$env/static/public';

export const handleFetch = (({ request, fetch }) => {
	const url = new URL(request.url);
	const path = `${url.pathname}${url.search}`;

	if (path.startsWith(PUBLIC_API_PATH)) {
		const api_path = path.slice(PUBLIC_API_PATH.length);
		request = new Request(`http://api${api_path}`, request);
	}

	return fetch(request);
}) satisfies HandleFetch;

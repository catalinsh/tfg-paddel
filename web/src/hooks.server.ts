import type { HandleFetch } from '@sveltejs/kit';

export const handleFetch = (({ request, fetch }) => {
	const url = new URL(request.url);
	const path = `${url.pathname}${url.search}`;

	if (path.startsWith('/api')) {
		const api_path = path.replace('/api/', '');

		request = new Request(`http://api/${api_path}`, request);
	}

	return fetch(request);
}) satisfies HandleFetch;

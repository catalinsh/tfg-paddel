import { get_current_user } from '$lib/api';
import type { LayoutLoad } from './$types';

export const load = (async () => {
	const token = localStorage.getItem('token') || '';

	const currentUser = get_current_user(token);

	return { currentUser };
}) satisfies LayoutLoad;

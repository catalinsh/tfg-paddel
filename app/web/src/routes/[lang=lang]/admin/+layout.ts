import { get_current_user } from '$lib/api';
import type { LayoutLoad } from './$types';

export const load = (async () => {
	const token = localStorage.getItem('token');

	if (!token) {
		return { currentUser: null };
	}

	const currentUser = await get_current_user();

	if (!currentUser) {
		return { currentUser: null };
	}

	return { currentUser };
}) satisfies LayoutLoad;

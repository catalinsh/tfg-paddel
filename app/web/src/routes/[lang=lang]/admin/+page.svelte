<script lang="ts">
	import { locale } from '$i18n/i18n-svelte';
	import { goto } from '$app/navigation';
	import { read_users } from '$lib/api';

	const token = localStorage.getItem('token');

	if (!token) {
		goto(`/${$locale}/login`, { replaceState: true });
	} else if (JSON.parse(atob(token.split('.')[1])).exp > new Date().getTime()) {
		localStorage.removeItem('token');
		goto(`/${$locale}/login`, { replaceState: true });
	}

	const users = read_users(token!);
</script>

<div>
	Database users:
	{#await users}
		fetching users...
	{:then r}
		{JSON.stringify(r)}
	{/await}
</div>

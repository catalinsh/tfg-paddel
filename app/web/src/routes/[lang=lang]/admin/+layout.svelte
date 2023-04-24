<script lang="ts">
	import { locale } from '$i18n/i18n-svelte';
	import { goto } from '$app/navigation';
	import type { LayoutData } from './$types';
	import BigNav from '$lib/BigNav.svelte';
	import Footer from '$lib/Footer.svelte';

	export let data: LayoutData;

	if (!data.currentUser) {
		localStorage.removeItem('token');
		goto(`/${$locale}/login`, { replaceState: true });
	}

	const currentUser = data.currentUser;
</script>

<div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
	<div class="mx-auto max-w-2xl">
		<BigNav {currentUser} />
		<slot />
		<Footer />
	</div>
</div>

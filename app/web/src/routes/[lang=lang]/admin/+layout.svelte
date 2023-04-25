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

{#if currentUser}
	<div class="mx-auto max-w-xl px-8 sm:px-12 md:max-w-3xl lg:px-16">
		<div class="mx-auto max-w-2xl">
			<BigNav />
			<slot />
			<Footer />
		</div>
	</div>
{/if}

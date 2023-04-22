<script lang="ts">
	import { locale } from '$i18n/i18n-svelte';
	import { goto } from '$app/navigation';
	import SmallNav from '$lib/SmallNav.svelte';
	import Footer from '$lib/Footer.svelte';

	goto(`/${$locale}/login`, { replaceState: true });
</script>

<div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
	<div class="mx-auto max-w-2xl">
		<SmallNav />

		<Footer />
	</div>
</div>

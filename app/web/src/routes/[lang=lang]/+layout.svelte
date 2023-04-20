<script lang="ts">
	import '../../app.css';

	import { setLocale } from '$i18n/i18n-svelte';
	import type { LayoutData } from './$types';
	import HeadHrefLangs from '$lib/HeadHrefLangs.svelte';

	export let data: LayoutData;

	setLocale(data.locale);
</script>

<svelte:head>
	<title>PaDDeL</title>
	<HeadHrefLangs />
</svelte:head>

<slot />

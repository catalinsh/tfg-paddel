<script lang="ts">
	import LL, { setLocale } from '$i18n/i18n-svelte';
	import type { LayoutData } from './$types';
	import HeadHrefLangs from '$lib/HeadHrefLangs.svelte';

	export let data: LayoutData;

	setLocale(data.locale);
</script>

<svelte:head>
	<meta name="description" content={$LL.PAGE_DESCRIPTION()} />
	<title>PaDDeL</title>
	<HeadHrefLangs />
</svelte:head>

<slot />

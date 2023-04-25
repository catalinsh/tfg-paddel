<script lang="ts">
	import LL, { setLocale } from '$i18n/i18n-svelte';
	import type { LayoutData } from './$types';
	import HeadHrefLangs from '$lib/HeadHrefLangs.svelte';
	import { localeLanguageCode } from '$lib/utils';

	export let data: LayoutData;

	document.querySelector('html')?.setAttribute('lang', localeLanguageCode(data.locale));

	setLocale(data.locale);
</script>

<svelte:head>
	<meta name="description" content={$LL.PAGE_DESCRIPTION()} />
	<title>PaDDeL</title>
	<HeadHrefLangs />
</svelte:head>

<slot />

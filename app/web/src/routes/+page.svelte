<script lang="ts">
	import { goto } from '$app/navigation';
	import type { Locales } from '$i18n/i18n-types';
	import { baseLocale, locales } from '$i18n/i18n-util';
	import resolveAcceptLanguage from 'resolve-accept-language';

	const userLang = navigator.language;

	const locale = resolveAcceptLanguage(userLang, locales, baseLocale) as Locales;

	goto(`/${locale}`, { replaceState: true });
</script>

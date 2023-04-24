import type { LayoutLoad } from './$types';
import type { Locales } from '$i18n/i18n-types';
import { loadLocaleAsync } from '$i18n/i18n-util.async';

export const load: LayoutLoad<{ locale: Locales }> = async ({ params }) => {
	const locale = params.lang as Locales;

	await loadLocaleAsync(locale);

	return { locale };
};

export const ssr = false;

import type { Locales } from "$i18n/i18n-types";

export const replaceLocaleInUrl = (url: URL, locale: string, full = false): string => {
	const [, , ...rest] = url.pathname.split('/');
	const new_pathname = `/${[locale, ...rest].join('/')}`;
	if (!full) {
		return `${new_pathname}${url.search}`;
	}
	const newUrl = new URL(url.toString());
	newUrl.pathname = new_pathname;
	return newUrl.toString();
};

export const localeLanguageCode = (l: Locales) => {
	const locale = new Intl.Locale(l);
	return locale.language;
};
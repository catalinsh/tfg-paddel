import { baseLocale, i18n, isLocale, locales } from '$i18n/i18n-util';
import { loadAllLocales } from '$i18n/i18n-util.sync';
import { localeLanguageCode } from '$lib/utils';
import type { Handle, RequestEvent } from '@sveltejs/kit';
import { ResolveAcceptLanguage } from 'resolve-accept-language';

loadAllLocales();
const L = i18n();

export const handle: Handle = async ({ event, resolve }) => {
	const [, lang] = event.url.pathname.split('/');

	if (!lang) {
		const locale = getPreferredLocale(event);

		return new Response(null, {
			status: 302,
			headers: { Location: `/${locale}` }
		});
	}

	const locale = isLocale(lang) ? (lang as Locales) : getPreferredLocale(event);
	const LL = L[locale];

	event.locals.locale = locale;
	event.locals.LL = LL;

	return resolve(event, {
		transformPageChunk: ({ html }) => {
			html = html.replace('%lang%', localeLanguageCode(locale));
			return html;
		}
	});
};

const getPreferredLocale = ({ request }: RequestEvent) => {
	const result = new ResolveAcceptLanguage(request.headers.get('Accept-Language') || '', locales);
	return (result.getBestMatch() as Locales) || baseLocale;
};

type Locales = import('$i18n/i18n-types').Locales;
type TranslationFunctions = import('$i18n/i18n-types').TranslationFunctions;

declare namespace App {
	interface Locals {
		locale: Locales;
		LL: TranslationFunctions;
	}
}

declare module '@fortawesome/pro-solid-svg-icons/index.es' {
	export * from '@fortawesome/pro-solid-svg-icons';
}

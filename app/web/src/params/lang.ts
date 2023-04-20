import type { ParamMatcher } from '@sveltejs/kit';
import { isLocale } from '$i18n/i18n-util';

export const match: ParamMatcher = (param) => {
	return isLocale(param);
};

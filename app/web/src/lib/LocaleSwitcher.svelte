<script lang="ts">
	import { browser } from '$app/environment';
	import { invalidateAll } from '$app/navigation';
	import { page } from '$app/stores';
	import LL, { setLocale, locale } from '$i18n/i18n-svelte';
	import type { Locales } from '$i18n/i18n-types';
	import { locales } from '$i18n/i18n-util';
	import { loadLocaleAsync } from '$i18n/i18n-util.async';
	import LanguageIcon from '$lib/icons/LanguageIcon.svelte';
	import CheckIcon from './icons/CheckIcon.svelte';
	import { localeLanguageCode, replaceLocaleInUrl } from './utils';

	const localeLanguage = (l: Locales) => {
		const locale = new Intl.Locale(l);

		const languageNames = new Intl.DisplayNames([locale], { type: 'language' });
		const language = languageNames.of(locale.language)!;

		return language.charAt(0).toUpperCase() + language.slice(1);
	};

	const switchLocale = async (newLocale: Locales, updateHistoryState = true) => {
		if (!newLocale || $locale === newLocale) return;

		await loadLocaleAsync(newLocale);

		setLocale(newLocale);
		localStorage.setItem('currentLocale', newLocale);

		document.querySelector('html')?.setAttribute('lang', localeLanguageCode(newLocale));

		if (updateHistoryState) {
			history.pushState({ locale: newLocale }, '', replaceLocaleInUrl($page.url, newLocale));
		}

		invalidateAll();
	};

	$: if (browser) {
		const lang = $page.params.lang as Locales;
		switchLocale(lang, false);
		history.replaceState(
			{ ...history.state, locale: lang },
			'',
			replaceLocaleInUrl($page.url, lang)
		);
	}

	let isDropdownOpen = false;
	const toggleDropdown = () => {
		isDropdownOpen = !isDropdownOpen;
	};

	const handleFocusOut = ({ relatedTarget, currentTarget }: FocusEvent) => {
		if (relatedTarget instanceof HTMLElement) {
			if ((currentTarget as HTMLElement).contains(relatedTarget)) {
				return;
			}
		}
		isDropdownOpen = false;
	};
</script>

<div class="relative inline-block" on:focusout={handleFocusOut}>
	<div>
		<button
			on:click={toggleDropdown}
			type="button"
			class="flex items-center rounded-full p-1.5 hover:bg-neutral-200"
			class:bg-neutral-200={isDropdownOpen}
			id="locale-menu-button"
			aria-expanded={isDropdownOpen}
			aria-haspopup="true"
			aria-controls="locale-menu"
		>
			<span class="sr-only">{$LL.LANGUAGE_SELECTION()}</span>
			<LanguageIcon class="h-6 w-6" />
		</button>
	</div>

	<ul
		id="locale-menu"
		class="absolute right-0 p-1 z-10 mt-3 w-32 origin-top-right rounded-md border border-neutral-300 bg-white shadow-md focus:outline-none"
		style:visibility={isDropdownOpen ? 'visible' : 'hidden'}
		role="menu"
		aria-orientation="vertical"
		aria-labelledby="locale-menu-button"
	>
			<li class="list-none">
				{#each locales as l}
					<a
						href={`${replaceLocaleInUrl($page.url, l)}`}
						class="flex flex-shrink-0 justify-between rounded-sm px-4 py-2 align-middle text-sm hover:bg-neutral-200"
						role="menuitem"
						aria-current={l === $locale ? 'location' : undefined}
					>
						<span>
							{localeLanguage(l)}
						</span>
						{#if l === $locale}
							<CheckIcon class="h-5 w-5" />
						{/if}
					</a>
				{/each}
			</li>
		</ul>
</div>

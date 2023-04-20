<script lang="ts">
	import { browser } from '$app/environment';
	import { invalidateAll } from '$app/navigation';
	import { page } from '$app/stores';
	import LL, { setLocale, locale } from '$i18n/i18n-svelte';
	import type { Locales } from '$i18n/i18n-types';
	import { locales } from '$i18n/i18n-util';
	import { loadLocaleAsync } from '$i18n/i18n-util.async';
	import { localeLanguage, localeLanguageCode, replaceLocaleInUrl } from './utils';
	import { Icon, Language } from 'svelte-hero-icons';

	const switchLocale = async (newLocale: Locales, updateHistoryState = true) => {
		if (!newLocale || $locale === newLocale) return;

		await loadLocaleAsync(newLocale);

		setLocale(newLocale);

		document.querySelector('html')?.setAttribute('lang', localeLanguageCode(newLocale));

		if (updateHistoryState) {
			history.pushState({ locale: newLocale }, '', replaceLocaleInUrl($page.url, newLocale));
		}

		invalidateAll();
	};

	const handlePopStateEvent = async ({ state }: PopStateEvent) => switchLocale(state.locale, false);

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
	let container: HTMLElement;
	const toggleDropdown = () => {
		isDropdownOpen = !isDropdownOpen;
	};
	const onWindowClick = (e: MouseEvent) => {
		if (!container.contains(e.target as Node)) {
			isDropdownOpen = false;
		}
	};
</script>

<svelte:window on:popstate={handlePopStateEvent} on:click={onWindowClick} />

<div class="relative inline-block" bind:this={container}>
	<div>
		<button
			on:click={toggleDropdown}
			type="button"
			class="flex items-center rounded-full p-1.5 hover:bg-neutral-200"
			class:bg-neutral-200={isDropdownOpen}
			id="menu-button"
			aria-expanded="true"
			aria-haspopup="true"
		>
			<span class="sr-only">{$LL.LANGUAGE_SELECTION()}</span>
			<Icon src={Language} class="h-6 w-6" />
		</button>
	</div>

	<div
		class="absolute right-0 z-10 mt-3 w-32 origin-top-right rounded-md border border-neutral-300 shadow-lg focus:outline-none dark:border-neutral-600"
		role="menu"
		class:hidden={!isDropdownOpen}
		aria-orientation="vertical"
		aria-labelledby="menu-button"
		tabindex="-1"
	>
		<div class="py-1" role="none">
			<li class="list-none">
				{#each locales as l}
					<a
						href={`${replaceLocaleInUrl($page.url, l)}`}
						class="flex flex-shrink-0 justify-between px-4 py-2 align-middle text-sm hover:bg-neutral-200 dark:hover:bg-neutral-700"
						role="menuitem"
						tabindex="-1"
						aria-current={l === $locale ? 'location' : undefined}
					>
						<span>
							{localeLanguage(l)}
						</span>
						{#if l === $locale}
							<svg
								fill="none"
								viewBox="0 0 24 24"
								stroke-width="1.5"
								stroke="currentColor"
								class="h-5 w-5"
							>
								<path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
							</svg>
						{/if}
					</a>
				{/each}
			</li>
		</div>
	</div>
</div>

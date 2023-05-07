<script lang="ts">
	import { goto } from '$app/navigation';
	import LL, { locale } from '$i18n/i18n-svelte';
	import ButtonSecondary from './ButtonSecondary.svelte';
	import LocaleSwitcher from './LocaleSwitcher.svelte';
	import PaddelIcon from './icons/PaddelIcon.svelte';

	const logOutHandler = () => {
		goto(`/${$locale}`, { replaceState: true });
		localStorage.removeItem('token');
	};
</script>

<nav class="flex justify-between py-4">
	<a href={`/${$locale}`} class="flex items-center gap-2 hover:underline">
		<PaddelIcon class="h-8 w-8" />
		<span class="sr-only font-bold sm:not-sr-only">PaDDeL</span>
	</a>
	<div class="flex items-center gap-2">
		<ButtonSecondary on:click={logOutHandler}>{$LL.LOG_OUT()}</ButtonSecondary>
		<LocaleSwitcher />
	</div>
</nav>

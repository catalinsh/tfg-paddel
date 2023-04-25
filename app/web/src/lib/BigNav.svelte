<script lang="ts">
	import { goto } from '$app/navigation';
	import { locale } from '$i18n/i18n-svelte';
	import ButtonSecondary from './ButtonSecondary.svelte';
	import LocaleSwitcher from './LocaleSwitcher.svelte';
	import PaddelIcon from './icons/PaddelIcon.svelte';

	const logOutHandler = () => {
		goto(`/${$locale}`, { replaceState: true });
		localStorage.removeItem('token');
	};
</script>

<nav class="flex justify-between py-2">
	<a href="/{$locale}" class="group inline-flex items-center gap-2 p-2">
		<PaddelIcon class="h-7 w-7" />
		<span class="hidden font-bold group-hover:underline sm:inline">PaDDeL</span>
	</a>
	<div class="flex items-center gap-2">
		<LocaleSwitcher />

		<ButtonSecondary on:click={logOutHandler}>Log out</ButtonSecondary>
	</div>
</nav>

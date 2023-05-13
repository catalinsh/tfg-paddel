<script lang="ts">
	import LL, { locale } from '$i18n/i18n-svelte';
	import LocaleSwitcher from '$lib/LocaleSwitcher.svelte';
	import PaddelIcon from '$lib/icons/PaddelIcon.svelte';
	import ButtonPrimary from './ButtonPrimary.svelte';
</script>

<nav class="flex justify-between py-6">
	<a data-sveltekit-reload href={`/${$locale}`} class="flex items-center gap-2 hover:underline">
		<PaddelIcon class="h-8 w-8" />
		<span class="sr-only font-bold sm:not-sr-only">PaDDeL</span>
	</a>

	<div class="flex items-center gap-2">
		<ButtonPrimary href={`/${$locale}/admin/models`}>
			{$LL.ADMINISTRATION()}
		</ButtonPrimary>
		<LocaleSwitcher />
	</div>
</nav>

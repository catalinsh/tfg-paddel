<script lang="ts">
	import LL, { locale } from '$i18n/i18n-svelte';
	import LocaleSwitcher from '$lib/LocaleSwitcher.svelte';
	import PaddelIcon from '$lib/icons/PaddelIcon.svelte';
</script>

<nav class="flex justify-between p-4">
	<a href={`/${$locale}`} class="flex items-center gap-2 hover:underline">
		<PaddelIcon class="h-8 w-8" />
		<span class="hidden font-bold sm:inline">PaDDeL</span>
	</a>

	<div class="flex items-center gap-2">
		<a
			href={`/${$locale}/admin`}
			class="rounded-sm bg-indigo-600 p-2 px-3.5 py-2.5 font-semibold text-white hover:bg-indigo-700"
		>
			{$LL.ADMINISTRATION()}
		</a>

		<LocaleSwitcher />
	</div>
</nav>

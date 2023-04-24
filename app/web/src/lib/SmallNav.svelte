<script>
	import LocaleSwitcher from './LocaleSwitcher.svelte';
	import { locale } from '$i18n/i18n-svelte';
	import LL from '$i18n/i18n-svelte';
	import ButtonPrimary from './ButtonPrimary.svelte';
	import PaddelIcon from './icons/PaddelIcon.svelte';
</script>

<nav class="flex justify-between py-2">
	<a href="/{$locale}" class="group inline-flex items-center gap-2 p-2">
		<PaddelIcon class="h-7 w-7" />
		<span class="hidden font-bold group-hover:underline sm:inline">PaDDeL</span>
	</a>
	<div class="flex items-center gap-2">
		<a href="/{$locale}/admin">
			<ButtonPrimary>
				{$LL.ADMINISTRATION()}
			</ButtonPrimary>
		</a>
		<LocaleSwitcher />
	</div>
</nav>

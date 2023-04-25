<script lang="ts">
	import LL from '$i18n/i18n-svelte';
	import { PUBLIC_API_LOCATION } from '$env/static/public';
</script>

<footer>
	<div class="mx-auto max-w-7xl py-12 md:flex md:items-center md:justify-between">
		<div class="flex justify-center space-x-6 md:order-2">
			<a
				href="https://github.com/cataand/tfg"
				target="_blank"
				class="text-xs text-neutral-500 hover:text-neutral-700">{$LL.SOURCE_CODE()}</a
			>
			<a
				href={`${PUBLIC_API_LOCATION}/docs`}
				target="_blank"
				class="text-xs text-neutral-500 hover:text-neutral-700">{$LL.API_DOCS()}</a
			>
		</div>
		<div class="mt-8 md:order-1 md:mt-0">
			<p class="text-center text-xs leading-5 text-neutral-600">
				&copy; 2023 {$LL.UNIVERSITY_OF_BURGOS()}
			</p>
		</div>
	</div>
</footer>

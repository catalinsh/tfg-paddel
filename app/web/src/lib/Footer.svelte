<script lang="ts">
	import LL, { locale } from '$i18n/i18n-svelte';
	import { PUBLIC_API_LOCATION } from '$env/static/public';
</script>

<footer>
	<div class="mx-auto max-w-7xl py-12 md:flex md:items-center md:justify-between">
		<div class="flex flex-wrap justify-around sm:justify-center sm:space-x-2 sm:content-normal content-between md:order-2 h-12 sm:h-auto">
			<a
				href="{`/${$locale}/about`}"
				class="text-xs px-2 text-neutral-500 hover:text-neutral-700">{$LL.ABOUT()}</a
			>
			<a
				href="https://github.com/cataand/tfg"
				target="_blank"
				class="text-xs px-2 text-neutral-500 hover:text-neutral-700">{$LL.SOURCE_CODE()}</a
			>
			<a
				href={`${PUBLIC_API_LOCATION}/docs`}
				target="_blank"
				class="text-xs px-2 text-neutral-500 hover:text-neutral-700">{$LL.API_DOCS()}</a
			>
		</div>
		<div class="mt-8 md:order-1 md:mt-0">
			<p class="text-center text-xs leading-5 text-neutral-600">
				&copy; 2023 <a href="https://www.ubu.es" class="underline hover:no-underline">{$LL.UNIVERSITY_OF_BURGOS()}</a>
			</p>
		</div>
	</div>
</footer>

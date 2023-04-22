<script lang="ts">
	import LL from '$i18n/i18n-svelte';
	import GithubIcon from './icons/GithubIcon.svelte';
</script>

<footer>
	<div class="mx-auto max-w-7xl px-6 py-12 md:flex md:items-center md:justify-between lg:px-8">
		<div class="flex justify-center space-x-6 md:order-2">
			<a
				href="https://github.com/cataand/tfg"
				target="_blank"
				class="text-zinc-400 hover:text-zinc-500 dark:hover:text-zinc-300"
			>
				<span class="sr-only">GitHub</span>
				<GithubIcon class="h-5 w-5" />
			</a>
		</div>
		<div class="mt-8 md:order-1 md:mt-0">
			<p class="text-center text-xs leading-5 text-zinc-500 dark:text-zinc-400">
				&copy; 2023 {$LL.UNIVERSITY_OF_BURGOS()}
			</p>
		</div>
	</div>
</footer>

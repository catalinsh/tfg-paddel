<script lang="ts">
	let clazz = '';
	export { clazz as class };
	export let href: string = '';
</script>

{#if href}
	<a
		{href}
		{...$$restProps}
		class="{clazz} flex w-full justify-center rounded-md bg-blue-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
	>
		<slot />
	</a>
{:else}
	<button
		on:click
		{...$$restProps}
		class="{clazz} flex w-full justify-center rounded-md bg-blue-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
	>
		<slot />
	</button>
{/if}

<script lang="ts">
	let clazz = '';
	export { clazz as class };
	export let href: string = '';
</script>

{#if href}
	<a
		{href}
		{...$$restProps}
		type="button"
		class="{clazz} rounded-md bg-white px-3 py-1.5 text-sm font-semibold leading-6 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
	>
		<slot />
	</a>
{:else}
	<button
		on:click
		{...$$restProps}
		type="button"
		class="{clazz} rounded-md bg-white px-3 py-1.5 text-sm font-semibold leading-6 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
	>
		<slot />
	</button>
{/if}

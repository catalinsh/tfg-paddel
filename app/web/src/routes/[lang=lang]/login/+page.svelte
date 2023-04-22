<script lang="ts">
	import SmallNav from '$lib/SmallNav.svelte';
	import Footer from '$lib/Footer.svelte';
	import { read_users } from '$lib/api';

	const users = read_users(
		'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjYXRhIiwiZXhwIjoxNjgyMTgzOTc3fQ.Rkqd_vqQuswLEO0nmNkjyHamlC0g6tQJV0DREWSMmRo'
	);
</script>

<div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
	<div class="mx-auto max-w-2xl">
		<SmallNav />
		Database users:
		<div>
			{#await users}
				fetching users...
			{:then r}
				{JSON.stringify(r)}
			{/await}
		</div>
		<Footer />
	</div>
</div>

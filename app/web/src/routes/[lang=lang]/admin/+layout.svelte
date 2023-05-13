<script lang="ts">
	import LL, { locale } from '$i18n/i18n-svelte';
	import { goto } from '$app/navigation';
	import type { LayoutData } from './$types';
	import BigNav from '$lib/BigNav.svelte';
	import Footer from '$lib/Footer.svelte';
	import { page } from '$app/stores';
	import UserIcon from '$lib/icons/UserIcon.svelte';
	import ModelIcon from '$lib/icons/ModelIcon.svelte';

	export let data: LayoutData;

	if (!data.currentUser) {
		localStorage.removeItem('token');
		goto(`/${$locale}/login`, { replaceState: true });
	}

	$: location = $page.url.pathname;

	const currentUser = data.currentUser;
</script>

{#if currentUser}
	<div class="mx-auto max-w-xl px-4 sm:px-6 md:max-w-3xl lg:px-8">
		<BigNav />
	</div>
	<div class="mx-auto max-w-xl sm:px-6 md:max-w-3xl lg:px-8">
		<div class="sm:block">
			<div class="border-b border-neutral-200">
				<div class="-mb-px flex space-x-8 justify-center" aria-label="Tabs">
					<a
						href={`/${$locale}/admin/users`}
						class="{location.includes("admin/users") ? "border-blue-500 text-blue-600" : "border-transparent text-neutral-500 hover:border-neutral-300 hover:text-neutral-700"} group inline-flex items-center border-b-2 px-1 py-4 text-sm font-medium"
					>
						<UserIcon class="{location.includes("admin/users") ? "text-blue-500" : "text-neutral-400 group-hover:text-neutral-500"} -ml-0.5 mr-2 h-5 w-5" />
						<span>{$LL.USERS()}</span>
					</a>
					<a
						href={`/${$locale}/admin/models`}
						class="{location.includes("admin/models") ? "border-blue-500 text-blue-600" : "border-transparent text-neutral-500 hover:border-neutral-300 hover:text-neutral-700"} group inline-flex items-center border-b-2 px-1 py-4 text-sm font-medium"
					>
						<ModelIcon class="{location.includes("admin/models") ? "text-blue-500" : "text-neutral-400 group-hover:text-neutral-500"} -ml-0.5 mr-2 h-5 w-5" />
						<span>{$LL.MODELS()}</span>
					</a>
				</div>
			</div>
		</div>
	</div>
	<slot />
	<div class="mx-auto max-w-xl px-4 sm:px-6 md:max-w-3xl lg:px-8">
		<Footer />
	</div>
{/if}

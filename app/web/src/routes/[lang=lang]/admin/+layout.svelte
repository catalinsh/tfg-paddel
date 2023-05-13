<script lang="ts">
	import { locale } from '$i18n/i18n-svelte';
	import { goto } from '$app/navigation';
	import type { LayoutData } from './$types';
	import BigNav from '$lib/BigNav.svelte';
	import Footer from '$lib/Footer.svelte';
	import { page } from '$app/stores';

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
						<svg
							class="{location.includes("admin/users") ? "text-blue-500" : "text-neutral-400 group-hover:text-neutral-500"} -ml-0.5 mr-2 h-5 w-5"
							viewBox="0 0 20 20"
							fill="currentColor"
							aria-hidden="true"
						>
							<path
								d="M10 8a3 3 0 100-6 3 3 0 000 6zM3.465 14.493a1.23 1.23 0 00.41 1.412A9.957 9.957 0 0010 18c2.31 0 4.438-.784 6.131-2.1.43-.333.604-.903.408-1.41a7.002 7.002 0 00-13.074.003z"
							/>
						</svg>
						<span>Usuarios</span>
					</a>
					<a
						href={`/${$locale}/admin/models`}
						class="{location.includes("admin/models") ? "border-blue-500 text-blue-600" : "border-transparent text-neutral-500 hover:border-neutral-300 hover:text-neutral-700"} group inline-flex items-center border-b-2 px-1 py-4 text-sm font-medium"
					>
						<svg
						class="{location.includes("admin/models") ? "text-blue-500" : "text-neutral-400 group-hover:text-neutral-500"} -ml-0.5 mr-2 h-5 w-5"
							xmlns="http://www.w3.org/2000/svg"
							fill="currentColor"
							viewBox="0 0 24 24"
							aria-hidden="true"
							stroke-width="1.5"
							stroke="currentColor"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								d="M21 7.5l-2.25-1.313M21 7.5v2.25m0-2.25l-2.25 1.313M3 7.5l2.25-1.313M3 7.5l2.25 1.313M3 7.5v2.25m9 3l2.25-1.313M12 12.75l-2.25-1.313M12 12.75V15m0 6.75l2.25-1.313M12 21.75V19.5m0 2.25l-2.25-1.313m0-16.875L12 2.25l2.25 1.313M21 14.25v2.25l-2.25 1.313m-13.5 0L3 16.5v-2.25"
							/>
						</svg>
						<span>Modelos</span>
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

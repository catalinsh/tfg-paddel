<script lang="ts">
	import LL, { locale } from '$i18n/i18n-svelte';
	import { goto } from '$app/navigation';
	import PaddelIcon from '$lib/icons/PaddelIcon.svelte';
	import { token_login } from '$lib/api';
	import Footer from '$lib/Footer.svelte';
	import ButtonPrimary from '$lib/ButtonPrimary.svelte';
	import SmallNav from '$lib/SmallNav.svelte';
	import ButtonSecondary from '$lib/ButtonSecondary.svelte';
	import BackIcon from '$lib/icons/BackIcon.svelte';

	const currentToken = localStorage.getItem('token');

	if (currentToken) {
		goto(`/${$locale}/admin`, { replaceState: true });
	}

	let username: string;
	let password: string;

	const submitHandler = async () => {
		const result = await token_login(username, password);

		if (result) {
			const token = result.access_token;
			localStorage.setItem('token', token);
			goto(`/${$locale}/admin`, { replaceState: true });
		}
	};
</script>

<div class="max-w-lg mx-auto px-8 sm:px-12 lg:px-16 py-6">
	<ButtonSecondary href={`/${$locale}`} class="inline-flex gap-1 items-center pl-2"><BackIcon class="h-5 w-5 inline"></BackIcon> {$LL.BACK()}</ButtonSecondary>

	<div class="mt-12">
		<div class="text-center">
			<PaddelIcon class="inline h-16 w-16 stroke-blue-600" />
		</div>
		<h2 class="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">
			{$LL.LOG_IN_TO_YOUR_ACCOUNT()}
		</h2>
	</div>

	<form class="space-y-6 mt-8" on:submit|preventDefault={submitHandler}>
		<div>
			<label for="username" class="block text-sm font-medium leading-6 text-gray-900">
				{$LL.USERNAME()}
			</label>
			<div class="mt-2">
				<input
					bind:value={username}
					id="username"
					name="username"
					type="text"
					autocomplete="nickname"
					required
					class="block w-full rounded-md"
				/>
			</div>
		</div>

		<div>
			<div class="block items-center justify-between">
				<label for="password" class="block text-sm font-medium leading-6 text-gray-900">
					{$LL.PASSWORD()}
				</label>
			</div>
			<div class="mt-2">
				<input
					bind:value={password}
					id="password"
					name="password"
					type="password"
					autocomplete="current-password"
					required
					class="block w-full rounded-md"
				/>
			</div>
		</div>

		<ButtonPrimary type="submit" on:click={submitHandler}>{$LL.LOG_IN()}</ButtonPrimary>
	</form>
</div>

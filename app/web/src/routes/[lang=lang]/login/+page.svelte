<script lang="ts">
	import LL, { locale } from '$i18n/i18n-svelte';
	import { goto } from '$app/navigation';
	import PaddelIcon from '$lib/icons/PaddelIcon.svelte';
	import { token_login } from '$lib/api';
	import ButtonPrimary from '$lib/ButtonPrimary.svelte';
	import ButtonSecondary from '$lib/ButtonSecondary.svelte';
	import BackIcon from '$lib/icons/BackIcon.svelte';
	import LocaleSwitcher from '$lib/LocaleSwitcher.svelte';
	import { onMount } from 'svelte';

	const currentToken = localStorage.getItem('token');

	if (currentToken) {
		goto(`/${$locale}/admin`, { replaceState: true });
	}

	let username: string;
	let password: string;
	let usernameInput: HTMLInputElement;
	let submitted = false;

	onMount(async () => {
		usernameInput.focus();
	});

	const submitHandler = async () => {
		submitted = false;
		const result = await token_login(username, password);

		if (result) {
			const token = result.access_token;
			localStorage.setItem('token', token);
			goto(`/${$locale}/admin/models`, { replaceState: true });
		} else {
			submitted = true;
		}
	};
</script>

<div class="mx-auto max-w-lg px-8 py-6 sm:px-12 lg:px-16">
	<div class="flex items-center justify-between">
		<ButtonSecondary href={`/${$locale}`} class="inline-flex items-center gap-1 pl-2">
			<BackIcon class="inline h-5 w-5" />
			{$LL.BACK()}
		</ButtonSecondary>
		<LocaleSwitcher />
	</div>

	<main>
		<div class="mt-12">
			<div class="text-center">
				<PaddelIcon class="inline h-16 w-16 stroke-blue-600" />
			</div>
			<h1 class="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">
				{$LL.LOG_IN_TO_YOUR_ACCOUNT()}
			</h1>
		</div>

		<div
			class="mt-8 rounded-md bg-red-50 p-4"
			aria-live="assertive"
			style:display={submitted ? 'block' : 'none'}
		>
			<div class="flex">
				<div class="flex-shrink-0">
					<svg
						class="h-5 w-5 text-red-400"
						viewBox="0 0 20 20"
						fill="currentColor"
						aria-hidden="true"
					>
						<path
							fill-rule="evenodd"
							d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.28 7.22a.75.75 0 00-1.06 1.06L8.94 10l-1.72 1.72a.75.75 0 101.06 1.06L10 11.06l1.72 1.72a.75.75 0 101.06-1.06L11.06 10l1.72-1.72a.75.75 0 00-1.06-1.06L10 8.94 8.28 7.22z"
							clip-rule="evenodd"
						/>
					</svg>
				</div>
				<div class="ml-3">
					<p class="text-sm font-medium text-red-800">{$LL.LOGIN_FAILED()}</p>
				</div>
			</div>
		</div>

		<form class="mt-8 space-y-6" on:submit|preventDefault={submitHandler}>
			<div>
				<label for="username" class="block text-sm font-medium leading-6 text-gray-900">
					{$LL.USERNAME()}
				</label>
				<div class="mt-2">
					<input
						bind:this={usernameInput}
						bind:value={username}
						id="username"
						name="username"
						type="text"
						autocomplete="nickname"
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
						class="block w-full rounded-md"
					/>
				</div>
			</div>

			<ButtonPrimary type="submit" on:click={submitHandler}>{$LL.LOG_IN()}</ButtonPrimary>
		</form>
	</main>
</div>

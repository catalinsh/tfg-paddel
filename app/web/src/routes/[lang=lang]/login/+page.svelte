<script lang="ts">
	import { locale } from '$i18n/i18n-svelte';
	import { goto } from '$app/navigation';
	import PaddelIcon from '$lib/icons/PaddelIcon.svelte';
	import { token_login } from '$lib/api';
	import SmallNav from '$lib/SmallNav.svelte';
	import Footer from '$lib/Footer.svelte';

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

<div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
	<div class="mx-auto max-w-lg">
		<div class="flex min-h-full flex-col justify-center px-6 py-12 lg:px-8">
			<div class="sm:mx-auto sm:w-full sm:max-w-sm">
				<div class="text-center">
					<PaddelIcon class="inline h-16 w-16 stroke-indigo-600" />
				</div>
				<h2 class="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">
					Sign in to your account
				</h2>
			</div>

			<div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
				<form class="space-y-6" on:submit|preventDefault={submitHandler}>
					<div>
						<label for="username" class="block text-sm font-medium leading-6 text-gray-900"
							>Username</label
						>
						<div class="mt-2">
							<input
								bind:value={username}
								id="username"
								name="username"
								type="text"
								autocomplete="nickname"
								required
								class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
							/>
						</div>
					</div>

					<div>
						<div class="block items-center justify-between">
							<label for="password" class="block text-sm font-medium leading-6 text-gray-900"
								>Password</label
							>
						</div>
						<div class="mt-2">
							<input
								bind:value={password}
								id="password"
								name="password"
								type="password"
								autocomplete="current-password"
								required
								class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
							/>
						</div>
					</div>

					<div>
						<button
							type="submit"
							class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
							>Sign in</button
						>
					</div>
				</form>
			</div>
		</div>

		<Footer />
	</div>
</div>

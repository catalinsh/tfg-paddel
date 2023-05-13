<script lang="ts">
	import LL, { locale } from '$i18n/i18n-svelte';
	import { goto } from '$app/navigation';
	import { read_users, create_user, delete_user } from '$lib/api';
	import ButtonPrimary from '$lib/ButtonPrimary.svelte';
	import ButtonSecondary from '$lib/ButtonSecondary.svelte';
	import type { LayoutData } from '../$types';
	import LoadingIcon from '$lib/icons/LoadingIcon.svelte';

	const token = localStorage.getItem('token');
	export let data: LayoutData;

	if (!token) {
		goto(`/${$locale}/login`, { replaceState: true });
	} else if (JSON.parse(atob(token.split('.')[1])).exp > new Date().getTime()) {
		localStorage.removeItem('token');
		goto(`/${$locale}/login`, { replaceState: true });
	}

	let usersLoading = read_users(token!);
	let selectedUser: { username: string; id: number };
	let createUserModal: HTMLDialogElement;
	let deleteUserModal: HTMLDialogElement;
	let createUserErrorMessage: string;

	const newUserHandler = async (e: Event) => {
		const formData = new FormData(e.target as HTMLFormElement);

		if ((formData.get('username') as string).length < 3) {
			createUserErrorMessage = $LL.USERNAME_TOO_SHORT();
			return;
		}

		const newUser = await create_user(
			formData.get('username') as string,
			formData.get('password') as string
		);

		if (newUser) {
			createUserModal.close();
			usersLoading = read_users(token!);
			(e.target as HTMLFormElement).reset();
		} else if ((formData.get('password') as string).length < 8) {
			createUserErrorMessage = $LL.PASSWORD_TOO_SHORT();
		} else {
			createUserErrorMessage = $LL.USER_ALREADY_EXISTS();
		}
	};

	const deleteSelectedUser = async () => {
		const deletedUser = await delete_user(selectedUser.id);
		if (deletedUser) {
			deleteUserModal.close();
			usersLoading = read_users(token!);
		}
	};
</script>

<div class="mx-auto mt-8 max-w-xl px-4 sm:px-6 md:max-w-3xl lg:px-8">
	<div class="sm:flex sm:items-center">
		<div class="sm:flex-auto">
			<h1 class="text-base font-semibold leading-6 text-neutral-900">{$LL.USER_MANAGEMENT()}</h1>
			<p class="mt-2 text-sm text-neutral-700">{$LL.USER_MANAGEMENT_DESC()}</p>
		</div>
		<div class="mt-4 sm:ml-16 sm:mt-0 sm:flex-none">
			<button
				on:click={() => createUserModal.showModal()}
				type="button"
				class="block rounded-md bg-blue-600 px-3 py-2 text-center text-sm font-semibold text-white shadow-sm hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
				>{$LL.ADD_USER()}</button
			>
		</div>
	</div>
	<div class="mt-8 flow-root">
		<div class="-mx-4 -my-2 sm:-mx-6 lg:-mx-8">
			<div class="inline-block min-w-full py-2 align-middle">
				{#key usersLoading}
					{#await usersLoading}
						<div class="mt-8 text-center">
							<span
								class="inline-flex items-center gap-2 px-4 text-left text-sm font-semibold"
								aria-live="assertive"
							>
								<LoadingIcon
									class="block h-5 w-5 flex-shrink-0 animate-spin fill-blue-600 text-neutral-200 dark:fill-blue-400 dark:text-neutral-700"
								/>
								Fetching Users...
							</span>
						</div>
					{:then users}
						<table class="min-w-full border-separate border-spacing-0">
							<thead>
								<tr>
									<th
										scope="col"
										class="sticky top-0 z-10 border-b border-neutral-300 bg-white bg-opacity-75 py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-neutral-900 backdrop-blur backdrop-filter sm:pl-6 lg:pl-8"
										>{$LL.ID()}</th
									>
									<th
										scope="col"
										class="sticky top-0 z-10 border-b border-neutral-300 bg-white bg-opacity-75 px-3 py-3.5 text-left text-sm font-semibold text-neutral-900 backdrop-blur backdrop-filter sm:table-cell"
										>{$LL.USERNAME()}</th
									>
									<th
										scope="col"
										class="sticky top-0 z-10 border-b border-neutral-300 bg-white bg-opacity-75 py-3.5 pl-3 pr-2 backdrop-blur backdrop-filter sm:pr-6 lg:pr-8"
									>
										<span class="sr-only">{$LL.ACTIONS()}</span>
									</th>
								</tr>
							</thead>
							<tbody>
								{#each users as user}
									<tr>
										<td
											class="whitespace-nowrap border-b border-neutral-200 py-4 pl-4 pr-3 text-sm font-medium text-neutral-900 sm:pl-6 lg:pl-8"
											>{user.id}</td
										>
										<td
											class="whitespace-nowrap border-b border-neutral-200 px-3 py-4 text-sm text-neutral-500 sm:table-cell"
											>{user.username}</td
										>
										<td
											class="relative whitespace-nowrap border-b border-neutral-200 py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-8 lg:pr-8"
										>
											<!--
									<button class="mr-4 text-blue-600 hover:text-blue-900">
										Edit<span class="sr-only">, {user.username}</span>
									</button>
									-->
											{#if user.id !== data.currentUser.id}
												<button
													on:click={() => {
														selectedUser = user;
														deleteUserModal.showModal();
													}}
													class="text-red-600 hover:text-red-900"
												>
													{$LL.DELETE()}<span class="sr-only">, {user.username}</span>
												</button>
											{:else}
												<button
													on:click={() => {
														selectedUser = user;
														deleteUserModal.showModal();
													}}
													class="text-gray-300"
													disabled
												>
													{$LL.DELETE()}<span class="sr-only">, {user.username}</span>
												</button>
											{/if}
										</td>
									</tr>
								{/each}
							</tbody>
						</table>
					{:catch e}
						Could not fetch userlist, reason: {e.message}
					{/await}
				{/key}
			</div>
		</div>
	</div>
</div>
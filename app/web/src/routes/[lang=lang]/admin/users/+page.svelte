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

<!-- Delete user modal -->
<dialog
	bind:this={deleteUserModal}
	class="relative z-10 p-0 backdrop:fixed backdrop:inset-0 backdrop:bg-gray-500 backdrop:bg-opacity-75 backdrop:transition-opacity"
	aria-labelledby="modal-title"
	aria-modal="true"
>
	<div class="fixed inset-0 z-10 overflow-y-auto">
		<div class="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
			<div
				class="relative transform overflow-hidden rounded-lg bg-white text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg"
			>
				<div class="bg-white px-4 pb-4 pt-5 sm:p-6 sm:pb-4">
					<div class="sm:flex sm:items-start">
						<div
							class="mx-auto flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-full bg-red-100 sm:mx-0 sm:h-10 sm:w-10"
						>
							<svg
								class="h-6 w-6 text-red-600"
								fill="none"
								viewBox="0 0 24 24"
								stroke-width="1.5"
								stroke="currentColor"
								aria-hidden="true"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z"
								/>
							</svg>
						</div>
						<div class="mt-3 text-center sm:ml-4 sm:mt-0 sm:text-left">
							<h3 class="text-base font-semibold leading-6 text-gray-900" id="modal-title">
								Delete {#if selectedUser}{selectedUser.username}{/if}'s account?
							</h3>
							<div class="mt-2">
								<p class="text-sm text-gray-500">
									Are you sure you want to permanently delete this account? This action cannot be
									undone.
								</p>
							</div>
						</div>
					</div>
				</div>
				<div class="bg-gray-50 px-4 py-3 sm:flex sm:flex-row-reverse sm:px-6">
					<button
						on:click={deleteSelectedUser}
						type="button"
						class="inline-flex w-full justify-center rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-500 sm:ml-3 sm:w-auto"
						>Delete</button
					>
					<button
						on:click={() => deleteUserModal.close()}
						type="button"
						class="mt-3 inline-flex w-full justify-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 sm:mt-0 sm:w-auto"
						>Cancel</button
					>
				</div>
			</div>
		</div>
	</div>
</dialog>

<!-- Create user modal -->
<dialog
	bind:this={createUserModal}
	class="relative z-10 p-0 backdrop:fixed backdrop:inset-0 backdrop:bg-gray-500 backdrop:bg-opacity-75 backdrop:transition-opacity"
	aria-labelledby="modal-title"
	aria-modal="true"
>
	<div class="fixed inset-0 z-10 overflow-y-auto">
		<div class="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
			<div
				class="relative transform overflow-hidden rounded-lg bg-white text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg"
			>
				<div class="bg-white px-4 pb-4 pt-5 sm:p-6">
					<div class="text-center sm:mt-0 sm:text-left">
						<h3 class="text-base font-semibold leading-6 text-gray-900" id="modal-title">
							Create new user
						</h3>

						{#if createUserErrorMessage}
							<div class="mt-2 rounded-md bg-red-50 p-4" aria-live="assertive">
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
										<p class="text-sm font-medium text-red-800">{createUserErrorMessage}</p>
									</div>
								</div>
							</div>
						{/if}

						<form on:submit|preventDefault={newUserHandler} class="mt-2">
							<div>
								<label for="username" class="block text-sm font-medium leading-6 text-gray-900">
									{$LL.USERNAME()}
								</label>
								<div class="mt-2">
									<input
										id="username"
										name="username"
										type="text"
										autocomplete="nickname"
										class="block w-full rounded-md"
									/>
								</div>
							</div>

							<div class="mt-4">
								<div class="block items-center justify-between">
									<label for="password" class="block text-sm font-medium leading-6 text-gray-900">
										{$LL.PASSWORD()}
									</label>
								</div>
								<div class="mt-2">
									<input
										id="password"
										name="password"
										type="password"
										autocomplete="current-password"
										class="block w-full rounded-md"
									/>
								</div>
							</div>
							<ButtonPrimary class="mt-4" type="submit">Create user</ButtonPrimary>
							<ButtonSecondary
								on:click={() => {
									createUserModal.close();
									createUserErrorMessage = '';
								}}
								class="mt-2 w-full"
								type="submit">Cancel</ButtonSecondary
							>
						</form>
					</div>
				</div>
			</div>
		</div>
	</div>
</dialog>

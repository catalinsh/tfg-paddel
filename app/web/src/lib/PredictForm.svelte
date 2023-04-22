<script lang="ts">
	import LL from '$i18n/i18n-svelte';
	import { createEventDispatcher } from 'svelte';
	import VideoIcon from '$lib/icons/VideoIcon.svelte';

	const dispatch = createEventDispatcher();

	let fileInput: HTMLInputElement;

	let file: File;
	let dominantHand: number;
	let videoHand: number;
	let age: number;
	let sex: number;

	const fileDropHandler = (e: DragEvent) => {
		if (e.dataTransfer?.items) {
			const item = e.dataTransfer.items[0];
			file = item.getAsFile()!;
			fileInput.files = e.dataTransfer.files;
		}
	};

	const inputSelectHandler = (e: Event) => {
		const files = (e.target as HTMLInputElement).files;
		if (files) {
			file = files[0];
		}
	};

	const submitHandler = () => {
		dispatch('submit', {
			dominantHand,
			videoHand,
			age,
			sex,
			file
		});
	};
</script>

<form on:submit|preventDefault={submitHandler}>
	<div class="mt-4 space-y-12">
		<div class="pb-6">
			<h2 class="text-base font-semibold leading-7 text-gray-900">{$LL.PREDICT()}</h2>
			<p class="mt-1 text-sm leading-6 text-gray-600">
				{$LL.PREDICT_HELP()}
			</p>

			<div class="mt-10 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
				<div class="sm:col-span-3">
					<span class="block text-base font-semibold leading-6 text-zinc-900">
						{$LL.YOUR_DOMINANT_HAND()}
					</span>
					<div class="mt-2 space-y-3">
						<div class="flex items-center gap-x-3">
							<input
								id="dominant-hand-left"
								name="dominant-hand"
								class="h-4 w-4 border-zinc-300 text-indigo-600 focus:ring-indigo-600"
								type="radio"
								value={0}
								bind:group={dominantHand}
								required
							/>
							<label
								for="dominant-hand-left"
								class="block text-sm font-medium leading-6 text-zinc-900"
							>
								{$LL.LEFT()}
							</label>
						</div>
						<div class="flex items-center gap-x-3">
							<input
								id="dominant-hand-right"
								name="dominant-hand"
								class="h-4 w-4 border-zinc-300 text-indigo-600 focus:ring-indigo-600"
								type="radio"
								value={1}
								bind:group={dominantHand}
								required
							/>
							<label
								for="dominant-hand-right"
								class="block text-sm font-medium leading-6 text-zinc-900"
							>
								{$LL.RIGHT()}
							</label>
						</div>
					</div>
				</div>

				<div class="sm:col-span-3">
					<span class="block text-base font-semibold leading-6 text-zinc-900">
						{$LL.HAND_SHOWN_IN_VIDEO()}
					</span>
					<div class="mt-2 space-y-3">
						<div class="flex items-center gap-x-3">
							<input
								id="video-hand-left"
								name="video-hand"
								class="h-4 w-4 border-zinc-300 text-indigo-600 focus:ring-indigo-600"
								type="radio"
								value={0}
								bind:group={videoHand}
								required
							/>
							<label
								for="video-hand-left"
								class="block text-sm font-medium leading-6 text-zinc-900"
							>
								{$LL.LEFT()}
							</label>
						</div>
						<div class="flex items-center gap-x-3">
							<input
								id="video-hand-right"
								name="video-hand"
								class="h-4 w-4 border-zinc-300 text-indigo-600 focus:ring-indigo-600"
								type="radio"
								value={1}
								bind:group={videoHand}
								required
							/>
							<label
								for="video-hand-right"
								class="block text-sm font-medium leading-6 text-zinc-900"
							>
								{$LL.RIGHT()}
							</label>
						</div>
					</div>
				</div>

				<div class="sm:col-span-3">
					<label for="age" class="block text-base font-semibold leading-6 text-zinc-900">
						{$LL.AGE()}
					</label>
					<div class="mt-2 flex">
						<input
							bind:value={age}
							id="age"
							class="block w-14 rounded-none rounded-l-md border-0 py-1.5 text-right text-zinc-900 ring-1 ring-inset ring-zinc-300 placeholder:text-zinc-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:leading-6"
							type="number"
							min="0"
							max="255"
							step="1"
							required
						/>
						<label
							for="age"
							class="inline-flex select-none items-center rounded-r-md border border-l-0 border-zinc-300 px-3 text-zinc-500 sm:text-sm"
						>
							{$LL.YEARS()}
						</label>
					</div>
				</div>

				<div class="sm:col-span-3">
					<span class="block text-base font-semibold leading-6 text-zinc-900"> Sexo </span>
					<div class="mt-2 space-y-3">
						<div class="flex items-center gap-x-3">
							<input
								id="sex-male"
								class="h-4 w-4 border-zinc-300 text-indigo-600 focus:ring-indigo-600"
								type="radio"
								value={0}
								bind:group={sex}
							/>
							<label for="sex-male" class="block text-sm font-medium leading-6 text-zinc-900">
								{$LL.MALE()}
							</label>
						</div>
						<div class="flex items-center gap-x-3">
							<input
								id="sex-female"
								class="h-4 w-4 border-zinc-300 text-indigo-600 focus:ring-indigo-600"
								type="radio"
								value={1}
								bind:group={sex}
							/>
							<label for="sex-female" class="block text-sm font-medium leading-6 text-zinc-900">
								{$LL.FEMALE()}
							</label>
						</div>
					</div>
				</div>

				<div class="col-span-full">
					<label for="video-upload" class="block text-base font-semibold leading-6 text-zinc-900">
						{$LL.VIDEO()}
					</label>
					<div
						class="mt-2 flex justify-center rounded-lg border border-dashed border-gray-900/25 px-6 py-10"
						on:click={() => {
							fileInput.click();
						}}
						on:keydown={(e) => {
							e.key === '13' && fileInput.click();
						}}
						on:drop|preventDefault={fileDropHandler}
						on:dragover|preventDefault
					>
						<div class="select-none text-center">
							<VideoIcon class="mx-auto h-12 w-12 text-gray-300" />
							<div class="mt-4 inline-flex text-sm leading-6 text-gray-600">
								<span
									class="relative cursor-pointer rounded-md bg-white font-semibold text-indigo-600 hover:text-indigo-500"
								>
									<span>{$LL.UPLOAD_A_FILE()}</span>
									<input
										bind:this={fileInput}
										on:change={inputSelectHandler}
										id="video-upload"
										name="video-upload"
										type="file"
										class="sr-only"
										accept="video/*"
										required
									/>
								</span>
								<p class="pl-1">{$LL.OR_DRAG_AND_DROP()}</p>
							</div>
							<p class="text-xs leading-5 text-gray-600">
								{#if !file}
									MP4, AVI, MKV, MOV...
								{:else}
									{file.name}
								{/if}
							</p>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>

	<div class="mt-6 flex items-center justify-end gap-x-6">
		<button
			type="submit"
			class="rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
		>
			{$LL.SEND()}
		</button>
	</div>
</form>

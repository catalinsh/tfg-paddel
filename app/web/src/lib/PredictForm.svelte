<script lang="ts">
	import LL from '$i18n/i18n-svelte';
	import VideoIcon from '$lib/icons/VideoIcon.svelte';
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher();

	let fileInput: HTMLInputElement;

	let dominantHand: number;
	let videoHand: number;
	let age: number;
	let sex: number;
	let file: File;

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

<form on:submit|preventDefault={submitHandler} class="grid grid-cols-1 gap-6 p-4 sm:grid-cols-6">
	<div class="flex flex-col gap-2 sm:col-span-3">
		<span class="font-semibold">{$LL.YOUR_DOMINANT_HAND()}</span>
		<label class="flex items-center gap-2">
			<input bind:group={dominantHand} type="radio" name="dominant-hand" value="0" required />
			<span>{$LL.LEFT()}</span>
		</label>
		<label class="flex items-center gap-2">
			<input bind:group={dominantHand} type="radio" name="dominant-hand" value="1" required />
			<span>{$LL.RIGHT()}</span>
		</label>
	</div>

	<div class="flex flex-col gap-2 sm:col-span-3">
		<span class="font-semibold">{$LL.HAND_SHOWN_IN_VIDEO()}</span>
		<label class="flex items-center gap-2">
			<input bind:group={videoHand} type="radio" name="video-hand" value="0" required />
			<span>{$LL.LEFT()}</span>
		</label>
		<label class="flex items-center gap-2">
			<input bind:group={videoHand} type="radio" name="video-hand" value="1" required />
			<span>{$LL.RIGHT()}</span>
		</label>
	</div>

	<label class="sm:col-span-3">
		<span class="font-semibold">{$LL.AGE()}</span>
		<div class="mt-1 flex rounded-sm">
			<input
				bind:value={age}
				type="number"
				max="256"
				min="1"
				step="1"
				name="full-name"
				required
				class="w-14 rounded-l-sm text-right"
			/>
			<span
				class="inline-flex select-none items-center rounded-r-sm border border-l-0 border-gray-500 px-3"
			>
				{$LL.YEARS()}
			</span>
		</div>
	</label>

	<div class="flex flex-col gap-2 sm:col-span-3">
		<span class="font-semibold">{$LL.SEX()}</span>
		<label class="flex items-center gap-2">
			<input bind:group={sex} type="radio" name="sex" value="0" required />
			<span>{$LL.MALE()}</span>
		</label>
		<label class="flex items-center gap-2">
			<input bind:group={sex} type="radio" name="sex" value="1" required />
			<span>{$LL.FEMALE()}</span>
		</label>
	</div>

	<div class="col-span-full">
		<label for="video-upload" class="block text-base font-semibold leading-6"
			>{$LL.VIDEO_FILE()}</label
		>
		<label
			on:drop|preventDefault={fileDropHandler}
			on:dragover|preventDefault
			class="mt-1 flex justify-center rounded-sm border border-dashed border-gray-500 px-6 py-10"
		>
			<div class="select-none text-center">
				<VideoIcon class="mx-auto h-12 w-12 text-gray-400" />
				<div class="mt-4 inline-flex text-sm leading-6 text-gray-600">
					<span
						class="relative cursor-pointer rounded-md bg-white font-semibold text-indigo-600 focus-within:outline-none focus-within:ring-2 focus-within:ring-indigo-600 focus-within:ring-offset-2 hover:text-indigo-500"
					>
						<span>{$LL.UPLOAD_A_FILE()}</span>
						<input
							bind:this={fileInput}
							on:change={inputSelectHandler}
							type="file"
							name="video-upload"
							accept="video/*"
							required
							id="video-upload"
							class="sr-only"
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
		</label>
	</div>

	<button
		type="submit"
		class="rounded-sm bg-neutral-600 py-2.5 font-semibold text-white hover:bg-neutral-700 sm:col-span-2"
	>
		{$LL.SEND()}
	</button>
</form>

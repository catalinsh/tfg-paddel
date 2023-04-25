<script lang="ts">
	import LL from '$i18n/i18n-svelte';
	import VideoIcon from '$lib/icons/VideoIcon.svelte';
	import { createEventDispatcher } from 'svelte';
	import ButtonPrimary from './ButtonPrimary.svelte';

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

<h1 class="text-xl font-semibold leading-7 text-gray-900">{$LL.PREDICT()}</h1>
<p class="mt-1 text-base leading-6 text-gray-600">
	{$LL.PREDICT_HELP()}
</p>

<form on:submit|preventDefault={submitHandler} class="mt-8 grid grid-cols-1 gap-6 sm:grid-cols-6">
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
		<div class="mt-2 flex rounded-md">
			<input
				bind:value={age}
				type="number"
				max="256"
				min="1"
				step="1"
				name="full-name"
				required
				class="w-14 rounded-l-md text-right"
			/>
			<span
				class="inline-flex select-none items-center rounded-r-md border border-l-0 border-gray-500 px-3"
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
		<span class="block text-base font-semibold leading-6">
			{$LL.VIDEO_FILE()}
		</span>

		<!-- svelte-ignore a11y-click-events-have-key-events -->
		<div
			on:drop|preventDefault={fileDropHandler}
			on:dragover|preventDefault
			on:click={() => {
				fileInput.click();
			}}
			class="mt-2 flex justify-center rounded-md border border-dashed border-gray-500 px-6 py-10"
		>
			<div class="select-none text-center">
				<VideoIcon class="mx-auto h-12 w-12 text-gray-400" />
				<div class="mt-4 inline text-sm text-gray-600">
					<label
						class="relative cursor-pointer rounded-md bg-white font-semibold text-blue-600 focus-within:outline-none focus-within:ring-2 focus-within:ring-blue-600 focus-within:ring-offset-2 hover:text-blue-500"
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
					</label>
					<span>{$LL.OR_DRAG_AND_DROP()}</span>
				</div>
				<p class="text-xs mt-2 text-gray-600 break-all">
					{#if !file}
						MP4, AVI, MKV, MOV...
					{:else}
						{file.name}
					{/if}
				</p>
			</div>
		</div>
	</div>

	<ButtonPrimary type="submit" class="sm:col-span-full">{$LL.SEND()}</ButtonPrimary>
</form>

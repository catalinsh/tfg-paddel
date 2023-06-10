<script lang="ts">
	import Footer from '$lib/Footer.svelte';
	import PredictForm from '$lib/PredictForm.svelte';
	import SmallNav from '$lib/SmallNav.svelte';
	import { predict } from '$lib/api';
	import type { AxiosProgressEvent } from 'axios';
	import LL from '$i18n/i18n-svelte';
	import LoadingIcon from '$lib/icons/LoadingIcon.svelte';
	import ButtonSecondary from '$lib/ButtonSecondary.svelte';
	import BackIcon from '$lib/icons/BackIcon.svelte';

	let progress = 0;
	$: uploadFinished = progress === 100;
	let uploadSpeed = NaN;
	let submitted = false;
	let result: { status: number } | Array<number> | undefined;
	let resetVar = 0;

	const submitHandler = async (e: CustomEvent) => {
		submitted = true;

		result = await predict(e.detail, (e: AxiosProgressEvent) => {
			progress = (100 * e.loaded) / e.total!;
			uploadSpeed = e.rate! / 1000000;
		});
	};

	const color = (value: number) => {
		const b = (0 - 120) * value
		const c = b + 120;

		// Return a CSS HSL string
		return 'hsl('+c+', 83.2%, 53.3%)';
	}

	const reset = () => {
		progress = 0;
		uploadSpeed = NaN;
		submitted = false;
		result = undefined;
		resetVar = 1 - resetVar;
	}
</script>

<div class="mx-auto max-w-xl px-8 sm:px-12 md:max-w-3xl lg:px-16">
	<SmallNav />
	{#key resetVar}
		<main>
			{#if !submitted}
				<PredictForm on:submit={submitHandler} />
			{:else if !result}
				<div
					class="mt-8 text-center"
					role="progressbar"
					aria-valuenow={progress}
					aria-valuemin={0}
					aria-valuemax={100}
				>
					<span
						class="inline-flex items-center gap-2 px-4 text-left text-sm font-semibold"
						aria-live="assertive"
					>
						<LoadingIcon
							class="block h-5 w-5 flex-shrink-0 animate-spin fill-blue-600 text-neutral-200 dark:fill-blue-400 dark:text-neutral-700"
						/>
						{#if !uploadFinished}
							{$LL.SENDING_DATA()}
						{:else}
							{$LL.PROCESSING_DATA()}
						{/if}
					</span>
					<div class="mt-4 h-1.5 w-full rounded-sm bg-neutral-200 dark:bg-neutral-700">
						<div class="h-1.5 rounded-sm bg-blue-600 dark:bg-blue-400" style="width: {progress}%" />
					</div>
					<div class="mt-2 flex justify-between text-sm" id="email-error">
						<span>{uploadSpeed.toFixed(2)} MB/s</span>
						<span>{progress.toFixed(2)}%</span>
					</div>
				</div>
			{:else if Array.isArray(result)}
				<div>
					<ButtonSecondary on:click={reset} class="inline-flex items-center gap-1 pl-2">
						<BackIcon class="inline h-5 w-5" />
						{$LL.BACK()}
					</ButtonSecondary>
				</div>

				<h1 class="mt-4 text-lg font-semibold">{$LL.PREDICTION_RESULT()}</h1>

				<span class="block text-center mt-6 text-lg font-bold">{(result[1] * 100).toFixed(2)}%</span>
				<div class="mt-2 mb-6 h-1.5 w-full rounded-sm bg-neutral-200 dark:bg-neutral-700">
					<div
						class="h-1.5 rounded-sm"
						style="width: {(result[1] * 100).toFixed(2)}%; background-color: {color(result[1])}"
					/>
				</div>

				<p aria-live="assertive">
					{$LL.PREDICTION_RESULT_DESC({ percentage: (result[1] * 100).toFixed(2) })}
				</p>
			{:else}
				<div class="mb-4">
					<ButtonSecondary on:click={reset} class="inline-flex items-center gap-1 pl-2">
						<BackIcon class="inline h-5 w-5" />
						{$LL.BACK()}
					</ButtonSecondary>
				</div>

				<h1 class="text-lg font-semibold">{$LL.THERE_WAS_A_PROBLEM()}</h1>
				<p aria-live="assertive">
					{#if 'status' in result && result.status === 422}
						{$LL.CANNOT_PROCESS_VIDEO()}
					{:else}
						{$LL.SOMETHING_WENT_WRONG()}
					{/if}
				</p>
			{/if}
		</main>
	{/key}
	<Footer />
</div>

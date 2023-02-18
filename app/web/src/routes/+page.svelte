<script lang="ts">
	import { PUBLIC_API_PATH } from '$env/static/public';

	let input: string;
	let result: number;

	const api_times_two = async () => {
		const res = await fetch(`${PUBLIC_API_PATH}/times_two/${input}`);
		const item = await res.json();

		result = item['result'];
	};
</script>

<form on:submit|preventDefault={api_times_two}>
	<label>
		Value to multiply by 2 through API:
		<input type="text" bind:value={input} />
	</label>
	<input type="submit" />
</form>

{result}

<script>
	// @ts-nocheck

	import { fade, fly } from 'svelte/transition';

	let files = [];
	let consent = true;
	let name = '';

	let toast = {
		show: false,
		message: 'Operation successful!',
		type: 'success'
	};

	let response = {};

	function sendFiles() {
		const formdata = new FormData();
		for (let file of files) {
			formdata.append('files', file);
		}
		formdata.append('name', name);
		formdata.append('consent', consent);

		fetch('http://127.0.0.1:8000/predict', {
			method: 'POST',
			body: formdata
		})
			.then((res) => {
				if (res.ok) {
					return res.json();
				} else {
					throw new Error('Something went wrong');
				}
			})
			.then((res) => {
				console.log(res);
				response = res;
				handleToasts(true, {
					message: 'Operation successful!',
					type: 'success',
					delay: 2000
				});
			})
			.catch((err) => {
				response.error = err.message;
				handleToasts(true, {
					message: err.message,
					type: 'error',
					delay: 2000
				});
			});
	}

	function handleToasts(
		show,
		{ message, type, delay } = {
			message: 'Operation successful!',
			type: 'success',
			delay: 3000
		}
	) {
		if (show) {
			toast.show = true;
			toast.message = message;
			toast.type = type;
			setTimeout(() => {
				toast.show = false;
			}, delay);
		}
	}

	function handleFiles(e) {
		e.preventDefault();
		response = {};
		files = e.target.files;
		if (files.length > 20) {
			handleToasts(true, {
				message: 'Maximum 20 files allowed',
				type: 'error',
				delay: 2000
			});
			let fileBuffer = [];
			Array.prototype.push.apply(fileBuffer, files);
			files = fileBuffer.slice(0, 20);
		}
	}
</script>

<navbar class="navbar bg-base-200 text-neutral-content mb-20">
	<div class="flex-1">
		<div class="btn normal-case text-xl">Image Classifier</div>
	</div>
	<div class="flex-none">
		<a href="https://github.com/vaishnav-mk/image-classification" target="_blank">
			<button class="btn btn-square btn-ghost">
				<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
					><path
						d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"
					/></svg
				>
			</button>
		</a>
	</div>
</navbar>

<div
	class="flex flex-col items-center justify-center max-w-5xl mx-auto bg-base-200 p-5 rounded-box mb-5"
>
	{#if files && files.length > 0}
		<div class="carousel carousel-center p-4 space-x-4 bg-neutral rounded-box">
			{#each files as file, i}
				<div id={`item-${i + 1}`} class="carousel-item w-full">
					<img src={URL.createObjectURL(file)} class="rounded-box w-full h-64" />
				</div>
			{/each}
		</div>
		<div class="flex justify-center w-full py-2 gap-2">
			{#each files as file, i}
				<a href={`#item-${i + 1}`} class="btn btn-xs">{i + 1}</a>
			{/each}
		</div>
	{:else}
		No images selected
	{/if}
</div>

<div class="flex items-center justify-center max-w-5xl mx-auto">
	<div class="mockup-window border bg-base-300 w-full max-h-4xl">
		<div class="flex flex-col items-center justify-center gap-3 px-4 py-16 bg-base-200">
			<div class="flex flex-col items-center justify-center gap-2">
				<input type="file" accept="image/*" multiple on:change={handleFiles} class="file-input" />
				{#if files.length}
					<input
						type="text"
						bind:value={name}
						placeholder="Your name here (optional)"
						class="input w-full max-w-xs"
					/>
				{/if}

				<div
					class={`alert ${
						consent ? 'alert-success' : 'alert-error'
					} shadow-lg text-black rounded-lg`}
				>
					<label class="label cursor-pointer gap-2">
						<input type="checkbox" class="toggle toggle-success" bind:checked={consent} />
						{consent ? '' : 'Do not'} share my images!
					</label>
				</div>
				<button
					class={`btn btn-primary w-full max-w-xs ${files.length ? '' : 'btn-disabled'}`}
					on:click={sendFiles}
				>
					Submit {name ? `as ${name}` : ''}</button
				>
			</div>
		</div>

		<div class="divider">
			{#if response.results}
				<div class="btn btn-info btn-xs">
					{response.results.bike.count ?? 0} bike(s) and {response.results.car.count ?? 0} car(s) detected
				</div>
			{:else}
				<div class={`btn btn-xs ${files.length ? 'btn-success' : ''}`}>
					{files.length ? files.length : 'No'} file(s) selected
				</div>
			{/if}
		</div>

		{#if files.length}
			<div class="flex flex-col items-center justify-between px-4 py-16 bg-base-200">
				{#if response.results}
					<div class="grid grid-cols-3 gap-4">
						{#each files as file}
							<div
								class={`grid h-auto card ${
									response?.results?.bike.files.includes(file.name) ? 'bg-green-300' : 'bg-blue-300'
								} rounded-box place-items-center p-2`}
							>
								<div class="flex flex-col items-center justify-center">
									<div class="badge font-bold mb-2 rounded-lg">
										{response?.results?.bike.files.includes(file.name) ? 'bike' : 'car'}
									</div>
									<img
										class="avatar rounded-xl h-64 w-64"
										src={URL.createObjectURL(file)}
										alt={file.name}
									/>
								</div>
							</div>
						{/each}
					</div>
				{:else if response.error}
					<div class="alert alert-error">
						{response.error}
					</div>
				{:else}
					<div class="grid grid-cols-3 gap-4">
						{#each files as file}
							<div class={`grid h-auto card bg-base-100 rounded-box place-items-center p-2`}>
								<img
									class="avatar rounded-xl h-64 w-64"
									src={URL.createObjectURL(file)}
									alt={file.name}
								/>
								<button
									class="btn btn-xs btn-error btn-circle absolute top-1 left-1"
									on:click={() => {
										let fileBuffer = [];
										Array.prototype.push.apply(fileBuffer, files);
										files = fileBuffer.filter((f) => f.name !== file.name);
									}}
								>
									<svg
										xmlns="http://www.w3.org/2000/svg"
										fill="none"
										viewBox="0 0 24 24"
										class="inline-block w-5 h-5 stroke-current"
										><path
											stroke-linecap="round"
											stroke-linejoin="round"
											stroke-width="2"
											d="M6 18L18 6M6 6l12 12"
										/></svg
									>
								</button>
							</div>
						{/each}
					</div>
				{/if}
			</div>
		{/if}
	</div>
</div>

{#if toast.show}
	<div class="toast" in:fly={{ y: 200, duration: 2000 }} out:fade>
		<div class={`alert ${toast.type == 'success' ? 'alert-success' : 'alert-error'}`}>
			<div>
				<span>{toast.message}</span>
			</div>
		</div>
	</div>
{/if}

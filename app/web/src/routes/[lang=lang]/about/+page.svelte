<script>
	import Footer from "$lib/Footer.svelte";
    import SmallNav from "$lib/SmallNav.svelte";
    import LL from '$i18n/i18n-svelte';
</script>

<div class="mx-auto max-w-xl px-8 sm:px-12 md:max-w-3xl lg:px-16">

<SmallNav />
    <h1 class="text-lg font-semibold">{$LL.ABOUT()}</h1>
    <p class="mt-6">
        {$LL.ABOUT_P1()}
    </p>

    <p class="mt-6">
        {$LL.ABOUT_P2()}
    </p>
<Footer />

</div>
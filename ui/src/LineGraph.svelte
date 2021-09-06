<script>
    import { onMount } from "svelte";
    let h, w;
    let plotLoaded = false;
    let plot;
    export let x, y;
    $: data = [
        {
            x: x,
            y: y,
            type: "scatter",
        },
    ];
    $: layout = {};

    // $: {
    //     // console.log(x, y);
    // }
    $: {
        if (plotLoaded) {
            console.log(data);
            Plotly.react(plot, data, layout);
        }
    }

    onMount(() => {
        Plotly.newPlot(plot, data, layout, { responsive: true });
        plotLoaded = true;
    });
</script>

<div bind:this={plot} bind:clientWidth={w} bind:clientHeight={h} />

<style>
    div {
        height: 100%;
        width: 100%;
    }
</style>
